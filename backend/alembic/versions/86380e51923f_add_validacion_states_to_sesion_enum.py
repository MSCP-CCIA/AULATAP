"""add validacion states to sesion enum

Revision ID: 86380e51923f
Revises: b364ea42fc33
Create Date: 2025-11-17 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86380e51923f'
down_revision: Union[str, None] = 'b364ea42fc33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE estadosesion ADD VALUE 'ValidacionAbierta'")
    op.execute("ALTER TYPE estadosesion ADD VALUE 'ValidacionCerrada'")


def downgrade() -> None:
    # No se realiza la operación inversa para evitar problemas con datos existentes.
    # Si es necesario, se requeriría una migración manual para manejar los datos.
    pass