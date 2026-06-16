import base64
import json
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from ..auth import get_current_user_id
from ..db import get_db
from ..models import Framework
from .frameworks_shared import coerce_json_value


router = APIRouter()
MAX_PUBLIC_LIBRARY_LIMIT = 50


class PublishFrameworkRequest(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    version: Optional[str] = None


class PublishFrameworkResponse(BaseModel):
    success: bool
    framework_id: str
    is_public: bool
    category: Optional[str]
    tags: List[str]
    published_at: Optional[datetime]
    updated_at: datetime


class PublicFrameworkItem(BaseModel):
    id: str
    title: str
    version: str
    family: str
    confidence: float
    category: Optional[str]
    tags: List[str]
    published_at: datetime
    updated_at: datetime
    preview_artefacts: List[dict]


class PublicFrameworkListResponse(BaseModel):
    items: List[PublicFrameworkItem]
    next_cursor: Optional[str] = None
    limit: int = Field(ge=1, le=MAX_PUBLIC_LIBRARY_LIMIT)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _get_owned_framework(db: Session, framework_id: str, user_id: str) -> Framework:
    framework = (
        db.query(Framework)
        .filter(Framework.id == framework_id, Framework.creator_id == user_id)
        .first()
    )

    if not framework:
        raise HTTPException(
            status_code=404,
            detail="Framework not found or you don't have permission",
        )

    return framework


def _preview_artefacts(framework: Framework) -> list[dict]:
    artefacts = coerce_json_value(framework.artefacts_json, {})
    if not isinstance(artefacts, dict):
        return []

    additional = artefacts.get("additional", [])
    if not isinstance(additional, list):
        return []

    preview = []
    for artefact in additional[:3]:
        if not isinstance(artefact, dict):
            continue
        preview.append(
            {
                "name": artefact.get("name", ""),
                "description": str(artefact.get("description", ""))[:100],
            }
        )
    return preview


def _sanitize_tags(tags: Optional[list[str]]) -> Optional[list[str]]:
    if tags is None:
        return None

    sanitized = []
    for tag in tags:
        value = str(tag).strip()
        if not value or value in sanitized:
            continue
        sanitized.append(value[:80])
        if len(sanitized) >= 20:
            break
    return sanitized


def _tag_list(framework: Framework) -> list[str]:
    tags = coerce_json_value(framework.tags_json, [])
    if not isinstance(tags, list):
        return []
    return [str(tag) for tag in tags if str(tag).strip()]


def _cursor_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def _encode_cursor(framework: Framework) -> Optional[str]:
    if framework.published_at is None:
        return None

    payload = {
        "published_at": _cursor_timestamp(framework.published_at),
        "id": framework.id,
    }
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _decode_cursor(cursor: str) -> tuple[datetime, str]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        published_at = datetime.fromisoformat(payload["published_at"])
        if published_at.tzinfo is not None:
            published_at = published_at.astimezone(timezone.utc).replace(tzinfo=None)
        framework_id = str(payload["id"])
    except (KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=400, detail="Invalid public library cursor"
        ) from exc

    return published_at, framework_id


def _public_item(framework: Framework) -> PublicFrameworkItem:
    return PublicFrameworkItem(
        id=framework.id,
        title=framework.title,
        version=framework.version or "1.0.0",
        family=framework.family or "Other",
        confidence=float(framework.confidence or 0.0),
        category=framework.category or framework.family or "Other",
        tags=_tag_list(framework),
        published_at=framework.published_at,
        updated_at=framework.updated_at,
        preview_artefacts=_preview_artefacts(framework),
    )


@router.get("/public", response_model=PublicFrameworkListResponse)
def list_public_frameworks(
    cursor: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=MAX_PUBLIC_LIBRARY_LIMIT),
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    query = db.query(Framework).filter(
        Framework.is_public.is_(True),
        Framework.published_at.isnot(None),
    )

    if cursor:
        published_at, framework_id = _decode_cursor(cursor)
        query = query.filter(
            or_(
                Framework.published_at < published_at,
                and_(
                    Framework.published_at == published_at,
                    Framework.id < framework_id,
                ),
            )
        )

    frameworks = (
        query.order_by(Framework.published_at.desc(), Framework.id.desc())
        .limit(limit + 1)
        .all()
    )
    page_items = frameworks[:limit]
    next_cursor = _encode_cursor(page_items[-1]) if len(frameworks) > limit else None

    return PublicFrameworkListResponse(
        items=[_public_item(framework) for framework in page_items],
        next_cursor=next_cursor,
        limit=limit,
    )


@router.post("/{framework_id}/publish", response_model=PublishFrameworkResponse)
def publish_framework(
    framework_id: str,
    request: Optional[PublishFrameworkRequest] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    framework = _get_owned_framework(db, framework_id, user_id)
    now = _utc_now()

    if request and request.version and request.version.strip():
        framework.version = request.version.strip()

    if request and request.category is not None:
        category = request.category.strip()
        framework.category = category or None
    elif not framework.category:
        framework.category = framework.family or "Other"

    if request and request.tags is not None:
        framework.tags_json = _sanitize_tags(request.tags) or []
    elif framework.tags_json is None:
        framework.tags_json = []

    framework.is_public = True
    framework.published_at = now
    framework.updated_at = now

    db.commit()
    db.refresh(framework)

    return PublishFrameworkResponse(
        success=True,
        framework_id=framework.id,
        is_public=framework.is_public,
        category=framework.category,
        tags=_tag_list(framework),
        published_at=framework.published_at,
        updated_at=framework.updated_at,
    )


@router.post("/{framework_id}/unpublish", response_model=PublishFrameworkResponse)
def unpublish_framework(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    framework = _get_owned_framework(db, framework_id, user_id)
    now = _utc_now()

    framework.is_public = False
    framework.published_at = None
    framework.updated_at = now

    db.commit()
    db.refresh(framework)

    return PublishFrameworkResponse(
        success=True,
        framework_id=framework.id,
        is_public=framework.is_public,
        category=framework.category,
        tags=_tag_list(framework),
        published_at=framework.published_at,
        updated_at=framework.updated_at,
    )
