# parser.py
from pdfminer.high_level import extract_text
import docx
import os

def extract_text_from_pdf(path):
    try:
        return extract_text(path)
    except Exception as e:
        return ""

def extract_text_from_docx(path):
    try:
        doc = docx.Document(path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return "\n".join(fullText)
    except Exception as e:
        return ""

def parse_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(path)
    elif ext in [".txt"]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        return ""
