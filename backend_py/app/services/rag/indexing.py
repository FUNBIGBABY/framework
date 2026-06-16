from __future__ import annotations

from typing import Any


PHASE9_DEFERRED_MESSAGE = (
    "RAG indexing and retrieval are deferred to Phase 9. "
    "Phase 5 Round 1 only quarantines legacy vector_sync external calls."
)


class RAGIndexingDeferredError(RuntimeError):
    """Raised while RAG indexing/retrieval is intentionally not wired."""


class RAGIndexingService:
    """Phase 5 quarantine stub for future RAG indexing operations."""

    def _raise_deferred(self, operation: str) -> None:
        raise RAGIndexingDeferredError(f"{operation}: {PHASE9_DEFERRED_MESSAGE}")

    def sync_library(self, *, current_user_id: str, request: dict[str, Any]) -> None:
        self._raise_deferred("Library indexing")

    def index_framework(
        self,
        *,
        current_user_id: str,
        framework: dict[str, Any],
    ) -> None:
        self._raise_deferred("Framework indexing")

    def log_event(self, *, current_user_id: str, event: dict[str, Any]) -> None:
        self._raise_deferred("Event indexing")
