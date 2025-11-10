"""
Implementación Concreta del Repositorio de Usuarios usando SQLAlchemy.
"""

from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from app.domain.repositories.usuario_repository import IUsuarioRepository
from app.infrastructure.persistence.models.usuario import Usuario as UsuarioModel
from app.core.security import get_password_hash


class UsuarioRepositoryImpl(IUsuarioRepository):
    """Implementación de IUsuarioRepository con SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, usuario_id: uuid.UUID) -> Optional[Usuario]:
        result = await self.session.get(UsuarioModel, usuario_id)
        return Usuario.model_validate(result) if result else None

    async def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(UsuarioModel).where(UsuarioModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()
        return Usuario.model_validate(db_user) if db_user else None

    async def create(self, usuario_create: UsuarioCreate) -> Usuario:
        hashed_password = get_password_hash(usuario_create.password)
        db_user = UsuarioModel(
            email=usuario_create.email,
            nombre_completo=usuario_create.nombre_completo,
            hashed_password=hashed_password,
            rol=usuario_create.rol
        )
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        return Usuario.model_validate(db_user)

    async def update(self, usuario_id: uuid.UUID, usuario_update: UsuarioUpdate) -> Optional[Usuario]:
        db_user = await self.session.get(UsuarioModel, usuario_id)
        if not db_user:
            return None

        update_data = usuario_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.session.flush()
        await self.session.refresh(db_user)
        return Usuario.model_validate(db_user)

    async def list_all(self) -> List[Usuario]:
        stmt = select(UsuarioModel).order_by(UsuarioModel.nombre_completo)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [Usuario.model_validate(u) for u in db_users]
