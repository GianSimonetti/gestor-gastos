from datetime import date

import app.main as main_module


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


def create_participant(client, headers, board_id, name="Ana"):
    response = client.post(
        f"/api/boards/{board_id}/participants",
        headers=headers,
        json={"name": name},
    )
    assert response.status_code == 201
    return response.json()


def personal_expense_payload(participant_id, **overrides):
    payload = {
        "name": "Supermercado",
        "amount": "30000.10",
        "category": "Alimentos",
        "date": "2026-01-15",
        "payer_id": participant_id,
        "person_id": participant_id,
        "description": "Compra semanal",
    }
    payload.update(overrides)
    return payload


def test_member_can_register_list_and_get_a_personal_expense(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    participant = create_participant(client, member, board["id"])

    created = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
        json=personal_expense_payload(participant["id"]),
    )
    listed = client.get(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
    )

    assert created.status_code == 201
    expense = created.json()
    assert expense == {
        "id": expense["id"],
        "board_id": board["id"],
        "name": "Supermercado",
        "amount": "30000.10",
        "category": "Alimentos",
        "date": "2026-01-15",
        "payer_id": participant["id"],
        "description": "Compra semanal",
        "expense_type": "personal",
        "allocations": [
            {
                "participant_id": participant["id"],
                "amount": "30000.10",
            }
        ],
    }
    assert listed.status_code == 200
    assert listed.json() == [expense]

    detail = client.get(
        f"/api/boards/{board['id']}/expenses/{expense['id']}",
        headers=member,
    )
    assert detail.status_code == 200
    assert detail.json() == expense


def test_expense_without_date_uses_current_date_in_argentina(client, monkeypatch):
    monkeypatch.setattr(
        main_module,
        "argentina_today",
        lambda: date(2026, 1, 15),
        raising=False,
    )
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    participant = create_participant(client, member, board["id"])
    payload = personal_expense_payload(
        participant["id"],
        amount="0.10",
        description=None,
    )
    payload.pop("date")

    response = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["date"] == "2026-01-15"
    assert response.json()["amount"] == "0.10"
    assert response.json()["description"] is None
    assert response.json()["allocations"][0]["amount"] == "0.10"


def test_expense_rejects_more_than_two_decimal_places(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    participant = create_participant(client, member, board["id"])

    response = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
        json=personal_expense_payload(participant["id"], amount="10.001"),
    )

    assert response.status_code == 422
    listed = client.get(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
    )
    assert listed.json() == []


def test_expense_rejects_people_from_another_board(client):
    member = authenticated_headers(client, "member@example.com")
    home = create_board(client, member, "Hogar")
    trip = create_board(client, member, "Viaje")
    home_person = create_participant(client, member, home["id"], "Ana")
    trip_person = create_participant(client, member, trip["id"], "Luis")

    wrong_payer = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json=personal_expense_payload(
            home_person["id"],
            payer_id=trip_person["id"],
        ),
    )
    wrong_person = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json=personal_expense_payload(
            home_person["id"],
            person_id=trip_person["id"],
        ),
    )

    assert wrong_payer.status_code == 422
    assert wrong_person.status_code == 422


def test_non_member_cannot_register_list_or_get_expenses(client):
    owner = authenticated_headers(client, "owner@example.com")
    board = create_board(client, owner)
    participant = create_participant(client, owner, board["id"])
    created = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=owner,
        json=personal_expense_payload(participant["id"]),
    ).json()
    outsider = authenticated_headers(client, "outsider@example.com")

    posted = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=outsider,
        json=personal_expense_payload(participant["id"]),
    )
    listed = client.get(
        f"/api/boards/{board['id']}/expenses",
        headers=outsider,
    )
    detail = client.get(
        f"/api/boards/{board['id']}/expenses/{created['id']}",
        headers=outsider,
    )

    assert posted.status_code == 403
    assert listed.status_code == 403
    assert detail.status_code == 403


