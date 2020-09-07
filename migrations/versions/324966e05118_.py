"""empty message

Revision ID: 324966e05118
Revises: 
Create Date: 2020-09-06 01:22:01.222809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '324966e05118'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('pw', sa.String(), nullable=True),
    sa.Column('access', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    # ### end Alembic commands ###