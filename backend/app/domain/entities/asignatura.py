"""
Define la entidad de negocio 'Asignatura' (Clase).
"""

import uuid
from pydantic import BaseModel, Field


class AsignaturaBase(BaseModel):
    """Modelo base para Asignatura."""
    nombre_materia: str = Field(..., max_length=50)
    grupo: str = Field(..., max_length=50)
    id_docente: uuid.UUID


class Asignatura(AsignaturaBase):
    """Modelo completo de la entidad Asignatura."""
    id: uuid.UUID

    class Config:
        from_attributes = True


class AsignaturaCreate(AsignaturaBase):
    """Modelo para crear una nueva Asignatura."""
    pass
