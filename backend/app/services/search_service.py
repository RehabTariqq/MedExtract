from app.db.database import database
from app.services.retrieval_service import retrieve_relevant_chunks

collection = database["documents"]


async def keyword_search(query: str) -> list[dict]:
    results = []
    cursor = collection.find({
        "$or": [
            {"filename": {"$regex": query, "$options": "i"}},
            {"tests.test_name": {"$regex": query, "$options": "i"}},
        ]
    })
    async for doc in cursor:
        results.append({
            "type": "keyword",
            "document_id": str(doc["_id"]),
            "filename": doc["filename"],
            "matched_tests": [t["test_name"] for t in doc.get("tests", []) if query.lower() in t["test_name"].lower()],
        })
    return results


def semantic_search(query: str) -> list[dict]:
    chunks = retrieve_relevant_chunks(query, document_id=None, top_k=5)
    return [
        {
            "type": "semantic",
            "document_id": c["document_id"],
            "page_number": c["page_number"],
            "text": c["text"][:200],
            "score": c["score"],
        }
        for c in chunks
    ]


async def combined_search(query: str) -> dict:
    keyword_results = await keyword_search(query)
    semantic_results = semantic_search(query)
    return {"keyword_results": keyword_results, "semantic_results": semantic_results}