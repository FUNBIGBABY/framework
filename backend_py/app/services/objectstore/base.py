from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ObjectStoreProviderError(RuntimeError):
    """Base error for object store provider failures."""


class ObjectStoreProvider(ABC):
    """Abstract interface for blob/object storage."""

    name: str

    @abstractmethod
    def put(self, key: str, data: bytes, content_type: Optional[str] = None) -> None:
        """Store bytes at a key."""

    @abstractmethod
    def get(self, key: str) -> bytes:
        """Return bytes stored at a key."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a key."""

    @abstractmethod
    def presigned_url(self, key: str, *, expires_seconds: int = 3600) -> str:
        """Return a temporary URL for a key."""
