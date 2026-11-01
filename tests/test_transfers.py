"""Transfer behavior and ledger consistency tests."""

from decimal import Decimal


def make_account(client, owner_name, opening_deposit):
    response = client.post(
        "/accounts",
        json={"owner_name": owner_name, "opening_deposit": str(opening_deposit)},
    )
    assert response.status_code == 201
    return response.json()


def test_transfer_updates_both_balances_and_creates_two_ledger_entries(client):
    sender = make_account(client, "Aarav Mehta", "500.00")
    recipient = make_account(client, "Mira Shah", "100.00")

    response = client.post(
        "/transfers",
        json={
            "from_account_id": sender["id"],
            "to_account_id": recipient["id"],
            "amount": "125.50",
            "reference": "Rent split",
        },
    )

    assert response.status_code == 201
    transfer = response.json()
    assert Decimal(transfer["amount"]) == Decimal("125.50")
    assert transfer["reference"] == "Rent split"

    sender_after = client.get(f"/accounts/{sender['id']}").json()
    recipient_after = client.get(f"/accounts/{recipient['id']}").json()
    assert Decimal(sender_after["balance"]) == Decimal("374.50")
    assert Decimal(recipient_after["balance"]) == Decimal("225.50")

    sender_entries = client.get(f"/accounts/{sender['id']}/transactions").json()
    recipient_entries = client.get(f"/accounts/{recipient['id']}/transactions").json()
    sender_transfer_entries = [entry for entry in sender_entries if entry["transfer_id"] == transfer["id"]]
    recipient_transfer_entries = [entry for entry in recipient_entries if entry["transfer_id"] == transfer["id"]]
    assert len(sender_transfer_entries) == 1
    assert len(recipient_transfer_entries) == 1
    assert sender_transfer_entries[0]["entry_type"] == "DEBIT"
    assert recipient_transfer_entries[0]["entry_type"] == "CREDIT"


def test_transfer_rejects_insufficient_funds_without_changing_balances(client):
    sender = make_account(client, "Aarav Mehta", "25.00")
    recipient = make_account(client, "Mira Shah", "10.00")

    response = client.post(
        "/transfers",
        json={
            "from_account_id": sender["id"],
            "to_account_id": recipient["id"],
            "amount": "30.00",
        },
    )

    assert response.status_code == 409
    assert Decimal(client.get(f"/accounts/{sender['id']}").json()["balance"]) == Decimal("25.00")
    assert Decimal(client.get(f"/accounts/{recipient['id']}").json()["balance"]) == Decimal("10.00")
    sender_entries = client.get(f"/accounts/{sender['id']}/transactions").json()
    assert len(sender_entries) == 1
    assert sender_entries[0]["entry_type"] == "DEPOSIT"


def test_transfer_rejects_same_source_and_destination(client):
    account = make_account(client, "Aarav Mehta", "100.00")

    response = client.post(
        "/transfers",
        json={
            "from_account_id": account["id"],
            "to_account_id": account["id"],
            "amount": "10.00",
        },
    )

    assert response.status_code == 400
    assert Decimal(client.get(f"/accounts/{account['id']}").json()["balance"]) == Decimal("100.00")


def test_transfer_rejects_unknown_destination(client):
    sender = make_account(client, "Aarav Mehta", "100.00")

    response = client.post(
        "/transfers",
        json={
            "from_account_id": sender["id"],
            "to_account_id": "missing-account",
            "amount": "10.00",
        },
    )

    assert response.status_code == 404
    assert Decimal(client.get(f"/accounts/{sender['id']}").json()["balance"]) == Decimal("100.00")


def test_transfer_rejects_zero_amount(client):
    sender = make_account(client, "Aarav Mehta", "100.00")
    recipient = make_account(client, "Mira Shah", "0.00")

    response = client.post(
        "/transfers",
        json={
            "from_account_id": sender["id"],
            "to_account_id": recipient["id"],
            "amount": "0.00",
        },
    )

    assert response.status_code == 422


def test_transfer_receipt_can_be_retrieved(client):
    sender = make_account(client, "Aarav Mehta", "100.00")
    recipient = make_account(client, "Mira Shah", "0.00")
    created = client.post(
        "/transfers",
        json={
            "from_account_id": sender["id"],
            "to_account_id": recipient["id"],
            "amount": "12.34",
        },
    ).json()

    receipt = client.get(f"/transfers/{created['id']}")

    assert receipt.status_code == 200
    assert receipt.json()["id"] == created["id"]
    assert Decimal(receipt.json()["amount"]) == Decimal("12.34")


def test_transaction_history_rejects_unknown_account(client):
    response = client.get("/accounts/missing-account/transactions")

    assert response.status_code == 404


def test_transaction_limit_is_bounded(client):
    response = client.get("/accounts/some-account/transactions?limit=1000")

    assert response.status_code == 422
