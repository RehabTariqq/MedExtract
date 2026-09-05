from fastapi import APIRouter
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()


@router.get("/ping")
def ping_users():
    return {"message": "users route working"}


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return await user_service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    return await user_service.get_user(user_id)


@router.get("/", response_model=list[UserResponse])
async def list_users():
    return await user_service.list_users()