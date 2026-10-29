import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PayloadSchemaType,
    PointStruct,
    VectorParams,
)

from app.core.config import QDRANT_API_KEY, QDRANT_HOST, QDRANT_PORT, QDRANT_URL
from app.services.embedding_service import EMBEDDING_DIM

COLLECTION_NAME = "medextract_chunks_v2"

if QDRANT_URL:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)
else:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

_collection_ready = False


def ensure_collection() -> None:
    global _collection_ready
    if _collection_ready:
        return
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )
    try:  # Qdrant Cloud needs an index to filter on a field efficiently
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="document_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )
    except Exception:
        pass  # already exists
    _collection_ready = True


def upsert_chunks(chunks: list[dict], embeddings: list[list[float]]) -> None:
    ensure_collection()
    points = [
        PointStruct(
            # Deterministic id: re-processing the same chunk overwrites instead of duplicating
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, chunk["chunk_id"])),
            vector=vector,
            payload={
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "page_number": chunk["page_number"],
                "text": chunk["text"],
            },
        )
        for chunk, vector in zip(chunks, embeddings)
    ]
    for i in range(0, len(points), 64):
        client.upsert(collection_name=COLLECTION_NAME, points=points[i : i + 64])


def search_similar(query_vector: list[float], document_id: str | None = None, top_k: int = 5):
    ensure_collection()
    query_filter = None
    if document_id:
        query_filter = Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))])
    # qdrant-client >= 1.16 removed .search(); query_points() is the replacement
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=top_k,
        with_payload=True,
    )
    return response.points
