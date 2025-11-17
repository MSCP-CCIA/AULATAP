"""
Caso de Uso: Listar todos los Horarios.
"""

from typing import List
from app.domain.entities.horario import Horario
from app.domain.repositories.horario_repository import IHorarioRepository


class ListarHorariosUseCase:
    """
    Clase que encapsula la lógica para listar todos los horarios.
    """

    def __init__(self, horario_repository: IHorarioRepository):
        """
        Inicializa el caso de uso con sus dependencias (inyectadas).
        """
        self.horario_repository = horario_repository

    async def execute(self) -> List[Horario]:
        """
        Ejecuta la lógica del caso de uso para listar horarios.
        """
        return await self.horario_repository.list_all()
