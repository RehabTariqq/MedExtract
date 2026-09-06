from fastapi import APIRouter
from app.services import comparison_service
from app.schemas.comparison import ComparisonResponse

router = APIRouter()


@router.get("/tests/{test_name}/history", response_model=ComparisonResponse)
async def get_test_comparison(test_name: str):
    return await comparison_service.compare_test(test_name)