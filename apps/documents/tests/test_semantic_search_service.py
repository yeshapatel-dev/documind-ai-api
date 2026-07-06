import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.documents.models import Document, DocumentChunk
from apps.documents.services.ai.semantic_search_service import (
    SemanticSearchService,
)


@pytest.mark.django_db
class TestSemanticSearchService:
    """
    Tests for SemanticSearchService.
    """

    QUESTION = "What is Django?"

    def setup_method(self):
        """
        Create reusable test data.
        """

        self.document = Document.objects.create(
            title="Test Document",
            file=SimpleUploadedFile(
                "test.pdf",
                b"dummy pdf",
                content_type="application/pdf",
            ),
        )

        self.chunk1 = DocumentChunk.objects.create(
            document=self.document,
            content="Python is a programming language.",
            embedding=[0.1] * 384,
            chunk_index=0,
        )

        self.chunk2 = DocumentChunk.objects.create(
            document=self.document,
            content="Django is a Python framework.",
            embedding=[0.2] * 384,
            chunk_index=1,
        )

    def test_should_return_ranked_chunks(self):
        """
        Test that semantic search returns ranked chunks.
        """

        # Act
        results = SemanticSearchService.search(
            chunks=self.document.chunks.all(),
            question=self.QUESTION,
        )

        # Assert
        assert len(results) == 2

        score, chunk = results[0]

        assert isinstance(score, float)
        assert isinstance(chunk, DocumentChunk)

    def test_should_return_empty_list_when_chunks_are_empty(self):
        """
        Test that semantic search returns an empty list when no chunks exist.
        """

        # Act
        results = SemanticSearchService.search(
            chunks=[],
            question=self.QUESTION,
        )

        # Assert
        assert results == []