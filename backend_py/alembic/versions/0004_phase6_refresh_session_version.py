"""add refresh session version for cookie auth

Revision ID: 0004_phase6_refresh_session_version
Revises: 0003_phase5_admin_user_disabled
Create Date: 2026-06-22 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "0004_phase6_refresh_session_version"
down_revision: Union[str, None] = "0003_phase5_admin_user_disabled"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "refresh_token_version",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "refresh_token_version")
