from apps.documents.models import Document, DocumentChunk
from apps.documents.services.ai.embedding_service import EmbeddingService
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

        # Extract text from PDF
        document.content = PDFExtractService.extract_text(document.file.path)

        # Split text into chunks
        chunks = TextChunkService.chunk_text(document.content)

        # Save extracted content
        document.save(update_fields=["content", "updated_at"])

        # Save chunks
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

        # Fetch saved chunks
        saved_chunks = list(document.chunks.order_by("chunk_index"))

        # Generate embeddings for all chunks
        embeddings = EmbeddingService.generate_embeddings(
            [chunk.content for chunk in saved_chunks]
        )

        # Attach embeddings to chunk objects
        for chunk, embedding in zip(saved_chunks, embeddings):
            chunk.embedding = embedding

        # Save all embeddings in a single query
        DocumentChunk.objects.bulk_update(
            saved_chunks,
            ["embedding"],
        )

        return document
