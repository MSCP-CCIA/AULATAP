"""
Define la entidad de negocio 'RegistroAsistencia'.
"""

import uuid
import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EstadoAsistencia(str, enum.Enum):
    """Define los estados posibles de una asistencia."""
    PRESENTE = "Presente"
    AUSENTE = "Ausente"
    TARDE = "Tarde"


class RegistroAsistenciaBase(BaseModel):
    """Modelo base para RegistroAsistencia."""
    id_sesion_clase: uuid.UUID
    id_estudiante: uuid.UUID
    hora_entrada: Optional[datetime] = None
    hora_salida: Optional[datetime] = None
    estado_asistencia: EstadoAsistencia = Field(default=EstadoAsistencia.AUSENTE)


class RegistroAsistencia(RegistroAsistenciaBase):
    """Modelo completo de la entidad RegistroAsistencia."""
    id: uuid.UUID

    class Config:
        from_attributes = True


class RegistroAsistenciaCreate(BaseModel):
    """Modelo para el 'tap' de asistencia."""
    id_sesion_clase: uuid.UUID
    id_estudiante: uuid.UUID
    hora_entrada: datetime
