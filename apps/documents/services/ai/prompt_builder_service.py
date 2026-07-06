from apps.documents.models import DocumentChunk


class PromptBuilderService:
    """
    Service for building prompts for the LLM.
    """

    @staticmethod
    def build_prompt(question: str, chunks: list[DocumentChunk]) -> str:
        """
        Build a prompt using the user question and retrieved document chunks.
        """

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        prompt = f"""
                You are a helpful AI assistant.

                Answer the user's question ONLY using the context below.

                If the answer cannot be found in the context, reply:
                "I couldn't find that information in the provided documents."

                Context:
                {context}

                Question:
                {question}

                Answer:
                """

        return prompt.strip()