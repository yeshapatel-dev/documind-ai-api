from apps.documents.models import DocumentChunk

from apps.documents.services.ai.semantic_search_service import SemanticSearchService


class DocumentRetrievalService:
    """
    Service for retrieving the most relevant chunks across all uploaded documents.
    """

    @staticmethod
    def retrieve(question: str, limit: int = 5):
        """
        Retrieve the most relevant chunks from all documents.
        """

        chunks = DocumentChunk.objects.select_related("document")

        return SemanticSearchService.search(
            chunks=chunks,
            question=question,
            top_k=limit,
        )