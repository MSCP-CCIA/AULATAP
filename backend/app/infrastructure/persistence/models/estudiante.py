from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import List


class Estudiante(Base):
    __tablename__ = "Estudiante"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_completo: Mapped[str] = mapped_column(VARCHAR(50))
    rfc_uid: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(50), unique=True)

    # Relación M-N con Asignatura (via Inscripcion)
    inscripciones: Mapped[List["Inscripcion"]] = relationship(
        "Inscripcion", back_populates="estudiante"
    )

    # Relación 1-N con RegistroAsistencia
    asistencias: Mapped[List["RegistroAsistencia"]] = relationship(
        "RegistroAsistencia", back_populates="estudiante"
    )