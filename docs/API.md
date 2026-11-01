# PocketBank API reference

This reference describes the clean `main` branch. All amounts are decimal currency values with two fractional digits. The currency is fictional and is not connected to any real bank or payment network.

## `POST /accounts`

Create an account.

Request:

```json
{
  "owner_name": "Aarav Mehta",
  "opening_deposit": "500.00"
}
```

`opening_deposit` is optional and defaults to `0.00`. The response includes an opaque account ID, owner name, balance, and UTC creation timestamp. A non-zero opening deposit creates a `DEPOSIT` ledger entry.

## `GET /accounts`

List all accounts in the local demo database.

## `GET /accounts/{account_id}`

Return one account and its current balance. Returns `404` when the account does not exist.

## `GET /accounts/{account_id}/transactions?limit=50`

Return the newest ledger entries for the account. `limit` must be between 1 and 100. Entry types are `DEPOSIT`, `DEBIT`, and `CREDIT`. Returns `404` for an unknown account.

## `GET /accounts/{account_id}/activity-summary`

Return the account's aggregate ledger activity:

- `total_credits` — sum of opening deposits and incoming transfers.
- `total_debits` — sum of outgoing transfers.
- `net_flow` — credits minus debits.
- `transaction_count` — number of ledger entries.

Returns `404` when the account does not exist. Values are returned with two decimal places.

## `POST /transfers`

Transfer simulated funds between two different accounts.

Request:

```json
{
  "from_account_id": "SENDER_ID",
  "to_account_id": "RECIPIENT_ID",
  "amount": "75.25",
  "reference": "Demo transfer"
}
```

The amount must be greater than zero and have at most two decimal places. Both accounts must exist, and the sender must have sufficient funds. A successful transfer writes a transfer record plus one debit and one credit ledger entry inside a database transaction.

Possible errors:

- `400` — source and destination are the same account.
- `404` — source or destination account does not exist.
- `409` — insufficient funds.
- `422` — request validation failed.

## `GET /transfers/{transfer_id}`

Return the receipt for a completed transfer. Returns `404` when the transfer does not exist.

## Interactive schema

FastAPI exposes the generated OpenAPI schema and interactive Swagger UI at `/docs` while the server is running.
