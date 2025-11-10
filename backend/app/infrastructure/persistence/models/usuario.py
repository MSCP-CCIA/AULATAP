from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import List


class Usuario(Base):
    __tablename__ = "Usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_completo: Mapped[str] = mapped_column(VARCHAR(50))
    email: Mapped[str] = mapped_column(VARCHAR(50), unique=True)

    # --- ADVERTENCIA ---
    # VARCHAR(50) es MUY corto para un password hash.
    # Se recomienda al menos 128 o 255.
    password_hash: Mapped[str] = mapped_column(VARCHAR(150))

    # Relación: 1-a-Muchos con Asignatura
    asignaturas_impartidas: Mapped[List["Asignatura"]] = relationship(
        "Asignatura", back_populates="docente"
    )