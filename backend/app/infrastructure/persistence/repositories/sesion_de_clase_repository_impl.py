"""
Implementación Concreta del Repositorio de Sesiones usando SQLAlchemy.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sesion_de_clase import SesionDeClase, SesionDeClaseCreate, SesionDeClaseUpdate, EstadoSesion
from app.domain.repositories.sesion_de_clase_repository import ISesionDeClaseRepository
from app.infrastructure.persistence.models.sesion_de_clase import SesionDeClase as SesionModel


class SesionDeClaseRepositoryImpl(ISesionDeClaseRepository):
    """Implementación de ISesionDeClaseRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, sesion_id: int) -> Optional[SesionDeClase]:
        result = await self.session.get(SesionModel, sesion_id)
        return SesionDeClase.model_validate(result) if result else None

    async def find_activa(self, id_clase: int, id_horario: int) -> Optional[SesionDeClase]:
        stmt = select(SesionModel).where(
            SesionModel.id_clase == id_clase,
            SesionModel.id_horario == id_horario,
            SesionModel.estado == EstadoSesion.EN_PROGRESO
        )
        result = await self.session.execute(stmt)
        db_sesion = result.scalars().first()
        return SesionDeClase.model_validate(db_sesion) if db_sesion else None

    async def find_active_by_asignaturas(self, id_asignaturas: List[int]) -> List[SesionDeClase]:
        """Busca sesiones activas para una lista de asignaturas."""
        stmt = select(SesionModel).where(
            SesionModel.id_clase.in_(id_asignaturas),
            SesionModel.estado == EstadoSesion.EN_PROGRESO
        )
        result = await self.session.execute(stmt)
        db_sesiones = result.scalars().all()
        return [SesionDeClase.model_validate(s) for s in db_sesiones]

    async def create(self, sesion_create: SesionDeClaseCreate) -> SesionDeClase:
        db_sesion = SesionModel(
            id_clase=sesion_create.id_clase,
            id_horario=sesion_create.id_horario,
            hora_inicio=datetime.utcnow(),
            estado=EstadoSesion.EN_PROGRESO,
            tema=sesion_create.tema
        )
        self.session.add(db_sesion)
        await self.session.flush()
        await self.session.refresh(db_sesion)
        return SesionDeClase.model_validate(db_sesion)

    async def update(self, sesion_id: int, sesion_update: SesionDeClaseUpdate) -> Optional[SesionDeClase]:
        db_sesion = await self.session.get(SesionModel, sesion_id)
        if not db_sesion:
            return None

        update_data = sesion_update.model_dump(exclude_unset=True)
        if 'hora_fin' not in update_data and sesion_update.estado == EstadoSesion.CERRADA:
            update_data['hora_fin'] = datetime.utcnow()

        for key, value in update_data.items():
            setattr(db_sesion, key, value)

        await self.session.flush()
        await self.session.refresh(db_sesion)
        return SesionDeClase.model_validate(db_sesion)
