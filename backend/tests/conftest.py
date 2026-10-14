import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def database_path(tmp_path):
    return tmp_path / "test.db"


@pytest.fixture
def client(database_path):
    app = create_app(
        database_url=f"sqlite:///{database_path.as_posix()}",
        jwt_secret="test-secret",
    )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def stored_password_hash(database_path):
    def load(email: str) -> str:
        with sqlite3.connect(database_path) as connection:
            row = connection.execute(
                "SELECT password_hash FROM users WHERE email = ?",
                (email,),
            ).fetchone()
        assert row is not None
        return row[0]

    return load

