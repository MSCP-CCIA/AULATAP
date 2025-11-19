"""
Implementación Concreta del Repositorio de Asistencia usando SQLAlchemy.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

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
        # Determine hora_entrada based on estado_asistencia and provided hora_registro
        if registro_create.estado_asistencia == EstadoAsistencia.AUSENTE:
            hora_entrada_to_set = None
        else:
            # If hora_registro is explicitly None but not AUSENTE, it's an error from the use case.
            # However, for current scenarios, it should either be a datetime or we default it.
            # Assuming if it's not AUSENTE, hora_registro should be valid.
            hora_entrada_to_set = registro_create.hora_registro
            if hora_entrada_to_set is None: # This should ideally be handled by schema defaults or validation
                 hora_entrada_to_set = datetime.utcnow()


        db_registro = AsistenciaModel(
            id_sesion_clase=registro_create.id_sesion_clase,
            id_estudiante=registro_create.id_estudiante,
            hora_entrada=hora_entrada_to_set, # Use the determined value
            estado_asistencia=registro_create.estado_asistencia
        )
        self.session.add(db_registro)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(db_registro)
        return RegistroAsistencia.model_validate(db_registro)

    async def update(self, registro_id: int, registro_update: RegistroAsistenciaUpdate) -> Optional[RegistroAsistencia]:
        db_registro = await self.session.get(AsistenciaModel, registro_id)
        if not db_registro:
            return None

        update_data = registro_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Special handling for hora_entrada if it needs to be explicitly set to None for AUSENTE
            # This logic should ideally come from the update_data itself if RegistroAsistenciaUpdate was extended
            # to include Optional[hora_entrada].
            if key == 'estado_asistencia' and value == EstadoAsistencia.AUSENTE:
                db_registro.hora_entrada = None
            else:
                setattr(db_registro, key, value)

        await self.session.flush()
        await self.session.refresh(db_registro)
        return RegistroAsistencia.model_validate(db_registro)

    async def list_by_sesion(self, sesion_id: int) -> List[RegistroAsistencia]:
        stmt = select(AsistenciaModel).where(AsistenciaModel.id_sesion_clase == sesion_id)
        result = await self.session.execute(stmt)
        db_registros = result.scalars().all()
        return [RegistroAsistencia.model_validate(r) for r in db_registros]
