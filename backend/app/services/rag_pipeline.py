import json
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.ingestion_service import ingestion_service
from app.services.retriever_service import retriever_service
from app.services.vector_store import vector_store

SYSTEM_PROMPT = (
    "You are a veterinary assistant AI. Answer only using the provided context. "
    "Do not invent facts. If the context is insufficient, say so clearly and recommend a veterinarian when appropriate. "
    "Always include citation markers like [1], [2] that match the provided sources."
)


class RagPipeline:
    def __init__(self) -> None:
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    "Breed: {breed}\n"
                    "Pet Context:\n{pet_context}\n\n"
                    "Conversation Summary:\n{chat_history}\n\n"
                    "Question:\n{question}\n\n"
                    "Context:\n{context}\n\n"
                    "Output requirements:\n"
                    "- Clear answer\n"
                    "- Use bullet points when helpful\n"
                    "- Cite sources inline like [1], [2]\n"
                    "- If context is insufficient, say what is missing",
                ),
            ]
        )
        self.output_parser = StrOutputParser()

    def ensure_index_ready(self) -> dict:
        ingestion_service.ensure_seed_documents()
        if vector_store.exists():
            return {"status": "ready", "source": "existing_index"}
        return self.ingest_documents()

    def ingest_documents(self) -> dict[str, Any]:
        documents = ingestion_service.ingestable_documents()
        result = vector_store.reset_index(documents)
        return {
            "status": "indexed",
            "documents_indexed": result["documents_indexed"],
            "index_dir": result["index_dir"],
        }

    def retrieve(self, question: str, breed: str, species: str, top_k: int | None = None) -> list[dict]:
        return retriever_service.retrieve(question, breed, species, top_k=top_k)

    async def stream_answer(
        self,
        *,
        question: str,
        breed: str,
        species: str,
        pet_context: str,
        chat_history: str,
    ):
        documents = self.retrieve(question, breed, species)
        if not documents:
            yield {
                "type": "metadata",
                "citations": [],
            }
            yield {
                "type": "token",
                "content": (
                    "I do not have enough indexed knowledge for this question yet. "
                    "Please ingest documents first or consult a veterinarian for case-specific advice."
                ),
            }
            yield {"type": "done", "citations": []}
            return

        citations = [
            {
                "index": index,
                "chunk_id": document["chunk_id"],
                "title": document["title"],
                "source": document["source"],
            }
            for index, document in enumerate(documents, start=1)
        ]
        context = "\n\n".join(
            f"[{index}] {document['title']} ({document['source']})\n{document['content']}"
            for index, document in enumerate(documents, start=1)
        )
        yield {"type": "metadata", "citations": citations}

        chain = self.prompt | self._build_llm() | self.output_parser
        async for chunk in chain.astream(
            {
                "breed": breed,
                "pet_context": pet_context,
                "chat_history": chat_history or "No previous messages.",
                "question": question,
                "context": context,
            }
        ):
            if chunk:
                yield {"type": "token", "content": chunk}

        yield {"type": "done", "citations": citations}

    @staticmethod
    def format_sse_event(payload: dict[str, Any]) -> bytes:
        return f"data: {json.dumps(payload)}\n\n".encode("utf-8")

    @staticmethod
    def _build_llm() -> ChatOpenAI:
        provider = settings.llm_provider.lower()
        if provider == "groq":
            if not settings.groq_api_key:
                raise RuntimeError("GROQ_API_KEY is not configured.")
            return ChatOpenAI(
                model=settings.llm_model_name,
                temperature=settings.llm_temperature,
                api_key=settings.groq_api_key,
                base_url=settings.groq_base_url,
                streaming=True,
            )

        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        return ChatOpenAI(
            model=settings.llm_model_name,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            streaming=True,
        )


rag_pipeline = RagPipeline()
