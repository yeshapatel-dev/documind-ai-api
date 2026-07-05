from django.db import models
from common.models.base import BaseModel

class Document(BaseModel):

    title = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to="documents/"
    )

    content = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class DocumentChunk(BaseModel):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
    )

    content = models.TextField()

    chunk_index = models.PositiveIntegerField()

    embedding = models.JSONField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"
