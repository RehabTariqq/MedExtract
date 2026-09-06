from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.llm.factory import get_llm_client

RAG_PROMPT = """You are answering a question about a medical report, using ONLY the context excerpts below. These excerpts come directly from the user's uploaded document.

Rules:
- Answer only using information present in the context below.
- If the answer is not present in the context, say "I couldn't find that in this document" — do not guess or use outside medical knowledge.
- Never diagnose, recommend treatment, or state whether a value is dangerous.
- Keep the answer concise and directly grounded in the excerpts.

Context excerpts:
{context}

Question: {question}

Answer:
"""


def answer_question(question: str, document_id: str | None = None) -> dict:
    chunks = retrieve_relevant_chunks(question, document_id=document_id, top_k=5)

    if not chunks:
        return {
            "answer": "I couldn't find any relevant information in your documents.",
            "sources": [],
        }

        context = "\n\n".join(
        f"[Document {c['document_id']}, Page {c['page_number']}]: {c['text']}" for c in chunks
    )
    prompt = RAG_PROMPT.format(context=context, question=question)

    client = get_llm_client()
    answer = client.generate(prompt)

    sources = [
        {
            "document_id": c["document_id"],
            "page_number": c["page_number"],
            "source_text": c["text"][:300],
        }
        for c in chunks
    ]

    return {"answer": answer, "sources": sources}