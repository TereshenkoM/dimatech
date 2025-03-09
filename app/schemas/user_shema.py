from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str = Field(min_length=8)
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)
    is_super_user: bool = Field(default=False)
