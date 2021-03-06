"""empty message

Revision ID: f67630dea8ee
Revises: d11144b6f8a5
Create Date: 2020-10-06 21:59:51.366456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f67630dea8ee'
down_revision = 'd11144b6f8a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('ticket', sa.Integer(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['users.id'], ),
    sa.ForeignKeyConstraint(['ticket'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('settings', sa.Column('setting', sa.String(), nullable=True))
    op.drop_column('settings', 'settings')
    op.drop_constraint('tickets_assign_user_fkey', 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'notes')
    op.drop_column('tickets', 'assign_user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('assign_user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tickets', sa.Column('notes', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('tickets_assign_user_fkey', 'tickets', 'users', ['assign_user'], ['id'])
    op.add_column('settings', sa.Column('settings', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('settings', 'setting')
    op.drop_table('notes')
    # ### end Alembic commands ###
