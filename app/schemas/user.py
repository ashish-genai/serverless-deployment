from pydantic import BaseModel
from typing import Optional
from ..models.user import UserRole

class UserBase(BaseModel):
    email: str
    username: str
    role: UserRole = UserRole.EMPLOYEE

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True