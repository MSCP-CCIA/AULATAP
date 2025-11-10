
"""
Schemas para la entidad Inscripcion (asociación entre Asignatura y Estudiante), utilizados en la API.
"""

import uuid
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

from .asignatura_schemas import AsignaturaPublic
from .estudiante_schemas import EstudiantePublic


# Schema base para Inscripcion
class InscripcionBase(BaseModel):
    id_asignatura: uuid.UUID = Field(..., example=uuid.uuid4())
    id_estudiante: uuid.UUID = Field(..., example=uuid.uuid4())


# Schema para la creación de una Inscripcion
class InscripcionCreate(InscripcionBase):
    pass


# No se define un Update, ya que es una tabla de relación.
# Si se necesita cambiar, se borra y se crea una nueva relación.


# Schema para la respuesta pública de una Inscripcion
class InscripcionPublic(BaseModel):
    fecha_inscripcion: date
    asignatura: AsignaturaPublic
    estudiante: EstudiantePublic

    class Config:
        from_attributes = True
