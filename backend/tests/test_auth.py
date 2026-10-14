def test_register_creates_account_without_exposing_plaintext_password(
    client,
    stored_password_hash,
):
    response = client.post(
        "/api/auth/register",
        json={"email": "ana@example.com", "password": "segura-123"},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "ana@example.com"
    assert "password" not in response.json()
    assert stored_password_hash("ana@example.com") != "segura-123"


def test_register_rejects_an_existing_email(client):
    credentials = {"email": "ana@example.com", "password": "segura-123"}
    assert client.post("/api/auth/register", json=credentials).status_code == 201

    response = client.post("/api/auth/register", json=credentials)

    assert response.status_code == 409


def test_login_returns_a_jwt_that_allows_access_to_the_current_account(client):
    credentials = {"email": "ana@example.com", "password": "segura-123"}
    client.post("/api/auth/register", json=credentials)

    login = client.post("/api/auth/login", json=credentials)

    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    token = login.json()["access_token"]

    current_account = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert current_account.status_code == 200
    assert current_account.json()["email"] == "ana@example.com"


def test_login_rejects_invalid_credentials(client):
    client.post(
        "/api/auth/register",
        json={"email": "ana@example.com", "password": "segura-123"},
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "ana@example.com", "password": "incorrecta"},
    )

    assert response.status_code == 401


def test_protected_endpoint_rejects_a_request_without_a_jwt(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401

