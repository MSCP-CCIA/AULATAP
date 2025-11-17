"""unir ramas de migracion

Revision ID: 478ee06edecd
Revises: 30b2cbb01c8b, 86380e51923f
Create Date: 2025-11-17 17:52:38.787260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '478ee06edecd'
down_revision: Union[str, Sequence[str], None] = ('30b2cbb01c8b', '86380e51923f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
