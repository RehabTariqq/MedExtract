from fastapi import APIRouter
from app.services import search_service

router = APIRouter()


@router.get("/search")
async def search(q: str):
    return await search_service.combined_search(q)