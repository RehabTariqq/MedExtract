from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]


async def check_connection() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False