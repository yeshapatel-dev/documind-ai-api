from apps.documents.models import Chat
from apps.documents.services.ai.ai_chat_service import AIChatService


class ChatService:
    """
    Service responsible for handling chat operations.
    """

    def __init__(self):
        """
        Initialize the chat service.
        """

        self.ai_chat_service = AIChatService()

    def ask(self, question: str) -> str:
        """
        Generate an AI response and store the conversation.
        """

        # Generate AI answer.
        answer = self.ai_chat_service.ask(
            question=question,
        )

        # Save chat history.
        Chat.objects.create(
            question=question,
            answer=answer,
        )

        return answer
    
    def get_history(self):
        """
        Return chat history.
        """

        return Chat.objects.all()