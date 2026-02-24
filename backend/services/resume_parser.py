from pypdf import PdfReader
from docx import Document
from io import BytesIO


def extract_text(file_bytes: bytes, filename: str) -> str:

    if filename.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif filename.lower().endswith(".docx"):
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        return file_bytes.decode(errors="ignore")