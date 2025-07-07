

from pathlib import Path
from typing import List

import pdfplumber


class DocumentParser:
    """
    Handle all the types of document parsing
    """

    @staticmethod
    def parse_document(file_path: Path) -> List[str]:
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            return DocumentParser._parse_pdf(file_path)
        elif ext == ".docx":
            return DocumentParser._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @staticmethod
    def _parse_pdf(file_path: Path) -> List[str]:
        """
        Parse a PDF file and return a list of text chunks (by page).
        Each item in the list represents the text content of one page.
        """
        print(f"Parsing PDF: {file_path}")
        paragraphs = []
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        cleaned_text = text.strip()
                        if cleaned_text:
                            paragraphs.append(cleaned_text)
                    else:
                        print(f"[WARN] Page {i+1} has no extractable text.")
        except Exception as e:
            print(f"[ERROR] Failed to parse PDF: {e}")
            raise

        return paragraphs

    @staticmethod
    def _parse_docx(file_path: Path) -> List[str]:
        # TODO: Implement actual DOCX parsing here
        print(f"Parsing DOCX: {file_path}")
        return []

    @staticmethod
    def _parse_txt(file_path: Path) -> List[str]:
        # TODO: Implement actual TXT parsing here
        print(f"Parsing txt: {file_path}")
        return []

    @staticmethod
    def _parse_excel(file_path: Path) -> List[str]:
        # TODO: Implement actual TXT parsing here
        print(f"Parsing excel: {file_path}")
        return []
