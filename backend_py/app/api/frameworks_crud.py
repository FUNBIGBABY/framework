from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from nanoid import generate
from sqlalchemy.orm import Session

from ..auth import get_current_user_id
from ..db import get_db
from ..models import Framework
from .frameworks_shared import (
    FrameworkCreateRequest,
    FrameworkDetailResponse,
    FrameworkListResponse,
    FrameworkMutationResponse,
    FrameworkUpdateRequest,
    coerce_json_value,
)


router = APIRouter()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


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


def _framework_detail_response(framework: Framework) -> FrameworkDetailResponse:
    return FrameworkDetailResponse(
        id=framework.id,
        title=framework.title,
        version=framework.version,
        family=framework.family,
        confidence=framework.confidence,
        creator_id=framework.creator_id,
        metadata=coerce_json_value(framework.metadata_json, {}),
        steps=coerce_json_value(framework.steps_json, []),
        artefacts=coerce_json_value(framework.artefacts_json, {}),
        risks=coerce_json_value(framework.risks_json, []),
        escalation=coerce_json_value(framework.escalation_json, []),
        created_at=framework.created_at,
        updated_at=framework.updated_at,
    )


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


def _coerce_raw_framework(raw_framework):
    if raw_framework is None:
        return None
    return coerce_json_value(raw_framework, None)


def create_framework(
    framework_data: FrameworkCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    metadata = framework_data.metadata or {}
    title = framework_data.title or metadata.get("title") or "Untitled Framework"
    version = framework_data.version or metadata.get("version") or "1.0.0"
    family = framework_data.family or "Other"
    confidence = (
        float(framework_data.confidence)
        if framework_data.confidence is not None
        else 0.0
    )
    raw_framework_json = _coerce_raw_framework(framework_data.raw_framework)
    if raw_framework_json is None:
        raw_framework_json = framework_data.model_dump(
            by_alias=True,
            exclude={"raw_framework"},
            exclude_none=True,
        )

    framework = Framework(
        id=f"fw_{generate(size=12)}",
        title=title,
        version=version,
        family=family,
        confidence=confidence,
        pov=framework_data.pov,
        creator_id=user_id,
        metadata_json=metadata,
        steps_json=framework_data.steps,
        artefacts_json=framework_data.artefacts,
        risks_json=framework_data.risks,
        escalation_json=framework_data.escalation,
        raw_framework_json=raw_framework_json,
        raw_metadata_json=metadata,
        created_at=_utc_now(),
        updated_at=_utc_now(),
    )

    db.add(framework)
    db.commit()
    db.refresh(framework)

    return FrameworkMutationResponse(
        success=True,
        message="Framework created successfully",
        framework_id=framework.id,
    )


@router.get("/my-frameworks", response_model=List[FrameworkListResponse])
def get_my_frameworks(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    frameworks = (
        db.query(Framework)
        .filter(Framework.creator_id == user_id)
        .order_by(Framework.created_at.desc())
        .all()
    )

    return [
        FrameworkListResponse(
            id=framework.id,
            title=framework.title,
            version=framework.version,
            family=framework.family,
            confidence=framework.confidence,
            created_at=framework.created_at,
            updated_at=framework.updated_at,
            preview_artefacts=_preview_artefacts(framework),
        )
        for framework in frameworks
    ]


@router.get("/my-frameworks/by-family")
def get_my_frameworks_by_family(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    frameworks = (
        db.query(Framework)
        .filter(Framework.creator_id == user_id)
        .order_by(Framework.created_at.desc())
        .all()
    )

    grouped = {}
    for framework in frameworks:
        family = framework.family or "Other"
        grouped.setdefault(family, []).append(
            {
                "id": framework.id,
                "title": framework.title,
                "version": framework.version,
                "family": framework.family,
                "confidence": framework.confidence,
                "created_at": framework.created_at.isoformat(),
                "updated_at": framework.updated_at.isoformat(),
                "preview_artefacts": _preview_artefacts(framework),
            }
        )

    return grouped


@router.get("/{framework_id}", response_model=FrameworkDetailResponse)
def get_framework_detail(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    framework = _get_owned_framework(db, framework_id, user_id)
    return _framework_detail_response(framework)


@router.get("/{framework_id}/binding")
def get_framework_binding(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    framework = _get_owned_framework(db, framework_id, user_id)
    pov_value = framework.pov

    if pov_value is None and framework.raw_framework_json:
        raw_data = coerce_json_value(framework.raw_framework_json, {})
        if isinstance(raw_data, dict):
            pov_value = raw_data.get("pov")
            nested_framework = raw_data.get("framework")
            if pov_value is None and isinstance(nested_framework, dict):
                pov_value = nested_framework.get("pov")

    return {
        "id": framework.id,
        "title": framework.title,
        "pov": pov_value,
        "family": framework.family,
        "confidence": framework.confidence,
        "created_at": framework.created_at,
        "updated_at": framework.updated_at,
    }


@router.put("/{framework_id}", response_model=FrameworkMutationResponse)
def update_framework(
    framework_id: str,
    framework_data: FrameworkUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    framework = _get_owned_framework(db, framework_id, user_id)
    fields_set = framework_data.model_fields_set

    if "metadata" in fields_set and framework_data.metadata is not None:
        metadata = framework_data.metadata
        framework.metadata_json = metadata
        if "title" not in fields_set and metadata.get("title"):
            framework.title = metadata["title"]
        if "version" not in fields_set and metadata.get("version"):
            framework.version = metadata["version"]

    if "title" in fields_set and framework_data.title:
        framework.title = framework_data.title
    if "version" in fields_set and framework_data.version:
        framework.version = framework_data.version
    if "family" in fields_set:
        framework.family = framework_data.family or "Other"
    if "confidence" in fields_set and framework_data.confidence is not None:
        framework.confidence = float(framework_data.confidence)
    if "pov" in fields_set:
        framework.pov = framework_data.pov
    if "steps" in fields_set and framework_data.steps is not None:
        framework.steps_json = framework_data.steps
    if "artefacts" in fields_set and framework_data.artefacts is not None:
        framework.artefacts_json = framework_data.artefacts
    if "risks" in fields_set and framework_data.risks is not None:
        framework.risks_json = framework_data.risks
    if "escalation" in fields_set and framework_data.escalation is not None:
        framework.escalation_json = framework_data.escalation
    if "raw_framework" in fields_set:
        framework.raw_framework_json = _coerce_raw_framework(
            framework_data.raw_framework
        )

    framework.updated_at = _utc_now()

    db.commit()
    db.refresh(framework)

    return FrameworkMutationResponse(
        success=True,
        message="Framework updated successfully",
        framework_id=framework.id,
    )


@router.delete("/{framework_id}")
def delete_framework(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    framework = _get_owned_framework(db, framework_id, user_id)

    db.delete(framework)
    db.commit()

    return {"success": True, "message": "Framework deleted successfully"}
