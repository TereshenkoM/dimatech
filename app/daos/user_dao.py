from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_models import UserORM


class UserDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_user_by_email(self, email: str) -> Optional[UserORM]:
        query = await self.session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        user = query.scalar_one_or_none()

        return user