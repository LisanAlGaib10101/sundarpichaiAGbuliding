import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file provided as bytes.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return clean_text(text)

def clean_text(text: str) -> str:
    """
    Cleans and normalizes the extracted text.
    """
    # Remove special characters but keep alphanumeric and some punctuation
    # Simple normalization: lowercase and removal of excessive whitespace
    text = text.replace('\n', ' ')
    text = " ".join(text.split())
    # Keep standard ascii + printable
    # For now, just return specific cleanup
    return text
