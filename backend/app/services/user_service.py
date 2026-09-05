from datetime import datetime
from bson import ObjectId
from app.db.database import database
from app.schemas.user import UserCreate, UserResponse
from app.core.exceptions import NotFoundException

collection = database["users"]


def serialize_user(user: dict) -> UserResponse:
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        created_at=user["created_at"],
    )


async def create_user(user_data: UserCreate) -> UserResponse:
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "created_at": datetime.utcnow(),
    }
    result = await collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return serialize_user(user_doc)


async def get_user(user_id: str) -> UserResponse:
    if not ObjectId.is_valid(user_id):
        raise NotFoundException("Invalid user ID")
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise NotFoundException("User not found")
    return serialize_user(user)


async def list_users() -> list[UserResponse]:
    users = []
    async for user in collection.find():
        users.append(serialize_user(user))
    return users