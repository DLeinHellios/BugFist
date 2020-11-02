"""empty message

Revision ID: b294c791120b
Revises: c2a03dd84082
Create Date: 2020-11-01 16:56:54.062700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b294c791120b'
down_revision = 'c2a03dd84082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'description')
    # ### end Alembic commands ###