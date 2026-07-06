from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service for generating sentence embeddings.
    """

    _model = SentenceTransformer("all-MiniLM-L6-v2")

    @classmethod
    def generate_embeddings(
        cls,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        return cls._model.encode(
            texts,
            convert_to_numpy=True,
        ).tolist()

    @classmethod
    def generate_embedding(
        cls,
        text: str,
    ) -> list[float]:
        """
        Generate embedding for a single text.
        """

        return cls.generate_embeddings([text])[0]