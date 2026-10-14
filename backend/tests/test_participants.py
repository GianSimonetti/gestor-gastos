def authenticated_headers(client, email: str) -> dict[str, str]:
    credentials = {"email": email, "password": "segura-123"}
    assert client.post("/api/auth/register", json=credentials).status_code == 201
    login = client.post("/api/auth/login", json=credentials)
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def create_board(client, headers, name="Hogar"):
    response = client.post(
        "/api/boards",
        headers=headers,
        json={"name": name},
    )
    assert response.status_code == 201
    return response.json()


def test_member_can_create_and_list_participants_without_accounts(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)

    created = client.post(
        f"/api/boards/{board['id']}/participants",
        headers=member,
        json={"name": "Ana"},
    )
    listed = client.get(
        f"/api/boards/{board['id']}/participants",
        headers=member,
    )

    assert created.status_code == 201
    assert created.json() == {
        "id": created.json()["id"],
        "board_id": board["id"],
        "name": "Ana",
    }
    assert listed.status_code == 200
    assert listed.json() == [created.json()]


def test_participants_belong_only_to_their_board(client):
    member = authenticated_headers(client, "member@example.com")
    home = create_board(client, member, "Hogar")
    trip = create_board(client, member, "Viaje")
    client.post(
        f"/api/boards/{home['id']}/participants",
        headers=member,
        json={"name": "Ana"},
    )

    response = client.get(
        f"/api/boards/{trip['id']}/participants",
        headers=member,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_non_member_cannot_create_or_list_participants(client):
    owner = authenticated_headers(client, "owner@example.com")
    board = create_board(client, owner)
    outsider = authenticated_headers(client, "outsider@example.com")

    created = client.post(
        f"/api/boards/{board['id']}/participants",
        headers=outsider,
        json={"name": "Ana"},
    )
    listed = client.get(
        f"/api/boards/{board['id']}/participants",
        headers=outsider,
    )

    assert created.status_code == 403
    assert listed.status_code == 403

