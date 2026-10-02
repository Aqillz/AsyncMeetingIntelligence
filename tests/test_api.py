import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.router import get_provider
from app.services.llm.base import BaseLLMProvider
import openai

class MockSuccessProvider(BaseLLMProvider):
    async def generate_completion(self, system_prompt: str, user_prompt: str) -> str:
        return "- Decision: Launch next week\n- Action Item: John to prepare slides."

class MockRateLimitProvider(BaseLLMProvider):
    async def generate_completion(self, system_prompt: str, user_prompt: str) -> str:
        # Simulating an upstream OpenAI rate limit exception
        response = httpx.Response(429, request=httpx.Request("POST", "url"))
        raise openai.RateLimitError("Rate limited", response=response, body={})

client = TestClient(app)

def test_generate_minutes_success():
    # Override the dependency to use the success mock
    app.dependency_overrides[get_provider] = MockSuccessProvider

    payload = {
        "transcript": "Let's decide on the launch date. Okay, we'll launch next week. John, please prepare the slides.",
        "meeting_context": "Q3 Planning"
    }

    response = client.post("/api/v1/minutes/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "John to prepare slides" in data["raw_llm_output"]
    
    # Clean up override
    app.dependency_overrides.clear()

def test_generate_minutes_rate_limit_handling():
    # Override the dependency to simulate a rate limit
    app.dependency_overrides[get_provider] = MockRateLimitProvider

    payload = {
        "transcript": "This is a long enough transcript to pass the min_length validation rule.",
        "meeting_context": "Weekly Sync"
    }

    response = client.post("/api/v1/minutes/generate", json=payload)
    
    assert response.status_code == 429
    assert "rate limit exceeded" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()