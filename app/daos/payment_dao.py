from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.payment_models import AccountORM, TransactionORM
import uuid


class PaymentDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_account_by_user_id(self, user_id) -> Optional[AccountORM]:
        query = await self.session.execute(
            select(AccountORM).where(AccountORM.user_id == user_id)
        )
        account = query.scalars().all()

        return account

    async def check_user_account(self, user_id, account_id):
        query = await self.session.execute(
            select(AccountORM).where(AccountORM.user_id == user_id, AccountORM.account_id == account_id)
        )

        account = query.scalar()

        return account

    async def create_user_account(self, user_id, account_id):
        user_id = uuid.UUID(user_id).hex
        account = AccountORM(user_id=user_id, account_id=account_id, balance=0)
        self.session.add(account)

        await self.session.commit()
        await self.session.refresh(account)

        return account

    async def check_transaction(self, transaction_id, account_id):
        query = await self.session.execute(
            select(TransactionORM).where(TransactionORM.transaction_id == transaction_id, TransactionORM.account_id == account_id)
        )

        transaction = query.scalar()

        return transaction
        
    async def create_transaction(self, account_id, transaction_id, amount):
        account = await self.session.get(
            AccountORM, 
            account_id, 
            with_for_update=True
        )
        if not account:
            raise ValueError("Account not found")
        
        new_balance = account.balance + amount
        if new_balance < 0:
            raise ValueError("Insufficient funds")

        account.balance = new_balance
        
        transaction = TransactionORM(
            account_id=account_id,
            transaction_id=transaction_id,
            amount=amount
        )
    
        self.session.add(transaction)
        await self.session.flush()
        await self.session.refresh(transaction)
        
        return transaction
    
    async def get_transaction_by_accounts(self, accounts):
        transactions_query = select(TransactionORM).where(
            TransactionORM.account_id.in_([account.id for account in accounts])
        ).order_by(TransactionORM.created_at.desc())
        
        result = await self.session.execute(transactions_query)
        transactions = result.scalars().all()

        return transactions