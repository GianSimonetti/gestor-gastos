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


def test_board_creator_becomes_a_member_and_can_access_the_board(client):
    owner = authenticated_headers(client, "owner@example.com")

    board = create_board(client, owner)
    response = client.get(f"/api/boards/{board['id']}", headers=owner)

    assert response.status_code == 200
    assert response.json() == {"id": board["id"], "name": "Hogar"}


def test_member_can_get_the_invitation_code_and_another_user_can_join(client):
    owner = authenticated_headers(client, "owner@example.com")
    board = create_board(client, owner)

    invitation = client.get(
        f"/api/boards/{board['id']}/invitation-code",
        headers=owner,
    )
    assert invitation.status_code == 200
    code = invitation.json()["invitation_code"]

    guest = authenticated_headers(client, "guest@example.com")
    joined = client.post(
        "/api/boards/join",
        headers=guest,
        json={"invitation_code": code},
    )

    assert joined.status_code == 200
    assert joined.json() == {"id": board["id"], "name": "Hogar"}
    assert client.get(f"/api/boards/{board['id']}", headers=guest).status_code == 200


def test_joined_member_has_the_same_permission_to_consult_the_code(client):
    owner = authenticated_headers(client, "owner@example.com")
    board = create_board(client, owner)
    invitation = client.get(
        f"/api/boards/{board['id']}/invitation-code",
        headers=owner,
    ).json()

    guest = authenticated_headers(client, "guest@example.com")
    client.post(
        "/api/boards/join",
        headers=guest,
        json=invitation,
    )

    guest_invitation = client.get(
        f"/api/boards/{board['id']}/invitation-code",
        headers=guest,
    )

    assert guest_invitation.status_code == 200
    assert guest_invitation.json() == invitation


def test_non_member_cannot_access_board_data_or_its_invitation_code(client):
    owner = authenticated_headers(client, "owner@example.com")
    board = create_board(client, owner)
    outsider = authenticated_headers(client, "outsider@example.com")

    board_response = client.get(
        f"/api/boards/{board['id']}",
        headers=outsider,
    )
    invitation_response = client.get(
        f"/api/boards/{board['id']}/invitation-code",
        headers=outsider,
    )

    assert board_response.status_code == 403
    assert invitation_response.status_code == 403


def test_board_list_only_contains_boards_the_user_has_joined(client):
    owner = authenticated_headers(client, "owner@example.com")
    create_board(client, owner, "Privado")
    outsider = authenticated_headers(client, "outsider@example.com")

    response = client.get("/api/boards", headers=outsider)

    assert response.status_code == 200
    assert response.json() == []


def test_join_rejects_an_unknown_invitation_code(client):
    user = authenticated_headers(client, "user@example.com")

    response = client.post(
        "/api/boards/join",
        headers=user,
        json={"invitation_code": "codigo-inexistente"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Código de invitación inválido"
