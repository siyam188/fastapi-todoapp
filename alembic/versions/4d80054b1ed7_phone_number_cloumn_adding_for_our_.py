"""phone number cloumn adding for our users table

Revision ID: 4d80054b1ed7
Revises: 
Create Date: 2026-10-17 11:15:33.507945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d80054b1ed7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column('users',sa.Column('phone_number',sa.String,nullable=True))

def downgrade() -> None:
   op.drop_column('users','phone_number')