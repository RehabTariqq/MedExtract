from fastapi import APIRouter
from app.api.v1.routes import documents, users, qa, comparison, search

api_router = APIRouter()

api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(qa.router, tags=["Q&A"])
api_router.include_router(comparison.router, tags=["Comparison"])
api_router.include_router(search.router, tags=["Search"])