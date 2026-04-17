from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def chat():
    return {"message": "Chat endpoint placeholder for RAG/LLM integration."}
