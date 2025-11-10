"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Asignaturas.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from app.domain.entities.asignatura import Asignatura, AsignaturaCreate

class IAsignaturaRepository(ABC):
    """Interfaz abstracta para el repositorio de asignaturas."""

    @abstractmethod
    async def get_by_id(self, asignatura_id: uuid.UUID) -> Optional[Asignatura]:
        """Obtiene una asignatura por su ID."""
        pass

    @abstractmethod
    async def list_by_docente(self, docente_id: uuid.UUID) -> List[Asignatura]:
        """Lista todas las asignaturas impartidas por un docente."""
        pass

    @abstractmethod
    async def create(self, asignatura_create: AsignaturaCreate) -> Asignatura:
        """Crea una nueva asignatura."""
        pass

    @abstractmethod
    async def esta_estudiante_inscrito(self, id_asignatura: uuid.UUID, id_estudiante: uuid.UUID) -> bool:
        """Verifica si un estudiante está inscrito en una asignatura."""
        pass

    @abstractmethod
    async def existe_clase_programada(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID) -> bool:
        """Verifica si una asignatura está programada en un horario."""
        pass
