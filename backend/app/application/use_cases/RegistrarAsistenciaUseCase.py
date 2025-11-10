"""
Caso de Uso: Registrar Asistencia (El "Tap" del estudiante).

Esta es la lógica de negocio central de la aplicación.
"""
import uuid
from datetime import datetime, timedelta
from app.domain.entities.registro_asistencia import RegistroAsistencia, RegistroAsistenciaCreate, EstadoAsistencia
from app.domain.entities.sesion_de_clase import EstadoSesion
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.core.config import settings
from app.core.exceptions import NotFoundException, ValidationException


class RegistrarAsistenciaUseCase:
    """Encapsula la lógica del "tap" de asistencia."""

    def __init__(self,
                 asistencia_repo: IRegistroAsistenciaRepository,
                 sesion_repo: ISesionDeClaseRepository,
                 estudiante_repo: IEstudianteRepository,
                 asignatura_repo: IAsignaturaRepository):
        self.asistencia_repo = asistencia_repo
        self.sesion_repo = sesion_repo
        self.estudiante_repo = estudiante_repo
        self.asignatura_repo = asignatura_repo

    async def execute(self, rfc_uid_estudiante: str, id_sesion: uuid.UUID) -> RegistroAsistencia:
        """
        Ejecuta el caso de uso.

        1. Valida el estudiante por RFC/UID.
        2. Valida la sesión y que esté activa.
        3. Valida que el estudiante esté inscrito en la asignatura de esa sesión.
        4. Valida que no haya un registro previo (idempotencia).
        5. Calcula el estado (Presente, Tarde).
        6. Crea el registro de asistencia.
        """

        # 1. Validar estudiante
        estudiante = await self.estudiante_repo.get_by_rfc_uid(rfc_uid_estudiante)
        if not estudiante:
            raise NotFoundException("Estudiante", rfc_uid_estudiante)

        # 2. Validar sesión
        sesion = await self.sesion_repo.get_by_id(id_sesion)
        if not sesion:
            raise NotFoundException("Sesión", id_sesion)
        if sesion.estado != EstadoSesion.EN_PROGRESO:
            raise ValidationException(
                f"La sesión no está 'EnProgreso'. Estado actual: {sesion.estado}",
                field="id_sesion"
            )

        # 3. Validar inscripción
        esta_inscrito = await self.asignatura_repo.esta_estudiante_inscrito(
            id_asignatura=sesion.id_clase,
            id_estudiante=estudiante.id
        )
        if not esta_inscrito:
            raise ValidationException(
                "El estudiante no está inscrito en esta asignatura.",
                field="rfc_uid_estudiante"
            )

        # 4. Validar duplicados (Idempotencia)
        registro_previo = await self.asistencia_repo.get_by_sesion_and_estudiante(
            id_sesion=id_sesion,
            id_estudiante=estudiante.id
        )
        if registro_previo:
            # Ya registró. Simplemente retornamos el registro existente.
            return registro_previo

        # 5. Calcular estado (Presente o Tarde)
        hora_actual = datetime.utcnow()
        tolerancia = timedelta(minutes=settings.SESSION_LATE_TOLERANCE_MINUTES)

        if hora_actual > (sesion.hora_inicio + tolerancia):
            estado_asistencia = EstadoAsistencia.TARDE
        else:
            estado_asistencia = EstadoAsistencia.PRESENTE

        # 6. Crear registro
        registro_create = RegistroAsistenciaCreate(
            id_sesion_clase=id_sesion,
            id_estudiante=estudiante.id,
            estado_asistencia=estado_asistencia,
            hora_registro=hora_actual
        )
        nuevo_registro = await self.asistencia_repo.create(registro_create)

        return nuevo_registro
