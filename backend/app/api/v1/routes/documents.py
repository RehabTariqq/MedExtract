from fastapi import APIRouter, BackgroundTasks, File, UploadFile

from app.core.exceptions import ValidationException
from app.schemas.document import DocumentResponse
from app.services import document_service, processing_service, storage_service

router = APIRouter()


@router.get("/ping")
def ping_documents():
    return {"message": "documents route working"}


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    filename = file.filename or "report.pdf"
    content = await file.read()

    is_pdf_type = file.content_type == "application/pdf" or filename.lower().endswith(".pdf")
    if not is_pdf_type or not content.startswith(b"%PDF"):
        raise ValidationException("Only PDF files are allowed")
    if len(content) > storage_service.MAX_FILE_SIZE:
        raise ValidationException("File exceeds maximum size of 20MB")

    file_path = storage_service.save_upload_file(content, filename)
    document = await document_service.create_document(filename, file_path)

    # Return immediately; the slow work happens after the response is sent.
    background_tasks.add_task(processing_service.process_document, document.id, file_path)
    return document


@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
async def reprocess_document(document_id: str, background_tasks: BackgroundTasks):
    """Re-run extraction/embedding for a document (e.g. ones uploaded before the bug fixes)."""
    file_path = await document_service.get_file_path(document_id)
    await document_service.set_status(document_id, "processing")
    background_tasks.add_task(processing_service.process_document, document_id, file_path)
    return await document_service.get_document(document_id)


@router.get("/", response_model=list[DocumentResponse])
async def list_documents():
    return await document_service.list_documents()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    return await document_service.get_document(document_id)


@router.get("/{document_id}/pages")
async def get_document_pages(document_id: str):
    return await document_service.get_document_pages(document_id)


@router.get("/{document_id}/tests")
async def get_document_tests(document_id: str):
    return await document_service.get_document_tests(document_id)


@router.get("/{document_id}/summary")
async def get_document_summary(document_id: str):
    summary = await document_service.get_summary(document_id)
    return {"summary": summary}
