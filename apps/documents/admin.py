from django.contrib import admin

from .models import Document
from apps.documents.services.document_service import DocumentService


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "uploaded_at",
        "updated_at",
    )

    search_fields = (
        "title",
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            DocumentService.process_document(obj)