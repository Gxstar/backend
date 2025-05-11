"""实现镜头卡口多对多

Revision ID: 7def2039519f
Revises: 6f1e5c25ad39
Create Date: 2025-05-11 11:15:33.776278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7def2039519f'
down_revision: Union[str, None] = '6f1e5c25ad39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
