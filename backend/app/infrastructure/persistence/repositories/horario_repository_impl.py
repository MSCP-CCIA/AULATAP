"""
Implementación Concreta del Repositorio de Horarios usando SQLAlchemy.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.horario import Horario, HorarioCreate
from app.domain.repositories.horario_repository import IHorarioRepository
from app.infrastructure.persistence.models.horario import Horario as HorarioModel

class HorarioRepositoryImpl(IHorarioRepository):
    """Implementación de IHorarioRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, horario_id: int) -> Optional[Horario]:
        result = await self.session.get(HorarioModel, horario_id)
        return Horario.model_validate(result) if result else None

    async def create(self, horario_create: HorarioCreate) -> Horario:
        db_horario = HorarioModel(
            dia_semana=horario_create.dia_semana,
            hora_inicio=horario_create.hora_inicio,
            hora_fin=horario_create.hora_fin
        )
        self.session.add(db_horario)
        await self.session.flush()
        await self.session.refresh(db_horario)
        return Horario.model_validate(db_horario)

    async def list_all(self) -> List[Horario]:
        stmt = select(HorarioModel).order_by(HorarioModel.dia_semana, HorarioModel.hora_inicio)
        result = await self.session.execute(stmt)
        db_horarios = result.scalars().all()
        return [Horario.model_validate(h) for h in db_horarios]
