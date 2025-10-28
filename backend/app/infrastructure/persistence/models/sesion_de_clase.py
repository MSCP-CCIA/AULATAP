import enum
import datetime
from sqlalchemy import (
    TIMESTAMP, VARCHAR, Enum, ForeignKey, ForeignKeyConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import Optional, List


class EstadoSesion(enum.Enum):
    EnProgreso = "EnProgreso"
    Cerrada = "Cerrada"


class SesionDeClase(Base):
    __tablename__ = "SesionDeClase"

    id: Mapped[int] = mapped_column(primary_key=True)
    hora_inicio: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    hora_fin: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True
    )
    estado: Mapped[EstadoSesion] = mapped_column(
        Enum(EstadoSesion), default=EstadoSesion.EnProgreso
    )

    # --- NOTA IMPORTANTE DE DISEÑO ---
    # El diagrama muestra una relación 1-N desde ClaseProgramada,
    # que tiene una clave compuesta (id_clase, id_horario).
    # Por lo tanto, esta tabla DEBE tener ambos FKs.
    id_clase: Mapped[int] = mapped_column()
    id_horario: Mapped[int] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_clase", "id_horario"],
            ["ClaseProgramada.id_clase", "ClaseProgramada.id_horario"]
        ),
    )

    # Relación N-1 con ClaseProgramada
    clase_programada: Mapped["ClaseProgramada"] = relationship(
        "ClaseProgramada", back_populates="sesiones"
    )

    # Relación 1-N con RegistroAsistencia
    asistencias: Mapped[List["RegistroAsistencia"]] = relationship(
        "RegistroAsistencia", back_populates="sesion_de_clase"
    )