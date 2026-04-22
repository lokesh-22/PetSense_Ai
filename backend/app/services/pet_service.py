from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.services.breed_service import breed_service
from app.services.store import store


class PetService:
    def list_pets(self, user_id: int) -> list[dict]:
        return store.list_pets(user_id)

    def create_pet(self, user: dict, payload: dict) -> dict:
        breed_profile = breed_service.fetch_breed_profile(payload["breed"], payload["species"])
        pet = store.create_pet(
            {
                **payload,
                "owner_id": user["id"],
                "breed_profile": breed_profile,
                "created_at": datetime.now(UTC).isoformat(),
            }
        )
        if not user.get("active_pet_id"):
            store.update_user_active_pet(user["id"], pet["id"])
        store.add_weight_log(pet["id"], payload["weight_kg"], datetime.now(UTC).isoformat())
        return store.get_pet(pet["id"])

    def update_pet(self, user_id: int, pet_id: int, payload: dict) -> dict:
        pet = store.get_pet(pet_id)
        if not pet or pet["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")

        breed_profile = breed_service.fetch_breed_profile(payload["breed"], payload["species"])
        updated = store.update_pet(
            pet_id,
            user_id,
            {
                **payload,
                "breed_profile": breed_profile,
            },
        )
        store.add_weight_log(pet_id, payload["weight_kg"], datetime.now(UTC).isoformat())
        return updated

    def switch_active_pet(self, user_id: int, pet_id: int) -> dict:
        pet = store.get_pet(pet_id)
        if not pet or pet["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")
        return store.update_user_active_pet(user_id, pet_id)

    def delete_pet(self, user: dict, pet_id: int) -> None:
        pet = store.get_pet(pet_id)
        if not pet or pet["owner_id"] != user["id"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")
        store.delete_pet(pet_id, user["id"])
        if user.get("active_pet_id") == pet_id:
            remaining = store.list_pets(user["id"])
            store.update_user_active_pet(user["id"], remaining[0]["id"] if remaining else None)


pet_service = PetService()
