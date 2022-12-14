"""empty message

Revision ID: b56d9f859557
Revises: d3b3f9c4131d
Create Date: 2022-05-18 20:17:29.935801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b56d9f859557'
down_revision = 'd3b3f9c4131d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('school',
    sa.Column('school_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('nickname', sa.String(length=128), nullable=False),
    sa.Column('associated_image', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('school_id')
    )
    op.add_column('student', sa.Column('status', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'status')
    op.drop_table('school')
    # ### end Alembic commands ###
