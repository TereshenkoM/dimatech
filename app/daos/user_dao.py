from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def create_user(
        self, email, password,
        first_name, last_name, father_name
    ):
        user = UserORM(
            emai=email,
            first_name=first_name,
            last_name=last_name,
            father_name=father_name
        )
        user.set_password(password=password)
        self.session.add(user)

        await self.session.commit()

    async def update_user(
        self, email, password,
        first_name, last_name, father_name
    ):
        query = await self.session.execute(select(UserORM).filter(
            UserORM.email == email
        ))
        user = query.scalar_one_or_none()
        if user:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.father_name = father_name
            user.set_password(password)
            await self.session.commit()

            return user
        else:
            raise Exception("User not found")

    async def delete_user(self, user_id):
        result = await self.session.execute(
            select(UserORM).filter(UserORM.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise Exception("User not found")

        await self.session.delete(user)
        await self.session.commit()
