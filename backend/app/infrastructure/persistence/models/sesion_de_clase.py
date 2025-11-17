"""
Modelo SQLAlchemy para SesionDeClase.
Refleja la tabla en la base de datos.
"""
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
    ValidacionAbierta = "ValidacionAbierta"
    ValidacionCerrada = "ValidacionCerrada"
    Cerrada = "Cerrada"


class SesionDeClase(Base):
    __tablename__ = "SesionDeClase"

    id: Mapped[int] = mapped_column(primary_key=True)

    # --- NUEVO CAMPO ---
    tema: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)

    # --- CAMPOS ORIGINALES ---
    hora_inicio: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    hora_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, nullable=True)
    estado: Mapped[EstadoSesion] = mapped_column(
        Enum(EstadoSesion, name="estadosesion", create_type=False), default=EstadoSesion.EnProgreso
    )

    # Clave compuesta para integridad con ClaseProgramada
    id_clase: Mapped[int] = mapped_column()
    id_horario: Mapped[int] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_clase", "id_horario"],
            ["ClaseProgramada.id_clase", "ClaseProgramada.id_horario"]
        ),
    )

    # Relaciones
    clase_programada: Mapped["ClaseProgramada"] = relationship(
        "ClaseProgramada", back_populates="sesiones"
    )
    asistencias: Mapped[List["RegistroAsistencia"]] = relationship(
        "RegistroAsistencia", back_populates="sesion_de_clase"
    )