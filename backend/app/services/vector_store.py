from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.core.config import settings
from app.services.embedding_service import embedding_service


class VectorStoreService:
    def __init__(self) -> None:
        self.index_dir = Path(settings.faiss_index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self._vector_store: FAISS | None = None

    def reset_index(self, documents: list[Document]) -> dict:
        if not documents:
            raise ValueError("No documents available for ingestion.")
        self._vector_store = FAISS.from_documents(documents, embedding_service)
        self._vector_store.save_local(str(self.index_dir), index_name="petsense")
        return {"documents_indexed": len(documents), "index_dir": str(self.index_dir)}

    def load(self) -> FAISS:
        if self._vector_store is None:
            self._vector_store = FAISS.load_local(
                str(self.index_dir),
                embedding_service,
                index_name="petsense",
                allow_dangerous_deserialization=True,
            )
        return self._vector_store

    def exists(self) -> bool:
        return (self.index_dir / "petsense.faiss").exists() and (self.index_dir / "petsense.pkl").exists()

    def similarity_search(self, query: str, k: int, fetch_k: int) -> list[tuple[Document, float]]:
        vector_store = self.load()
        return vector_store.similarity_search_with_relevance_scores(query=query, k=k, fetch_k=fetch_k)

    def all_documents(self) -> list[Document]:
        vector_store = self.load()
        docstore = getattr(vector_store, "docstore", None)
        if not docstore or not hasattr(docstore, "_dict"):
            return []
        return list(docstore._dict.values())


vector_store = VectorStoreService()
