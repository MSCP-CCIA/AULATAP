"""
Caso de Uso: Cerrar una Sesión de Clase.
"""

from datetime import datetime
from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseUpdate, EstadoSesion
from app.domain.entities.clase_programada import ClaseProgramada # New import
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository
from app.core.exceptions import NotFoundException, ForbiddenException, ValidationException


class CerrarSesionUseCase:
    """
    Clase que encapsula la lógica para cerrar una sesión de clase.
    """

    def __init__(self,
                 sesion_repo: ISesionDeClaseRepository,
                 asignatura_repo: IAsignaturaRepository,
                 clase_programada_repo: IClaseProgramadaRepository):
        """
        Inicializa el caso de uso con sus dependencias (inyectadas).
        """
        self.sesion_repo = sesion_repo
        self.asignatura_repo = asignatura_repo
        self.clase_programada_repo = clase_programada_repo

    async def execute(self, sesion_id: int, docente_id: int) -> tuple[SesionDeClase, ClaseProgramada]:
        """
        Ejecuta la lógica para cerrar una sesión de clase.

        1. Obtiene la sesión por su ID.
        2. Verifica que la sesión exista y esté "EnProgreso".
        3. Verifica que el docente autenticado sea el dueño de la asignatura asociada a la sesión.
        4. Actualiza el estado de la sesión a "Cerrada" y establece la hora de fin.
        5. Devuelve la sesión cerrada junto con la clase programada asociada.
        """

        # 1. Obtener la sesión
        sesion = await self.sesion_repo.get_by_id(sesion_id)
        if not sesion:
            raise NotFoundException(resource="SesionDeClase", identifier=sesion_id)

        # 2. Verificar que la sesión esté "EnProgreso"
        if sesion.estado != EstadoSesion.EN_PROGRESO:
            raise ValidationException(detail=f"La sesión {sesion_id} no está en progreso. Estado actual: {sesion.estado.value}")

        # 3. Verificar que el docente sea dueño de la asignatura asociada a la sesión
        # Necesitamos obtener la clase programada para obtener el id_asignatura
        clase_programada = await self.clase_programada_repo.get_by_asignatura_and_horario(
            sesion.id_clase, sesion.id_horario
        )
        if not clase_programada:
            # Esto no debería pasar si la sesión existe y es válida, pero es una buena verificación.
            raise NotFoundException(resource="ClaseProgramada", identifier=f"Asignatura ID: {sesion.id_clase}, Horario ID: {sesion.id_horario}")

        owns_asignatura = await self.asignatura_repo.docente_owns_asignatura(docente_id, clase_programada.id_clase)
        if not owns_asignatura:
            raise ForbiddenException(detail="El docente no tiene permiso para cerrar esta sesión.")

        # 4. Actualizar la sesión a "Cerrada"
        sesion_update = SesionDeClaseUpdate(
            estado=EstadoSesion.CERRADA,
            hora_fin=datetime.utcnow()
        )
        sesion_cerrada = await self.sesion_repo.update(sesion_id, sesion_update)

        if not sesion_cerrada:
            # Esto solo ocurriría si la sesión desaparece entre get y update, lo cual es improbable.
            raise NotFoundException(resource="SesionDeClase", identifier=sesion_id)

        return sesion_cerrada, clase_programada