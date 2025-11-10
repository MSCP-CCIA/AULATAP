
"""
Schemas para la entidad RegistroAsistencia, utilizados en la API.
"""

import uuid
import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .estudiante_schemas import EstudiantePublic
from .sesion_de_clase_schemas import SesionDeClasePublic


# Enum para los estados de asistencia (reutilizado de la entidad)
class EstadoAsistencia(str, enum.Enum):
    PRESENTE = "Presente"
    AUSENTE = "Ausente"
    TARDE = "Tarde"


# Schema para el "tap" de una tarjeta NFC para registrar asistencia.
# Esto es lo que enviaría el dispositivo que lee la tarjeta.
class AsistenciaTapCreate(BaseModel):
    rfc_uid: str = Field(..., description="RFC o UID leído de la tarjeta NFC")
    id_sesion_clase: uuid.UUID = Field(..., description="ID de la sesión de clase actual")


# Schema para la creación manual de un registro de asistencia
class RegistroAsistenciaCreate(BaseModel):
    id_sesion_clase: uuid.UUID
    id_estudiante: uuid.UUID
    estado_asistencia: EstadoAsistencia = Field(default=EstadoAsistencia.PRESENTE)


# Schema para la actualización de un registro de asistencia
class RegistroAsistenciaUpdate(BaseModel):
    estado_asistencia: Optional[EstadoAsistencia] = None


# Schema para la respuesta pública de un RegistroAsistencia
class RegistroAsistenciaPublic(BaseModel):
    id: uuid.UUID
    hora_entrada: Optional[datetime] = None
    hora_salida: Optional[datetime] = None
    estado_asistencia: EstadoAsistencia
    estudiante: EstudiantePublic
    # Opcionalmente, podríamos incluir la sesión para dar más contexto
    # sesion: SesionDeClasePublic

    class Config:
        from_attributes = True
