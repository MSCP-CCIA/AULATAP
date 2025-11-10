"""
Implementación Concreta del Repositorio de Clases Programadas usando SQLAlchemy.
"""

import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.clase_programada import ClaseProgramada, ClaseProgramadaCreate
from app.domain.repositories.clase_programada_repository import IClaseProgramadaRepository
from app.infrastructure.persistence.models.clase_programada import ClaseProgramada as ClaseProgramadaModel

class ClaseProgramadaRepositoryImpl(IClaseProgramadaRepository):
    """Implementación de IClaseProgramadaRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, clase_programada_create: ClaseProgramadaCreate) -> ClaseProgramada:
        """Crea una nueva clase programada."""
        db_clase_programada = ClaseProgramadaModel(
            id_clase=clase_programada_create.id_clase,
            id_horario=clase_programada_create.id_horario
        )
        self.session.add(db_clase_programada)
        await self.session.flush()
        # No se puede hacer refresh en un objeto sin clave primaria simple.
        # Construimos el objeto de dominio manualmente.
        return ClaseProgramada(
            id_clase=db_clase_programada.id_clase,
            id_horario=db_clase_programada.id_horario
        )

    async def get_by_asignatura_and_horario(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID) -> Optional[ClaseProgramada]:
        """Obtiene una clase programada por ID de asignatura y horario."""
        stmt = select(ClaseProgramadaModel).where(
            ClaseProgramadaModel.id_clase == id_asignatura,
            ClaseProgramadaModel.id_horario == id_horario
        )
        result = await self.session.execute(stmt)
        db_clase_programada = result.scalars().first()
        return ClaseProgramada.model_validate(db_clase_programada) if db_clase_programada else None
