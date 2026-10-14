from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash


ALGORITHM = "HS256"
TOKEN_LIFETIME = timedelta(minutes=30)
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, encoded_password: str) -> bool:
    return password_hash.verify(password, encoded_password)


def create_access_token(user_id: int, secret: str) -> str:
    now = datetime.now(UTC)
    return jwt.encode(
        {
            "sub": str(user_id),
            "iat": now,
            "exp": now + TOKEN_LIFETIME,
        },
        secret,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str, secret: str) -> int:
    payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    return int(payload["sub"])

