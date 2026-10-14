import os
import secrets
from contextlib import asynccontextmanager

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, create_database
from app.models import Board, BoardMembership, User
from app.schemas import (
    BoardCreate,
    BoardResponse,
    Credentials,
    InvitationCodeResponse,
    JoinBoardRequest,
    TokenResponse,
    UserResponse,
)
from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def create_app(
    database_url: str | None = None,
    jwt_secret: str | None = None,
) -> FastAPI:
    resolved_database_url = database_url or os.getenv(
        "DATABASE_URL",
        "sqlite:///./gestor-gastos.db",
    )
    resolved_jwt_secret = (
        jwt_secret
        or os.getenv("JWT_SECRET")
        or secrets.token_urlsafe(32)
    )
    engine, session_factory = create_database(resolved_database_url)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        Base.metadata.create_all(engine)
        yield
        engine.dispose()

    app = FastAPI(title="Gestor de gastos API", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def get_session():
        with session_factory() as session:
            yield session

    def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
    ) -> User:
        unauthorized = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            user_id = decode_access_token(token, resolved_jwt_secret)
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            raise unauthorized from None

        user = session.get(User, user_id)
        if user is None:
            raise unauthorized
        return user

    def get_member_board(
        board_id: int,
        user: User,
        session: Session,
    ) -> Board:
        board = session.get(Board, board_id)
        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tablero no encontrado",
            )
        membership = session.get(
            BoardMembership,
            (user.id, board_id),
        )
        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No pertenecés a este tablero",
            )
        return board

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.post(
        "/api/auth/register",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def register(
        credentials: Credentials,
        session: Session = Depends(get_session),
    ):
        email = str(credentials.email).lower()
        if session.scalar(select(User).where(User.email == email)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            )

        user = User(
            email=email,
            password_hash=hash_password(credentials.password),
        )
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            ) from None
        session.refresh(user)
        return user

    @app.post("/api/auth/login", response_model=TokenResponse)
    def login(
        credentials: Credentials,
        session: Session = Depends(get_session),
    ):
        email = str(credentials.email).lower()
        user = session.scalar(select(User).where(User.email == email))
        if user is None or not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña inválidos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenResponse(
            access_token=create_access_token(
                user.id,
                resolved_jwt_secret,
            )
        )

    @app.get("/api/auth/me", response_model=UserResponse)
    def current_account(user: User = Depends(get_current_user)):
        return user

    @app.post(
        "/api/boards",
        response_model=BoardResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_board(
        payload: BoardCreate,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        board = Board(
            name=payload.name,
            invitation_code=secrets.token_urlsafe(9),
        )
        session.add(board)
        session.flush()
        session.add(
            BoardMembership(user_id=user.id, board_id=board.id)
        )
        session.commit()
        session.refresh(board)
        return board

    @app.get("/api/boards", response_model=list[BoardResponse])
    def list_boards(
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        return session.scalars(
            select(Board)
            .join(
                BoardMembership,
                BoardMembership.board_id == Board.id,
            )
            .where(BoardMembership.user_id == user.id)
            .order_by(Board.id)
        ).all()

    @app.post("/api/boards/join", response_model=BoardResponse)
    def join_board(
        payload: JoinBoardRequest,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        board = session.scalar(
            select(Board).where(
                Board.invitation_code == payload.invitation_code
            )
        )
        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código de invitación inválido",
            )

        membership = session.get(
            BoardMembership,
            (user.id, board.id),
        )
        if membership is None:
            session.add(
                BoardMembership(user_id=user.id, board_id=board.id)
            )
            session.commit()
        return board

    @app.get(
        "/api/boards/{board_id}",
        response_model=BoardResponse,
    )
    def get_board(
        board_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        return get_member_board(board_id, user, session)

    @app.get(
        "/api/boards/{board_id}/invitation-code",
        response_model=InvitationCodeResponse,
    )
    def get_invitation_code(
        board_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        board = get_member_board(board_id, user, session)
        return InvitationCodeResponse(
            invitation_code=board.invitation_code
        )

    app.state.session_factory = session_factory
    return app


app = create_app()

