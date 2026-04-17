from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard")
async def health_dashboard():
    return {"message": "Health dashboard placeholder."}


@router.post("/symptoms")
async def analyze_symptoms():
    return {"message": "Symptom analysis placeholder."}
