from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.inscripcion_repository import IInscripcionRepository
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.domain.entities.sesion_de_clase import SesionDeClase, EstadoSesion, SesionDeClaseUpdate
from app.domain.entities.registro_asistencia import RegistroAsistencia, EstadoAsistencia, RegistroAsistenciaCreate
from app.core.exceptions import NotFoundException, ForbiddenException, ValidationException

class CerrarValidacionUseCase:
    def __init__(self,
                 sesion_de_clase_repository: ISesionDeClaseRepository,
                 inscripcion_repository: IInscripcionRepository,
                 registro_asistencia_repository: IRegistroAsistenciaRepository):
        self.sesion_de_clase_repository = sesion_de_clase_repository
        self.inscripcion_repository = inscripcion_repository
        self.registro_asistencia_repository = registro_asistencia_repository

    async def execute(self, id_sesion: int, id_docente: int) -> SesionDeClase:
        sesion = await self.sesion_de_clase_repository.get_by_id(id_sesion)
        if not sesion:
            raise NotFoundException("SesionDeClase", id_sesion)

        # Aquí también aplica el problema de la validación del docente. Se omite por ahora.

        if sesion.estado != EstadoSesion.VALIDACION_ABIERTA:
            raise ValidationException(f"La validación no está abierta. Estado actual: '{sesion.estado}'.")

        # 1. Cambiar estado de la sesión
        update_payload = SesionDeClaseUpdate(estado=EstadoSesion.VALIDACION_CERRADA)
        updated_sesion = await self.sesion_de_clase_repository.update(id_sesion, update_payload)
        if not updated_sesion:
            raise NotFoundException("SesionDeClase", id_sesion)

        # 2. Obtener todos los estudiantes inscritos en la asignatura
        id_asignatura = sesion.id_clase
        inscripciones = await self.inscripcion_repository.find_by_asignatura(id_asignatura)
        estudiantes_inscritos_ids = {insc.id_estudiante for insc in inscripciones}

        # 3. Obtener todos los estudiantes que SÍ registraron asistencia
        registros_presentes = await self.registro_asistencia_repository.list_by_sesion(id_sesion)
        estudiantes_presentes_ids = {reg.id_estudiante for reg in registros_presentes}

        # 4. Determinar estudiantes ausentes
        estudiantes_ausentes_ids = estudiantes_inscritos_ids - estudiantes_presentes_ids

        # 5. Crear registro de 'Ausente' para cada uno
        for id_estudiante in estudiantes_ausentes_ids:
            create_payload = RegistroAsistenciaCreate(
                id_sesion_clase=id_sesion,
                id_estudiante=id_estudiante,
                estado_asistencia=EstadoAsistencia.AUSENTE
            )
            await self.registro_asistencia_repository.create(create_payload)

        return updated_sesion
