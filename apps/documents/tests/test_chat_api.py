import pytest

from unittest.mock import patch
from rest_framework.test import APIClient

from apps.documents.models import Document, Chat


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

    @patch("apps.documents.api.v1.views.chat_view.ChatService.ask")
    def test_should_return_ai_answer(self, mock_chat_service):
        """
        Test that the API returns the AI generated answer.
        """

        # Arrange
        mock_chat_service.return_value = self.ANSWER

        # Act
        response = self.client.post(
            self.URL,
            {
                "question": self.QUESTION,
            },
            format="json",
        )

        # Assert
        assert response.status_code == 200

        assert response.json() == {
            "answer": self.ANSWER,
        }

        mock_chat_service.assert_called_once_with(
            question=self.QUESTION,
        )

    def test_should_return_400_when_question_is_missing(self):
        """
        Test that the API returns 400 when the question is missing.
        """

        response = self.client.post(
            self.URL,
            {},
            format="json",
        )

        assert response.status_code == 400

        assert "question" in response.json()

    def test_should_return_chat_history(self):
        """
        Test that the API returns chat history.
        """

        Chat.objects.create(
            question="Question 1",
            answer="Answer 1",
        )

        Chat.objects.create(
            question="Question 2",
            answer="Answer 2",
        )

        response = self.client.get(self.URL)

        assert response.status_code == 200

        assert len(response.json()) == 2
        assert response.json()[0]["question"] == "Question 2"
        assert response.json()[1]["question"] == "Question 1"