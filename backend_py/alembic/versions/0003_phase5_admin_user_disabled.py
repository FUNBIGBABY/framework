"""phase 5 admin user disabled fields

Revision ID: 0003_phase5_admin_user_disabled
Revises: 0002_phase5_framework_publish_fields
Create Date: 2026-06-07
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_phase5_admin_user_disabled"
down_revision: Union[str, None] = "0002_phase5_framework_publish_fields"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "is_disabled",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )
    op.add_column("users", sa.Column("disabled_at", sa.DateTime(), nullable=True))
    op.create_index("ix_users_is_disabled", "users", ["is_disabled"])


def downgrade() -> None:
    op.drop_index("ix_users_is_disabled", table_name="users")
    op.drop_column("users", "disabled_at")
    op.drop_column("users", "is_disabled")
