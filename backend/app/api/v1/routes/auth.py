from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.db.database import database
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()
collection = database["users_auth"]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(request: RegisterRequest):
    existing = await collection.find_one({"email": request.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(request.password)
    result = await collection.insert_one({"email": request.email, "password": hashed})
    token = create_access_token({"sub": str(result.inserted_id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(request: LoginRequest):
    user = await collection.find_one({"email": request.email})
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}