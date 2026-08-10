import pytest

from unittest.mock import patch

from apps.documents.models import Chat
from apps.documents.services.chat_service import ChatService


@pytest.mark.django_db
class TestChatService:
    """
    Tests for ChatService.
    """

    QUESTION = "How many casual leaves are allowed?"

    ANSWER = "7 casual leaves are allowed."

    @patch("apps.documents.services.chat_service.AIChatService.ask")
    def test_should_generate_answer_and_save_chat(self, mock_ai_chat):
        """
        Test that the service generates an AI answer and stores the chat.
        """

        # Arrange
        mock_ai_chat.return_value = self.ANSWER

        service = ChatService()

        # Act
        answer = service.ask(question=self.QUESTION)

        chat = Chat.objects.get()

        # Assert
        assert answer == self.ANSWER

        assert chat.question == self.QUESTION
        assert chat.answer == self.ANSWER

        mock_ai_chat.assert_called_once_with(question=self.QUESTION)

    def test_should_return_chat_history(self):
        """
        Test that chat history is returned in descending order.
        """

        Chat.objects.create(
            question="Question 1",
            answer="Answer 1",
        )

        Chat.objects.create(
            question="Question 2",
            answer="Answer 2",
        )

        service = ChatService()

        history = service.get_history()

        assert len(history) == 2
        assert history[0].question == "Question 2"
        assert history[1].question == "Question 1"