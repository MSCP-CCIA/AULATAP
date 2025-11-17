"""
Implementación Concreta del Repositorio de Inscripciones usando SQLAlchemy.
"""

from datetime import date
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.inscripcion import Inscripcion, InscripcionCreate
from app.domain.repositories.inscripcion_repository import IInscripcionRepository
from app.infrastructure.persistence.models.inscripcion import Inscripcion as InscripcionModel


class InscripcionRepositoryImpl(IInscripcionRepository):
    """Implementación de IInscripcionRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, inscripcion_create: InscripcionCreate) -> Inscripcion:
        """Crea una nueva inscripción."""
        db_inscripcion = InscripcionModel(
            id_clase=inscripcion_create.id_clase,
            id_estudiante=inscripcion_create.id_estudiante,
            fecha_inscripcion=date.today()
        )
        self.session.add(db_inscripcion)
        await self.session.flush()
        # No se puede hacer refresh en un objeto sin clave primaria simple.
        # Construimos el objeto de dominio manualmente.
        return Inscripcion(
            id_clase=db_inscripcion.id_clase,
            id_estudiante=db_inscripcion.id_estudiante,
            fecha_inscripcion=db_inscripcion.fecha_inscripcion
        )

    async def get_by_asignatura_and_estudiante(self, id_asignatura: int, id_estudiante: int) -> Optional[Inscripcion]:
        """Obtiene una inscripción por ID de asignatura y estudiante."""
        stmt = select(InscripcionModel).where(
            InscripcionModel.id_clase == id_asignatura,
            InscripcionModel.id_estudiante == id_estudiante
        )
        result = await self.session.execute(stmt)
        db_inscripcion = result.scalars().first()
        return Inscripcion.model_validate(db_inscripcion) if db_inscripcion else None

    async def list_by_estudiante(self, id_estudiante: int) -> List[Inscripcion]:
        """Lista todas las inscripciones de un estudiante."""
        stmt = select(InscripcionModel).where(InscripcionModel.id_estudiante == id_estudiante)
        result = await self.session.execute(stmt)
        db_inscripciones = result.scalars().all()
        return [Inscripcion.model_validate(i) for i in db_inscripciones]

    async def find_by_asignatura(self, id_asignatura: int) -> List[Inscripcion]:
        """Busca todas las inscripciones para una asignatura."""
        stmt = select(InscripcionModel).where(InscripcionModel.id_clase == id_asignatura)
        result = await self.session.execute(stmt)
        db_inscripciones = result.scalars().all()
        return [Inscripcion.model_validate(i) for i in db_inscripciones]
