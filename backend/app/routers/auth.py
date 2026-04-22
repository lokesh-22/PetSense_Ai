from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.auth import AuthResponse, LoginRequest, RefreshRequest, RegisterRequest, UserRead
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest):
    return auth_service.register(payload.email, payload.password, payload.full_name)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    return auth_service.login(payload.email, payload.password)


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(payload: RefreshRequest):
    return auth_service.refresh(payload.refresh_token)


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user
