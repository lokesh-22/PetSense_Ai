from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.pet import ActivePetSwitch, PetCreate, PetRead, PetUpdate
from app.services.pet_service import pet_service

router = APIRouter()


@router.get("/", response_model=list[PetRead])
async def list_pets(current_user: dict = Depends(get_current_user)):
    return pet_service.list_pets(current_user["id"])


@router.post("/", response_model=PetRead)
async def create_pet(payload: PetCreate, current_user: dict = Depends(get_current_user)):
    return pet_service.create_pet(current_user, payload.model_dump())


@router.put("/{pet_id}", response_model=PetRead)
async def update_pet(
    pet_id: int,
    payload: PetUpdate,
    current_user: dict = Depends(get_current_user),
):
    return pet_service.update_pet(current_user["id"], pet_id, payload.model_dump())


@router.post("/active")
async def switch_active_pet(payload: ActivePetSwitch, current_user: dict = Depends(get_current_user)):
    user = pet_service.switch_active_pet(current_user["id"], payload.pet_id)
    return {"active_pet_id": user["active_pet_id"]}


@router.delete("/{pet_id}")
async def delete_pet(pet_id: int, current_user: dict = Depends(get_current_user)):
    pet_service.delete_pet(current_user, pet_id)
    return {"status": "deleted"}
