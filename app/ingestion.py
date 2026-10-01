from pathlib import Path
from io import BytesIO
import re
import fitz
from docx import Document

def normalize_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def ingest_uploaded_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()
    if suffix == ".txt":
        text = data.decode("utf-8", errors="replace")
    elif suffix == ".docx":
        doc = Document(BytesIO(data))
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif suffix == ".pdf":
        with fitz.open(stream=data, filetype="pdf") as doc:
            text = "\n".join(page.get_text("text") for page in doc)
    else:
        raise ValueError("Supported formats are .txt, .docx and .pdf.")
    text = normalize_text(text)
    if not text:
        raise ValueError("No readable text was found.")
    return text
