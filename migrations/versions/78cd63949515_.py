"""empty message

Revision ID: 78cd63949515
Revises: 33fa1e3900a2
Create Date: 2020-10-10 17:16:36.244219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78cd63949515'
down_revision = '33fa1e3900a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('notes', sa.Column('ticket_id', sa.Integer(), nullable=True))
    op.drop_constraint('notes_author_fkey', 'notes', type_='foreignkey')
    op.drop_constraint('notes_ticket_fkey', 'notes', type_='foreignkey')
    op.create_foreign_key(None, 'notes', 'tickets', ['ticket_id'], ['id'])
    op.create_foreign_key(None, 'notes', 'users', ['author_id'], ['id'])
    op.drop_column('notes', 'ticket')
    op.drop_column('notes', 'author')
    op.add_column('tickets', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('tickets', sa.Column('raise_user_id', sa.Integer(), nullable=True))
    op.add_column('tickets', sa.Column('resolve_user_id', sa.Integer(), nullable=True))
    op.drop_constraint('tickets_category_fkey', 'tickets', type_='foreignkey')
    op.drop_constraint('tickets_resolve_user_fkey', 'tickets', type_='foreignkey')
    op.drop_constraint('tickets_raise_user_fkey', 'tickets', type_='foreignkey')
    op.create_foreign_key(None, 'tickets', 'users', ['resolve_user_id'], ['id'])
    op.create_foreign_key(None, 'tickets', 'category', ['category_id'], ['id'])
    op.create_foreign_key(None, 'tickets', 'users', ['raise_user_id'], ['id'])
    op.drop_column('tickets', 'raise_user')
    op.drop_column('tickets', 'resolve_user')
    op.drop_column('tickets', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tickets', sa.Column('resolve_user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tickets', sa.Column('raise_user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.create_foreign_key('tickets_raise_user_fkey', 'tickets', 'users', ['raise_user'], ['id'])
    op.create_foreign_key('tickets_resolve_user_fkey', 'tickets', 'users', ['resolve_user'], ['id'])
    op.create_foreign_key('tickets_category_fkey', 'tickets', 'category', ['category'], ['id'])
    op.drop_column('tickets', 'resolve_user_id')
    op.drop_column('tickets', 'raise_user_id')
    op.drop_column('tickets', 'category_id')
    op.add_column('notes', sa.Column('author', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('notes', sa.Column('ticket', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.create_foreign_key('notes_ticket_fkey', 'notes', 'tickets', ['ticket'], ['id'])
    op.create_foreign_key('notes_author_fkey', 'notes', 'users', ['author'], ['id'])
    op.drop_column('notes', 'ticket_id')
    op.drop_column('notes', 'author_id')
    # ### end Alembic commands ###
