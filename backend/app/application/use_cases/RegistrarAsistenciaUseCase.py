from datetime import datetime, timedelta
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.domain.repositories.inscripcion_repository import IInscripcionRepository
from app.domain.entities.registro_asistencia import RegistroAsistencia, EstadoAsistencia, RegistroAsistenciaCreate
from app.core.exceptions import NotFoundException, ValidationException

class RegistrarAsistenciaUseCase:
    def __init__(self,
                 sesion_de_clase_repository: ISesionDeClaseRepository,
                 registro_asistencia_repository: IRegistroAsistenciaRepository,
                 estudiante_repository: IEstudianteRepository,
                 inscripcion_repository: IInscripcionRepository):
        self.sesion_de_clase_repository = sesion_de_clase_repository
        self.registro_asistencia_repository = registro_asistencia_repository
        self.estudiante_repository = estudiante_repository
        self.inscripcion_repository = inscripcion_repository

    async def execute(self, id_sesion: int, codigo_rfid: str) -> RegistroAsistencia:
        sesion = await self.sesion_de_clase_repository.get_by_id(id_sesion)
        if not sesion:
            raise NotFoundException("SesionDeClase", id_sesion)

        if sesion.estado != "ValidacionAbierta":
            raise ValidationException("La validación de asistencia no está abierta para esta sesión.")

        estudiante = await self.estudiante_repository.find_by_rfid(codigo_rfid)
        if not estudiante:
            raise NotFoundException("Estudiante", f"RFID {codigo_rfid}")

        # Similar al caso de uso anterior, `sesion.clase_programada` no existe en el modelo de dominio.
        # Se necesita un método en el repositorio para obtener el id_asignatura de la sesión.
        # Asumimos que `sesion.id_clase` corresponde a `id_asignatura`.
        id_asignatura = sesion.id_clase 
        
        inscripcion = await self.inscripcion_repository.find_by_estudiante_and_asignatura(estudiante.id, id_asignatura)
        if not inscripcion:
            raise ValidationException(f"El estudiante no está inscrito en la asignatura de esta clase.")

        existing_registro = await self.registro_asistencia_repository.find_by_sesion_and_estudiante(id_sesion, estudiante.id)
        if existing_registro:
            raise ValidationException("El estudiante ya tiene un registro de asistencia para esta sesión.")

        hora_actual = datetime.utcnow()
        limite_tardanza = sesion.hora_inicio + timedelta(minutes=15)
        estado = EstadoAsistencia.PRESENTE if hora_actual <= limite_tardanza else EstadoAsistencia.TARDE

        create_payload = RegistroAsistenciaCreate(
            id_sesion_clase=id_sesion,
            id_estudiante=estudiante.id,
            hora_registro=hora_actual,
            estado_asistencia=estado
        )
        
        return await self.registro_asistencia_repository.create(create_payload) 