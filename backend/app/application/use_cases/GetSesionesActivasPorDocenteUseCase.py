from typing import List, Tuple
from app.domain.entities.sesion_de_clase import SesionDeClase
from app.domain.entities.clase_programada import ClaseProgramada
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository


class GetSesionesActivasPorDocenteUseCase:
    """
    Clase que encapsula la lógica para obtener las sesiones de clase activas de un docente.
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

    async def execute(self, docente_id: int) -> List[Tuple[SesionDeClase, ClaseProgramada]]:
        """
        Ejecuta la lógica para obtener las sesiones activas de un docente.

        1. Obtiene todas las asignaturas del docente.
        2. Extrae los IDs de esas asignaturas.
        3. Busca todas las sesiones activas asociadas a esos IDs de asignatura.
        4. Para cada sesión, obtiene la clase programada asociada.
        """

        # 1. Obtener todas las asignaturas del docente
        asignaturas_docente = await self.asignatura_repo.list_by_docente(docente_id)
        if not asignaturas_docente:
            return []  # Si el docente no tiene asignaturas, no hay sesiones activas.

        # 2. Extraer los IDs de esas asignaturas
        id_asignaturas = [asignatura.id for asignatura in asignaturas_docente]

        # 3. Buscar todas las sesiones activas asociadas a esos IDs de asignatura
        sesiones_activas = await self.sesion_repo.find_active_by_asignaturas(id_asignaturas)

        # 4. Para cada sesión, obtener la clase programada asociada
        result = []
        for sesion in sesiones_activas:
            clase_programada = await self.clase_programada_repo.get_by_asignatura_and_horario(
                sesion.id_clase, sesion.id_horario
            )
            if clase_programada: # Ensure clase_programada is found
                result.append((sesion, clase_programada))
        
        return result
