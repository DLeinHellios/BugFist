"""empty message

Revision ID: c2a03dd84082
Revises: b2c793daec8c
Create Date: 2020-11-01 16:48:14.300502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2a03dd84082'
down_revision = 'b2c793daec8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('register_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'register_date')
    op.drop_column('users', 'last_login')
    # ### end Alembic commands ###