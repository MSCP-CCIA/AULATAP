"""
Define la entidad de negocio 'Horario'.
"""

import uuid
import datetime
import enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo

class DiaSemana(str, enum.Enum):
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"
    DOMINGO = "Domingo"

class HorarioBase(BaseModel):
    """Modelo base para Horario."""
    dia_semana: DiaSemana
    hora_inicio: datetime.time
    hora_fin: datetime.time

    @field_validator('hora_fin')
    @classmethod
    def validar_horas(cls, v: datetime.time, info: ValidationInfo) -> datetime.time:
        """Valida que la hora de fin sea posterior a la de inicio."""
        if 'hora_inicio' in info.data and v <= info.data['hora_inicio']:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
        return v

class Horario(HorarioBase):
    """Modelo completo de la entidad Horario."""
    id: uuid.UUID

    class Config:
        from_attributes = True

class HorarioCreate(HorarioBase):
    """Modelo para crear un nuevo Horario."""
    pass

class HorarioPublic(Horario):
    """DTO público para Horario (en este caso es igual a la entidad)."""
    pass
