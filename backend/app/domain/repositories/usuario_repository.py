"""
Define la Interfaz (un contrato abstracto) para el Repositorio de Usuarios.
La capa de Dominio solo depende de esta abstracción, no de la
implementación concreta (SQLAlchemy).
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.usuario import Usuario, UsuarioCreate, UsuarioUpdate

class IUsuarioRepository(ABC):
    """Interfaz abstracta para el repositorio de usuarios."""

    @abstractmethod
    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
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

    @abstractmethod
    async def update(self, usuario_id: int, usuario_update: UsuarioUpdate) -> Optional[Usuario]:
        """Actualiza un usuario existente."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Usuario]:
        """Lista todos los usuarios."""
        pass
