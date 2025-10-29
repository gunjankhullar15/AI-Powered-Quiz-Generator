"""merge heads

Revision ID: 280a7727d8ce
Revises: 12018d463779, fdb2d8c13f71
Create Date: 2025-10-29 17:03:41.267314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '280a7727d8ce'
down_revision: Union[str, Sequence[str], None] = ('12018d463779', 'fdb2d8c13f71')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
