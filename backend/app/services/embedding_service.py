import json
from hashlib import sha256
from pathlib import Path

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


class CachedEmbeddingService(Embeddings):
    def __init__(self) -> None:
        self.cache_path = Path(settings.embedding_cache_path)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.cache_path.exists():
            self.cache_path.write_text("{}", encoding="utf-8")
        self.backend = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        cache = self._read_cache()
        uncached = []
        ordered_keys = []

        for text in texts:
            key = self._cache_key(text)
            ordered_keys.append(key)
            if key not in cache:
                uncached.append(text)

        if uncached:
            embeddings = self.backend.embed_documents(uncached)
            for text, embedding in zip(uncached, embeddings, strict=False):
                cache[self._cache_key(text)] = embedding
            self._write_cache(cache)

        return [cache[key] for key in ordered_keys]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    @staticmethod
    def _cache_key(text: str) -> str:
        return sha256(text.encode("utf-8")).hexdigest()

    def _read_cache(self) -> dict[str, list[float]]:
        return json.loads(self.cache_path.read_text(encoding="utf-8"))

    def _write_cache(self, cache: dict[str, list[float]]) -> None:
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")


embedding_service = CachedEmbeddingService()
