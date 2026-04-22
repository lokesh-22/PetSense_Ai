from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import api_router
from app.services.rag_pipeline import rag_pipeline
from app.services.store import store
from app.services.vector_store import vector_store


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/healthz")
    async def healthcheck():
        return {"status": "ok"}

    @application.get("/health")
    async def system_health():
        return {
            "status": "ok",
            "database": "configured",
            "redis": "configured",
            "faiss_index_ready": vector_store.exists(),
            "llm_provider": settings.llm_provider,
            "embedding_model": settings.embedding_model_name,
        }

    @application.on_event("startup")
    async def startup_event():
        store.ensure_initialized()
        rag_pipeline.ensure_index_ready()

    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = create_application()
