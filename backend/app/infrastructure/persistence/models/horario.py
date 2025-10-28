import datetime
from sqlalchemy import VARCHAR, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import List


class Horario(Base):
    __tablename__ = "Horario"

    id: Mapped[int] = mapped_column(primary_key=True)
    dia_semana: Mapped[str] = mapped_column(VARCHAR(10))
    hora_inicio: Mapped[datetime.time] = mapped_column(TIME)
    hora_fin: Mapped[datetime.time] = mapped_column(TIME)

    # Relación M-N con Asignatura (via ClaseProgramada)
    clases_programadas: Mapped[List["ClaseProgramada"]] = relationship(
        "ClaseProgramada", back_populates="horario"
    )