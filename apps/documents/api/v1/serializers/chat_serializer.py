from rest_framework import serializers
from apps.documents.models import Chat

class ChatSerializer(serializers.Serializer):
    """
    Serializer for document chat requests.
    """

    question = serializers.CharField(max_length=1000)

class ChatHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for chat history.
    """

    class Meta:
        model = Chat
        fields = [
            "id",
            "question",
            "answer",
            "uploaded_at",
        ]