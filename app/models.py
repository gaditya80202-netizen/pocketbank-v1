"""Request and response models for the simulated banking API."""

from decimal import Decimal

from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

OwnerName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=80)]
Money = Annotated[Decimal, Field(max_digits=12, decimal_places=2)]


class AccountCreate(BaseModel):
    """Data required to create a simulated bank account."""

    owner_name: OwnerName
    opening_deposit: Money = Field(default=Decimal("0.00"), ge=0)


class AccountResponse(BaseModel):
    """Public representation of a simulated bank account."""

    id: str
    owner_name: str
    balance: Decimal
    created_at: str


class TransferCreate(BaseModel):
    """Data required to transfer simulated funds between two accounts."""

    from_account_id: str = Field(min_length=1, max_length=64)
    to_account_id: str = Field(min_length=1, max_length=64)
    amount: Money = Field(gt=0)
    reference: str | None = Field(default=None, max_length=120)


class TransferResponse(BaseModel):
    """Representation of a completed simulated transfer."""

    id: str
    from_account_id: str
    to_account_id: str
    amount: Decimal
    reference: str | None
    created_at: str


class TransactionResponse(BaseModel):
    """One debit, credit, or opening-deposit entry in an account ledger."""

    id: str
    transfer_id: str | None
    account_id: str
    entry_type: str
    amount: Decimal
    description: str
    created_at: str
