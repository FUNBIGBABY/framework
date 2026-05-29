from __future__ import annotations

from typing import Optional

from .base import ObjectStoreProvider


class MinioObjectStoreProvider(ObjectStoreProvider):
    """Phase 2 stub for MinIO object storage."""

    name = "minio"

    def put(self, key: str, data: bytes, content_type: Optional[str] = None) -> None:
        raise NotImplementedError("MinioObjectStoreProvider is a Phase 2 stub.")

    def get(self, key: str) -> bytes:
        raise NotImplementedError("MinioObjectStoreProvider is a Phase 2 stub.")

    def delete(self, key: str) -> None:
        raise NotImplementedError("MinioObjectStoreProvider is a Phase 2 stub.")

    def presigned_url(self, key: str, *, expires_seconds: int = 3600) -> str:
        raise NotImplementedError("MinioObjectStoreProvider is a Phase 2 stub.")
