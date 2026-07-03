from apps.documents.models import Document
from apps.documents.services.pdf_extractor import PDFExtractService

class DocumentService:
    """
    Service for handling document related operations.
    """

    @staticmethod
    def process_document(document: Document) -> Document:
        """
        Process an uploaded document and persist the extracted content.
        """
        document.content = PDFExtractService.extract_text(document.file.path)

        document.save(update_fields=["content", "updated_at"])

        return document
