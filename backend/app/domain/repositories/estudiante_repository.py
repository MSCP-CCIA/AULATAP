"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Estudiantes.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.estudiante import Estudiante, EstudianteCreate


class IEstudianteRepository(ABC):
    """Interfaz abstracta para el repositorio de estudiantes."""

    @abstractmethod
    async def get_by_id(self, estudiante_id: int) -> Optional[Estudiante]:
        """Obtiene un estudiante por su ID."""
        pass

    @abstractmethod
    async def get_by_rfc_uid(self, rfc_uid: str) -> Optional[Estudiante]:
        """Obtiene un estudiante por su RFC/UID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Estudiante]:
        """Obtiene un estudiante por su email."""
        pass

    @abstractmethod
    async def create(self, estudiante_create: EstudianteCreate) -> Estudiante:
        """Crea un nuevo estudiante."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Estudiante]:
        """Lista todos los estudiantes."""
        pass
