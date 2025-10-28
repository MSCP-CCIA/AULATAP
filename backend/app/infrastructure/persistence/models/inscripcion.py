import datetime
from sqlalchemy import ForeignKey, DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Inscripcion(Base):
    __tablename__ = "Inscripcion"

    # Clave primaria compuesta (PK, FK)
    id_clase: Mapped[int] = mapped_column(
        ForeignKey("Asignatura.id"), primary_key=True
    )
    id_estudiante: Mapped[int] = mapped_column(
        ForeignKey("Estudiante.id"), primary_key=True
    )

    fecha_inscripcion: Mapped[datetime.date] = mapped_column(DATE)

    # Relaciones para acceder a los objetos
    clase: Mapped["Asignatura"] = relationship(back_populates="inscripciones")
    estudiante: Mapped["Estudiante"] = relationship(back_populates="inscripciones")