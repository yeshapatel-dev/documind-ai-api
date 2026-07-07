from rest_framework import serializers

from apps.documents.models import Document


class ChatSerializer(serializers.Serializer):
    """
    Serializer for document chat requests.
    """

    document_id = serializers.UUIDField()

    question = serializers.CharField()

    def validate_document_id(self, value):
        """
        Validate that the document exists.
        """

        if not Document.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Document does not exist."
            )

        return value