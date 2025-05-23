"""添加lens_mount_link表

Revision ID: f9a0c4ccce3d
Revises: e771c5968920
Create Date: 2025-05-11 11:33:25.509721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f9a0c4ccce3d'
down_revision: Union[str, None] = 'e771c5968920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lensmountlink',
    sa.Column('lens_id', sa.Integer(), nullable=False),
    sa.Column('mount_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lens_id'], ['lens.id'], ),
    sa.ForeignKeyConstraint(['mount_id'], ['mount.id'], ),
    sa.PrimaryKeyConstraint('lens_id', 'mount_id')
    )
    op.drop_constraint('lens_ibfk_3', 'lens', type_='foreignkey')
    op.drop_column('lens', 'mount_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lens', sa.Column('mount_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('lens_ibfk_3', 'lens', 'mount', ['mount_id'], ['id'])
    op.drop_table('lensmountlink')
    # ### end Alembic commands ###
