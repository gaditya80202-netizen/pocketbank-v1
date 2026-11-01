# Architecture notes

PocketBank is deliberately a small monolithic API. It is a review target, not a production banking architecture.

```text
HTTP client / Swagger UI
          |
          v
     FastAPI routes  (app/main.py)
          |
          v
   Pydantic contracts (app/models.py)
          |
          v
   Business services  (app/service.py)
          |
          v
    SQLite database   (app/database.py)
       |         |
   accounts   transfers + ledger entries
```

## Request flow

1. FastAPI parses and validates the incoming JSON using the Pydantic request models.
2. The route obtains a request-scoped SQLite connection through `get_database`.
3. The route calls a function in `service.py` to apply business rules.
4. The service reads or writes the database using parameterized SQL.
5. A response model defines the shape returned to the caller.

## Transfer consistency

A transfer starts an SQLite `BEGIN IMMEDIATE` transaction. It verifies both accounts and the sender's balance, creates a transfer record, updates both balances, and inserts a debit and a credit ledger entry. The transaction commits only if all steps succeed; exceptions cause rollback. Integer cents are stored in SQLite to avoid binary floating-point arithmetic for money.

## Deliberate limits

- No authentication or per-customer authorization.
- No real payment rails, external bank connection, KYC, AML, or regulatory workflow.
- No production-grade concurrency, audit, disaster-recovery, or operational controls.
- The API is intended for localhost demonstrations with fictional data.
