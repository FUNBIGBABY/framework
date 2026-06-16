from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..auth import get_current_user_id
from ..services.rag import RAGIndexingDeferredError, RAGIndexingService


router = APIRouter()


class SyncLibraryRequest(BaseModel):
    project_id: Optional[str] = None
    api_key: Optional[str] = None
    id_token: Optional[str] = None
    vector_store_id: Optional[str] = None
    limit: int = 1000
    include_organization: bool = True


class EventLogRequest(BaseModel):
    type: str
    framework_id: Optional[str] = None
    payload: Optional[dict] = None


class PushFrameworkRequest(BaseModel):
    framework: dict
    vector_store_id: Optional[str] = None


def get_rag_indexing_service() -> RAGIndexingService:
    return RAGIndexingService()


def _phase9_deferred(exc: RAGIndexingDeferredError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=str(exc),
    )


@router.post("/sync-library")
def sync_library(
    req: SyncLibraryRequest,
    current_user_id: str = Depends(get_current_user_id),
    service: RAGIndexingService = Depends(get_rag_indexing_service),
):
    try:
        service.sync_library(
            current_user_id=current_user_id,
            request=req.model_dump(),
        )
    except RAGIndexingDeferredError as exc:
        raise _phase9_deferred(exc) from exc


@router.post("/log-event")
def log_event(
    req: EventLogRequest,
    current_user_id: str = Depends(get_current_user_id),
    service: RAGIndexingService = Depends(get_rag_indexing_service),
):
    try:
        service.log_event(
            current_user_id=current_user_id,
            event=req.model_dump(),
        )
    except RAGIndexingDeferredError as exc:
        raise _phase9_deferred(exc) from exc


@router.post("/push-framework")
def push_framework(
    req: PushFrameworkRequest,
    current_user_id: str = Depends(get_current_user_id),
    service: RAGIndexingService = Depends(get_rag_indexing_service),
):
    try:
        service.index_framework(
            current_user_id=current_user_id,
            framework=req.framework,
        )
    except RAGIndexingDeferredError as exc:
        raise _phase9_deferred(exc) from exc
