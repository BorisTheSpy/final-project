from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    email: EmailStr
    role: Optional[str] = "Customer"


class UserCreate(UserBase):
    password: str # Password is not stored, but required for creation


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


class User(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(User):
    token: str