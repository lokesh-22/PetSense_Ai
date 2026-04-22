from fastapi import HTTPException, status

from app.services.rag_pipeline import rag_pipeline
from app.services.store import store


class ChatService:
    def list_messages(self, user_id: int, pet_id: int) -> list[dict]:
        pet = store.get_pet(pet_id)
        if not pet or pet["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")
        return store.list_chat_messages(pet_id)

    async def stream_message(self, user: dict, pet: dict, message: str):
        if pet["owner_id"] != user["id"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")

        recent_history = store.list_chat_messages(pet["id"])[-6:]
        history_text = "\n".join(
            f"{item['role'].upper()}: {item['content']}" for item in recent_history
        )
        pet_context = (
            f"Name: {pet['name']}\n"
            f"Species: {pet['species']}\n"
            f"Breed: {pet['breed']}\n"
            f"Age: {pet['age_years']} years\n"
            f"Weight: {pet['weight_kg']} kg\n"
            f"Known breed risks: {', '.join(pet['breed_profile'].get('risk_tags', []))}"
        )

        async for event in rag_pipeline.stream_answer(
            question=message,
            breed=pet["breed"],
            species=pet["species"],
            pet_context=pet_context,
            chat_history=history_text,
        ):
            yield event


chat_service = ChatService()
