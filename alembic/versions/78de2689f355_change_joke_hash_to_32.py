"""change_joke_hash_to_32

Revision ID: 78de2689f355
Revises: 05eb10e293b6
Create Date: 2025-09-03 11:49:46.933514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78de2689f355'
down_revision: Union[str, Sequence[str], None] = '05eb10e293b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
