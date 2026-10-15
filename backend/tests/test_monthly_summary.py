from decimal import Decimal

from app.monthly_summary import calculate_monthly_summary


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


def create_personal_expense(
    client,
    headers,
    board_id,
    participant_id,
    *,
    amount,
    expense_date,
):
    response = client.post(
        f"/api/boards/{board_id}/expenses",
        headers=headers,
        json={
            "name": "Gasto",
            "amount": amount,
            "category": "General",
            "date": expense_date,
            "payer_id": participant_id,
            "person_id": participant_id,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_monthly_summary_uses_decimal_and_allows_negative_remaining():
    consumed, remaining = calculate_monthly_summary(
        available_base=Decimal("100.00"),
        expense_totals=[Decimal("33.33"), Decimal("66.68")],
    )

    assert consumed == Decimal("100.01")
    assert remaining == Decimal("-0.01")


def test_member_can_configure_and_get_monthly_summary(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)

    configured = client.put(
        f"/api/boards/{board['id']}/monthly-summary/2026/1",
        headers=member,
        json={"available_base": "500000.00"},
    )
    fetched = client.get(
        f"/api/boards/{board['id']}/monthly-summary/2026/1",
        headers=member,
    )

    expected = {
        "board_id": board["id"],
        "year": 2026,
        "month": 1,
        "available_base": "500000.00",
        "consumed": "0.00",
        "remaining": "500000.00",
    }
    assert configured.status_code == 200
    assert configured.json() == expected
    assert fetched.status_code == 200
    assert fetched.json() == expected


def test_monthly_summary_uses_total_expenses_for_board_and_month(client):
    member = authenticated_headers(client, "member@example.com")
    home = create_board(client, member, "Hogar")
    trip = create_board(client, member, "Viaje")
    carla = create_participant(client, member, home["id"], "Carla")
    ana = create_participant(client, member, home["id"], "Ana")
    traveler = create_participant(client, member, trip["id"], "Luis")

    assert client.put(
        f"/api/boards/{home['id']}/monthly-summary/2026/1",
        headers=member,
        json={"available_base": "100.00"},
    ).status_code == 200
    create_personal_expense(
        client,
        member,
        home["id"],
        carla["id"],
        amount="20.00",
        expense_date="2026-01-01",
    )
    shared = client.post(
        f"/api/boards/{home['id']}/expenses",
        headers=member,
        json={
            "name": "Cena",
            "amount": "80.01",
            "category": "Comidas",
            "date": "2026-01-31",
            "payer_id": carla["id"],
            "expense_type": "equal",
            "participant_ids": [carla["id"], ana["id"]],
        },
    )
    assert shared.status_code == 201
    assert shared.json()["allocations"] == [
        {"participant_id": carla["id"], "amount": "40.01"},
        {"participant_id": ana["id"], "amount": "40.00"},
    ]
    create_personal_expense(
        client,
        member,
        home["id"],
        carla["id"],
        amount="999.00",
        expense_date="2026-02-01",
    )
    create_personal_expense(
        client,
        member,
        trip["id"],
        traveler["id"],
        amount="777.00",
        expense_date="2026-01-15",
    )

    january = client.get(
        f"/api/boards/{home['id']}/monthly-summary/2026/1",
        headers=member,
    )
    february = client.get(
        f"/api/boards/{home['id']}/monthly-summary/2026/2",
        headers=member,
    )

    assert january.status_code == 200
    assert january.json() == {
        "board_id": home["id"],
        "year": 2026,
        "month": 1,
        "available_base": "100.00",
        "consumed": "100.01",
        "remaining": "-0.01",
    }
    assert february.status_code == 200
    assert february.json() == {
        "board_id": home["id"],
        "year": 2026,
        "month": 2,
        "available_base": "0.00",
        "consumed": "999.00",
        "remaining": "-999.00",
    }


def test_monthly_available_is_reconfigured_for_same_month(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    url = f"/api/boards/{board['id']}/monthly-summary/2026/1"

    assert client.put(
        url,
        headers=member,
        json={"available_base": "100.00"},
    ).status_code == 200
    updated = client.put(
        url,
        headers=member,
        json={"available_base": "125.50"},
    )

    assert updated.status_code == 200
    assert updated.json()["available_base"] == "125.50"
    assert client.get(url, headers=member).json()["available_base"] == "125.50"


def test_monthly_available_rejects_negative_or_excess_precision(client):
    member = authenticated_headers(client, "member@example.com")
    board = create_board(client, member)
    url = f"/api/boards/{board['id']}/monthly-summary/2026/1"

    negative = client.put(
        url,
        headers=member,
        json={"available_base": "-0.01"},
    )
    excess_precision = client.put(
        url,
        headers=member,
        json={"available_base": "10.001"},
    )

    assert negative.status_code == 422
    assert excess_precision.status_code == 422


def test_non_member_cannot_configure_or_get_monthly_summary(client):
    owner = authenticated_headers(client, "owner@example.com")
    outsider = authenticated_headers(client, "outsider@example.com")
    board = create_board(client, owner)
    url = f"/api/boards/{board['id']}/monthly-summary/2026/1"

    configured = client.put(
        url,
        headers=outsider,
        json={"available_base": "100.00"},
    )
    fetched = client.get(url, headers=outsider)

    assert configured.status_code == 403
    assert fetched.status_code == 403
