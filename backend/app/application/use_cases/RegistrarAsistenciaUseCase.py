"""
Caso de Uso: Registrar Asistencia (El "Tap" del estudiante).

Esta es la lógica de negocio central de la aplicación.
"""
from datetime import datetime, timedelta
from app.domain.entities.registro_asistencia import RegistroAsistencia, RegistroAsistenciaCreate, EstadoAsistencia
from app.domain.entities.sesion_de_clase import EstadoSesion
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.domain.repositories.inscripcion_repository import IInscripcionRepository
from app.core.config import settings
from app.core.exceptions import NotFoundException, ValidationException


class RegistrarAsistenciaUseCase:
    """Encapsula la lógica del "tap" de asistencia."""

    def __init__(self,
                 asistencia_repo: IRegistroAsistenciaRepository,
                 sesion_repo: ISesionDeClaseRepository,
                 estudiante_repo: IEstudianteRepository,
                 inscripcion_repo: IInscripcionRepository):
        self.asistencia_repo = asistencia_repo
        self.sesion_repo = sesion_repo
        self.estudiante_repo = estudiante_repo
        self.inscripcion_repo = inscripcion_repo

    async def execute(self, rfc_uid_estudiante: str) -> RegistroAsistencia:
        """
        Ejecuta el caso de uso.

        1. Buscar al estudiante por rfc_uid.
        2. Buscar en qué asignaturas está inscrito ese estudiante.
        3. Buscar si alguna de esas asignaturas tiene una SesionDeClase con estado="EnProgreso" ahora mismo.
        4. Si encuentra una (y solo una), crea el RegistroAsistencia (calculando si está "Presente" o "Tarde").
        5. Si no encuentra sesión, o encuentra múltiples, devuelve un error (ValidationException).
        """

        # 1. Buscar al estudiante por rfc_uid.
        estudiante = await self.estudiante_repo.get_by_rfc_uid(rfc_uid_estudiante)
        if not estudiante:
            raise NotFoundException(resource="Estudiante", identifier=rfc_uid_estudiante)

        # 2. Buscar en qué asignaturas está inscrito ese estudiante.
        inscripciones = await self.inscripcion_repo.list_by_estudiante(estudiante.id)
        if not inscripciones:
            raise ValidationException("El estudiante no está inscrito en ninguna asignatura.", field="rfc_uid_estudiante")

        id_asignaturas_inscritas = [i.id_clase for i in inscripciones]

        # 3. Buscar si alguna de esas asignaturas tiene una SesionDeClase con estado="EnProgreso"
        sesiones_activas = await self.sesion_repo.find_active_by_asignaturas(id_asignaturas_inscritas)

        # 4. Validar el número de sesiones activas
        if len(sesiones_activas) == 0:
            raise ValidationException("No hay ninguna sesión de clase en progreso para las asignaturas del estudiante.", field="rfc_uid_estudiante")
        if len(sesiones_activas) > 1:
            raise ValidationException("El estudiante está inscrito en múltiples asignaturas con sesiones activas simultáneamente.", field="rfc_uid_estudiante")

        sesion = sesiones_activas[0]

        # Validar duplicados (Idempotencia)
        registro_previo = await self.asistencia_repo.get_by_sesion_and_estudiante(
            sesion_id=sesion.id,
            estudiante_id=estudiante.id
        )
        if registro_previo:
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
            id_sesion_clase=sesion.id,
            id_estudiante=estudiante.id,
            estado_asistencia=estado_asistencia,
            hora_registro=hora_actual
        )
        nuevo_registro = await self.asistencia_repo.create(registro_create)

        return nuevo_registro
