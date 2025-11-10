"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Clases Programadas.
"""

from abc import ABC, abstractmethod
import uuid
from typing import Optional
from app.domain.entities.clase_programada import ClaseProgramada, ClaseProgramadaCreate

class IClaseProgramadaRepository(ABC):
    """Interfaz abstracta para el repositorio de clases programadas."""

    @abstractmethod
    async def create(self, clase_programada_create: ClaseProgramadaCreate) -> ClaseProgramada:
        """Crea una nueva clase programada."""
        pass

    @abstractmethod
    async def get_by_asignatura_and_horario(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID) -> Optional[ClaseProgramada]:
        """Obtiene una clase programada por ID de asignatura y horario."""
        pass
