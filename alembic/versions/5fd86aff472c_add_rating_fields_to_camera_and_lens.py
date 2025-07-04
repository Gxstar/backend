"""add_rating_fields_to_camera_and_lens

Revision ID: 5fd86aff472c
Revises: 319a8e16f354
Create Date: 2025-07-02 22:28:45.757746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5fd86aff472c'
down_revision: Union[str, None] = '319a8e16f354'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('camera', sa.Column('rating', sa.Numeric(precision=2, scale=1), nullable=True))
    op.add_column('camera', sa.Column('rating_count', sa.Integer(), nullable=False))
    op.add_column('lens', sa.Column('rating', sa.Numeric(precision=2, scale=1), nullable=True))
    op.add_column('lens', sa.Column('rating_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lens', 'rating_count')
    op.drop_column('lens', 'rating')
    op.drop_column('camera', 'rating_count')
    op.drop_column('camera', 'rating')
    # ### end Alembic commands ###
