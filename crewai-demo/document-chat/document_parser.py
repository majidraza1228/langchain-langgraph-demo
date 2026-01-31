"""Document text extraction utilities for PDF, DOCX, and TXT files."""

import io

MAX_CHARS = 100_000  # Safety limit for LLM context window


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyPDF2."""
    import PyPDF2

    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
    return "\n\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes using python-docx."""
    import docx

    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n\n".join(
        paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()
    )


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Extract text from plain text bytes."""
    return file_bytes.decode("utf-8", errors="replace")


def extract_text(filename: str, file_bytes: bytes) -> str:
    """
    Extract text from a document file.

    Args:
        filename: Name of the file (used to determine type by extension).
        file_bytes: Raw bytes of the file.

    Returns:
        Extracted text, truncated to MAX_CHARS if necessary.

    Raises:
        ValueError: If the file type is not supported.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext == "docx":
        text = extract_text_from_docx(file_bytes)
    elif ext == "txt":
        text = extract_text_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")

    if not text.strip():
        raise ValueError(
            "No text could be extracted from the document. "
            "The file may be empty or contain only images/scanned content."
        )

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[... Document truncated due to size ...]"

    return text
