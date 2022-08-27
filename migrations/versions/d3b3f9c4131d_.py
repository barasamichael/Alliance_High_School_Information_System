"""empty message

Revision ID: d3b3f9c4131d
Revises: 8c587e593f95
Create Date: 2022-05-18 12:42:52.404212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3b3f9c4131d'
down_revision = '8c587e593f95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house', sa.Column('associated_image', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('house', 'associated_image')
    # ### end Alembic commands ###