def test_member_can_register_an_equal_shared_expense(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    payer = create_participant(client, member, board["id"], "Carla")
    ana = create_participant(client, member, board["id"], "Ana")
    luis = create_participant(client, member, board["id"], "Luis")

    response = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
        json={
            "name": "Cena",
            "amount": "100.00",
            "category": "Comidas",
            "date": "2026-01-15",
            "payer_id": payer["id"],
            "expense_type": "equal",
            "participant_ids": [payer["id"], ana["id"], luis["id"]],
        },
    )

    assert response.status_code == 201
    expense = response.json()
    assert expense["expense_type"] == "equal"
    assert expense["allocations"] == [
        {"participant_id": payer["id"], "amount": "33.34"},
        {"participant_id": ana["id"], "amount": "33.33"},
        {"participant_id": luis["id"], "amount": "33.33"},
    ]
    assert expense["debts"] == [
        {"participant_id": ana["id"], "amount": "33.33"},
        {"participant_id": luis["id"], "amount": "33.33"},
    ]


def test_member_can_register_a_custom_shared_expense(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    payer = create_participant(client, member, board["id"], "Carla")
    ana = create_participant(client, member, board["id"], "Ana")

    response = client.post(
        f"/api/boards/{board['id']}/expenses",
        headers=member,
        json={
            "name": "Alquiler",
            "amount": "150000.00",
            "category": "Vivienda",
            "date": "2026-01-15",
            "payer_id": payer["id"],
            "expense_type": "custom",
            "allocations": [
                {"participant_id": payer["id"], "amount": "40000.00"},
                {"participant_id": ana["id"], "amount": "110000.00"},
            ],
        },
    )

    assert response.status_code == 201
    assert response.json()["allocations"] == [
        {"participant_id": payer["id"], "amount": "40000.00"},
        {"participant_id": ana["id"], "amount": "110000.00"},
    ]
    assert response.json()["debts"] == [
        {"participant_id": ana["id"], "amount": "110000.00"}
    ]
    detail = client.get(
        f"/api/boards/{board['id']}/expenses/{response.json()['id']}",
        headers=member,
    )
    assert detail.status_code == 200
    assert detail.json()["allocations"] == response.json()["allocations"]
    assert detail.json()["debts"] == response.json()["debts"]


def test_custom_expense_rejects_invalid_sum_negative_and_foreign_people(client):
    member = authenticated_headers(client, "member@example.com")
    home = create_board(client, member, "Hogar")
    trip = create_board(client, member, "Viaje")
    payer = create_participant(client, member, home["id"], "Carla")
    ana = create_participant(client, member, home["id"], "Ana")
    outsider = create_participant(client, member, trip["id"], "Luis")
    base = {
        "name": "Alquiler",
        "amount": "150000.00",
        "category": "Vivienda",
        "payer_id": payer["id"],
        "expense_type": "custom",
    }

    invalid_sum = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json={
            **base,
            "allocations": [
                {"participant_id": payer["id"], "amount": "40000.00"},
                {"participant_id": ana["id"], "amount": "100000.00"},
            ],
        },
    )
    negative = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json={
            **base,
            "allocations": [
                {"participant_id": payer["id"], "amount": "150000.01"},
                {"participant_id": ana["id"], "amount": "-0.01"},
            ],
        },
    )
    foreign_person = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json={
            **base,
            "allocations": [
                {"participant_id": payer["id"], "amount": "40000.00"},
                {"participant_id": outsider["id"], "amount": "110000.00"},
            ],
        },
    )

    assert invalid_sum.status_code == 422
    assert "sumar exactamente" in invalid_sum.json()["detail"]
    assert negative.status_code == 422
    assert foreign_person.status_code == 422
    assert client.get(
        f"/api/boards/{home['id']}/expenses", headers=member
    ).json() == []


def test_equal_expense_rejects_foreign_payer_or_participant(client):
    member = authenticated_headers(client, "member@example.com")
    home = create_board(client, member, "Hogar")
    trip = create_board(client, member, "Viaje")
    home_person = create_participant(client, member, home["id"], "Ana")
    trip_person = create_participant(client, member, trip["id"], "Luis")
    payload = {
        "name": "Cena",
        "amount": "100.00",
        "category": "Comidas",
        "expense_type": "equal",
    }

    wrong_payer = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json={
            **payload,
            "payer_id": trip_person["id"],
            "participant_ids": [home_person["id"]],
        },
    )
    wrong_participant = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json={
            **payload,
            "payer_id": home_person["id"],
            "participant_ids": [home_person["id"], trip_person["id"]],
        },
    )

    assert wrong_payer.status_code == 422
    assert wrong_participant.status_code == 422

