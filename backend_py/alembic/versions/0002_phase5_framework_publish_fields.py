"""phase 5 framework publish fields

Revision ID: 0002_phase5_framework_publish_fields
Revises: 0001_phase4_postgres_pgvector
Create Date: 2026-06-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0002_phase5_framework_publish_fields"
down_revision: Union[str, None] = "0001_phase4_postgres_pgvector"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


JSONB = postgresql.JSONB(astext_type=sa.Text())


def upgrade() -> None:
    op.add_column(
        "frameworks",
        sa.Column(
            "is_public",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )
    op.add_column("frameworks", sa.Column("category", sa.String(), nullable=True))
    op.add_column(
        "frameworks",
        sa.Column(
            "tags_json",
            JSONB,
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )
    op.add_column("frameworks", sa.Column("published_at", sa.DateTime(), nullable=True))

    op.create_index("ix_frameworks_is_public", "frameworks", ["is_public"])
    op.create_index("ix_frameworks_category", "frameworks", ["category"])
    op.create_index("ix_frameworks_published_at", "frameworks", ["published_at"])


def downgrade() -> None:
    op.drop_index("ix_frameworks_published_at", table_name="frameworks")
    op.drop_index("ix_frameworks_category", table_name="frameworks")
    op.drop_index("ix_frameworks_is_public", table_name="frameworks")

    op.drop_column("frameworks", "published_at")
    op.drop_column("frameworks", "tags_json")
    op.drop_column("frameworks", "category")
    op.drop_column("frameworks", "is_public")
