"""
Implementación Concreta del Repositorio de Asistencia usando SQLAlchemy.
"""

from typing import Optional, List
import uuid
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.domain.entities.registro_asistencia import RegistroAsistencia, RegistroAsistenciaCreate, EstadoAsistencia
from app.domain.repositories.registro_asistencia_repository import IRegistroAsistenciaRepository
from app.infrastructure.persistence.models.registro_asistencia import RegistroAsistencia as AsistenciaModel


class RegistroAsistenciaRepositoryImpl(IRegistroAsistenciaRepository):
    """Implementación de IRegistroAsistenciaRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_sesion_and_estudiante(self, sesion_id: uuid.UUID, estudiante_id: uuid.UUID) -> Optional[
        RegistroAsistencia]:
        stmt = select(AsistenciaModel).where(
            AsistenciaModel.id_sesion_clase == sesion_id,
            AsistenciaModel.id_estudiante == estudiante_id
        )
        result = await self.session.execute(stmt)
        db_registro = result.scalars().first()
        return RegistroAsistencia.model_validate(db_registro) if db_registro else None

    async def create_or_update_tap(self, registro_data: RegistroAsistenciaCreate) -> RegistroAsistencia:
        """
        Usa un 'UPSERT' de PostgreSQL para ser idempotente.
        Si el estudiante ya 'tapeó', no hace nada.
        Si el estudiante estaba 'Ausente' (creado por el sistema), actualiza su estado.
        """

        # Datos a insertar
        insert_data = {
            "id_sesion_clase": registro_data.id_sesion_clase,
            "id_estudiante": registro_data.id_estudiante,
            "hora_entrada": registro_data.hora_entrada,
            "estado_asistencia": EstadoAsistencia.PRESENTE  # Asumimos 'Presente' en el tap
        }

        # Declaración de 'INSERT ... ON CONFLICT'
        stmt = pg_insert(AsistenciaModel).values(**insert_data)

        # Qué hacer en conflicto (misma sesion + estudiante)
        # 'DO UPDATE' solo si el estado actual es 'Ausente'.
        # Si ya era 'Presente' o 'Tarde', no lo sobrescribe.
        stmt = stmt.on_conflict_do_update(
            index_elements=["id_sesion_clase", "id_estudiante"],
            set_={
                "hora_entrada": stmt.excluded.hora_entrada,
                "estado_asistencia": stmt.excluded.estado_asistencia
            },
            where=(AsistenciaModel.estado_asistencia == EstadoAsistencia.AUSENTE)
        )

        # Ejecutar y retornar el registro insertado/actualizado
        result = await self.session.execute(stmt.returning(AsistenciaModel))
        await self.session.flush()

        db_registro = result.scalars().first()

        # Si 'first()' es None, significa que hubo conflicto pero el 'WHERE'
        # (estado == AUSENTE) no se cumplió, así que no se actualizó nada.
        # En ese caso, solo cargamos el registro existente.
        if db_registro:
            return RegistroAsistencia.model_validate(db_registro)
        else:
            return await self.get_by_sesion_and_estudiante(
                registro_data.id_sesion_clase,
                registro_data.id_estudiante
            )

    async def list_by_sesion(self, sesion_id: uuid.UUID) -> List[RegistroAsistencia]:
        stmt = select(AsistenciaModel).where(AsistenciaModel.id_sesion_clase == sesion_id)
        result = await self.session.execute(stmt)
        db_registros = result.scalars().all()
        return [RegistroAsistencia.model_validate(r) for r in db_registros]
