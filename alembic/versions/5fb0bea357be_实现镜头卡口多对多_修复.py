"""实现镜头卡口多对多（修复）

Revision ID: 5fb0bea357be
Revises: 78f21f9197ba
Create Date: 2025-05-11 11:25:14.309244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5fb0bea357be'
down_revision: Union[str, None] = '78f21f9197ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
