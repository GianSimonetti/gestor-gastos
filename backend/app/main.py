import os
import secrets
from contextlib import asynccontextmanager
from datetime import date, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, create_database
from app.expense_distribution import DistributionError, distribute_expense
from app.monthly_summary import calculate_monthly_summary
from app.models import (
    Board,
    BoardMembership,
    Expense,
    ExpenseAllocation,
    MonthlyBudget,
    Participant,
    User,
)
from app.schemas import (
    BoardCreate,
    BoardResponse,
    Credentials,
    ExpenseCreate,
    ExpenseResponse,
    InvitationCodeResponse,
    JoinBoardRequest,
    MonthlyBudgetSet,
    MonthlySummaryResponse,
    ParticipantCreate,
    ParticipantResponse,
    TokenResponse,
    UserResponse,
)
from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def argentina_today() -> date:
    return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).date()


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

    def get_board_participant(
        participant_id: int,
        board_id: int,
        session: Session,
    ) -> Participant:
        participant = session.get(Participant, participant_id)
        if participant is None or participant.board_id != board_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="La persona no pertenece al tablero",
            )
        return participant

    def get_monthly_summary(
        board_id: int,
        year: int,
        month: int,
        session: Session,
    ) -> MonthlySummaryResponse:
        month_start = date(year, month, 1)
        next_month = (
            date(year + 1, 1, 1)
            if month == 12
            else date(year, month + 1, 1)
        )
        budget = session.get(MonthlyBudget, (board_id, year, month))
        available_base = (
            budget.available_base if budget is not None else Decimal("0.00")
        )
        consumed_value = session.scalar(
            select(func.sum(Expense.amount)).where(
                Expense.board_id == board_id,
                Expense.date >= month_start,
                Expense.date < next_month,
            )
        )
        consumed, remaining = calculate_monthly_summary(
            available_base=available_base,
            expense_totals=[consumed_value or Decimal("0.00")],
        )
        return MonthlySummaryResponse(
            board_id=board_id,
            year=year,
            month=month,
            available_base=available_base,
            consumed=consumed,
            remaining=remaining,
        )

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

    @app.post(
        "/api/boards/{board_id}/participants",
        response_model=ParticipantResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_participant(
        board_id: int,
        payload: ParticipantCreate,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        participant = Participant(
            board_id=board_id,
            name=payload.name,
        )
        session.add(participant)
        session.commit()
        session.refresh(participant)
        return participant

    @app.get(
        "/api/boards/{board_id}/participants",
        response_model=list[ParticipantResponse],
    )
    def list_participants(
        board_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        return session.scalars(
            select(Participant)
            .where(Participant.board_id == board_id)
            .order_by(Participant.id)
        ).all()

    @app.post(
        "/api/boards/{board_id}/expenses",
        response_model=ExpenseResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_expense(
        board_id: int,
        payload: ExpenseCreate,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        get_board_participant(payload.payer_id, board_id, session)

        custom_allocations = (
            [
                (allocation.participant_id, allocation.amount)
                for allocation in payload.allocations
            ]
            if payload.allocations is not None
            else None
        )
        try:
            allocations = distribute_expense(
                amount=payload.amount,
                expense_type=payload.expense_type,
                person_id=payload.person_id,
                participant_ids=payload.participant_ids,
                custom_allocations=custom_allocations,
            )
        except DistributionError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(error),
            ) from error

        for participant_id, _ in allocations:
            get_board_participant(participant_id, board_id, session)

        expense = Expense(
            board_id=board_id,
            name=payload.name,
            amount=payload.amount,
            category=payload.category,
            date=payload.date or argentina_today(),
            payer_id=payload.payer_id,
            description=payload.description,
            expense_type=payload.expense_type,
        )
        session.add(expense)
        session.flush()
        session.add_all(
            [
                ExpenseAllocation(
                    expense_id=expense.id,
                    participant_id=participant_id,
                    amount=allocated_amount,
                )
                for participant_id, allocated_amount in allocations
            ]
        )
        session.commit()
        session.refresh(expense)
        return expense

    @app.put(
        "/api/boards/{board_id}/monthly-summary/{year}/{month}",
        response_model=MonthlySummaryResponse,
    )
    def set_monthly_budget(
        board_id: int,
        payload: MonthlyBudgetSet,
        year: int = Path(ge=1, le=9998),
        month: int = Path(ge=1, le=12),
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        budget = session.get(MonthlyBudget, (board_id, year, month))
        if budget is None:
            budget = MonthlyBudget(
                board_id=board_id,
                year=year,
                month=month,
                available_base=payload.available_base,
            )
            session.add(budget)
        else:
            budget.available_base = payload.available_base
        session.flush()
        summary = get_monthly_summary(board_id, year, month, session)
        session.commit()
        return summary

    @app.get(
        "/api/boards/{board_id}/monthly-summary/{year}/{month}",
        response_model=MonthlySummaryResponse,
    )
    def read_monthly_summary(
        board_id: int,
        year: int = Path(ge=1, le=9998),
        month: int = Path(ge=1, le=12),
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        return get_monthly_summary(board_id, year, month, session)

    @app.get(
        "/api/boards/{board_id}/expenses",
        response_model=list[ExpenseResponse],
    )
    def list_expenses(
        board_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        return session.scalars(
            select(Expense)
            .where(Expense.board_id == board_id)
            .order_by(Expense.id)
        ).all()

    @app.get(
        "/api/boards/{board_id}/expenses/{expense_id}",
        response_model=ExpenseResponse,
    )
    def get_expense(
        board_id: int,
        expense_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ):
        get_member_board(board_id, user, session)
        expense = session.get(Expense, expense_id)
        if expense is None or expense.board_id != board_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gasto no encontrado",
            )
        return expense

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

