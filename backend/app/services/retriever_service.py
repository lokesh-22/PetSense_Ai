from collections import Counter

from langchain_core.documents import Document

from app.core.config import settings
from app.services.vector_store import vector_store
from app.utils.text import tokenize


class RetrieverService:
    def retrieve(self, query: str, breed: str, species: str, top_k: int | None = None) -> list[dict]:
        semantic_hits = vector_store.similarity_search(
            query=query,
            k=top_k or settings.rag_top_k,
            fetch_k=settings.rag_fetch_k,
        )
        filtered = self._filter_semantic_hits(semantic_hits, breed, species)
        if len(filtered) >= (top_k or settings.rag_top_k):
            return filtered[: top_k or settings.rag_top_k]

        lexical_hits = self._keyword_fallback(query, breed, species)
        merged: dict[str, dict] = {item["chunk_id"]: item for item in filtered}
        for item in lexical_hits:
            merged.setdefault(item["chunk_id"], item)
        results = list(merged.values())
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[: top_k or settings.rag_top_k]

    def _filter_semantic_hits(
        self,
        semantic_hits: list[tuple[Document, float]],
        breed: str,
        species: str,
    ) -> list[dict]:
        breed_slug = breed.lower().replace(" ", "-")
        filtered = []
        for document, score in semantic_hits:
            doc_breed = document.metadata.get("breed", "universal")
            doc_species = document.metadata.get("species", "all")
            if doc_breed not in {breed_slug, "universal"}:
                continue
            if doc_species not in {species.lower(), "all"}:
                continue
            filtered.append(
                {
                    "chunk_id": document.metadata["chunk_id"],
                    "title": document.metadata.get("title", "Untitled"),
                    "source": document.metadata.get("source", "Unknown"),
                    "breed": doc_breed,
                    "species": doc_species,
                    "content": document.page_content,
                    "score": round(float(score), 4),
                    "metadata": document.metadata,
                }
            )
        return filtered

    def _keyword_fallback(self, query: str, breed: str, species: str) -> list[dict]:
        breed_slug = breed.lower().replace(" ", "-")
        query_counts = Counter(tokenize(query))
        results = []
        for document in vector_store.all_documents():
            doc_breed = document.metadata.get("breed", "universal")
            doc_species = document.metadata.get("species", "all")
            if doc_breed not in {breed_slug, "universal"}:
                continue
            if doc_species not in {species.lower(), "all"}:
                continue
            document_counts = Counter(tokenize(document.page_content))
            overlap = sum(min(query_counts[token], document_counts[token]) for token in query_counts)
            if overlap == 0:
                continue
            results.append(
                {
                    "chunk_id": document.metadata["chunk_id"],
                    "title": document.metadata.get("title", "Untitled"),
                    "source": document.metadata.get("source", "Unknown"),
                    "breed": doc_breed,
                    "species": doc_species,
                    "content": document.page_content,
                    "score": round(overlap / max(len(query_counts), 1), 4),
                    "metadata": document.metadata,
                }
            )
        results.sort(key=lambda item: item["score"], reverse=True)
        return results


retriever_service = RetrieverService()
