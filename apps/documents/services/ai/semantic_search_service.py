from sklearn.metrics.pairwise import cosine_similarity

from apps.documents.models import DocumentChunk
from apps.documents.services.ai.embedding_service import EmbeddingService


class SemanticSearchService:
    """
    Service for semantic document retrieval.
    """

    @staticmethod
    def search(chunks, question: str, top_k: int = 5):
        """
        Return the most relevant chunks with similarity scores.
        """

        question_embedding = EmbeddingService.generate_embedding(
            question
        )

        scored_chunks = []

        for chunk in chunks:

            score = cosine_similarity(
                [question_embedding],
                [chunk.embedding],
            )[0][0]

            scored_chunks.append((score, chunk))

        scored_chunks.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return scored_chunks[:top_k]