
"""
Schemas para la entidad Usuario, utilizados en la API.
"""

import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Schema base para Usuario
class UsuarioBase(BaseModel):
    email: EmailStr = Field(..., example="profesor@example.com")
    nombre_completo: str = Field(..., min_length=3, max_length=50, example="Juan Pérez")


# Schema para la creación de un Usuario (lo que se pide en el request)
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, example="una_contraseña_segura")


# Schema para la actualización de un Usuario
class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="profesor_nuevo@example.com")
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=50, example="Juan Alberto Pérez")
    password: Optional[str] = Field(None, min_length=8, example="otra_contraseña_mas_segura")


# Schema para representar al Usuario tal como está en la base de datos (incluye el hashed_password)
class UsuarioInDB(UsuarioBase):
    id: uuid.UUID
    password_hash: str

    class Config:
        from_attributes = True


# Schema para la respuesta pública (lo que se devuelve al cliente)
class UsuarioPublic(UsuarioBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# Schema para el token de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema para los datos contenidos dentro del token JWT
class TokenData(BaseModel):
    email: Optional[str] = None

