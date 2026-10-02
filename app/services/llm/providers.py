import openai
from huggingface_hub import AsyncInferenceClient
from app.services.llm.base import BaseLLMProvider
from app.core.config import config

class OpenAICompatibleProvider(BaseLLMProvider):
    """Handles Groq and Ollama via OpenAI SDK compatibility."""
    def __init__(self, base_url: str, api_key: str, model: str):
        self.model = model
        self.client = openai.AsyncOpenAI(
            base_url=base_url,
            api_key=api_key if api_key else "dummy-key-for-local",
            timeout=config.LLM_TIMEOUT_SECONDS
        )

    async def generate_completion(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2 # Low temperature for factual meeting minutes
        )
        return response.choices[0].message.content

class HuggingFaceProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str):
        self.model = model
        self.client = AsyncInferenceClient(token=api_key)

    async def generate_completion(self, system_prompt: str, user_prompt: str) -> str:
        # HF expects a concatenated prompt for causal LMs or specific chat templates
        formatted_prompt = f"System: {system_prompt}\nUser: {user_prompt}\nAssistant:"
        response = await self.client.text_generation(
            formatted_prompt,
            model=self.model,
            max_new_tokens=1024,
            temperature=0.2
        )
        return response