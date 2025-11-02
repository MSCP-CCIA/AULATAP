"""
Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.exceptions import register_exception_handlers
from app.core.logger import logger
from app.presentation.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación (startup/shutdown).
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    if settings.is_development:
        await init_db()  # Solo en desarrollo

    yield

    # Shutdown
    logger.info("Shutting down application")
    await close_db()


# ==================== CREATE APP ====================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sistema de Asistencia Inteligente con NFC",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# ==================== CORS ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# ==================== EXCEPTION HANDLERS ====================

register_exception_handlers(app)

# ==================== ROUTERS ====================

app.include_router(api_v1_router, prefix="/api/v1")


# ==================== ROOT ENDPOINT ====================

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )