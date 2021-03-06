"""empty message

Revision ID: 251972af456b
Revises: 35be9f1c8d76
Create Date: 2018-08-09 20:51:06.409358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '251972af456b'
down_revision = '35be9f1c8d76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.String(length=100), nullable=False))
    op.create_foreign_key(None, 'posts', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###
