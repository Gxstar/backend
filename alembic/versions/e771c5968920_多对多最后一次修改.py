"""多对多最后一次修改

Revision ID: e771c5968920
Revises: 5fb0bea357be
Create Date: 2025-05-11 11:30:38.548262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e771c5968920'
down_revision: Union[str, None] = '5fb0bea357be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
