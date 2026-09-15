import cohere
from app.core.config import COHERE_API_KEY

_client = cohere.ClientV2(api_key=COHERE_API_KEY)

EMBEDDING_DIM = 1024


def embed_text(text: str) -> list[float]:
    response = _client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"],
    )
    return response.embeddings.float_[0]


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = _client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"],
    )
    return response.embeddings.float_