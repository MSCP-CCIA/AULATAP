"""
Define la entidad de negocio 'Horario'.
"""

import uuid
import datetime
from pydantic import BaseModel, Field


class HorarioBase(BaseModel):
    """Modelo base para Horario."""
    dia_semana: str = Field(..., max_length=10)
    hora_inicio: datetime.time
    hora_fin: datetime.time


class Horario(HorarioBase):
    """Modelo completo de la entidad Horario."""
    id: uuid.UUID

    class Config:
        from_attributes = True


class HorarioCreate(HorarioBase):
    """Modelo para crear un nuevo Horario."""
    pass
