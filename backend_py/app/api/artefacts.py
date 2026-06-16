from datetime import datetime, timezone
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from nanoid import generate
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..auth import get_current_user_id
from ..db import get_db
from ..models import Artefact, Framework


router = APIRouter()
JsonContainer = Union[dict[str, Any], list[Any]]


class ArtefactBaseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ArtefactCreateRequest(ArtefactBaseRequest):
    name: str = Field(min_length=1)
    artefact_type: Optional[str] = "custom"
    content_json: JsonContainer = Field(default_factory=dict)
    metadata_json: JsonContainer = Field(default_factory=dict)
    ord: int = 0


class ArtefactUpdateRequest(ArtefactBaseRequest):
    name: Optional[str] = Field(default=None, min_length=1)
    artefact_type: Optional[str] = None
    content_json: Optional[JsonContainer] = None
    metadata_json: Optional[JsonContainer] = None
    ord: Optional[int] = None


class ArtefactResponse(BaseModel):
    id: str
    framework_id: str
    name: str
    artefact_type: Optional[str]
    content_json: JsonContainer
    metadata_json: JsonContainer
    ord: int
    created_at: datetime
    updated_at: datetime


class ArtefactMutationResponse(BaseModel):
    success: bool
    message: str
    framework_id: str
    artefact_id: str


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


def _get_artefact(db: Session, framework_id: str, artefact_id: str) -> Artefact:
    artefact = (
        db.query(Artefact)
        .filter(Artefact.id == artefact_id, Artefact.framework_id == framework_id)
        .first()
    )
    if not artefact:
        raise HTTPException(status_code=404, detail="Artefact not found")
    return artefact


def _artefact_response(artefact: Artefact) -> ArtefactResponse:
    return ArtefactResponse(
        id=artefact.id,
        framework_id=artefact.framework_id,
        name=artefact.name,
        artefact_type=artefact.artefact_type,
        content_json=artefact.content_json,
        metadata_json=artefact.metadata_json,
        ord=artefact.ord,
        created_at=artefact.created_at,
        updated_at=artefact.updated_at,
    )


@router.get("/{framework_id}/artefacts", response_model=List[ArtefactResponse])
def list_artefacts(
    framework_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _get_owned_framework(db, framework_id, user_id)
    artefacts = (
        db.query(Artefact)
        .filter(Artefact.framework_id == framework_id)
        .order_by(Artefact.ord.asc(), Artefact.created_at.asc(), Artefact.id.asc())
        .all()
    )
    return [_artefact_response(artefact) for artefact in artefacts]


@router.post(
    "/{framework_id}/artefacts",
    response_model=ArtefactResponse,
    status_code=201,
)
def create_artefact(
    framework_id: str,
    request: ArtefactCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _get_owned_framework(db, framework_id, user_id)
    now = _utc_now()
    artefact = Artefact(
        id=f"art_{generate(size=12)}",
        framework_id=framework_id,
        name=request.name,
        artefact_type=request.artefact_type,
        content_json=request.content_json,
        metadata_json=request.metadata_json,
        ord=request.ord,
        created_at=now,
        updated_at=now,
    )

    db.add(artefact)
    db.commit()
    db.refresh(artefact)

    return _artefact_response(artefact)


@router.get(
    "/{framework_id}/artefacts/{artefact_id}",
    response_model=ArtefactResponse,
)
def get_artefact(
    framework_id: str,
    artefact_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _get_owned_framework(db, framework_id, user_id)
    artefact = _get_artefact(db, framework_id, artefact_id)
    return _artefact_response(artefact)


@router.put(
    "/{framework_id}/artefacts/{artefact_id}",
    response_model=ArtefactResponse,
)
def update_artefact(
    framework_id: str,
    artefact_id: str,
    request: ArtefactUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _get_owned_framework(db, framework_id, user_id)
    artefact = _get_artefact(db, framework_id, artefact_id)
    fields_set = request.model_fields_set

    if "name" in fields_set and request.name is not None:
        artefact.name = request.name
    if "artefact_type" in fields_set:
        artefact.artefact_type = request.artefact_type
    if "content_json" in fields_set and request.content_json is not None:
        artefact.content_json = request.content_json
    if "metadata_json" in fields_set and request.metadata_json is not None:
        artefact.metadata_json = request.metadata_json
    if "ord" in fields_set and request.ord is not None:
        artefact.ord = request.ord

    artefact.updated_at = _utc_now()
    db.commit()
    db.refresh(artefact)

    return _artefact_response(artefact)


@router.delete(
    "/{framework_id}/artefacts/{artefact_id}",
    response_model=ArtefactMutationResponse,
)
def delete_artefact(
    framework_id: str,
    artefact_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _get_owned_framework(db, framework_id, user_id)
    artefact = _get_artefact(db, framework_id, artefact_id)

    db.delete(artefact)
    db.commit()

    return ArtefactMutationResponse(
        success=True,
        message="Artefact deleted successfully",
        framework_id=framework_id,
        artefact_id=artefact_id,
    )
