"""
Implementación Concreta del Repositorio de Asignaturas usando SQLAlchemy.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import exists

from app.domain.entities.asignatura import Asignatura, AsignaturaCreate
from app.domain.repositories.asignatura_repository import IAsignaturaRepository
from app.infrastructure.persistence.models.asignatura import Asignatura as AsignaturaModel
from app.infrastructure.persistence.models.inscripcion import Inscripcion as InscripcionModel
from app.infrastructure.persistence.models.clase_programada import ClaseProgramada as ClaseProgramadaModel

class AsignaturaRepositoryImpl(IAsignaturaRepository):
    """Implementación de IAsignaturaRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, asignatura_id: int) -> Optional[Asignatura]:
        result = await self.session.get(AsignaturaModel, asignatura_id)
        return Asignatura.model_validate(result) if result else None

    async def list_by_docente(self, docente_id: int) -> List[Asignatura]:
        stmt = select(AsignaturaModel).where(AsignaturaModel.id_docente == docente_id).order_by(AsignaturaModel.nombre_materia)
        result = await self.session.execute(stmt)
        db_asignaturas = result.scalars().all()
        return [Asignatura.model_validate(a) for a in db_asignaturas]

    async def create(self, asignatura_create: AsignaturaCreate) -> Asignatura:
        db_asignatura = AsignaturaModel(
            nombre_materia=asignatura_create.nombre_materia,
            grupo=asignatura_create.grupo,
            id_docente=asignatura_create.id_docente
        )
        self.session.add(db_asignatura)
        await self.session.flush()
        await self.session.refresh(db_asignatura)
        return Asignatura.model_validate(db_asignatura)

    async def esta_estudiante_inscrito(self, id_asignatura: int, id_estudiante: int) -> bool:
        """Verifica si un estudiante está inscrito en una asignatura."""
        stmt = select(exists().where(
            InscripcionModel.id_clase == id_asignatura,
            InscripcionModel.id_estudiante == id_estudiante
        ))
        result = await self.session.execute(stmt)
        return result.scalar() is True

    async def existe_clase_programada(self, id_asignatura: int, id_horario: int) -> bool:
        """Verifica si una asignatura está programada en un horario."""
        stmt = select(exists().where(
            ClaseProgramadaModel.id_clase == id_asignatura,
            ClaseProgramadaModel.id_horario == id_horario
        ))
        result = await self.session.execute(stmt)
        return result.scalar() is True

    async def docente_owns_asignatura(self, docente_id: int, asignatura_id: int) -> bool:
        """Verifica si un docente es dueño de una asignatura."""
        stmt = select(exists().where(
            AsignaturaModel.id == asignatura_id,
            AsignaturaModel.id_docente == docente_id
        ))
        result = await self.session.execute(stmt)
        return result.scalar() is True
