from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.dependencies import get_current_user
from app.schemas.chat import ChatRequest
from app.services.chat_service import chat_service
from app.services.rag_pipeline import rag_pipeline
from app.services.store import store

router = APIRouter()


@router.get("/{pet_id}")
async def list_messages(pet_id: int, current_user: dict = Depends(get_current_user)):
    return {"items": chat_service.list_messages(current_user["id"], pet_id)}


@router.post("/")
async def chat(payload: ChatRequest, current_user: dict = Depends(get_current_user)):
    pet = store.get_pet(payload.pet_id)
    if not pet or pet["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")

    async def event_stream():
        timestamp = datetime.now(UTC).isoformat()
        store.add_chat_message(
            {
                "user_id": current_user["id"],
                "pet_id": payload.pet_id,
                "role": "user",
                "content": payload.message,
                "sources": [],
                "created_at": timestamp,
            }
        )

        assistant_chunks: list[str] = []
        citations: list[dict] = []

        async for event in chat_service.stream_message(current_user, pet, payload.message):
            if event["type"] == "token":
                assistant_chunks.append(event["content"])
            elif event["type"] == "metadata":
                citations = event["citations"]
            elif event["type"] == "done":
                store.add_chat_message(
                    {
                        "user_id": current_user["id"],
                        "pet_id": payload.pet_id,
                        "role": "assistant",
                        "content": "".join(assistant_chunks).strip(),
                        "sources": citations,
                        "created_at": datetime.now(UTC).isoformat(),
                    }
                )
            yield rag_pipeline.format_sse_event(event)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
