from fastapi import APIRouter

from . import (
    ai_ops,
    artefacts,
    exports,
    frameworks_crud,
    frameworks_public,
    generation,
    vector_sync,
)
from .frameworks_shared import FrameworkMutationResponse
from .vector_sync import (
    EventLogRequest,
    PushFrameworkRequest,
    SyncLibraryRequest,
    log_event,
    push_framework,
    sync_library,
)


router = APIRouter(prefix="/api/frameworks", tags=["frameworks"])
router.add_api_route(
    "",
    frameworks_crud.create_framework,
    methods=["POST"],
    response_model=FrameworkMutationResponse,
)
router.include_router(generation.router)
router.include_router(frameworks_public.router)
router.include_router(artefacts.router)
router.include_router(frameworks_crud.router)
router.include_router(exports.router)
router.include_router(ai_ops.router)
router.include_router(vector_sync.router)


__all__ = [
    "EventLogRequest",
    "PushFrameworkRequest",
    "SyncLibraryRequest",
    "log_event",
    "push_framework",
    "router",
    "sync_library",
]
