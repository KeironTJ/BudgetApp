"""empty message

Revision ID: 70b7777bcc90
Revises: f60fe8f54dbf
Create Date: 2025-04-01 22:35:03.354650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70b7777bcc90'
down_revision = 'f60fe8f54dbf'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_foreign_key("fk_message_user", "user", ["user_id"], ["id"])  # Explicit name

def downgrade():
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint("fk_message_user", type_='foreignkey')  # Explicit name when dropping
