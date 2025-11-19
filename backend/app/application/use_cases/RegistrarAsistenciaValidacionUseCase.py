from datetime import datetime, timedelta
from typing import Tuple
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository
from app.domain.entities.registro_asistencia import RegistroAsistencia, EstadoAsistencia, RegistroAsistenciaUpdate, RegistroAsistenciaCreate
from app.domain.entities.sesion_de_clase import EstadoSesion, SesionDeClase
from app.domain.entities.clase_programada import ClaseProgramada
from app.domain.entities.estudiante import Estudiante
from app.core.exceptions import NotFoundException, ValidationException

class RegistrarAsistenciaValidacionUseCase:
    def __init__(self,
                 registro_asistencia_repository: IRegistroAsistenciaRepository,
                 sesion_de_clase_repository: ISesionDeClaseRepository,
                 estudiante_repository: IEstudianteRepository,
                 clase_programada_repository: IClaseProgramadaRepository):
        self.registro_asistencia_repository = registro_asistencia_repository
        self.sesion_de_clase_repository = sesion_de_clase_repository
        self.estudiante_repository = estudiante_repository
        self.clase_programada_repository = clase_programada_repository

    async def execute(self, id_sesion: int, codigo_rfid: str) -> Tuple[RegistroAsistencia, Estudiante, ClaseProgramada, SesionDeClase]:
        # 1. Verificar que la sesión esté en estado VALIDACION_ABIERTA
        sesion = await self.sesion_de_clase_repository.get_by_id(id_sesion)
        if not sesion:
            raise NotFoundException("Sesión de Clase", f"ID {id_sesion}")
        if sesion.estado != EstadoSesion.VALIDACION_ABIERTA:
            raise ValidationException(
                f"La sesión {id_sesion} no está en estado de validación abierta. Estado actual: {sesion.estado}"
            )

        # 2. Buscar estudiante por RFID
        estudiante = await self.estudiante_repository.get_by_rfc_uid(codigo_rfid)
        if not estudiante:
            raise NotFoundException("Estudiante", f"RFID {codigo_rfid}")

        # 3. Obtener la ClaseProgramada para obtener la Asignatura
        clase_programada = await self.clase_programada_repository.get_by_asignatura_and_horario(
            sesion.id_clase, sesion.id_horario
        )
        if not clase_programada:
            raise NotFoundException("Clase Programada", f"Asignatura ID {sesion.id_clase}, Horario ID {sesion.id_horario} para Sesión {id_sesion}")

        # 4. Obtener o crear el registro de asistencia del estudiante para esta sesión
        registro_asistencia = await self.registro_asistencia_repository.get_by_sesion_and_estudiante(id_sesion, estudiante.id)
        
        hora_actual = datetime.utcnow()
        estado_asistencia_actual = registro_asistencia.estado_asistencia if registro_asistencia else EstadoAsistencia.AUSENTE

        # Aplicar reglas de negocio para el estado
        if estado_asistencia_actual == EstadoAsistencia.PRESENTE:
            target_estado = EstadoAsistencia.PRESENTE
        elif estado_asistencia_actual == EstadoAsistencia.TARDE:
            target_estado = EstadoAsistencia.TARDE
        elif estado_asistencia_actual == EstadoAsistencia.AUSENTE:
            target_estado = EstadoAsistencia.TARDE
        else:
            raise ValidationException(f"Estado de asistencia desconocido: {estado_asistencia_actual}")

        if registro_asistencia:
            # Si el registro existe, actualizar su estado y hora_salida
            update_payload = RegistroAsistenciaUpdate(
                hora_salida=hora_actual,
                estado_asistencia=target_estado
            )
            updated_registro = await self.registro_asistencia_repository.update(registro_asistencia.id, update_payload)
        else:
            # Si no existe, crear uno. Asumimos que es un "tap" de entrada tardía o validación inicial
            create_payload = RegistroAsistenciaCreate(
                id_sesion_clase=id_sesion,
                id_estudiante=estudiante.id,
                hora_registro=hora_actual,  # Set hora_registro to current time
                estado_asistencia=target_estado  # Set initial state based on rules
            )
            updated_registro = await self.registro_asistencia_repository.create(create_payload)
        
        return updated_registro, estudiante, clase_programada, sesion
