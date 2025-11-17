"""
Define la entidad de negocio 'ClaseProgramada'.
"""

from pydantic import BaseModel
from app.domain.entities.asignatura import Asignatura # New import
from app.domain.entities.horario import Horario # New import

class ClaseProgramadaBase(BaseModel):
    """Modelo base para ClaseProgramada."""
    id_clase: int
    id_horario: int

class ClaseProgramada(ClaseProgramadaBase):
    """Modelo completo de la entidad ClaseProgramada."""
    asignatura: Asignatura # Add asignatura field
    horario: Horario      # Add horario field

    class Config:
        from_attributes = True

class ClaseProgramadaCreate(ClaseProgramadaBase):
    """Modelo para crear una nueva ClaseProgramada."""
    pass
