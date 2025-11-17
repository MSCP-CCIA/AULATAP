
"""
Schemas para la entidad ClaseProgramada (asociación entre Asignatura y Horario), utilizados en la API.
"""

from pydantic import BaseModel, Field
from typing import Optional

from .asignatura_schemas import AsignaturaPublic
from .horario_schemas import HorarioPublic


# Schema base para ClaseProgramada
class ClaseProgramadaBase(BaseModel):
    id_asignatura: int = Field(..., example=1)
    id_horario: int = Field(..., example=1)


# Schema para la creación de una ClaseProgramada
class ClaseProgramadaCreate(ClaseProgramadaBase):
    pass


# No se define un Update, ya que es una tabla de relación.
# Si se necesita cambiar, se borra y se crea una nueva relación.


# Schema para la respuesta pública de una ClaseProgramada
class ClaseProgramadaPublic(BaseModel):
    asignatura: AsignaturaPublic
    horario: HorarioPublic

    class Config:
        from_attributes = True
