"""empty message

Revision ID: 33fa1e3900a2
Revises: f67630dea8ee
Create Date: 2020-10-10 16:18:37.149583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33fa1e3900a2'
down_revision = 'f67630dea8ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('tickets', sa.Column('resolve_date', sa.DateTime(), nullable=True))
    op.add_column('tickets', sa.Column('resolve_user', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tickets', 'users', ['resolve_user'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'resolve_user')
    op.drop_column('tickets', 'resolve_date')
    op.drop_column('notes', 'date')
    # ### end Alembic commands ###
