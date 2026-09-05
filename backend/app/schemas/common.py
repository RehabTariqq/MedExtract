from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[Any] = None


class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None