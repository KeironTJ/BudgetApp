"""empty message

Revision ID: 9225873930c2
Revises: 3b7bba196559
Create Date: 2025-04-04 23:13:49.541353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9225873930c2'
down_revision = '3b7bba196559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    # ### end Alembic commands ###
