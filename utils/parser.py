"""
PDF text extraction using PyPDF2 and pdfplumber fallback.
"""

from pathlib import Path
from typing import BinaryIO, Union


def extract_text_from_pdf(file: Union[str, Path, BinaryIO, bytes]) -> str:
    """
    Extract text from a PDF file.
    Uses PyPDF2 first, then pdfplumber if needed for better extraction.
    """
    if isinstance(file, (str, Path)):
        path = Path(file)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        with open(path, "rb") as f:
            data = f.read()
    elif isinstance(file, bytes):
        data = file
    elif hasattr(file, "read"):
        data = file.read()
        if hasattr(file, "seek"):
            file.seek(0)
    else:
        raise TypeError("file must be path (str/Path), file-like, or bytes")

    text = _extract_with_pypdf2(data)
    if not text or len(text.strip()) < 50:
        text_plumber = _extract_with_pdfplumber(data)
        if text_plumber and len(text_plumber.strip()) > len(text.strip()):
            text = text_plumber
    return text or ""


def _extract_with_pypdf2(data: bytes) -> str:
    """Extract text using PyPDF2."""
    try:
        from PyPDF2 import PdfReader
        from io import BytesIO
        reader = PdfReader(BytesIO(data))
        parts = []
        for page in reader.pages:
            part = page.extract_text()
            if part:
                parts.append(part)
        return "\n".join(parts) if parts else ""
    except Exception:
        return ""


def _extract_with_pdfplumber(data: bytes) -> str:
    """Extract text using pdfplumber."""
    try:
        import pdfplumber
        from io import BytesIO
        parts = []
        with pdfplumber.open(BytesIO(data)) as pdf:
            for page in pdf.pages:
                part = page.extract_text()
                if part:
                    parts.append(part)
        return "\n".join(parts) if parts else ""
    except Exception:
        return ""
