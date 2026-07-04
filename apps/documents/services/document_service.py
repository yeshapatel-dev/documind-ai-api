from apps.documents.models import Document, DocumentChunk
from apps.documents.services.pdf_extractor import PDFExtractService
from apps.documents.services.text_chunk_service import TextChunkService

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

        chunks = TextChunkService.chunk_text(document.content)

        document.save(update_fields=["content", "updated_at"])

        DocumentChunk.objects.bulk_create(
            [
                DocumentChunk(
                    document=document,
                    content=chunk,
                    chunk_index=index,
                )
                for index, chunk in enumerate(chunks)
            ]
        )

        return document
