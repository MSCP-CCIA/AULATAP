"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Horarios.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.horario import Horario, HorarioCreate


class IHorarioRepository(ABC):
    """Interfaz abstracta para el repositorio de horarios."""

    @abstractmethod
    async def get_by_id(self, horario_id: int) -> Optional[Horario]:
        """Obtiene un horario por su ID."""
        pass

    @abstractmethod
    async def create(self, horario_create: HorarioCreate) -> Horario:
        """Crea un nuevo horario."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Horario]:
        """Lista todos los horarios."""
        pass
