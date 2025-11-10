
"""
Schemas para la entidad SesionDeClase, utilizados en la API.
"""

import uuid
import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .clase_programada_schemas import ClaseProgramadaPublic


# Enum para los estados de la sesión (reutilizado de la entidad)
class EstadoSesion(str, enum.Enum):
    EN_PROGRESO = "EnProgreso"
    CERRADA = "Cerrada"


# Schema base para SesionDeClase
class SesionDeClaseBase(BaseModel):
    id_clase_programada: uuid.UUID = Field(..., description="ID de la clase programada (asignatura + horario)")
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase", example="Introducción a las Derivadas")


# Schema para la creación de una SesionDeClase (ej. al abrir una sesión)
class SesionDeClaseCreate(BaseModel):
    id_clase_programada: uuid.UUID
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")


# Schema para la actualización de una SesionDeClase (ej. al cerrar una sesión)
class SesionDeClaseUpdate(BaseModel):
    estado: Optional[EstadoSesion] = Field(None, example=EstadoSesion.CERRADA)
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")


# Schema para la respuesta pública de una SesionDeClase
class SesionDeClasePublic(BaseModel):
    id: uuid.UUID
    hora_inicio: datetime
    hora_fin: Optional[datetime] = None
    estado: EstadoSesion
    tema: Optional[str] = None
    clase_programada: ClaseProgramadaPublic

    class Config:
        from_attributes = True
