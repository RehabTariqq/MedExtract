from fastapi import APIRouter
from app.api.v1.routes import documents, users, qa

api_router = APIRouter()

api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(qa.router, tags=["Q&A"])