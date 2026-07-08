
from apps.documents.services.ai.llm.base_llm_service import BaseLLMService
from apps.documents.services.ai.llm.gemini_service import GeminiService
from apps.documents.services.ai.prompt_builder_service import PromptBuilderService
from apps.documents.services.ai.document_retrieval_service import DocumentRetrievalService


class AIChatService:
    """
    Service responsible for orchestrating the complete
    Retrieval-Augmented Generation (RAG) pipeline.
    """

    def __init__(self, llm_service: BaseLLMService | None = None):
        """
        Initialize the AI chat service.
        """

        self.llm_service = llm_service or GeminiService()

    def ask(self, question: str ) -> str:
        """
        Answer a user's question using the most relevant content across all uploaded documents.
        """

        # Retrieve the most relevant chunks.
        ranked_chunks = DocumentRetrievalService.retrieve(question=question)

        # Remove similarity scores.
        chunks = [chunk for _, chunk in ranked_chunks]

        # Build the final prompt.
        prompt = PromptBuilderService.build_prompt(
            question=question,
            chunks=chunks,
        )

        # Ask the LLM.
        return self.llm_service.generate_response(
            prompt=prompt,
        )