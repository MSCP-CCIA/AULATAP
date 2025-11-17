
"""
Schemas para la entidad Horario, utilizados en la API.
"""

import datetime
import enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional


# Enum para los días de la semana (reutilizado de la entidad)
class DiaSemana(str, enum.Enum):
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"
    DOMINGO = "Domingo"


# Schema base para Horario
class HorarioBase(BaseModel):
    dia_semana: DiaSemana = Field(..., example="Lunes")
    hora_inicio: datetime.time = Field(..., example="08:00:00")
    hora_fin: datetime.time = Field(..., example="10:00:00")

    @field_validator('hora_fin')
    @classmethod
    def validar_horas(cls, v: datetime.time, info: ValidationInfo) -> datetime.time:
        """Valida que la hora de fin sea posterior a la de inicio."""
        if 'hora_inicio' in info.data and v <= info.data['hora_inicio']:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
        return v


# Schema para la creación de un Horario
class HorarioCreate(HorarioBase):
    pass


# Schema para la actualización de un Horario
class HorarioUpdate(BaseModel):
    dia_semana: Optional[DiaSemana] = Field(None, example="Martes")
    hora_inicio: Optional[datetime.time] = Field(None, example="09:00:00")
    hora_fin: Optional[datetime.time] = Field(None, example="11:00:00")


# Schema para la respuesta pública de un Horario
class HorarioPublic(HorarioBase):
    id: int

    class Config:
        from_attributes = True
