"""
Caso de Uso: Programar una Asignatura en un Horario.
(Maneja la tabla pivote 'ClaseProgramada')
"""
import uuid
from app.domain.entities.clase_programada import ClaseProgramada, ClaseProgramadaCreate
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.horario_repository import IHorarioRepository
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository
from app.core.exceptions import NotFoundException, AlreadyExistsException


class ProgramarClaseUseCase:
    """Encapsula la lógica para programar una clase."""

    def __init__(self,
                 asignatura_repository: IAsignaturaRepository,
                 horario_repository: IHorarioRepository,
                 clase_programada_repository: IClaseProgramadaRepository):
        self.asignatura_repository = asignatura_repository
        self.horario_repository = horario_repository
        self.clase_programada_repository = clase_programada_repository

    async def execute(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID) -> ClaseProgramada:
        """
        Ejecuta el caso de uso.

        Verifica que ambos existan, que no haya una programación previa y luego la crea.
        """
        # 1. Verificar Asignatura
        asignatura = await self.asignatura_repository.get_by_id(id_asignatura)
        if not asignatura:
            raise NotFoundException("Asignatura", id_asignatura)

        # 2. Verificar Horario
        horario = await self.horario_repository.get_by_id(id_horario)
        if not horario:
            raise NotFoundException("Horario", id_horario)

        # 3. Verificar que no exista ya la programación
        clase_programada_existente = await self.clase_programada_repository.get_by_asignatura_and_horario(id_asignatura, id_horario)
        if clase_programada_existente:
            raise AlreadyExistsException("ClaseProgramada", "combinación de asignatura y horario")

        # 4. Crear la programación
        clase_programada_create = ClaseProgramadaCreate(id_clase=id_asignatura, id_horario=id_horario)
        nueva_clase_programada = await self.clase_programada_repository.create(clase_programada_create)

        return nueva_clase_programada
