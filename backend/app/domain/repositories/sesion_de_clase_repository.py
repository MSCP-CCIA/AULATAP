"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Sesiones.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseCreate, SesionDeClaseUpdate


class ISesionDeClaseRepository(ABC):
    """Interfaz abstracta para el repositorio de sesiones."""

    @abstractmethod
    async def get_by_id(self, sesion_id: uuid.UUID) -> Optional[SesionDeClase]:
        """Obtiene una sesión por su ID."""
        pass

    @abstractmethod
    async def find_activa(self, id_clase: uuid.UUID, id_horario: uuid.UUID) -> Optional[SesionDeClase]:
        """Busca una sesión activa para una clase/horario."""
        pass

    @abstractmethod
    async def create(self, sesion_create: SesionDeClaseCreate) -> SesionDeClase:
        """Inicia una nueva sesión de clase."""
        pass

    @abstractmethod
    async def update(self, sesion_id: uuid.UUID, sesion_update: SesionDeClaseUpdate) -> Optional[SesionDeClase]:
        """Actualiza una sesión (ej. para cerrarla)."""
        pass
