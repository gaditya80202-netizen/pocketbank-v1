# PocketBank — AI Pull-Request Review Demo

PocketBank is a small **simulated banking API** built to give an AI pull-request review agent a realistic codebase to inspect. It supports account creation, opening deposits, transfers, receipts, and transaction history.

> **Important:** This is an educational demonstration only. It is not a real banking system. It has no real customer data, authentication, payment rails, KYC, regulatory controls, production key management, or deployment hardening. Never connect it to real money or use real credentials.

## Why this repository exists

The project is intentionally small enough to understand, but has multiple files, API contracts, persistence, business rules, and tests. Its `main` branch is the clean baseline. Separate `demo/*` branches introduce focused pull-request scenarios so an AI reviewer can demonstrate security, quality, testing, and documentation review.

## Features

- Create simulated accounts with an optional opening deposit.
- View accounts and balances.
- Transfer simulated funds atomically between accounts.
- Prevent self-transfers and transfers that exceed the sender's balance.
- Record matching debit and credit ledger entries.
- Retrieve a transfer receipt and account transaction history.
- Interactive API documentation at `/docs`.
- SQLite persistence; no external database server is required.

## Requirements

- Python 3.11 or newer.
- `pip`.

## Run locally (Fedora / Linux)

```bash
cd banking-review-demo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

The API starts at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` to try the endpoints. The SQLite file `banking_demo.db` is created automatically and is ignored by Git.

To use a different database path for a one-off run:

```bash
BANKING_DATABASE_PATH=/tmp/pocketbank-demo.db uvicorn app.main:app --reload
```

## Seed two fictional accounts

In another terminal, with the virtual environment activated:

```bash
python -m scripts.seed_demo
```

The script creates two fictional accounts and performs one small sample transfer only when the database is empty. It prints the account IDs. You can then inspect the results in `/docs`.

## Run tests

```bash
pytest
```

The tests use a temporary SQLite database, so they do not change your local demo data.

## Main API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Process health check |
| `POST` | `/accounts` | Create an account, optionally with an opening deposit |
| `GET` | `/accounts` | List accounts |
| `GET` | `/accounts/{account_id}` | Get account and current balance |
| `GET` | `/accounts/{account_id}/transactions` | List up to 100 ledger entries |
| `POST` | `/transfers` | Transfer simulated funds |
| `GET` | `/transfers/{transfer_id}` | Retrieve a transfer receipt |

## Example API calls

Create an account:

```bash
curl -X POST http://127.0.0.1:8000/accounts \\
  -H 'Content-Type: application/json' \\
  -d '{"owner_name":"Aarav Mehta","opening_deposit":"500.00"}'
```

Create a second account, then copy both returned IDs into a transfer request:

```bash
curl -X POST http://127.0.0.1:8000/transfers \\
  -H 'Content-Type: application/json' \\
  -d '{"from_account_id":"SENDER_ID","to_account_id":"RECIPIENT_ID","amount":"75.25","reference":"Demo transfer"}'
```

## Repository map

```text
app/
  database.py   SQLite schema, connection setup, request dependency
  main.py       FastAPI application factory and HTTP endpoints
  models.py     Pydantic request/response contracts
  service.py    Account, transfer, ledger, and summary business rules
scripts/
  seed_demo.py  Creates fictional demo data
 tests/         API and business-behavior tests
 docs/          Architecture, API, safety, and showcase instructions
 showcase/      PR scenario descriptions
```

## Showcase PRs for the AI reviewer

The repository includes local Git branches (also provided in the companion Git bundle):

- `demo/security-hardcoded-secret` — hardcoded admin credential and unsafe SQL construction.
- `demo/quality-overdraft-check` — a transfer-validation regression that can allow an overdraft.
- `demo/tests-daily-limit-no-tests` — a daily outgoing-transfer limit is implemented and documented, but its boundary behavior is not tested.
- `demo/docs-statement-endpoint` — a new public endpoint is added without updating the API documentation.
- `demo/clean-activity-summary` — a complete activity-summary feature with tests and documentation.

See [`docs/SHOWCASE_GUIDE.md`](docs/SHOWCASE_GUIDE.md) for exact push and PR instructions. The intentionally defective branches are **review exercises only**; do not deploy or use them as a starting point for real software.

## License

MIT. See [`LICENSE`](LICENSE).
