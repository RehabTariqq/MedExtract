"""Runs the slow part of an upload (OCR, LLM extraction, embeddings) in the background."""
import json
import logging

from starlette.concurrency import run_in_threadpool

from app.services import (
    chunking_service,
    document_service,
    embedding_service,
    extraction_service,
    pdf_service,
    summary_service,
    vector_store,
)

logger = logging.getLogger(__name__)


async def process_document(document_id: str, file_path: str) -> None:
    try:
        await document_service.set_status(document_id, "processing")

        # 1. Text (blocking: pdfplumber + OCR) -> run in a worker thread
        pages = await run_in_threadpool(pdf_service.extract_text_from_pdf, file_path)
        await document_service.update_document_pages(document_id, pages, "processing")

        if not any(p["text"].strip() for p in pages):
            raise RuntimeError("No readable text found in this PDF (even after OCR).")

        # 2. Embeddings first, so Q&A works even if structured extraction has trouble
        chunks = chunking_service.chunk_pages(pages, document_id)
        if chunks:
            texts = [c["text"] for c in chunks]
            embeddings = await run_in_threadpool(embedding_service.embed_texts, texts)
            await run_in_threadpool(vector_store.upsert_chunks, chunks, embeddings)

        # 3. Structured test extraction, page by page
        all_tests: list[dict] = []
        for page in pages:
            tests = await run_in_threadpool(
                extraction_service.extract_tests_from_page, page["text"], page["page_number"]
            )
            all_tests.extend(tests)
        await document_service.save_extracted_tests(document_id, all_tests)

        # 4. Summary
        summary = await run_in_threadpool(summary_service.generate_report_summary, all_tests)
        await document_service.save_summary(document_id, summary)

        await document_service.set_status(document_id, "processed")
        logger.info("Document %s processed: %d chunks, %d tests", document_id, len(chunks), len(all_tests))

    except Exception as e:
        logger.exception("Processing failed for document %s", document_id)
        await document_service.set_status(document_id, "failed", error=f"{type(e).__name__}: {e}"[:500])
