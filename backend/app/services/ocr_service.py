import pytesseract
from pdf2image import convert_from_path


def ocr_pdf_page(file_path: str, page_number: int) -> str:
    images = convert_from_path(file_path, first_page=page_number, last_page=page_number)
    if not images:
        return ""
    return pytesseract.image_to_string(images[0])