"""character limit to message field

Revision ID: 980f2bf5c9fb
Revises: a816f73f88d9
Create Date: 2022-07-31 15:10:20.785506

"""
from alembic import op
import sqlalchemy as sa

revision = '980f2bf5c9fb'
down_revision = 'a816f73f88d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        table_name="alarms",
        column_name="message",
        existing_type=sa.String(),
        type_=sa.String(150),
    )


def downgrade() -> None:
    op.alter_column(
        table_name="alarms",
        column_name="message",
        existing_type=sa.String(150),
        type_=sa.String(),
    )
