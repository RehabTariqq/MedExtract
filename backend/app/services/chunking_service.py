import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

CHUNK_SIZE = 400  # tokens
CHUNK_OVERLAP = 50  # tokens


def chunk_pages(pages: list[dict], document_id: str) -> list[dict]:
    """
    Takes [{page_number, text}, ...] and returns a list of chunk dicts:
    {chunk_id, document_id, page_number, text}
    """
    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"]
        if not text.strip():
            continue

        tokens = encoding.encode(text)
        start = 0
        while start < len(tokens):
            end = min(start + CHUNK_SIZE, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens)

            chunks.append({
                "chunk_id": f"{document_id}_{chunk_index}",
                "document_id": document_id,
                "page_number": page["page_number"],
                "text": chunk_text,
            })

            chunk_index += 1
            if end == len(tokens):
                break
            start = end - CHUNK_OVERLAP

    return chunks