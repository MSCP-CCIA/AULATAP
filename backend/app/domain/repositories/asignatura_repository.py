"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Asignaturas.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.asignatura import Asignatura, AsignaturaCreate

class IAsignaturaRepository(ABC):
    """Interfaz abstracta para el repositorio de asignaturas."""

    @abstractmethod
    async def get_by_id(self, asignatura_id: int) -> Optional[Asignatura]:
        """Obtiene una asignatura por su ID."""
        pass

    @abstractmethod
    async def list_by_docente(self, docente_id: int) -> List[Asignatura]:
        """Lista todas las asignaturas impartidas por un docente."""
        pass

    @abstractmethod
    async def create(self, asignatura_create: AsignaturaCreate) -> Asignatura:
        """Crea una nueva asignatura."""
        pass

    @abstractmethod
    async def esta_estudiante_inscrito(self, id_asignatura: int, id_estudiante: int) -> bool:
        """Verifica si un estudiante está inscrito en una asignatura."""
        pass

    @abstractmethod
    async def existe_clase_programada(self, id_asignatura: int, id_horario: int) -> bool:
        """Verifica si una asignatura está programada en un horario."""
        pass

    @abstractmethod
    async def docente_owns_asignatura(self, docente_id: int, asignatura_id: int) -> bool:
        """Verifica si un docente es dueño de una asignatura."""
        pass
