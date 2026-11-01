"""Behavior tests for the account statement endpoint added in this demo PR."""

from decimal import Decimal


def test_account_statement_includes_owner_balance_and_ledger_entries(client):
    created = client.post(
        "/accounts",
        json={"owner_name": "Mira Shah", "opening_deposit": "250.00"},
    )
    assert created.status_code == 201
    account = created.json()

    response = client.get(f"/accounts/{account['id']}/statement")

    assert response.status_code == 200
    statement = response.json()
    assert statement["account_id"] == account["id"]
    assert statement["owner_name"] == "Mira Shah"
    assert Decimal(statement["current_balance"]) == Decimal("250.00")
    assert len(statement["entries"]) == 1
    assert statement["entries"][0]["entry_type"] == "DEPOSIT"


def test_account_statement_returns_404_for_unknown_account(client):
    response = client.get("/accounts/missing-account/statement")

    assert response.status_code == 404
