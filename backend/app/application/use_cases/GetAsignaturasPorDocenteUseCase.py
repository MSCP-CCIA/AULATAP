"""
Caso de Uso: Obtener Asignaturas por Docente.
"""

from typing import List
from app.domain.entities.asignatura import Asignatura
from app.domain.repositories.asignatura_repository import IAsignaturaRepository


class GetAsignaturasPorDocenteUseCase:
    """
    Clase que encapsula la lógica para obtener las asignaturas de un docente.
    """

    def __init__(self, asignatura_repository: IAsignaturaRepository):
        """
        Inicializa el caso de uso con sus dependencias (inyectadas).
        """
        self.asignatura_repository = asignatura_repository

    async def execute(self, docente_id: int) -> List[Asignatura]:
        """
        Ejecuta la lógica del caso de uso para listar asignaturas por docente.
        """
        return await self.asignatura_repository.list_by_docente(docente_id)
