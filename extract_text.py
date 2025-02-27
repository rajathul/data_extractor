import pytesseract
import pdfplumber


def extract_text(file_path):
    document = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_document = page.extract_text()
            if page_document:
                document += page_document.lower() + "\n"
            else:
                # Apply OCR with Portuguese language setting
                image = page.to_image()
                document += pytesseract.image_to_string(image, lang="por").lower() + "\n"

    return document.strip().encode("utf-8").decode("utf-8")