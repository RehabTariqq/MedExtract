from fastapi import APIRouter

from app.schemas.qa import AnswerResponse, QuestionRequest
from app.services import rag_service

router = APIRouter()


# Plain `def` (not async): these call blocking network code, so FastAPI runs them in a thread
# instead of freezing the whole server while Cohere/Groq respond.
@router.post("/documents/{document_id}/ask", response_model=AnswerResponse)
def ask_document_question(document_id: str, request: QuestionRequest):
    return rag_service.answer_question(request.question, document_id=document_id)


@router.post("/ask", response_model=AnswerResponse)
def ask_all_documents(request: QuestionRequest):
    return rag_service.answer_question(request.question, document_id=None)
