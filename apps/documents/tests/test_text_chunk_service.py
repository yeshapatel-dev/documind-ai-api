import pytest
from apps.documents.services.text_chunk_service import TextChunkService

class TestTextChunkService:

    TEXT = "Lorem ipsum " * 300

    def test_should_split_text_into_multiple_chunks(self):
        """test that the text is split into multiple chunks with specified chunk size and overlap."""
        
        chunks = TextChunkService.chunk_text(self.TEXT)

        assert isinstance(chunks, list)
        assert len(chunks) > 1