"""empty message

Revision ID: 00b23b1da8ca
Revises: 9225873930c2
Create Date: 2025-04-08 19:44:50.614032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00b23b1da8ca'
down_revision = '9225873930c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meal_plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('meal_date', sa.DateTime(), nullable=False),
    sa.Column('meal_description', sa.String(length=500), nullable=False),
    sa.Column('meal_source', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meal_plan')
    # ### end Alembic commands ###
