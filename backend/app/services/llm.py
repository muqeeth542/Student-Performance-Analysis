from __future__ import annotations

import json
from typing import AsyncGenerator
import httpx
from openai import AsyncOpenAI


class LLMService:
    def __init__(
        self,
        provider: str,
        ollama_base_url: str,
        ollama_model: str,
        openai_model: str,
        openai_api_key: str | None,
    ):
        self.provider = provider.lower()
        self.ollama_base_url = ollama_base_url.rstrip("/")
        self.ollama_model = ollama_model
        self.openai_model = openai_model
        self.openai_client = AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        if self.provider == "openai":
            if self.openai_client is None:
                raise RuntimeError("OPENAI_API_KEY is not configured")
            stream = await self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                stream=True,
            )
            async for event in stream:
                token = event.choices[0].delta.content or ""
                if token:
                    yield token
            return

        payload = {
            "model": self.ollama_model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", f"{self.ollama_base_url}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    content = data.get("message", {}).get("content", "")
                    if content:
                        yield content

    async def generate(self, prompt: str) -> str:
        parts: list[str] = []
        async for token in self.generate_stream(prompt):
            parts.append(token)
        return "".join(parts)
