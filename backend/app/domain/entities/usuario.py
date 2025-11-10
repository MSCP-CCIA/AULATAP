"""
Define la entidad de negocio 'Usuario' (Profesor).
Esto es un modelo Pydantic, NO un modelo de SQLAlchemy.
Define la forma de los datos que usa la lógica de negocio.
"""

import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioBase(BaseModel):
    """Modelo base para Usuario con campos comunes."""
    email: EmailStr
    nombre_completo: str = Field(..., max_length=50)
    rol: str = Field("docente", max_length=20)


class Usuario(UsuarioBase):
    """Modelo completo de la entidad Usuario (leído desde la DB)."""
    id: uuid.UUID

    class Config:
        from_attributes = True


class UsuarioCreate(UsuarioBase):
    """Modelo para crear un nuevo Usuario (requiere password)."""
    password: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    """Modelo para actualizar un Usuario existente."""
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = Field(None, max_length=50)
    rol: Optional[str] = Field(None, max_length=20)


class UsuarioPublic(UsuarioBase):
    """Modelo seguro para retornar al cliente (sin ID o hashes)."""
    id: uuid.UUID

    class Config:
        from_attributes = True
