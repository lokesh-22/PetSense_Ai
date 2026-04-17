from fastapi import APIRouter

router = APIRouter()


@router.post("/ingredients")
async def scan_ingredients():
    return {"message": "Food ingredient scanner placeholder."}
