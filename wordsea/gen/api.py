import logging
from typing import Any

from openai import OpenAI
from pydantic import BaseModel

from wordsea.config import settings


class ImagePrompt(BaseModel):
    """Structured output model for image prompt generation."""

    explanation: str
    prompt: str


class OpenAIAPI:
    """OpenAI API client with structured outputs for image prompt generation."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str = "mistrall-small-3.2",
    ) -> None:
        """Initialize OpenAI API client.

        Args:
            base_url: Override the default OpenAI API base URL
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use for completions
        """
        self.client = OpenAI(
            base_url=base_url or settings.openai_api_url,
            api_key=api_key or settings.api_key.get_secret_value(),
        )
        self.model = model

    def health(self) -> bool:
        """Check if the API is accessible."""
        try:
            # Simple test to verify API connectivity
            self.client.models.list()
            return True
        except Exception as e:
            logging.error(f"API health check failed: {e}")
            return False

    def generate(self, word: str, prompt: str) -> dict[str, Any] | None:
        """Generate structured image prompt using OpenAI API.

        Args:
            word: The word to generate an image prompt for
            prompt: The full prompt containing word definition and context

        Returns:
            Dictionary with generated response or None if generation failed
        """
        try:
            completion = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                response_format=ImagePrompt,
                temperature=0.15,
                max_tokens=1024,
            )

            if completion.choices[0]:
                result = completion.choices[0].message.parsed.model_dump()
                result["word"] = word
                return result
            else:
                logging.error(
                    f"Failed to parse response for {word}: {completion.choices[0].message.content}"
                )
                return None

        except Exception as e:
            logging.error(f"Error generating prompt for {word}: {e}")
            return None
