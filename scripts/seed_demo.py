"""Seed the local PocketBank database with fictional demonstration accounts."""

from decimal import Decimal

from app.database import connect_database
from app.main import app
from app.service import create_account, list_accounts, transfer_funds


def main() -> None:
    """Create two fictional accounts and one sample transfer if the DB is empty."""

    database_path = app.state.database_path
    connection = connect_database(database_path)
    try:
        existing_accounts = list_accounts(connection)
        if existing_accounts:
            print(f"Database already contains {len(existing_accounts)} account(s); no seed data added.")
            for account in existing_accounts:
                print(f"- {account['owner_name']}: {account['id']} (balance {account['balance']})")
            return

        aarav = create_account(connection, "Aarav Mehta", Decimal("1500.00"))
        mira = create_account(connection, "Mira Shah", Decimal("800.00"))
        transfer = transfer_funds(
            connection,
            str(aarav["id"]),
            str(mira["id"]),
            Decimal("125.50"),
            "Sample transfer",
        )

        print("Created fictional demo data:")
        print(f"- Aarav Mehta account ID: {aarav['id']}")
        print(f"- Mira Shah account ID:  {mira['id']}")
        print(f"- Sample transfer ID:    {transfer['id']}")
        print("No real bank or payment network was contacted.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
