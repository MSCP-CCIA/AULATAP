"""
Implementación Concreta del Repositorio de Asistencia usando SQLAlchemy.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.registro_asistencia import RegistroAsistencia, RegistroAsistenciaCreate, RegistroAsistenciaUpdate, EstadoAsistencia
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.infrastructure.persistence.models.registro_asistencia import RegistroAsistencia as AsistenciaModel


class RegistroAsistenciaRepositoryImpl(IRegistroAsistenciaRepository):
    """Implementación de IRegistroAsistenciaRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, registro_id: int) -> Optional[RegistroAsistencia]:
        result = await self.session.get(AsistenciaModel, registro_id)
        return RegistroAsistencia.model_validate(result) if result else None

    async def get_by_sesion_and_estudiante(self, sesion_id: int, estudiante_id: int) -> Optional[RegistroAsistencia]:
        stmt = select(AsistenciaModel).where(
            AsistenciaModel.id_sesion_clase == sesion_id,
            AsistenciaModel.id_estudiante == estudiante_id
        )
        result = await self.session.execute(stmt)
        db_registro = result.scalars().first()
        return RegistroAsistencia.model_validate(db_registro) if db_registro else None

    async def create(self, registro_create: RegistroAsistenciaCreate) -> RegistroAsistencia:
        db_registro = AsistenciaModel(
            id_sesion_clase=registro_create.id_sesion_clase,
            id_estudiante=registro_create.id_estudiante,
            hora_entrada=registro_create.hora_registro,
            estado_asistencia=registro_create.estado_asistencia
        )
        self.session.add(db_registro)
        await self.session.flush()
        await self.session.refresh(db_registro)
        return RegistroAsistencia.model_validate(db_registro)

    async def update(self, registro_id: int, registro_update: RegistroAsistenciaUpdate) -> Optional[RegistroAsistencia]:
        db_registro = await self.session.get(AsistenciaModel, registro_id)
        if not db_registro:
            return None

        update_data = registro_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_registro, key, value)

        await self.session.flush()
        await self.session.refresh(db_registro)
        return RegistroAsistencia.model_validate(db_registro)

    async def list_by_sesion(self, sesion_id: int) -> List[RegistroAsistencia]:
        stmt = select(AsistenciaModel).where(AsistenciaModel.id_sesion_clase == sesion_id)
        result = await self.session.execute(stmt)
        db_registros = result.scalars().all()
        return [RegistroAsistencia.model_validate(r) for r in db_registros]
