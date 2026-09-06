import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from app.services.embedding_service import EMBEDDING_DIM

COLLECTION_NAME = "medextract_chunks"

client = QdrantClient(host="localhost", port=6333)


def ensure_collection():
    collections = client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def upsert_chunks(chunks: list[dict], embeddings: list[list[float]]):
    ensure_collection()
    points = []
    for chunk, vector in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "page_number": chunk["page_number"],
                    "text": chunk["text"],
                },
            )
        )
    client.upsert(collection_name=COLLECTION_NAME, points=points)


def search_similar(query_vector: list[float], document_id: str | None = None, top_k: int = 5):
    ensure_collection()
    query_filter = None
    if document_id:
        query_filter = Filter(
            must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
        )
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=query_filter,
        limit=top_k,
    )
    return results