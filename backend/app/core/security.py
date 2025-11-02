"""
Security Module
Funciones de seguridad: password hashing, JWT generation/validation, OAuth2 scheme.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

# ==================== PASSWORD HASHING ====================

# SOLUCIÓN TEMPORAL: Cambiamos 'bcrypt' por 'plaintext' para evitar
# el error de carga del backend en tu entorno.
# ¡RECUERDA CAMBIARLO A ["bcrypt"] ANTES DE IR A PRODUCCIÓN!
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña plana coincide con su hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash bcrypt almacenado en DB

    Returns:
        True si coincide, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera hash bcrypt de una contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash bcrypt
    """
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> None:
    """
    Valida que la contraseña cumpla con los requisitos de seguridad.

    Args:
        password: Contraseña a validar

    Raises:
        ValueError: Si no cumple requisitos
    """
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters")

    if settings.PASSWORD_REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")

    if settings.PASSWORD_REQUIRE_LOWERCASE and not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter")

    if settings.PASSWORD_REQUIRE_DIGIT and not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")

    if settings.PASSWORD_REQUIRE_SPECIAL and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        raise ValueError("Password must contain at least one special character")


# ==================== JWT TOKEN GENERATION ====================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un JWT access token.

    Args:
        data: Payload del token (debe incluir 'sub' con user ID)
        expires_delta: Tiempo de expiración (default: config)

    Returns:
        Token JWT firmado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Genera un JWT refresh token.

    Args:
        data: Payload del token (debe incluir 'sub' con user ID)

    Returns:
        Refresh token JWT firmado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodifica y valida un access token.

    Args:
        token: JWT token

    Returns:
        Payload del token

    Raises:
        UnauthorizedException: Si el token es inválido o expirado
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Validar que sea un access token
        if payload.get("type") != "access":
            raise UnauthorizedException(detail="Invalid token type")

        return payload

    except JWTError as e:
        raise UnauthorizedException(detail=f"Invalid token: {str(e)}")


def decode_refresh_token(token: str) -> Dict[str, Any]:
    """
    Decodifica y valida un refresh token.

    Args:
        token: JWT refresh token

    Returns:
        Payload del token

    Raises:
        UnauthorizedException: Si el token es inválido o expirado
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Validar que sea un refresh token
        if payload.get("type") != "refresh":
            raise UnauthorizedException(detail="Invalid token type")

        return payload

    except JWTError as e:
        raise UnauthorizedException(detail=f"Invalid refresh token: {str(e)}")


# ==================== OAUTH2 SCHEME ====================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="Bearer"
)


async def get_token_payload(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Dependency para extraer y validar el payload del JWT.

    Args:
        token: Token extraído del header Authorization

    Returns:
        Payload del token

    Raises:
        UnauthorizedException: Si el token es inválido
    """
    return decode_access_token(token)


# ==================== HELPER FUNCTIONS ====================

def extract_user_id_from_token(payload: Dict[str, Any]) -> UUID:
    """
    Extrae el user ID del payload del token.

    Args:
        payload: Payload decodificado del JWT

    Returns:
        UUID del usuario

    Raises:
        UnauthorizedException: Si no hay 'sub' en el payload
    """
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException(detail="Token missing 'sub' claim")

    try:
        return UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException(detail="Invalid user ID format in token")


def check_token_permission(payload: Dict[str, Any], required_permission: str) -> None:
    """
    Verifica que el token tenga un permiso específico.

    Args:
        payload: Payload del token
        required_permission: Permiso requerido (ej: "write:attendance")

    Raises:
        HTTPException 403: Si no tiene el permiso
    """
    permissions = payload.get("permissions", [])

    # Admin tiene todos los permisos
    if "*:*" in permissions:
        return

    if required_permission not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required permission: {required_permission}"
        )

