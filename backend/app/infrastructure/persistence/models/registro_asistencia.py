import enum
import datetime
from sqlalchemy import TIMESTAMP, VARCHAR, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import Optional


class EstadoAsistencia(enum.Enum):
    Presente = "Presente"
    Ausente = "Ausente"
    Tarde = "Tarde"


class RegistroAsistencia(Base):
    __tablename__ = "RegistroAsistencia"

    id: Mapped[int] = mapped_column(primary_key=True)
    hora_entrada: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True
    )
    hora_salida: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True
    )
    estado_asistencia: Mapped[EstadoAsistencia] = mapped_column(
        Enum(EstadoAsistencia), default=EstadoAsistencia.Ausente
    )

    id_sesion_clase: Mapped[int] = mapped_column(ForeignKey("SesionDeClase.id"))
    id_estudiante: Mapped[int] = mapped_column(ForeignKey("Estudiante.id"))

    # Relaciones N-1
    sesion_de_clase: Mapped["SesionDeClase"] = relationship(
        "SesionDeClase", back_populates="asistencias"
    )
    estudiante: Mapped["Estudiante"] = relationship(
        "Estudiante", back_populates="asistencias"
    )