from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping_documents():
    return {"message": "documents route working"}