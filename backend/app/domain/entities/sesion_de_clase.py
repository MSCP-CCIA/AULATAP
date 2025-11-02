"""
Define la entidad de negocio 'SesionDeClase'.
"""

import uuid
import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EstadoSesion(str, enum.Enum):
    """Define los estados posibles de una sesión."""
    EN_PROGRESO = "EnProgreso"
    CERRADA = "Cerrada"


class SesionDeClaseBase(BaseModel):
    """Modelo base para SesionDeClase."""
    id_clase: uuid.UUID
    id_horario: uuid.UUID
    hora_inicio: datetime
    hora_fin: Optional[datetime] = None
    estado: EstadoSesion = Field(default=EstadoSesion.EN_PROGRESO)


class SesionDeClase(SesionDeClaseBase):
    """Modelo completo de la entidad SesionDeClase."""
    id: uuid.UUID

    class Config:
        from_attributes = True


class SesionDeClaseCreate(BaseModel):
    """Modelo para crear una nueva SesionDeClase."""
    id_clase: uuid.UUID
    id_horario: uuid.UUID


class SesionDeClaseUpdate(BaseModel):
    """Modelo para actualizar una SesionDeClase (ej. cerrarla)."""
    estado: Optional[EstadoSesion] = None
    hora_fin: Optional[datetime] = None
