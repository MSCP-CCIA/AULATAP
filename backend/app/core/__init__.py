"""
Core Module - AulaTap Backend
Contiene configuración central, seguridad, base de datos y utilidades compartidas.
"""

from app.core.config import settings
from app.core.database import get_db, engine, async_session_factory
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
)
from app.core.exceptions import (
    AulaTapException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
)

__all__ = [
    # Config
    "settings",
    # Database
    "get_db",
    "engine",
    "async_session_factory",
    # Security
    "create_access_token",
    "create_refresh_token",
    "verify_password",
    "get_password_hash",
    # Exceptions
    "AulaTapException",
    "NotFoundException",
    "UnauthorizedException",
    "ForbiddenException",
    "ValidationException",
]