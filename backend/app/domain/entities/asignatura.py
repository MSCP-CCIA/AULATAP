"""
Define la entidad de negocio 'Asignatura' (Clase).
"""

import uuid
from pydantic import BaseModel, Field
from typing import Optional


# --- TU CÓDIGO ---

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


class AsignaturaPublic(BaseModel):
    """
    DTO público para retornar al cliente.
    (Oculta el id_docente si no es necesario)
    """
    id: uuid.UUID
    nombre_materia: str
    grupo: str

    # Si quisieras incluir al docente, lo anidarías aquí
    # docente: Optional[UsuarioPublic] = None

    class Config:
        from_attributes = True

