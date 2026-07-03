import pytest
from pathlib import Path

from apps.documents.services.pdf_extractor import PDFExtractService


class TestPDFExtractService:
    """
    Test for the Extracting text from PDF files using fitz service.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """setup common test data."""

        self.sample_pdf_path = (
            Path(__file__).parent
            / "resources"
            / "Leave-Policy.pdf"
        )

    def test_extract_text_returns_pdf_content(self):
        """test that the extacting content from PDF file retuns a non-empty string."""

        # Arrange
        pdf_path = self.sample_pdf_path

        # Act
        extracted_text = PDFExtractService.extract_text(pdf_path)

        # Assert
        assert isinstance(extracted_text, str)
        assert extracted_text.strip() # != ""