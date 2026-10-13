import json
from typing import Any

from litellm import completion


class LLMClient:
    """Provider-agnostic client for calling an LLM through LiteLLM."""

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def complete(self, prompt: str) -> str:
        """Send a prompt to the configured LLM and return text."""

        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content

    def complete_json(self, prompt: str) -> dict[str, Any]:
        """Send a prompt and return a parsed JSON object."""

        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        return json.loads(content)