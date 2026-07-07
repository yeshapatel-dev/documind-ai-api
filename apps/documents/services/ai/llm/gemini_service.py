from google import genai
from google.genai.types import GenerateContentConfig

from django.conf import settings

from apps.documents.services.ai.llm.base_llm_service import BaseLLMService


class GeminiService(BaseLLMService):
    """
    Gemini implementation of the base LLM service.
    """

    MODEL = "gemini-2.5-flash"

    def __init__(self):
        """
        Initialize the Gemini client.
        """

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_response( self, prompt: str) -> str:
        """
        Generate a response using Gemini.
        """

        response = self.client.models.generate_content(
            model=self.MODEL,
            contents=prompt,
            config=GenerateContentConfig(temperature=0.2),
        )

        return response.text.strip()