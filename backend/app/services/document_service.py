from datetime import datetime
from bson import ObjectId
from app.db.database import database
from app.schemas.document import DocumentResponse
from app.core.exceptions import NotFoundException

collection = database["documents"]


def serialize_document(doc: dict) -> DocumentResponse:
    return DocumentResponse(
        id=str(doc["_id"]),
        filename=doc["filename"],
        status=doc["status"],
        uploaded_at=doc["uploaded_at"],
    )


async def create_document(filename: str, file_path: str) -> DocumentResponse:
    doc = {
        "filename": filename,
        "file_path": file_path,
        "status": "uploaded",
        "uploaded_at": datetime.utcnow(),
        "pages": [],
    }
    result = await collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_document(doc)


async def update_document_pages(document_id: str, pages: list[dict], status: str) -> None:
    await collection.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": {"pages": pages, "status": status}},
    )


async def list_documents() -> list[DocumentResponse]:
    docs = []
    async for doc in collection.find():
        docs.append(serialize_document(doc))
    return docs


async def get_document(document_id: str) -> DocumentResponse:
    if not ObjectId.is_valid(document_id):
        raise NotFoundException("Invalid document ID")
    doc = await collection.find_one({"_id": ObjectId(document_id)})
    if not doc:
        raise NotFoundException("Document not found")
    return serialize_document(doc)


async def get_document_pages(document_id: str) -> list[dict]:
    if not ObjectId.is_valid(document_id):
        raise NotFoundException("Invalid document ID")
    doc = await collection.find_one({"_id": ObjectId(document_id)})
    if not doc:
        raise NotFoundException("Document not found")
    return doc.get("pages", [])


async def save_extracted_tests(document_id: str, tests: list[dict]) -> None:
    await collection.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": {"tests": tests}},
    )


async def get_document_tests(document_id: str) -> list[dict]:
    if not ObjectId.is_valid(document_id):
        raise NotFoundException("Invalid document ID")
    doc = await collection.find_one({"_id": ObjectId(document_id)})
    if not doc:
        raise NotFoundException("Document not found")
    return doc.get("tests", [])


async def save_summary(document_id: str, summary: str) -> None:
    await collection.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": {"summary": summary}},
    )


async def get_summary(document_id: str) -> str:
    if not ObjectId.is_valid(document_id):
        raise NotFoundException("Invalid document ID")
    doc = await collection.find_one({"_id": ObjectId(document_id)})
    if not doc:
        raise NotFoundException("Document not found")
    return doc.get("summary", "")