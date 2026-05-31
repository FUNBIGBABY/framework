from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Optional

from .base import VectorStoreProvider


class PgVectorProvider(VectorStoreProvider):
    """Vector store placeholder; pgvector retrieval wiring remains Phase 9 scope."""

    name = "pgvector"

    def upsert_vectors(
        self,
        namespace: str,
        chunks_with_vectors: Iterable[Mapping[str, Any]],
    ) -> None:
        raise NotImplementedError(
            "PgVectorProvider is intentionally deferred to Phase 9. "
            "Phase 4 only creates the Postgres/pgvector schema baseline."
        )

    def search_by_vector(
        self,
        namespace: str,
        vector: list[float],
        k: int = 5,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError(
            "PgVectorProvider is intentionally deferred to Phase 9. "
            "Phase 4 only creates the Postgres/pgvector schema baseline."
        )

    def delete(
        self,
        namespace: str,
        ids: Optional[Iterable[str] | str] = None,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> None:
        raise NotImplementedError(
            "PgVectorProvider is intentionally deferred to Phase 9. "
            "Phase 4 only creates the Postgres/pgvector schema baseline."
        )
