"""
Caso de Uso: Crear una nueva Asignatura.
"""
import uuid
from app.domain.entities.asignatura import Asignatura, AsignaturaCreate
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.usuario_repository import IUsuarioRepository
from app.core.exceptions import NotFoundException


class CrearAsignaturaUseCase:
    """Encapsula la lógica para crear una asignatura."""

    def __init__(self, asignatura_repository: IAsignaturaRepository,
                 usuario_repository: IUsuarioRepository):
        self.asignatura_repository = asignatura_repository
        self.usuario_repository = usuario_repository

    async def execute(self, asignatura_create: AsignaturaCreate) -> Asignatura:
        """
        Ejecuta el caso de uso.

        Verifica que el docente (usuario) exista.
        """
        # 1. Verificar que el docente exista
        docente = await self.usuario_repository.get_by_id(asignatura_create.id_docente)
        if not docente:
            raise NotFoundException("Usuario (Docente)", asignatura_create.id_docente)

        # 2. Crear la asignatura
        nueva_asignatura = await self.asignatura_repository.create(asignatura_create)
        return nueva_asignatura
