from datetime import datetime, timedelta
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.domain.repositories.inscripcion_repository import IInscripcionRepository
from app.domain.entities.registro_asistencia import RegistroAsistencia, EstadoAsistencia, RegistroAsistenciaCreate
from app.domain.entities.sesion_de_clase import EstadoSesion
from app.core.exceptions import NotFoundException, ValidationException

class RegistrarAsistenciaUseCase:
    def __init__(self,
                 registro_asistencia_repository: IRegistroAsistenciaRepository,
                 sesion_de_clase_repository: ISesionDeClaseRepository,
                 estudiante_repository: IEstudianteRepository,
                 inscripcion_repository: IInscripcionRepository):
        self.registro_asistencia_repository = registro_asistencia_repository
        self.sesion_de_clase_repository = sesion_de_clase_repository
        self.estudiante_repository = estudiante_repository
        self.inscripcion_repository = inscripcion_repository

    async def execute(self, codigo_rfid: str) -> RegistroAsistencia:
        # 1. Buscar estudiante por RFID
        estudiante = await self.estudiante_repository.get_by_rfc_uid(codigo_rfid)
        if not estudiante:
            raise NotFoundException("Estudiante", f"RFID {codigo_rfid}")

        # 2. Buscar inscripciones del estudiante para encontrar sus asignaturas
        inscripciones = await self.inscripcion_repository.list_by_estudiante(estudiante.id)
        if not inscripciones:
            raise ValidationException("El estudiante no está inscrito en ninguna asignatura.")

        # 3. Encontrar la sesión única en progreso para las asignaturas del estudiante
        ids_asignaturas = [inscripcion.id_clase for inscripcion in inscripciones]
        sesiones_activas = await self.sesion_de_clase_repository.find_active_by_asignaturas(ids_asignaturas)

        sesiones_en_progreso = [s for s in sesiones_activas if s.estado == EstadoSesion.EN_PROGRESO]

        if not sesiones_en_progreso:
            raise ValidationException("No hay ninguna sesión de clase en progreso para este estudiante.")

        if len(sesiones_en_progreso) > 1:
            raise ValidationException("Hay múltiples sesiones en progreso para este estudiante. No se puede determinar la sesión.")

        sesion = sesiones_en_progreso[0]
        id_sesion = sesion.id

        # 4. Verificar que el estudiante no haya registrado asistencia previamente en esta sesión
        existing_registro = await self.registro_asistencia_repository.get_by_sesion_and_estudiante(id_sesion, estudiante.id)
        if existing_registro:
            raise ValidationException("El estudiante ya tiene un registro de asistencia para esta sesión.")

        # 5. Determinar estado de asistencia (Presente o Tarde)
        hora_actual = datetime.utcnow()
        limite_tardanza = sesion.hora_inicio + timedelta(minutes=15)
        estado = EstadoAsistencia.PRESENTE if hora_actual <= limite_tardanza else EstadoAsistencia.TARDE

        # 6. Crear y guardar el registro de asistencia
        create_payload = RegistroAsistenciaCreate(
            id_sesion_clase=id_sesion,
            id_estudiante=estudiante.id,
            hora_registro=hora_actual,
            estado_asistencia=estado
        )
        
        return await self.registro_asistencia_repository.create(create_payload)