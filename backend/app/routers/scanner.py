from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.scanner import IngredientScanRequest
from app.services.scanner_service import scanner_service

router = APIRouter()


@router.post("/ingredients")
async def scan_ingredients(
    payload: IngredientScanRequest,
    current_user: dict = Depends(get_current_user),
):
    return scanner_service.scan(payload.ingredients_text)
