from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.payment_models import AccountORM, TransactionORM


class PaymentDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_account_by_user_id(self, user_id) -> Optional[AccountORM]:
        query = await self.session.execute(
            select(AccountORM).where(AccountORM.user_id == user_id)
        )
        account = query.scalars().all()

        return account