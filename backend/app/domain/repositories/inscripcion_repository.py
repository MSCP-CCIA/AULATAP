"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Inscripciones.
"""

from abc import ABC, abstractmethod
import uuid
from typing import Optional
from app.domain.entities.inscripcion import Inscripcion, InscripcionCreate

class IInscripcionRepository(ABC):
    """Interfaz abstracta para el repositorio de inscripciones."""

    @abstractmethod
    async def create(self, inscripcion_create: InscripcionCreate) -> Inscripcion:
        """Crea una nueva inscripción."""
        pass

    @abstractmethod
    async def get_by_asignatura_and_estudiante(self, id_asignatura: uuid.UUID, id_estudiante: uuid.UUID) -> Optional[Inscripcion]:
        """Obtiene una inscripción por ID de asignatura y estudiante."""
        pass
