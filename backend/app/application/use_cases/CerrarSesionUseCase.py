"""
Caso de Uso: Cerrar una Sesión de Clase activa.
"""
import uuid
from datetime import datetime
from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseUpdate, EstadoSesion
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.core.exceptions import NotFoundException, ValidationException, UnauthorizedException


class CerrarSesionUseCase:
    """Encapsula la lógica para cerrar una sesión."""

    def __init__(self,
                 sesion_repository: ISesionDeClaseRepository,
                 asignatura_repository: IAsignaturaRepository):
        self.sesion_repository = sesion_repository
        self.asignatura_repository = asignatura_repository

    async def execute(self, id_sesion: uuid.UUID, id_docente: uuid.UUID) -> SesionDeClase:
        """
        Ejecuta el caso de uso.

        1. Verifica que la sesión exista.
        2. Verifica que la sesión pertenezca al docente.
        3. Verifica que esté "EnProgreso".
        4. La cierra y actualiza la hora_fin.
        """

        # 1. Verificar sesión
        sesion = await self.sesion_repository.get_by_id(id_sesion)
        if not sesion:
            raise NotFoundException("Sesión", id_sesion)

        # 2. Verificar pertenencia
        asignatura = await self.asignatura_repository.get_by_id(sesion.id_clase)
        if not asignatura or asignatura.id_docente != id_docente:
            raise UnauthorizedException("El docente no tiene permisos para cerrar esta sesión.")

        # 3. Verificar estado
        if sesion.estado != EstadoSesion.EN_PROGRESO:
            raise ValidationException(
                f"La sesión no está 'EnProgreso'. Estado actual: {sesion.estado}",
                field="id_sesion"
            )

        # 4. Cerrar sesión
        update_data = SesionDeClaseUpdate(
            estado=EstadoSesion.CERRADA,
            hora_fin=datetime.utcnow()
        )
        sesion_cerrada = await self.sesion_repository.update(id_sesion, update_data)

        return sesion_cerrada
