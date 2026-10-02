import os

class Config:
    # Provider selection: 'groq', 'ollama', or 'huggingface'
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    
    # Base URLs and Model names
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
    
    # Timeout configurations
    LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "60"))
    
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

config = Config()