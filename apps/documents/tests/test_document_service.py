import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

from apps.documents.models import Document
from apps.documents.services.document_service import DocumentService


@pytest.mark.django_db
class TestDocumentService:

    TITLE = "Test PDF"
    EXTRACTED_TEXT = "This is extracted text."
    CHUNKS = [
        "Chunk 1",
        "Chunk 2",
    ]

    @patch("apps.documents.services.document_service.TextChunkService.chunk_text")
    @patch("apps.documents.services.document_service.PDFExtractService.extract_text")
    def test_should_process_document_successfully(self, mock_extract_text, mock_chunk_text):
        """test that the process document method extracts text, splits chunks, saves the document and creates document chunks."""
        
        # Arrange
        mock_extract_text.return_value = self.EXTRACTED_TEXT
        mock_chunk_text.return_value = self.CHUNKS

        document = Document.objects.create(
            title=self.TITLE,
            file=SimpleUploadedFile(
                "test.pdf",
                b"dummy pdf",
                content_type="application/pdf",
            ),
        )

        # Act
        DocumentService.process_document(document)

        document.refresh_from_db()

        # Assert
        assert document.content == self.EXTRACTED_TEXT
        assert document.chunks.count() == len(self.CHUNKS)

        assert document.chunks.first().content == self.CHUNKS[0]
        assert document.chunks.last().content == self.CHUNKS[1]

        mock_extract_text.assert_called_once_with(document.file.path)
        mock_chunk_text.assert_called_once_with(self.EXTRACTED_TEXT)