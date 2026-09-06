from pydantic import BaseModel
from typing import Optional


class QuestionRequest(BaseModel):
    question: str


class SourceItem(BaseModel):
    document_id: str
    page_number: int
    source_text: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceItem]