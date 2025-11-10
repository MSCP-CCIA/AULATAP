"""
Define la entidad de negocio 'Inscripcion'.
"""

import uuid
from datetime import date
from pydantic import BaseModel, Field

class InscripcionBase(BaseModel):
    """Modelo base para Inscripcion."""
    id_clase: uuid.UUID
    id_estudiante: uuid.UUID

class Inscripcion(InscripcionBase):
    """Modelo completo de la entidad Inscripcion."""
    fecha_inscripcion: date

    class Config:
        from_attributes = True

class InscripcionCreate(InscripcionBase):
    """Modelo para crear una nueva Inscripcion."""
    pass
