"""Added tables to manage family groups

Revision ID: 697c7364abfc
Revises: e1c56c48a04c
Create Date: 2025-04-17 21:30:22.741170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '697c7364abfc'
down_revision = 'e1c56c48a04c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('family', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_family_name'), ['name'], unique=True)

    op.create_table('family_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=False),
    sa.Column('role_in_family', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'family_id', name='_user_family_uc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('family_members')
    with op.batch_alter_table('family', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_family_name'))

    op.drop_table('family')
    # ### end Alembic commands ###
