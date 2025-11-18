"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Sesiones.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseCreate, SesionDeClaseUpdate


class ISesionDeClaseRepository(ABC):
    """Interfaz abstracta para el repositorio de sesiones."""

    @abstractmethod
    async def get_by_id(self, sesion_id: int) -> Optional[SesionDeClase]:
        """Obtiene una sesión por su ID."""
        pass

    @abstractmethod
    async def find_activa(self, id_clase: int, id_horario: int) -> Optional[SesionDeClase]:
        """Busca una sesión activa para una clase/horario."""
        pass

    @abstractmethod
    async def find_active_by_asignaturas(self, id_asignaturas: List[int]) -> List[SesionDeClase]:
        """Busca sesiones activas para una lista de asignaturas."""
        pass

    @abstractmethod
    async def find_validation_open_by_asignaturas(self, id_asignaturas: List[int]) -> List[SesionDeClase]:
        """Busca sesiones con validación abierta para una lista de asignaturas."""
        pass

    @abstractmethod
    async def create(self, sesion_create: SesionDeClaseCreate) -> SesionDeClase:
        """Inicia una nueva sesión de clase."""
        pass

    @abstractmethod
    async def update(self, sesion_id: int, sesion_update: SesionDeClaseUpdate) -> Optional[SesionDeClase]:
        """Actualiza una sesión (ej. para cerrarla)."""
        pass
