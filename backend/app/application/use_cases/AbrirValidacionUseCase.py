from typing import Tuple
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository
from app.domain.entities.sesion_de_clase import SesionDeClase, EstadoSesion, SesionDeClaseUpdate
from app.domain.entities.clase_programada import ClaseProgramada
from app.core.exceptions import NotFoundException, ForbiddenException, ValidationException

class AbrirValidacionUseCase:
    def __init__(self,
                 sesion_de_clase_repository: ISesionDeClaseRepository,
                 asignatura_repo: IAsignaturaRepository,
                 clase_programada_repo: IClaseProgramadaRepository):
        self.sesion_de_clase_repository = sesion_de_clase_repository
        self.asignatura_repo = asignatura_repo
        self.clase_programada_repo = clase_programada_repo

    async def execute(self, id_sesion: int, id_docente: int) -> Tuple[SesionDeClase, ClaseProgramada]:
        sesion = await self.sesion_de_clase_repository.get_by_id(id_sesion)
        if not sesion:
            raise NotFoundException("SesionDeClase", id_sesion)

        clase_programada = await self.clase_programada_repo.get_by_asignatura_and_horario(
            sesion.id_clase, sesion.id_horario
        )
        if not clase_programada:
            raise NotFoundException(resource="ClaseProgramada", identifier=f"Asignatura ID: {sesion.id_clase}, Horario ID: {sesion.id_horario}")

        owns_asignatura = await self.asignatura_repo.docente_owns_asignatura(id_docente, clase_programada.id_clase)
        if not owns_asignatura:
            raise ForbiddenException(detail="El docente no tiene permiso para modificar esta sesión.")

        if sesion.estado != EstadoSesion.EN_PROGRESO:
            raise ValidationException(f"La sesión no está en estado '{EstadoSesion.EN_PROGRESO}'. Estado actual: '{sesion.estado.value}'.")

        update_payload = SesionDeClaseUpdate(estado=EstadoSesion.VALIDACION_ABIERTA)
        updated_sesion = await self.sesion_de_clase_repository.update(id_sesion, update_payload)
        
        if not updated_sesion:
             raise NotFoundException("SesionDeClase", id_sesion)

        return updated_sesion, clase_programada
