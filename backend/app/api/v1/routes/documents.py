from fastapi import APIRouter, UploadFile, File
from app.schemas.document import DocumentResponse
from app.services import (
    document_service,
    storage_service,
    pdf_service,
    extraction_service,
    summary_service,
    chunking_service,
    embedding_service,
    vector_store,
)
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

    all_tests = []
    for page in pages:
        tests = extraction_service.extract_tests_from_page(page["text"], page["page_number"])
        all_tests.extend(tests)
    await document_service.save_extracted_tests(document.id, all_tests)

    summary_text = summary_service.generate_report_summary(all_tests)
    await document_service.save_summary(document.id, summary_text)

    chunks = chunking_service.chunk_pages(pages, document.id)
    if chunks:
        chunk_texts = [c["text"] for c in chunks]
        embeddings = embedding_service.embed_texts(chunk_texts)
        vector_store.upsert_chunks(chunks, embeddings)

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


@router.get("/{document_id}/tests")
async def get_document_tests(document_id: str):
    return await document_service.get_document_tests(document_id)


@router.get("/{document_id}/summary")
async def get_document_summary(document_id: str):
    summary = await document_service.get_summary(document_id)
    return {"summary": summary}