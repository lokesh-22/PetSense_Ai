from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "PetSense AI API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql://petsense:petsense@localhost:5432/petsense"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 10080
    breed_catalog_path: str = str(PROJECT_ROOT / "data" / "breed_data.json")
    toxic_ingredients_path: str = str(PROJECT_ROOT / "data" / "toxic_ingredients.json")
    redis_url: str = "redis://localhost:6379/0"
    faiss_index_dir: str = str(PROJECT_ROOT / "data" / "faiss_index")
    knowledge_base_dir: str = str(PROJECT_ROOT / "data" / "knowledge_base")
    embedding_provider: str = "huggingface"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_cache_path: str = str(PROJECT_ROOT / "data" / "faiss_index" / "embedding_cache.json")
    llm_provider: str = "openai"
    llm_model_name: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    rag_top_k: int = 4
    rag_fetch_k: int = 8
    chunk_size: int = 900
    chunk_overlap: int = 150

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
