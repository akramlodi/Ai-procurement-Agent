import io
import logging

import fitz
from docx import Document

logger = logging.getLogger(__name__)


class TextExtractor:
    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext == "pdf":
            return self._extract_pdf(file_bytes)
        if ext in ("docx", "doc"):
            return self._extract_docx(file_bytes)
        raise ValueError(f"Unsupported file type: {ext}")

    def _extract_pdf(self, file_bytes: bytes) -> str:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            pages = [page.get_text() for page in doc]
            doc.close()
            return "\n\n".join(pages)
        except Exception as e:
            logger.error("PyMuPDF extraction failed: %s", e)
            raise

    def _extract_docx(self, file_bytes: bytes) -> str:
        try:
            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except Exception as e:
            logger.error("python-docx extraction failed: %s", e)
            raise
