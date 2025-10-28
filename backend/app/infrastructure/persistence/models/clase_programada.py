from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import List


class ClaseProgramada(Base):
    __tablename__ = "ClaseProgramada"

    # Clave primaria compuesta (PK, FK)
    id_clase: Mapped[int] = mapped_column(
        ForeignKey("Asignatura.id"), primary_key=True
    )
    id_horario: Mapped[int] = mapped_column(
        ForeignKey("Horario.id"), primary_key=True
    )

    # Relaciones para acceder a los objetos
    asignatura: Mapped["Asignatura"] = relationship(
        back_populates="clases_programadas"
    )
    horario: Mapped["Horario"] = relationship(
        back_populates="clases_programadas"
    )

    # Relación 1-N con SesionDeClase
    sesiones: Mapped[List["SesionDeClase"]] = relationship(
        "SesionDeClase", back_populates="clase_programada"
    )