from app.database.config import Base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import text, ForeignKey, UUID as SA_UUID
from typing import Annotated
from datetime import datetime
import uuid


class AccountORM(Base):
    __tablename__ = 'account'

    id: Mapped[Annotated[
        uuid.UUID, 
        mapped_column(
            SA_UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    ]]    
    balance: Mapped[Annotated[int, mapped_column(nullable=False, default=0)]]
    user_id: Mapped[Annotated[uuid.UUID, mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False)]
    ]
    created_at: Mapped[Annotated[
        datetime, 
        mapped_column(server_default=text("TIMEZONE('utc', now()::timestamp)"))
    ]]

    @validates('balance')
    def validate_balance(self, balance: int) -> int:
        if len(balance) < 0:
            raise ValueError('Баланс не может быть отрицательным')
        return balance


class TransactionORM(Base):
    __tablename__ = 'transaction'

    id: Mapped[Annotated[
        uuid.UUID, 
        mapped_column(
            SA_UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    ]]    
    account_id: Mapped[Annotated[uuid.UUID, mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey('account.id', ondelete='CASCADE'),
        nullable=False)]
    ]
    amount: Mapped[Annotated[int, mapped_column(nullable=False)]]
    signature: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[Annotated[
        datetime, 
        mapped_column(server_default=text("TIMEZONE('utc', now()::timestamp)"))
    ]]

    @validates('amount')
    def validate_balance(self, amount: int) -> int:
        if len(amount) <= 0:
            raise ValueError('Сумма пополнения должна быть больше нуля')
        return amount