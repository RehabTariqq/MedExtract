from typing import Any, Optional
from pydantic import BaseModel, field_validator


def _to_str(v: Any) -> Optional[str]:
    """LLMs sometimes return numbers or null; always store text."""
    if v is None:
        return None
    s = str(v).strip()
    return s or None


class MedicalTest(BaseModel):
    test_name: str
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: str = "unclear"
    category: Optional[str] = None
    page_number: Optional[int] = None  # filled in by the backend, not the LLM
    source_text: str = ""

    @field_validator("test_name", "value", mode="before")
    @classmethod
    def _required_text(cls, v):
        s = _to_str(v)
        if s is None:
            raise ValueError("must not be empty")
        return s

    @field_validator("unit", "reference_range", "category", mode="before")
    @classmethod
    def _optional_text(cls, v):
        return _to_str(v)

    @field_validator("source_text", mode="before")
    @classmethod
    def _source_text(cls, v):
        return _to_str(v) or ""

    @field_validator("status", mode="before")
    @classmethod
    def _status(cls, v):
        s = (_to_str(v) or "unclear").lower()
        return s if s in {"normal", "high", "low", "unclear"} else "unclear"


class ExtractionResult(BaseModel):
    tests: list[MedicalTest] = []
