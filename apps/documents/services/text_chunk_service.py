from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunkService:
    """
    service for splitting text into overlapping chunks for downstream AI processing.
    """

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[str]:
        """
        Split text into overlapping chunks.
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

        return text_splitter.split_text(text)