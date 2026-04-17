from fastapi import APIRouter

from app.routers import auth, chat, health, pets, scanner

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(pets.router, prefix="/pets", tags=["pets"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(scanner.router, prefix="/scanner", tags=["scanner"])
