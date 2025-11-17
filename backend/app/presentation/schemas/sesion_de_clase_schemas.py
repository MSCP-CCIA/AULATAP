
"""
Schemas para la entidad SesionDeClase, utilizados en la API.
"""

import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .clase_programada_schemas import ClaseProgramadaPublic


# Enum para los estados de la sesión (reutilizado de la entidad)
class EstadoSesion(str, enum.Enum):
    EN_PROGRESO = "EnProgreso"
    VALIDACION_ABIERTA = "ValidacionAbierta"
    VALIDACION_CERRADA = "ValidacionCerrada"
    CERRADA = "Cerrada"


# Schema base para SesionDeClase
class SesionDeClaseBase(BaseModel):
    id_clase_programada: int = Field(..., description="ID de la clase programada (asignatura + horario)", example=1)
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase", example="Introducción a las Derivadas")


# Schema para la creación de una SesionDeClase (ej. al abrir una sesión)
class SesionDeClaseCreate(BaseModel):
    id_clase_programada: int
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")


# Schema para la actualización de una SesionDeClase (ej. al cerrar una sesión)
class SesionDeClaseUpdate(BaseModel):
    estado: Optional[EstadoSesion] = Field(None, example=EstadoSesion.CERRADA)
    tema: Optional[str] = Field(None, max_length=100, description="Tema de la sesión de clase")


# Schema para la petición de abrir una sesión
class AbrirSesionRequest(BaseModel):
    id_asignatura: int = Field(..., description="ID de la asignatura a la que pertenece la sesión")
    id_horario: int = Field(..., description="ID del horario en el que se programa la sesión")
    tema: Optional[str] = Field(None, max_length=100, description="Tema opcional para la sesión")


# Schema para la respuesta pública de una SesionDeClase
class SesionDeClasePublic(BaseModel):
    id: int
    hora_inicio: datetime
    hora_fin: Optional[datetime] = None
    estado: EstadoSesion
    tema: Optional[str] = None
    clase_programada: ClaseProgramadaPublic

    class Config:
        from_attributes = True
