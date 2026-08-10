from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.documents.api.v1.serializers.chat_serializer import ChatSerializer, ChatHistorySerializer
from apps.documents.services.chat_service import ChatService


class ChatAPIView(APIView):
    """
    API endpoint for chatting with uploaded documents..
    """

    def post(self, request):
        """
        Answer a user's question using the selected document.
        """

        serializer = ChatSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)


        answer = ChatService().ask(
            question=serializer.validated_data["question"],
        )

        return Response(
            {"answer": answer}, status=status.HTTP_200_OK
        )
    
    def get(self, request):
        """
        Return chat history.
        """

        chats = ChatService().get_history()

        serializer = ChatHistorySerializer(
            chats,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )