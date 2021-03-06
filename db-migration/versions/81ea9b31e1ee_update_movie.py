"""update movie

Revision ID: 81ea9b31e1ee
Revises: 2e702a5c1b74
Create Date: 2021-08-30 21:01:50.887229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ea9b31e1ee'
down_revision = '2e702a5c1b74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'year')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('year', sa.VARCHAR(length=4), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
