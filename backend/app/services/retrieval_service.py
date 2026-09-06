from app.services.embedding_service import embed_text
from app.services.vector_store import search_similar


def retrieve_relevant_chunks(query: str, document_id: str | None = None, top_k: int = 5) -> list[dict]:
    query_vector = embed_text(query)
    results = search_similar(query_vector, document_id=document_id, top_k=top_k)

    chunks = []
    for r in results:
        chunks.append({
            "chunk_id": r.payload.get("chunk_id"),
            "document_id": r.payload.get("document_id"),
            "page_number": r.payload.get("page_number"),
            "text": r.payload.get("text"),
            "score": r.score,
        })
    return chunks