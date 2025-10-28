from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import List


class Asignatura(Base):
    __tablename__ = "Asignatura"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_materia: Mapped[str] = mapped_column(VARCHAR(50))
    grupo: Mapped[str] = mapped_column(VARCHAR(50))
    id_docente: Mapped[int] = mapped_column(ForeignKey("Usuario.id"))

    # Relación N-1 con Usuario
    docente: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="asignaturas_impartidas"
    )

    # Relación M-N con Estudiante (via Inscripcion)
    inscripciones: Mapped[List["Inscripcion"]] = relationship(
        "Inscripcion", back_populates="clase"
    )

    # Relación M-N con Horario (via ClaseProgramada)
    clases_programadas: Mapped[List["ClaseProgramada"]] = relationship(
        "ClaseProgramada", back_populates="asignatura"
    )