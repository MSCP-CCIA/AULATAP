"""
Caso de Uso: Abrir una nueva Sesión de Clase.
"""
import uuid
from datetime import datetime
from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseCreate, EstadoSesion
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.core.exceptions import NotFoundException, ValidationException, UnauthorizedException


class AbrirSesionUseCase:
    """Encapsula la lógica para abrir una sesión."""

    def __init__(self,
                 sesion_repository: ISesionDeClaseRepository,
                 asignatura_repository: IAsignaturaRepository):
        self.sesion_repository = sesion_repository
        self.asignatura_repository = asignatura_repository

    async def execute(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID, id_docente: uuid.UUID, tema: str | None) -> SesionDeClase:
        """
        Ejecuta el caso de uso.

        1. Verifica que la asignatura exista y pertenezca al docente.
        2. Verifica que la asignatura esté programada en ese horario.
        3. Verifica que no haya otra sesión activa para esa clase/horario.
        4. Crea y retorna la nueva sesión.
        """

        # 1. Verificar Asignatura y pertenencia
        asignatura = await self.asignatura_repository.get_by_id(id_asignatura)
        if not asignatura:
            raise NotFoundException("Asignatura", id_asignatura)
        if asignatura.id_docente != id_docente:
            raise UnauthorizedException("El docente no tiene permisos sobre esta asignatura.")

        # 2. Verifica que la asignatura esté programada en ese horario.
        programada = await self.asignatura_repository.existe_clase_programada(id_asignatura, id_horario)
        if not programada:
            raise ValidationException(f"La asignatura '{asignatura.nombre_materia}' no está programada en el horario especificado.",
                                      field="id_horario")

        # 3. Verificar si ya hay una sesión activa
        sesion_activa = await self.sesion_repository.find_activa(
            id_clase=id_asignatura,
            id_horario=id_horario
        )
        if sesion_activa:
            raise ValidationException(
                f"Ya existe una sesión activa (ID: {sesion_activa.id}) para esta clase.",
                field="id_clase_programada"
            )

        # 4. Crear la sesión
        sesion_create = SesionDeClaseCreate(
            id_clase=id_asignatura,
            id_horario=id_horario,
            tema=tema
        )
        nueva_sesion = await self.sesion_repository.create(sesion_create)

        return nueva_sesion
