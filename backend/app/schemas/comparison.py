from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TestHistoryItem(BaseModel):
    document_id: str
    filename: str
    uploaded_at: datetime
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: str


class ComparisonResponse(BaseModel):
    test_name: str
    history: list[TestHistoryItem]
    comparisons: list[dict]