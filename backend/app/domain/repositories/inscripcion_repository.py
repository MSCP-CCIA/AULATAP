"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Inscripciones.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.inscripcion import Inscripcion, InscripcionCreate

class IInscripcionRepository(ABC):
    """Interfaz abstracta para el repositorio de inscripciones."""

    @abstractmethod
    async def create(self, inscripcion_create: InscripcionCreate) -> Inscripcion:
        """Crea una nueva inscripción."""
        pass

    @abstractmethod
    async def get_by_asignatura_and_estudiante(self, id_asignatura: int, id_estudiante: int) -> Optional[Inscripcion]:
        """Obtiene una inscripción por ID de asignatura y estudiante."""
        pass

    @abstractmethod
    async def list_by_estudiante(self, id_estudiante: int) -> List[Inscripcion]:
        """Lista todas las inscripciones de un estudiante."""
        pass

    @abstractmethod
    async def find_by_asignatura(self, id_asignatura: int) -> List[Inscripcion]:
        """Busca todas las inscripciones para una asignatura."""
        pass
