from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.health import SymptomRequest
from app.services.health_service import health_service

router = APIRouter()


@router.get("/dashboard")
async def health_dashboard(current_user: dict = Depends(get_current_user)):
    return health_service.get_dashboard(current_user)


@router.post("/symptoms")
async def analyze_symptoms(payload: SymptomRequest, current_user: dict = Depends(get_current_user)):
    return health_service.analyze_symptoms(
        current_user["id"],
        payload.pet_id,
        payload.symptoms,
        payload.duration,
    )


@router.get("/weight/{pet_id}")
async def weight_overview(pet_id: int, current_user: dict = Depends(get_current_user)):
    return health_service.build_weight_overview(pet_id, current_user["id"])
