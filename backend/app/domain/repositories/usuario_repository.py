"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Usuarios.
La capa de Dominio solo depende de esta abstracción, no de la
implementación concreta (SQLAlchemy).
"""

from abc import ABC, abstractmethod
from typing import Optional
import uuid
from app.domain.entities.usuario import Usuario, UsuarioCreate

class IUsuarioRepository(ABC):
    """Interfaz abstracta para el repositorio de usuarios."""

    @abstractmethod
    async def get_by_id(self, usuario_id: uuid.UUID) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email."""
        pass

    @abstractmethod
    async def create(self, usuario_create: UsuarioCreate) -> Usuario:
        """Crea un nuevo usuario en la base de datos."""
        pass
