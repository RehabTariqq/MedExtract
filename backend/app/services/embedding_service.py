import time

import cohere

from app.core.config import COHERE_API_KEY

EMBEDDING_DIM = 1024
EMBED_MODEL = "embed-english-v3.0"
BATCH_SIZE = 96  # Cohere's hard limit per embed call

_client: cohere.ClientV2 | None = None


def _get_client() -> cohere.ClientV2:
    global _client
    if _client is None:
        if not COHERE_API_KEY:
            raise RuntimeError("COHERE_API_KEY is not set. Add it to backend/.env (or your Render env vars).")
        _client = cohere.ClientV2(api_key=COHERE_API_KEY)
    return _client


def _embed_batch(texts: list[str], input_type: str) -> list[list[float]]:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = _get_client().embed(
                texts=texts,
                model=EMBED_MODEL,
                input_type=input_type,
                embedding_types=["float"],
            )
            return response.embeddings.float_
        except Exception as e:  # trial keys are rate limited; back off and retry
            last_error = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Cohere embedding failed: {last_error}")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed document chunks (for storing)."""
    vectors: list[list[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        vectors.extend(_embed_batch(texts[i : i + BATCH_SIZE], "search_document"))
    return vectors


def embed_query(text: str) -> list[float]:
    """Embed a user question (for searching). Cohere v3 needs a different input_type for queries."""
    return _embed_batch([text], "search_query")[0]


# Backwards-compatible alias
def embed_text(text: str) -> list[float]:
    return embed_query(text)
