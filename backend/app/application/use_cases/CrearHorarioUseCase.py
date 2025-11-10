"""
Caso de Uso: Crear un nuevo Horario.
"""
from app.domain.entities.horario import Horario, HorarioCreate
from app.domain.repositories.horario_repository import IHorarioRepository


class CrearHorarioUseCase:
    """Encapsula la lógica para crear un horario."""

    def __init__(self, horario_repository: IHorarioRepository):
        self.horario_repository = horario_repository

    async def execute(self, horario_create: HorarioCreate) -> Horario:
        """
        Ejecuta el caso de uso.

        La validación de horas (fin > inicio) ocurre en el DTO.
        """
        nuevo_horario = await self.horario_repository.create(horario_create)
        return nuevo_horario
