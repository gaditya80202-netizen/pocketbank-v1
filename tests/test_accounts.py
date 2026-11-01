"""Account creation and lookup tests."""

from decimal import Decimal


def test_create_account_starts_with_zero_balance(client):
    response = client.post("/accounts", json={"owner_name": "Aarav Mehta"})

    assert response.status_code == 201
    body = response.json()
    assert body["owner_name"] == "Aarav Mehta"
    assert Decimal(body["balance"]) == Decimal("0.00")
    assert body["id"]


def test_opening_deposit_is_recorded_in_the_ledger(client):
    account_response = client.post(
        "/accounts",
        json={"owner_name": "Mira Shah", "opening_deposit": "1250.50"},
    )
    account = account_response.json()

    assert account_response.status_code == 201
    assert Decimal(account["balance"]) == Decimal("1250.50")

    transactions = client.get(f"/accounts/{account['id']}/transactions")
    assert transactions.status_code == 200
    assert len(transactions.json()) == 1
    assert transactions.json()[0]["entry_type"] == "DEPOSIT"
    assert Decimal(transactions.json()[0]["amount"]) == Decimal("1250.50")


def test_account_lookup_returns_404_for_unknown_id(client):
    response = client.get("/accounts/not-a-real-account")

    assert response.status_code == 404


def test_account_creation_rejects_invalid_owner_name(client):
    response = client.post("/accounts", json={"owner_name": " "})

    assert response.status_code == 422
