"""
Schemas para la entidad RegistroAsistencia, utilizados en la API.
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.domain.entities.registro_asistencia import EstadoAsistencia


class RegistrarAsistenciaRequest(BaseModel):
    """Schema para el "tap" de una tarjeta NFC."""
    rfc_uid_estudiante: str = Field(..., description="RFC o UID leído de la tarjeta NFC del estudiante")


class EstudianteInfo(BaseModel):
    """Información mínima del estudiante para la respuesta."""
    nombre_completo: str

    class Config:
        from_attributes = True


class AsignaturaInfo(BaseModel):
    """Información mínima de la asignatura para la respuesta."""
    nombre_materia: str
    grupo: str

    class Config:
        from_attributes = True


class RegistroAsistenciaPublic(BaseModel):
    """Schema para la respuesta pública de un RegistroAsistencia exitoso."""
    id: int
    hora_entrada: datetime
    estado_asistencia: EstadoAsistencia
    estudiante: EstudianteInfo
    asignatura: AsignaturaInfo
    tema_sesion: str | None

    class Config:
        from_attributes = True
