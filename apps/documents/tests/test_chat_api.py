import pytest

from unittest.mock import patch
from rest_framework.test import APIClient

from apps.documents.models import Document


@pytest.mark.django_db
class TestChatAPIView:
    """
    Tests for the document chat API.
    """

    URL = "/api/v1/documents/chat/"

    QUESTION = "How many casual leaves are allowed?"

    ANSWER = "7 casual leaves are allowed."

    def setup_method(self):
        """
        Create test data.
        """

        self.client = APIClient()

        self.document = Document.objects.create(
            title="Leave Policy",
            file="documents/test.pdf",
        )

    @patch("apps.documents.api.v1.views.chat_view.AIChatService.ask")
    def test_should_return_ai_answer(self, mock_ai_chat):
        """
        Test that the API returns the AI generated answer.
        """

        # Arrange
        mock_ai_chat.return_value = self.ANSWER

        # Act
        response = self.client.post(
            self.URL,
            {
                "document_id": str(self.document.id),
                "question": self.QUESTION,
            },
            format="json",
        )

        # Assert
        assert response.status_code == 200

        assert response.json() == {
            "answer": self.ANSWER,
        }

        mock_ai_chat.assert_called_once_with(
            document=self.document,
            question=self.QUESTION,
        )

    def test_should_return_400_for_invalid_document(self):
        """
        Test that the API returns 400 for an invalid document id.
        """

        response = self.client.post(
            self.URL,
            {
                "document_id": "00000000-0000-0000-0000-000000000000",
                "question": self.QUESTION,
            },
            format="json",
        )

        assert response.status_code == 400

        assert "document_id" in response.json()

    def test_should_return_400_when_question_is_missing(self):
        """
        Test that the API returns 400 when the question is missing.
        """

        response = self.client.post(
            self.URL,
            {
                "document_id": str(self.document.id),
            },
            format="json",
        )

        assert response.status_code == 400

        assert "question" in response.json()