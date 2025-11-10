"""
Caso de Uso: Inscribir un Estudiante en una Asignatura.
(Maneja la tabla pivote 'Inscripcion')
"""
import uuid
from app.domain.entities.inscripcion import Inscripcion, InscripcionCreate
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.domain.repositories.inscripcion_repository import IInscripcionRepository
from app.core.exceptions import NotFoundException, AlreadyExistsException


class InscribirEstudianteUseCase:
    """Encapsula la lógica para inscribir un estudiante."""

    def __init__(self,
                 asignatura_repository: IAsignaturaRepository,
                 estudiante_repository: IEstudianteRepository,
                 inscripcion_repository: IInscripcionRepository):
        self.asignatura_repository = asignatura_repository
        self.estudiante_repository = estudiante_repository
        self.inscripcion_repository = inscripcion_repository

    async def execute(self, id_asignatura: uuid.UUID, id_estudiante: uuid.UUID) -> Inscripcion:
        """
        Ejecuta el caso de uso.

        Verifica que ambos existan, que no haya una inscripción previa y luego la crea.
        """
        # 1. Verificar Asignatura
        asignatura = await self.asignatura_repository.get_by_id(id_asignatura)
        if not asignatura:
            raise NotFoundException("Asignatura", id_asignatura)

        # 2. Verificar Estudiante
        estudiante = await self.estudiante_repository.get_by_id(id_estudiante)
        if not estudiante:
            raise NotFoundException("Estudiante", id_estudiante)

        # 3. Verificar que no exista ya la inscripción
        inscripcion_existente = await self.inscripcion_repository.get_by_asignatura_and_estudiante(id_asignatura, id_estudiante)
        if inscripcion_existente:
            raise AlreadyExistsException("Inscripción", "combinación de asignatura y estudiante")

        # 4. Crear la inscripción
        inscripcion_create = InscripcionCreate(id_clase=id_asignatura, id_estudiante=id_estudiante)
        nueva_inscripcion = await self.inscripcion_repository.create(inscripcion_create)

        return nueva_inscripcion
