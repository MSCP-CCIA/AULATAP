
"""
Endpoint para la autenticación de usuarios.
"""
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.core.dependencies import get_current_active_user
from app.infrastructure.persistence.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.presentation.schemas.usuario_schemas import Token, UsuarioPublic
from app.domain.entities.usuario import Usuario

router = APIRouter()


async def authenticate_user(email: str, password: str, db: AsyncSession) -> Usuario | None:
    """
    Autentica a un usuario.
    """
    user_repo = UsuarioRepositoryImpl(db)
    user = await user_repo.get_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Proporciona un token de acceso JWT para un usuario autenticado.
    """
    user = await authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UsuarioPublic, dependencies=[Depends(get_current_active_user)])
async def read_users_me(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Devuelve los datos del usuario actualmente autenticado.
    """
    return current_user
