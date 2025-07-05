

from pathlib import Path
from typing import List


class DocumentParser:
    """
    Handle all the types of document parsing
    """

    @staticmethod
    def parse_document(file_path: Path) -> List[str]:
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            return DocumentParser._parse_pdf(file_path)
        elif ext == ".docx":
            return DocumentParser._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @staticmethod
    def _parse_pdf(file_path: Path) -> List[str]:
        # TODO: Implement actual PDF parsing here
        print(f"Parsing PDF: {file_path}")
        return []

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
