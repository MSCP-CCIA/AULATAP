"""
Dependencies Module
FastAPI dependencies para autenticación, autorización e inyección de servicios.
"""

from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_token_payload, extract_user_id_from_token, oauth2_scheme
from app.core.exceptions import UnauthorizedException, ForbiddenException

from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import IUsuarioRepository
from app.infrastructure.persistence.repositories.usuario_repository_impl import UsuarioRepositoryImpl


# ==================== USER AUTHENTICATION ====================

async def get_usuario_repository(db: AsyncSession = Depends(get_db)) -> IUsuarioRepository:
    """Inyecta UsuarioRepository."""
    return UsuarioRepositoryImpl(db)


async def get_current_user(
        token_payload: Dict[str, Any] = Depends(get_token_payload),
        usuario_repo: IUsuarioRepository = Depends(get_usuario_repository)
) -> Usuario:
    """
    Dependency que retorna el usuario autenticado actual.
    """
    user_id = extract_user_id_from_token(token_payload)

    user = await usuario_repo.get_by_id(user_id)

    if not user:
        raise UnauthorizedException(detail="User not found")

    return user


async def get_current_active_user(
        current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependency que verifica que el usuario esté activo.
    NOTA: Actualmente, la entidad Usuario no tiene un campo 'is_active'.
    Esta dependencia simplemente retorna el usuario autenticado.
    Si se añade un campo 'is_active' en el futuro, se debería implementar aquí.
    """
    # if not current_user.is_active:
    #     raise ForbiddenException(detail="Inactive user")

    return current_user


# ==================== PERMISSION CHECKING ====================

class PermissionChecker:
    """
    Dependency class para verificar permisos específicos.
    (Este código está bien como está)
    """

    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    async def __call__(self, token_payload: Dict[str, Any] = Depends(get_token_payload)):
        user_permissions = token_payload.get("permissions", [])

        if "*:*" in user_permissions:
            return

        for required in self.required_permissions:
            if required not in user_permissions:
                raise ForbiddenException(
                    detail=f"Missing required permission: {required}"
                )


def require_role(allowed_roles: list[str]):
    """
    Dependency factory para verificar roles.
    (Este código está bien como está)
    """

    async def role_checker(token_payload: Dict[str, Any] = Depends(get_token_payload)):
        user_role = token_payload.get("role")

        if user_role not in allowed_roles:
            raise ForbiddenException(
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )

    return role_checker

# ==================== REPOSITORY INJECTION ====================
# (Comentados temporalmente para evitar ModuleNotFoundError)

# async def get_professor_repository(db: AsyncSession = Depends(get_db)): # -> ProfessorRepositoryImpl:
#     """Inyecta ProfessorRepository."""
#     return ProfessorRepositoryImpl(db)
#
#
# async def get_student_repository(db: AsyncSession = Depends(get_db)):
#     """Inyecta StudentRepository."""
#     from app.infrastructure.persistence.repositories.student_repository_impl import StudentRepositoryImpl
#     return StudentRepositoryImpl(db)
#
#
# async def get_nfc_card_repository(db: AsyncSession = Depends(get_db)):
#     """Inyecta NFCCardRepository."""
#     from app.infrastructure.persistence.repositories.nfc_card_repository_impl import NFCCardRepositoryImpl
#     return NFCCardRepositoryImpl(db)
#
#
# async def get_attendance_repository(db: AsyncSession = Depends(get_db)):
#     """Inyecta AttendanceRepository."""
#     from app.infrastructure.persistence.repositories.attendance_repository_impl import AttendanceRepositoryImpl
#     return AttendanceRepositoryImpl(db)
#
#
# async def get_session_repository(db: AsyncSession = Depends(get_db)):
#     """Inyecta SessionRepository."""
#     from app.infrastructure.persistence.repositories.session_repository_impl import SessionRepositoryImpl
#     return SessionRepositoryImpl(db)
#
#
# async def get_class_repository(db: AsyncSession = Depends(get_db)):
#     """Inyecta ClassRepository."""
#     from app.infrastructure.persistence.repositories.class_repository_impl import ClassRepositoryImpl
#     return ClassRepositoryImpl(db)
