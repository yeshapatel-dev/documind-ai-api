from abc import ABC, abstractmethod


class BaseLLMService(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the language model.
        """
        pass