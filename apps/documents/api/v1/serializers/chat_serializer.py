from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    """
    Serializer for document chat requests.
    """

    question = serializers.CharField(max_length=1000)
