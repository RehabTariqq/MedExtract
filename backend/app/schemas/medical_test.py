from pydantic import BaseModel
from typing import Optional


class MedicalTest(BaseModel):
    test_name: str
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: str
    category: Optional[str] = None
    page_number: int
    source_text: str


class ExtractionResult(BaseModel):
    tests: list[MedicalTest]