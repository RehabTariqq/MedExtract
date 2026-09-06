from fastapi import APIRouter, UploadFile, File
from app.schemas.document import DocumentResponse
from app.services import document_service, storage_service, pdf_service
from app.core.exceptions import ValidationException

router = APIRouter()

ALLOWED_TYPES = ["application/pdf"]


@router.get("/ping")
def ping_documents():
    return {"message": "documents route working"}


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise ValidationException("Only PDF files are allowed")

    content = await file.read()

    if len(content) > storage_service.MAX_FILE_SIZE:
        raise ValidationException("File exceeds maximum size of 20MB")

    file_path = storage_service.save_upload_file(content, file.filename)
    document = await document_service.create_document(file.filename, file_path)

    pages = pdf_service.extract_text_from_pdf(file_path)
    await document_service.update_document_pages(document.id, pages, "processed")

    document.status = "processed"
    return document


@router.get("/", response_model=list[DocumentResponse])
async def list_documents():
    return await document_service.list_documents()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    return await document_service.get_document(document_id)


@router.get("/{document_id}/pages")
async def get_document_pages(document_id: str):
    return await document_service.get_document_pages(document_id)