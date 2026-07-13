"""add authenticated ownership to materials

Revision ID: 0005_material_owner
Revises: 0004_phase6_refresh_session_version
Create Date: 2026-07-13 00:00:00.000000

Existing materials intentionally remain ownerless. They are quarantined from
authenticated retrieval until an authorized data owner establishes a verified
mapping; the migration neither assigns an arbitrary user nor deletes data.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "0005_material_owner"
down_revision: Union[str, None] = "0004_phase6_refresh_session_version"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("materials", sa.Column("owner_id", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_materials_owner_id_users",
        "materials",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_materials_owner_id", "materials", ["owner_id"])


def downgrade() -> None:
    raise RuntimeError(
        "0005_material_owner is irreversible: dropping owner_id would destroy "
        "the Material authorization boundary and ownership mappings. Restore "
        "only through a separately reviewed data-preserving rollback migration."
    )
