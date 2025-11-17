"""
Caso de Uso: Abrir una Sesión de Clase.
"""

from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseCreate
from app.domain.entities.clase_programada import ClaseProgramada # New import
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository
from app.core.exceptions import ForbiddenException, NotFoundException, ValidationException


class AbrirSesionUseCase:
    """
    Clase que encapsula la lógica para abrir una sesión de clase.
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

    async def execute(self, docente_id: int, id_asignatura: int, id_horario: int, tema: str | None = None) -> tuple[SesionDeClase, ClaseProgramada]:
        """
        Ejecuta la lógica para abrir una sesión de clase.

        1. Verifica que el docente sea dueño de la asignatura.
        2. Verifica que la clase esté programada en ese horario.
        3. Verifica que no haya una sesión activa para esa clase programada.
        4. Crea y devuelve la nueva sesión de clase junto con la clase programada.
        """

        # 1. Verificar que el docente sea dueño de la asignatura
        owns_asignatura = await self.asignatura_repo.docente_owns_asignatura(docente_id, id_asignatura)
        if not owns_asignatura:
            raise ForbiddenException(detail="El docente no es dueño de esta asignatura.")

        # 2. Verificar que la clase esté programada en ese horario
        clase_programada = await self.clase_programada_repo.get_by_asignatura_and_horario(id_asignatura, id_horario)
        if not clase_programada:
            raise NotFoundException(
                resource="ClaseProgramada",
                identifier=f"Asignatura ID: {id_asignatura}, Horario ID: {id_horario}"
            )

        # 3. Verificar que no haya una sesión activa para esa clase programada
        #    (Se asume que solo puede haber una sesión "EnProgreso" por clase programada a la vez)
        sesion_activa_existente = await self.sesion_repo.find_activa(id_asignatura, id_horario)
        if sesion_activa_existente:
            raise ValidationException(
                detail="Ya existe una sesión activa para esta clase programada.",
                field="id_asignatura, id_horario"
            )

        # 4. Crear la nueva sesión de clase
        sesion_create = SesionDeClaseCreate(
            id_clase=id_asignatura,
            id_horario=id_horario,
            tema=tema
        )
        nueva_sesion = await self.sesion_repo.create(sesion_create)

        return nueva_sesion, clase_programada