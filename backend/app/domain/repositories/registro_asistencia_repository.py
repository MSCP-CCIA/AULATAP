"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Asistencia.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.registro_asistencia import RegistroAsistencia, RegistroAsistenciaCreate, RegistroAsistenciaUpdate


class IRegistroAsistenciaRepository(ABC):
    """Interfaz abstracta para el repositorio de asistencia."""

    @abstractmethod
    async def get_by_id(self, registro_id: int) -> Optional[RegistroAsistencia]:
        """Obtiene un registro de asistencia por su ID."""
        pass

    @abstractmethod
    async def get_by_sesion_and_estudiante(self, sesion_id: int, estudiante_id: int) -> Optional[RegistroAsistencia]:
        """Busca si ya existe un registro de asistencia para este estudiante en esta sesión."""
        pass

    @abstractmethod
    async def create(self, registro_create: RegistroAsistenciaCreate) -> RegistroAsistencia:
        """Crea un nuevo registro de asistencia."""
        pass

    @abstractmethod
    async def update(self, registro_id: int, registro_update: RegistroAsistenciaUpdate) -> Optional[RegistroAsistencia]:
        """Actualiza un registro de asistencia (ej. para marcar salida)."""
        pass

    @abstractmethod
    async def list_by_sesion(self, sesion_id: int) -> List[RegistroAsistencia]:
        """Lista todos los registros de asistencia de una sesión."""
        pass
