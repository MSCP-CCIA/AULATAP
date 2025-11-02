"""
Database Module
Configuración de SQLAlchemy con soporte asíncrono (psycopg).
"""

from typing import AsyncGenerator, Optional, Dict, Any
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, QueuePool

from app.core.config import settings
from app.core.logger import logger

# ==================== BASE DECLARATIVE ====================

# Importar la Base de la capa de persistencia (la misma que usa Alembic)
try:
    from app.infrastructure.persistence.models.base import Base
except ImportError:
    logger.warning("No se pudo importar 'Base' desde 'infrastructure'. Creando una Base declarativa genérica.")
    logger.warning("Esto es normal si solo se prueba el 'core', pero fallará con 'autogenerate' de Alembic.")
    Base = declarative_base()


# ==================== ENGINE CONFIGURATION (CORREGIDO) ====================

def get_engine() -> AsyncEngine:
    """
    Crea y configura el async engine de SQLAlchemy.
    Pasa los argumentos del pool solo si se usa QueuePool (producción).
    """

    # Argumentos base para el engine
    engine_args: Dict[str, Any] = {
        "echo": settings.DATABASE_ECHO,
        "pool_pre_ping": True,
    }

    # Configuración del pool basada en el entorno
    if settings.is_development:
        engine_args["poolclass"] = NullPool
    else:
        # Solo en producción (QueuePool) pasamos los argumentos de tamaño
        engine_args["poolclass"] = QueuePool
        engine_args["pool_size"] = settings.DATABASE_POOL_SIZE
        engine_args["max_overflow"] = settings.DATABASE_MAX_OVERFLOW
        engine_args["pool_timeout"] = settings.DATABASE_POOL_TIMEOUT

    # Crear el engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        **engine_args
    )

    try:
        db_url_safe = settings.DATABASE_URL.split('@')[1]
        logger.info(f"Database engine created: {db_url_safe}")
    except Exception:
        logger.info("Database engine created.")

    return engine


# Singleton del engine
engine = get_engine()

# ==================== SESSION FACTORY ====================

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ==================== DEPENDENCY FOR FASTAPI ====================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que provee una sesión de base de datos para FastAPI endpoints.
    Maneja el rollback en excepciones, pero NO hace auto-commit.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ==================== DATABASE LIFECYCLE ====================

async def init_db() -> None:
    """
    Inicializa la base de datos (crear tablas si no existen).
    NOTA: En producción usar Alembic migrations en lugar de esto.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (if they didn't exist)")


async def close_db() -> None:
    """
    Cierra el engine y libera conexiones.
    """
    await engine.dispose()
    logger.info("Database engine disposed")


# ==================== TRANSACTION CONTEXT MANAGER ====================

class DatabaseTransaction:
    """
    Context manager para transacciones manuales.
    """

    def __init__(self):
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self) -> AsyncSession:
        self.session = async_session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.session:
            return

        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()

