from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_pets():
    return {"items": [], "message": "Pet listing placeholder."}


@router.post("/")
async def create_pet():
    return {"message": "Pet creation placeholder."}
