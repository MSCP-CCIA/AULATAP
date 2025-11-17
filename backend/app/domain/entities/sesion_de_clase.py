"""
Define la entidad de negocio 'SesionDeClase'.
"""

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
    id_clase: int
    id_horario: int
    hora_inicio: datetime
    hora_fin: Optional[datetime] = None
    estado: EstadoSesion = Field(default=EstadoSesion.EN_PROGRESO)
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")


class SesionDeClase(SesionDeClaseBase):
    """Modelo completo de la entidad SesionDeClase."""
    id: int

    class Config:
        from_attributes = True


class SesionDeClaseCreate(BaseModel):
    """Modelo para crear una nueva SesionDeClase."""
    id_clase: int
    id_horario: int
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")


class SesionDeClaseUpdate(BaseModel):
    """Modelo para actualizar una SesionDeClase (ej. cerrarla)."""
    estado: Optional[EstadoSesion] = None
    hora_fin: Optional[datetime] = None
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")
