from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class AccountResponse(BaseModel):
    id: str
    balance: int
    created_at: datetime

class TransactionResponse(BaseModel):
    id: str
    transaction_id: str
    account_id: str
    amount: int
    created_at: datetime

class UserInfoResponse(BaseModel):
    user_id: str
    user_fullname: str
    email: EmailStr

class AccountInfoResponse(BaseModel):
    accounts: List[AccountResponse]

class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]

class TransactionCreateRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    user_id: str
    account_id: str
    amount: int = Field(..., gt=0)
    signature: str = Field(..., min_length=64, max_length=64)

class SignatureRequest(BaseModel):
    transaction_id: str
    user_id: str
    account_id: str
    amount: int

class AdminAccountInfo(BaseModel):
    account_id: str
    balance: int

class AdminUserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    father_name: Optional[str]
    accounts: List[AdminAccountInfo]

class AdminUserListResponse(BaseModel):
    users: List[AdminUserResponse]

class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    father_name: Optional[str] = None
    password: str = Field(..., min_length=8)

class AdminUpdateUserRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    password: Optional[str] = None

class AdminDeleteUserRequest(BaseModel):
    user_id: str