
"""
Schemas para la entidad Estudiante, utilizados en la API.
"""

import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Schema base para Estudiante
class EstudianteBase(BaseModel):
    email: EmailStr = Field(..., example="estudiante@example.com")
    nombre_completo: str = Field(..., min_length=3, max_length=50, example="Ana Gómez")
    rfc_uid: str = Field(..., max_length=50, description="RFC o UID de la tarjeta NFC", example="GOMA881122ABC")


# Schema para la creación de un Estudiante
class EstudianteCreate(EstudianteBase):
    pass


# Schema para la actualización de un Estudiante
class EstudianteUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="ana.gomez@example.com")
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=50, example="Ana María Gómez")
    rfc_uid: Optional[str] = Field(None, max_length=50, example="GOMA881122XYZ")


# Schema para la respuesta pública de un Estudiante
class EstudiantePublic(EstudianteBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
