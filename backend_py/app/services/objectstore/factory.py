from __future__ import annotations

import os
from typing import Optional

from .base import ObjectStoreProvider
from .minio import MinioObjectStoreProvider
from .oss import OSSObjectStoreProvider
from .s3 import S3ObjectStoreProvider


def get_objectstore_provider(provider_name: Optional[str] = None) -> ObjectStoreProvider:
    """Return the configured object store provider without making network calls."""

    selected = (
        provider_name or os.getenv("OBJECT_STORE_PROVIDER") or "minio"
    ).strip().lower()
    providers = {
        "minio": MinioObjectStoreProvider,
        "oss": OSSObjectStoreProvider,
        "s3": S3ObjectStoreProvider,
    }

    provider_cls = providers.get(selected)
    if provider_cls is None:
        supported = ", ".join(sorted(providers))
        raise ValueError(
            f"Unknown OBJECT_STORE_PROVIDER '{selected}'. Supported providers: {supported}"
        )

    return provider_cls()
