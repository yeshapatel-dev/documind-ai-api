from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service for generating text embeddings using Sentence Transformers.
    """

    # Using the "all-MiniLM-L6-v2" model for generating embeddings.
    # load the model once and reuse it for generating embeddings.
    MODEL = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    @staticmethod
    def generate_embeddings(texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts.
        """

        embeddings = EmbeddingService.MODEL.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings.tolist()