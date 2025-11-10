"""
Define la entidad de negocio 'ClaseProgramada'.
"""

import uuid
from pydantic import BaseModel

class ClaseProgramadaBase(BaseModel):
    """Modelo base para ClaseProgramada."""
    id_clase: uuid.UUID
    id_horario: uuid.UUID

class ClaseProgramada(ClaseProgramadaBase):
    """Modelo completo de la entidad ClaseProgramada."""
    class Config:
        from_attributes = True

class ClaseProgramadaCreate(ClaseProgramadaBase):
    """Modelo para crear una nueva ClaseProgramada."""
    pass
