"""
Implementación Concreta del Repositorio de Estudiantes usando SQLAlchemy.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.estudiante import Estudiante, EstudianteCreate
from app.domain.repositories.estudiante_repository import IEstudianteRepository
from app.infrastructure.persistence.models.estudiante import Estudiante as EstudianteModel

class EstudianteRepositoryImpl(IEstudianteRepository):
    """Implementación de IEstudianteRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, estudiante_id: int) -> Optional[Estudiante]:
        result = await self.session.get(EstudianteModel, estudiante_id)
        return Estudiante.model_validate(result) if result else None

    async def get_by_rfc_uid(self, rfc_uid: str) -> Optional[Estudiante]:
        stmt = select(EstudianteModel).where(EstudianteModel.rfc_uid == rfc_uid)
        result = await self.session.execute(stmt)
        db_estudiante = result.scalars().first()
        return Estudiante.model_validate(db_estudiante) if db_estudiante else None

    async def get_by_email(self, email: str) -> Optional[Estudiante]:
        stmt = select(EstudianteModel).where(EstudianteModel.email == email)
        result = await self.session.execute(stmt)
        db_estudiante = result.scalars().first()
        return Estudiante.model_validate(db_estudiante) if db_estudiante else None

    async def create(self, estudiante_create: EstudianteCreate) -> Estudiante:
        db_estudiante = EstudianteModel(
            email=estudiante_create.email,
            nombre_completo=estudiante_create.nombre_completo,
            rfc_uid=estudiante_create.rfc_uid
        )
        self.session.add(db_estudiante)
        await self.session.flush()
        await self.session.refresh(db_estudiante)
        return Estudiante.model_validate(db_estudiante)

    async def list_all(self) -> List[Estudiante]:
        stmt = select(EstudianteModel).order_by(EstudianteModel.nombre_completo)
        result = await self.session.execute(stmt)
        db_estudiantes = result.scalars().all()
        return [Estudiante.model_validate(e) for e in db_estudiantes]
