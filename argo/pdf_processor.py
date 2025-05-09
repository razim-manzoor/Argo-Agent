import pdfplumber
from typing import Generator
from config import config
import re
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
        return text.strip()[:config.MAX_TEXT_LENGTH]

    @staticmethod
    def stream_pages(pdf_path: str) -> Generator[str, None, None]:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    yield PDFProcessor.clean_text(text)
        except Exception as e:
            logger.error(f"PDF processing failed: {str(e)}")
            raise

    @staticmethod
    def safe_extract(pdf_path: str) -> str:
        try:
            return " ".join(PDFProcessor.stream_pages(pdf_path))
        except Exception as e:
            logger.error(f"Failed to process {pdf_path}: {str(e)}")
            return ""