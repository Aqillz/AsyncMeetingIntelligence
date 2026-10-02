from app.services.llm.base import BaseLLMProvider
from app.services.llm.providers import OpenAICompatibleProvider, HuggingFaceProvider
from app.core.config import config

def get_llm_provider() -> BaseLLMProvider:
    if config.LLM_PROVIDER == "groq":
        if not config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY must be set for Groq provider.")
        return OpenAICompatibleProvider(
            base_url="https://api.groq.com/openai/v1",
            api_key=config.GROQ_API_KEY,
            model=config.LLM_MODEL
        )
    elif config.LLM_PROVIDER == "huggingface":
        if not config.HF_API_KEY:
            raise ValueError("HF_API_KEY must be set for HuggingFace provider.")
        return HuggingFaceProvider(
            api_key=config.HF_API_KEY,
            model=config.LLM_MODEL
        )
    elif config.LLM_PROVIDER == "ollama":
        return OpenAICompatibleProvider(
            base_url=config.OLLAMA_BASE_URL,
            api_key="ollama", # Required by SDK, ignored by Ollama
            model=config.LLM_MODEL
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")