import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier (UUID)",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When this file was uploaded to the system."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text="When this file was last updated"
    )

    class Meta:
        abstract = True