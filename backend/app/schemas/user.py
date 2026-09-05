from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime


class UserInDB(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)