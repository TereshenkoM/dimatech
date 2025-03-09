from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
    father_name: str
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)
    is_super_user: bool = Field(default=False)
