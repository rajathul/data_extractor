import pdfplumber
import fitz
import io

# def extract_text(file_path):
#     document = ""
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             page_document = page.extract_text()
#             if page_document:
#                 document += page_document.lower() + "\n"

#     return document.strip().encode("utf-8").decode("utf-8")

def extract_text(uploaded_file):
    document = ""

    # Convert uploaded file to bytes
    pdf_bytes = uploaded_file.getvalue()

    # First attempt: Use pdfplumber
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    document += text.lower() + "\n"

        if document.strip():  # If extraction was successful, return result
            return document.strip()
    
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    # Fallback: Use PyMuPDF (pymupdf) if pdfplumber fails
    try:
        with fitz.open("pdf", pdf_bytes) as pdf:
            for page in pdf:
                text = page.get_text("text")
                if text:
                    document += text.lower() + "\n"

        return document.strip()
    
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
        return "Error: Could not extract text from PDF."