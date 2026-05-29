from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Optional

from .base import VectorStoreProvider


class PgVectorProvider(VectorStoreProvider):
    """Phase 2 stub for the future PostgreSQL + pgvector implementation."""

    name = "pgvector"

    def upsert_vectors(
        self,
        namespace: str,
        chunks_with_vectors: Iterable[Mapping[str, Any]],
    ) -> None:
        raise NotImplementedError(
            "PgVectorProvider is a Phase 2 stub. SQLAlchemy/pgvector wiring is deferred to Phase 4."
        )

    def search_by_vector(
        self,
        namespace: str,
        vector: list[float],
        k: int = 5,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError(
            "PgVectorProvider is a Phase 2 stub. SQLAlchemy/pgvector wiring is deferred to Phase 4."
        )

    def delete(
        self,
        namespace: str,
        ids: Optional[Iterable[str] | str] = None,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> None:
        raise NotImplementedError(
            "PgVectorProvider is a Phase 2 stub. SQLAlchemy/pgvector wiring is deferred to Phase 4."
        )
