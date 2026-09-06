import pdfplumber
from app.services.ocr_service import ocr_pdf_page


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Returns a list of {page_number, text} dicts, one per page.
    Falls back to OCR if a page has no extractable text (scanned page).
    """
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                text = ocr_pdf_page(file_path, i)
            pages.append({"page_number": i, "text": text})
    return pages