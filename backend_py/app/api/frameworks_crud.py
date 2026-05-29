import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_user_id
from ..db import get_db
from ..models import Framework
from .frameworks_shared import FrameworkDetailResponse, FrameworkListResponse


router = APIRouter()


# New feature: Retrieve all frameworks for the current user.
@router.get("/my-frameworks", response_model=List[FrameworkListResponse])
def get_my_frameworks(
    user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    Get all frameworks created by the current user

    Sort in descending order of creation time List
    For the "Your Frameworks" list page
    """

    frameworks = (
        db.query(Framework)
        .filter(Framework.creator_id == user_id)
        .order_by(Framework.created_at.desc())
        .all()
    )

    result = []
    for fw in frameworks:
        # Analyze artefacts for preview
        artefacts = json.loads(fw.artefacts_json)
        additional = artefacts.get("additional", [])

        # Only the first 3 artifacts are used for card display.
        preview_artefacts = []
        if additional:
            for art in additional[:3]:
                preview_artefacts.append(
                    {
                        "name": art.get("name", ""),
                        "description": art.get("description", "")[
                            :100
                        ],  # Truncation description
                    }
                )

        result.append(
            FrameworkListResponse(
                id=fw.id,
                title=fw.title,
                version=fw.version,
                family=fw.family,
                confidence=fw.confidence,
                created_at=fw.created_at,
                updated_at=fw.updated_at,
                preview_artefacts=preview_artefacts,
            )
        )

    return result


# New feature: Retrieve frameworks by family group
@router.get("/my-frameworks/by-family")
def get_my_frameworks_by_family(
    user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    Retrieve the current user's frameworks and group them by family.

    Return format:
    {
        "Financial": [framework1, framework2, ...],
        "Healthcare": [...],
        ...
    }
    """

    frameworks = (
        db.query(Framework)
        .filter(Framework.creator_id == user_id)
        .order_by(Framework.created_at.desc())
        .all()
    )

    # Grouped by family
    grouped = {}
    for fw in frameworks:
        family = fw.family or "Other"

        if family not in grouped:
            grouped[family] = []

        # Analysis of Artefacts
        artefacts = json.loads(fw.artefacts_json)
        additional = artefacts.get("additional", [])

        preview_artefacts = []
        if additional:
            for art in additional[:3]:
                preview_artefacts.append(
                    {
                        "name": art.get("name", ""),
                        "description": art.get("description", "")[:100],
                    }
                )

        grouped[family].append(
            {
                "id": fw.id,
                "title": fw.title,
                "version": fw.version,
                "family": fw.family,
                "confidence": fw.confidence,
                "created_at": fw.created_at.isoformat(),
                "updated_at": fw.updated_at.isoformat(),
                "preview_artefacts": preview_artefacts,
            }
        )

    return grouped


# New feature: Retrieve detailed information for a single framework.
@router.get("/{framework_id}", response_model=FrameworkDetailResponse)
def get_framework_detail(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get complete information about the framework

    Only able to access the frameworks they created
    """

    framework = (
        db.query(Framework)
        .filter(
            Framework.id == framework_id,
            Framework.creator_id
            == user_id,  # Ensure that only your own account can be accessed.
        )
        .first()
    )

    if not framework:
        raise HTTPException(
            status_code=404,
            detail="Framework not found or you don't have permission to access it",
        )

    return FrameworkDetailResponse(
        id=framework.id,
        title=framework.title,
        version=framework.version,
        family=framework.family,
        confidence=framework.confidence,
        creator_id=framework.creator_id,
        metadata=json.loads(framework.metadata_json),
        steps=json.loads(framework.steps_json),
        artefacts=json.loads(framework.artefacts_json),
        risks=json.loads(framework.risks_json),
        escalation=json.loads(framework.escalation_json),
        created_at=framework.created_at,
        updated_at=framework.updated_at,
    )


# Added: Binding information interface (/api/frameworks/{id}/binding)
@router.get("/{framework_id}/binding")
def get_framework_binding(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Retrieve the framework's POV, family, and confidence binding information.
    (Used for displaying POV and confidence level simultaneously in a frame card or detail page on the front end)
    """
    # 🔍 Query the framework of the current user
    fw = (
        db.query(Framework)
        .filter(Framework.id == framework_id, Framework.creator_id == user_id)
        .first()
    )

    if not fw:
        raise HTTPException(
            status_code=404, detail="Framework not found or access denied"
        )

    # Trying to extract the POV (the complete content returned by AI) from raw_framework_json.
    pov_value = None
    try:
        if fw.raw_framework_json:
            raw_data = json.loads(fw.raw_framework_json)
            pov_value = raw_data.get("pov")
    except Exception:
        pov_value = None

    #  Return unified binding information
    return {
        "id": fw.id,
        "title": fw.title,
        "pov": pov_value,
        "family": fw.family,
        "confidence": fw.confidence,
        "created_at": fw.created_at,
        "updated_at": fw.updated_at,
    }


# Added: Updated framework
@router.put("/{framework_id}")
def update_framework(
    framework_id: str,
    framework_data: dict,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Update the framework (save from the Editor)

    You can only update the framework you created.
    """

    framework = (
        db.query(Framework)
        .filter(Framework.id == framework_id, Framework.creator_id == user_id)
        .first()
    )

    if not framework:
        raise HTTPException(
            status_code=404, detail="Framework not found or you don't have permission"
        )

    # Update field
    metadata = framework_data.get("metadata", {})
    framework.title = metadata.get("title", framework.title)
    framework.version = metadata.get("version", framework.version)

    # Update JSON fields
    framework.metadata_json = json.dumps(metadata, ensure_ascii=False)
    framework.steps_json = json.dumps(
        framework_data.get("steps", []), ensure_ascii=False
    )
    framework.artefacts_json = json.dumps(
        framework_data.get("artefacts", {}), ensure_ascii=False
    )
    framework.risks_json = json.dumps(
        framework_data.get("risks", []), ensure_ascii=False
    )
    framework.escalation_json = json.dumps(
        framework_data.get("escalation", []), ensure_ascii=False
    )

    framework.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(framework)

    return {
        "success": True,
        "message": "Framework updated successfully",
        "framework_id": framework.id,
    }


# Added: Remove framework
@router.delete("/{framework_id}")
def delete_framework(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    remove framework

    You can only delete the framework you created.
    """

    framework = (
        db.query(Framework)
        .filter(Framework.id == framework_id, Framework.creator_id == user_id)
        .first()
    )

    if not framework:
        raise HTTPException(
            status_code=404, detail="Framework not found or you don't have permission"
        )

    db.delete(framework)
    db.commit()

    return {"success": True, "message": "Framework deleted successfully"}
