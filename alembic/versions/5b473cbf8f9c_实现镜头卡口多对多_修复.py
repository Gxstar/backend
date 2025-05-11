"""实现镜头卡口多对多（修复）

Revision ID: 5b473cbf8f9c
Revises: 7def2039519f
Create Date: 2025-05-11 11:16:38.247163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5b473cbf8f9c'
down_revision: Union[str, None] = '7def2039519f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
