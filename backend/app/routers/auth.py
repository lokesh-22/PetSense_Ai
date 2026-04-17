from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    return {"message": "Registration endpoint placeholder."}


@router.post("/login")
async def login():
    return {"message": "Login endpoint placeholder."}


@router.post("/refresh")
async def refresh_token():
    return {"message": "Refresh token endpoint placeholder."}
