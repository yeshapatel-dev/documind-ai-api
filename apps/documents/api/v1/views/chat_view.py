from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.documents.api.v1.serializers.chat_serializer import ChatSerializer
from apps.documents.models import Document
from apps.documents.services.ai.ai_chat_service import AIChatService
from apps.documents.services.ai.llm.gemini_service import GeminiService


class ChatAPIView(APIView):
    """
    API endpoint for chatting with a document.
    """

    def post(self, request):
        """
        Answer a user's question using the selected document.
        """

        serializer = ChatSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        document = Document.objects.get(
            id=serializer.validated_data["document_id"],
        )

        answer = AIChatService(
            llm_service=GeminiService(),
        ).ask(
            document=document,
            question=serializer.validated_data["question"],
        )

        return Response(
            {"answer": answer}, status=status.HTTP_200_OK
        )