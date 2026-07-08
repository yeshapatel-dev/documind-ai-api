import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.documents.models import Document, DocumentChunk
from apps.documents.services.ai.ai_chat_service import AIChatService


class FakeLLMService:
    """
    Fake LLM service used for testing.
    """

    RESPONSE = "This is the AI response."

    def generate_response(self, prompt: str) -> str:
        """
        Return a fake response.
        """

        return self.RESPONSE


@pytest.mark.django_db
class TestAIChatService:
    """
    Tests for AIChatService.
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

        DocumentChunk.objects.create(
            document=self.document,
            content="Django is a Python web framework.",
            embedding=[0.2] * 384,
            chunk_index=0,
        )

        DocumentChunk.objects.create(
            document=self.document,
            content="Python is a programming language.",
            embedding=[0.1] * 384,
            chunk_index=1,
        )

        self.ai_chat_service = AIChatService(
            llm_service=FakeLLMService(),
        )

    def test_should_return_ai_response(self):
        """
        Test that AIChatService returns the LLM response.
        """

        # Act
        response = self.ai_chat_service.ask(
            question=self.QUESTION,
        )

        # Assert
        assert response == FakeLLMService.RESPONSE