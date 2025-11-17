"""
Define la entidad de negocio 'RegistroAsistencia'.
"""

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
    id_sesion_clase: int
    id_estudiante: int
    hora_entrada: Optional[datetime] = None
    hora_salida: Optional[datetime] = None
    estado_asistencia: EstadoAsistencia = Field(default=EstadoAsistencia.AUSENTE)


class RegistroAsistencia(RegistroAsistenciaBase):
    """Modelo completo de la entidad RegistroAsistencia."""
    id: int

    class Config:
        from_attributes = True


class RegistroAsistenciaCreate(BaseModel):
    """Modelo para el 'tap' de asistencia."""
    id_sesion_clase: int
    id_estudiante: int
    hora_registro: datetime = Field(default_factory=datetime.utcnow)
    estado_asistencia: EstadoAsistencia


class RegistroAsistenciaUpdate(BaseModel):
    """Modelo para actualizar un registro de asistencia."""
    hora_salida: Optional[datetime] = None
    estado_asistencia: Optional[EstadoAsistencia] = None
