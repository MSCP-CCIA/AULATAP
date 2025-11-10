"""
Caso de Uso: Crear un nuevo Estudiante.
"""
from app.domain.entities.estudiante import Estudiante, EstudianteCreate
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.core.exceptions import AlreadyExistsException


class CrearEstudianteUseCase:
    """Encapsula la lógica para crear un estudiante."""

    def __init__(self, estudiante_repository: IEstudianteRepository):
        self.estudiante_repository = estudiante_repository

    async def execute(self, estudiante_create: EstudianteCreate) -> Estudiante:
        """
        Ejecuta el caso de uso.

        Verifica que el email y el rfc_uid no existan.
        """
        # 1. Verificar email
        existing = await self.estudiante_repository.get_by_email(estudiante_create.email)
        if existing:
            raise AlreadyExistsException("Estudiante", "email", estudiante_create.email)

        # 2. Verificar RFC/UID
        existing = await self.estudiante_repository.get_by_rfc_uid(estudiante_create.rfc_uid)
        if existing:
            raise AlreadyExistsException("Estudiante", "rfc_uid", estudiante_create.rfc_uid)

        # 3. Crear estudiante
        nuevo_estudiante = await self.estudiante_repository.create(estudiante_create)
        return nuevo_estudiante
