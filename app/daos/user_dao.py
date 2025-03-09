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

    async def get_user_by_id(self, id: str) -> Optional[UserORM]:
        query = await self.session.execute(
            select(UserORM).where(UserORM.id == id)
        )
        user = query.scalar_one_or_none()

        return user
    
    async def get_users(self):
        query = await self.session.execute(
            select(UserORM)
        )

        users = query.scalars().all()

        return users

    async def create_user(self, email, password, first_name, last_name, father_name):
        user = UserORM(
            email = email,
            first_name=first_name,
            last_name=last_name,
            father_name = father_name
        )
        user.set_password(password=password)
        print(user.password)
        self.session.add(user)

        await self.session.commit()