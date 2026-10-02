from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_completion(self, system_prompt: str, user_prompt: str) -> str:
        """Generates text from the LLM based on prompts."""
        pass