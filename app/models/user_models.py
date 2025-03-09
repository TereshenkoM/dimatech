from app.database.config import Base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import text
from typing import Annotated
from passlib.context import CryptContext
from datetime import datetime


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[Annotated[int, mapped_column(primary_key=True, index=True)]]
    email: Mapped[Annotated[str, mapped_column(unique=True, index=True, nullable=False)]]
    first_name: Mapped[Annotated[str, mapped_column(nullable=False)]]
    last_name: Mapped[Annotated[str, mapped_column(nullable=False)]]
    father_name: Mapped[str]
    password: Mapped[Annotated[str, 128, mapped_column(nullable=False)]]
    is_active: Mapped[Annotated[bool, mapped_column(default=True)]]
    is_staff: Mapped[Annotated[bool, mapped_column(default=False)]]
    is_super_user: Mapped[Annotated[bool, mapped_column(default=False)]]
    created_at: Mapped[Annotated[
        datetime, mapped_column(
            server_default=text("TIMEZONE('utc', now()::timestamp)")
        )
    ]]

    @validates('password')
    def validate_password(self, password: str) -> str:
        if len(password) < 8:
            raise ValueError('Минимальная длина пароля должна составлять 8 символов')
        return password

    def set_password(self, password: str) -> None:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password)


    def __str__(self):
        return f'{self.id} - {self.password}'