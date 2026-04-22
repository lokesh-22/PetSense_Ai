from fastapi import APIRouter

from app.schemas.ingestion import IngestResponse
from app.services.rag_pipeline import rag_pipeline

router = APIRouter()


@router.post("/", response_model=IngestResponse)
async def ingest_documents():
    return rag_pipeline.ingest_documents()
