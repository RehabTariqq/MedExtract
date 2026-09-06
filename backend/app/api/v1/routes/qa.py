from fastapi import APIRouter
from app.schemas.qa import QuestionRequest, AnswerResponse
from app.services import rag_service

router = APIRouter()


@router.post("/documents/{document_id}/ask", response_model=AnswerResponse)
async def ask_document_question(document_id: str, request: QuestionRequest):
    result = rag_service.answer_question(request.question, document_id=document_id)
    return result
@router.post("/ask", response_model=AnswerResponse)
async def ask_all_documents(request: QuestionRequest):
    result = rag_service.answer_question(request.question, document_id=None)
    return result