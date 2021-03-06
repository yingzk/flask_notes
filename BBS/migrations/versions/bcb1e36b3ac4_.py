"""empty message

Revision ID: bcb1e36b3ac4
Revises: 88ad4b4af1df
Create Date: 2018-08-08 22:50:13.905186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcb1e36b3ac4'
down_revision = '88ad4b4af1df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('priority', table_name='banner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('priority', 'banner', ['priority'], unique=True)
    # ### end Alembic commands ###
