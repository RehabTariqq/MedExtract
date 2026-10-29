from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str  # uploaded | processing | processed | failed
    uploaded_at: datetime
    error: Optional[str] = None
