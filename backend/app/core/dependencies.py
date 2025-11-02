"""
Dependencies Module
FastAPI dependencies para autenticación, autorización e inyección de servicios.
"""

from typing import Dict, Any
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_token_payload, extract_user_id_from_token, oauth2_scheme
from app.core.exceptions import UnauthorizedException, ForbiddenException


# Imports necesarios de domain/infrastructure (ajustar según tu estructura)
# --- TEMPORALMENTE COMENTADO PARA PRUEBAS ---
# from app.domain.entities.professor import Professor
# from app.infrastructure.persistence.repositories.professor_repository_impl import ProfessorRepositoryImpl

# ==================== USER AUTHENTICATION ====================

async def get_current_user(
        token_payload: Dict[str, Any] = Depends(get_token_payload),
        db: AsyncSession = Depends(get_db)
):  # -> Professor:  <-- Temporalmente comentado
    """
    Dependency que retorna el usuario autenticado actual.
    """
    user_id = extract_user_id_from_token(token_payload)

    # --- TEMPORALMENTE COMENTADO PARA PRUEBAS ---
    # professor_repo = ProfessorRepositoryImpl(db)
    # professor = await professor_repo.get_by_id(user_id)
    #
    # if not professor:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    #
    # return professor

    # --- Temporalmente retornamos el ID para que la app no se rompa ---
    print(f"Mock get_current_user: ID {user_id}")
    return {"user_id": user_id}


async def get_current_active_user(
        current_user=Depends(get_current_user)  # : Professor = Depends(get_current_user) <-- Temporal
):  # -> Professor:
    """
    Dependency que verifica que el usuario esté activo.
    """
    # --- TEMPORALMENTE COMENTADO PARA PRUEBAS ---
    # if not current_user.is_active:
    #     raise ForbiddenException(detail="Inactive user")
    #
    # return current_user
    print(f"Mock get_current_active_user: {current_user}")
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
