from datetime import datetime
from app.db.database import database

collection = database["conversations"]


async def save_turn(session_id: str, role: str, content: str):
    await collection.insert_one({
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow(),
    })


async def get_recent_turns(session_id: str, limit: int = 10) -> list[dict]:
    turns = []
    cursor = collection.find({"session_id": session_id}).sort("timestamp", -1).limit(limit)
    async for turn in cursor:
        turns.append({"role": turn["role"], "content": turn["content"]})
    return list(reversed(turns))