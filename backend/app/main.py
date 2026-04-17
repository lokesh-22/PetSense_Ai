from fastapi import FastAPI

from app.core.config import settings
from app.routers import api_router


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = create_application()
