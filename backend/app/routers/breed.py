from fastapi import APIRouter, Query

from app.services.breed_service import breed_service

router = APIRouter()


@router.get("/supported")
async def list_supported_breeds():
    return {"items": breed_service.list_supported_breeds()}


@router.get("/fetch")
async def fetch_breed_info(
    breed: str = Query(..., min_length=2),
    species: str = Query(..., pattern="^(dog|cat)$"),
):
    return breed_service.fetch_breed_profile(breed, species)
