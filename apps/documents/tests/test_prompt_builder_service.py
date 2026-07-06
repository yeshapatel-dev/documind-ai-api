import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.documents.models import Document, DocumentChunk
from apps.documents.services.ai.prompt_builder_service import (
    PromptBuilderService,
)


@pytest.mark.django_db
class TestPromptBuilderService:
    """
    Tests for PromptBuilderService.
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

        self.chunk = DocumentChunk.objects.create(
            document=self.document,
            content="Django is a Python web framework.",
            chunk_index=0,
        )

    def test_should_build_prompt_with_context_and_question(self):
        """
        Test that prompt contains both the question and retrieved context.
        """

        # Act
        prompt = PromptBuilderService.build_prompt(
            question=self.QUESTION,
            chunks=[self.chunk],
        )

        # Assert
        assert self.QUESTION in prompt
        assert self.chunk.content in prompt
        assert "Context:" in prompt
        assert "Answer:" in prompt

    def test_should_build_prompt_when_context_is_empty(self):
        """
        Test that prompt is still generated when no chunks are provided.
        """

        # Act
        prompt = PromptBuilderService.build_prompt(
            question=self.QUESTION,
            chunks=[],
        )

        # Assert
        assert self.QUESTION in prompt
        assert "Context:" in prompt
        assert "Answer:" in prompt