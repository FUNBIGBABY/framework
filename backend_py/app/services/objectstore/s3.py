from __future__ import annotations

from typing import Optional

from .base import ObjectStoreProvider


class S3ObjectStoreProvider(ObjectStoreProvider):
    """Phase 2 stub for S3-compatible object storage."""

    name = "s3"

    def put(self, key: str, data: bytes, content_type: Optional[str] = None) -> None:
        raise NotImplementedError("S3ObjectStoreProvider is a Phase 2 stub.")

    def get(self, key: str) -> bytes:
        raise NotImplementedError("S3ObjectStoreProvider is a Phase 2 stub.")

    def delete(self, key: str) -> None:
        raise NotImplementedError("S3ObjectStoreProvider is a Phase 2 stub.")

    def presigned_url(self, key: str, *, expires_seconds: int = 3600) -> str:
        raise NotImplementedError("S3ObjectStoreProvider is a Phase 2 stub.")
