"""Tests for the account activity summary feature."""

from decimal import Decimal


def create_account(client, name, deposit):
    response = client.post(
        "/accounts",
        json={"owner_name": name, "opening_deposit": str(deposit)},
    )
    assert response.status_code == 201
    return response.json()


def test_activity_summary_counts_opening_deposit_and_transfer_entries(client):
    sender = create_account(client, "Aarav Mehta", "500.00")
    recipient = create_account(client, "Mira Shah", "100.00")
    transfer = client.post(
        "/transfers",
        json={
            "from_account_id": sender["id"],
            "to_account_id": recipient["id"],
            "amount": "125.50",
        },
    )
    assert transfer.status_code == 201

    sender_summary = client.get(f"/accounts/{sender['id']}/activity-summary")
    recipient_summary = client.get(f"/accounts/{recipient['id']}/activity-summary")

    assert sender_summary.status_code == 200
    assert sender_summary.json()["transaction_count"] == 2
    assert Decimal(sender_summary.json()["total_credits"]) == Decimal("500.00")
    assert Decimal(sender_summary.json()["total_debits"]) == Decimal("125.50")
    assert Decimal(sender_summary.json()["net_flow"]) == Decimal("374.50")

    assert recipient_summary.status_code == 200
    assert recipient_summary.json()["transaction_count"] == 2
    assert Decimal(recipient_summary.json()["total_credits"]) == Decimal("225.50")
    assert Decimal(recipient_summary.json()["total_debits"]) == Decimal("0.00")
    assert Decimal(recipient_summary.json()["net_flow"]) == Decimal("225.50")


def test_activity_summary_returns_zero_totals_for_new_account(client):
    account = create_account(client, "Aarav Mehta", "0.00")

    response = client.get(f"/accounts/{account['id']}/activity-summary")

    assert response.status_code == 200
    assert response.json()["transaction_count"] == 0
    assert Decimal(response.json()["total_credits"]) == Decimal("0.00")
    assert Decimal(response.json()["total_debits"]) == Decimal("0.00")
    assert Decimal(response.json()["net_flow"]) == Decimal("0.00")


def test_activity_summary_returns_404_for_unknown_account(client):
    response = client.get("/accounts/missing-account/activity-summary")

    assert response.status_code == 404
