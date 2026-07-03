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