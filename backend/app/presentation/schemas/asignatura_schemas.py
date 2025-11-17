
"""
Schemas para la entidad Asignatura, utilizados en la API.
"""

from pydantic import BaseModel, Field
from typing import Optional

from .usuario_schemas import UsuarioPublic


# Schema base para Asignatura
class AsignaturaBase(BaseModel):
    nombre_materia: str = Field(..., min_length=3, max_length=50, example="Cálculo I")
    grupo: str = Field(..., max_length=10, example="Grupo A")
    id_docente: int = Field(..., example=1)


# Schema para la creación de una Asignatura
class AsignaturaCreate(AsignaturaBase):
    pass


# Schema para la actualización de una Asignatura
class AsignaturaUpdate(BaseModel):
    nombre_materia: Optional[str] = Field(None, min_length=3, max_length=50, example="Cálculo Avanzado")
    grupo: Optional[str] = Field(None, max_length=10, example="Grupo B")
    id_docente: Optional[int] = Field(None, example=1)


# Schema para la respuesta pública de una Asignatura
class AsignaturaPublic(AsignaturaBase):
    id: int
    docente: Optional[UsuarioPublic] = None  # Anidar el docente para respuestas enriquecidas

    class Config:
        from_attributes = True
