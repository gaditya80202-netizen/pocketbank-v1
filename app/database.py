"""SQLite setup and request-scoped connection management."""

import sqlite3
from collections.abc import Generator
from pathlib import Path

from fastapi import Request


def connect_database(database_path: str | Path) -> sqlite3.Connection:
    """Open a SQLite connection with row access and foreign keys enabled."""

    connection = sqlite3.connect(str(database_path), timeout=10, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    return connection


def initialize_database(database_path: str | Path) -> None:
    """Create the tables and indexes required by the demo application."""

    path = Path(database_path)
    if str(database_path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)

    connection = connect_database(database_path)
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                owner_name TEXT NOT NULL CHECK(length(owner_name) BETWEEN 2 AND 80),
                balance_cents INTEGER NOT NULL DEFAULT 0 CHECK(balance_cents >= 0),
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS transfers (
                id TEXT PRIMARY KEY,
                from_account_id TEXT NOT NULL REFERENCES accounts(id),
                to_account_id TEXT NOT NULL REFERENCES accounts(id),
                amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
                reference TEXT,
                created_at TEXT NOT NULL,
                CHECK(from_account_id <> to_account_id)
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                transfer_id TEXT REFERENCES transfers(id),
                account_id TEXT NOT NULL REFERENCES accounts(id),
                entry_type TEXT NOT NULL CHECK(entry_type IN ('DEPOSIT', 'DEBIT', 'CREDIT')),
                amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
                description TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_transactions_account_created
                ON transactions(account_id, created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_transfers_created
                ON transfers(created_at DESC);
            """
        )
    finally:
        connection.close()


def get_database(request: Request) -> Generator[sqlite3.Connection, None, None]:
    """Provide a database connection for one HTTP request and always close it."""

    connection = connect_database(request.app.state.database_path)
    try:
        yield connection
    finally:
        connection.close()
