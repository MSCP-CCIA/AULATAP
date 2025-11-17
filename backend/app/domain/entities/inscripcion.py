"""
Define la entidad de negocio 'Inscripcion'.
"""

from datetime import date
from pydantic import BaseModel, Field

class InscripcionBase(BaseModel):
    """Modelo base para Inscripcion."""
    id_clase: int
    id_estudiante: int

class Inscripcion(InscripcionBase):
    """Modelo completo de la entidad Inscripcion."""
    fecha_inscripcion: date

    class Config:
        from_attributes = True

class InscripcionCreate(InscripcionBase):
    """Modelo para crear una nueva Inscripcion."""
    pass
