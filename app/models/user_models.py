import uuid
from datetime import datetime
from typing import Annotated

from passlib.context import CryptContext
from sqlalchemy import UUID as SA_UUID
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.config import Base


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[Annotated[
        uuid.UUID,
        mapped_column(
            SA_UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    ]]
    email: Mapped[Annotated[str, mapped_column(
        unique=True, index=True, nullable=False
    )]]
    first_name: Mapped[Annotated[str, mapped_column(nullable=False)]]
    last_name: Mapped[Annotated[str, mapped_column(nullable=False)]]
    father_name: Mapped[str]
    password: Mapped[Annotated[str, mapped_column(nullable=False)]]
    is_active: Mapped[Annotated[bool, mapped_column(default=True)]]
    is_staff: Mapped[Annotated[bool, mapped_column(default=False)]]
    is_super_user: Mapped[Annotated[bool, mapped_column(default=False)]]
    created_at: Mapped[Annotated[
        datetime,
        mapped_column(server_default=text("TIMEZONE('utc', now()::timestamp)"))
    ]]

    def set_password(self, password: str) -> None:
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password)

    def get_fullname(self):
        if self.father_name:
            return f"{self.last_name} {self.first_name} {self.father_name}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.id} - {self.password}"
