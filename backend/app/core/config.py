from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Local RAG API"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5
    llm_provider: str = "ollama"  # ollama | openai
    ollama_model: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434"
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    data_dir: Path = Path("backend/storage")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
