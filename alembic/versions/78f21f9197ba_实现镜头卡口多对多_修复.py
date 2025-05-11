"""实现镜头卡口多对多（修复）

Revision ID: 78f21f9197ba
Revises: c15665dd67fd
Create Date: 2025-05-11 11:24:29.501028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '78f21f9197ba'
down_revision: Union[str, None] = 'c15665dd67fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
