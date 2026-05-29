import json
import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from nanoid import generate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth import get_current_user_id
from ..db import get_db
from ..models import SyncedVectorItem
from ..services.vectorstore import VectorStoreProviderError, get_vectorstore_provider


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
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    payload: Optional[dict] = None


class PushFrameworkRequest(BaseModel):
    framework: dict
    vector_store_id: Optional[str] = None



def _legacy_vector_provider():
    provider = get_vectorstore_provider("openai_legacy")
    try:
        provider.ensure_enabled()
    except VectorStoreProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return provider


def _read_api_key(provided):
    if provided:
        return provided
    v1 = os.getenv("VITE_FIREBASE_API_KEY")
    v2 = os.getenv("FIREBASE_API_KEY")
    return v1 or v2


def _read_project_id(provided):
    if provided:
        return provided
    p1 = os.getenv("FIREBASE_PROJECT_ID")
    return p1


def _ensure_id_token(api_key, provided):
    import requests as _requests

    if provided:
        return provided
    env_tok = os.getenv("FIREBASE_ID_TOKEN")
    if env_tok:
        return env_tok
    if not api_key:
        return None
    mail = os.getenv("FIREBASE_USER_EMAIL")
    pwd = os.getenv("FIREBASE_USER_PASSWORD")
    if mail and pwd:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        try:
            r = _requests.post(
                url,
                json={"email": mail, "password": pwd, "returnSecureToken": True},
                timeout=30,
            )
            if r.status_code == 200:
                d = r.json()
                tok = d.get("idToken")
                if tok:
                    return tok
        except Exception:
            pass
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    r = _requests.post(url, json={"returnSecureToken": True}, timeout=30)
    if r.status_code != 200:
        return None
    d = r.json()
    return d.get("idToken")


def _val(v):
    if not isinstance(v, dict):
        return v
    if "stringValue" in v:
        return v["stringValue"]
    if "booleanValue" in v:
        return v["booleanValue"]
    if "integerValue" in v:
        try:
            return int(v["integerValue"])
        except Exception:
            return v["integerValue"]
    if "doubleValue" in v:
        try:
            return float(v["doubleValue"])
        except Exception:
            return v["doubleValue"]
    if "timestampValue" in v:
        return v["timestampValue"]
    if "mapValue" in v:
        fields = v.get("mapValue", {}).get("fields", {})
        return {k: _val(fields[k]) for k in fields} if fields else {}
    if "arrayValue" in v:
        arr = v.get("arrayValue", {}).get("values", [])
        return [_val(x) for x in arr] if arr else []
    return v



@router.post("/sync-library")
def sync_library(
    req: SyncLibraryRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    import requests as _requests

    provider = _legacy_vector_provider()
    project_id = _read_project_id(req.project_id)
    api_key = _read_api_key(req.api_key)
    id_token = _ensure_id_token(api_key, req.id_token)
    vs_id = req.vector_store_id or os.getenv("OPENAI_VECTOR_STORE_LIBRARY")
    if not project_id or not api_key or not id_token or not vs_id:
        raise HTTPException(status_code=400, detail="missing parameters")

    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents:runQuery"
    headers = {"Authorization": f"Bearer {id_token}"}
    params = {"key": api_key}
    body_public = {
        "structuredQuery": {
            "from": [{"collectionId": "frameworks"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "isPublic"},
                    "op": "EQUAL",
                    "value": {"booleanValue": True},
                }
            },
            "limit": req.limit,
        }
    }
    r = _requests.post(
        url, headers=headers, params=params, json=body_public, timeout=60
    )
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail=r.text)
    items = {}
    for it in r.json():
        doc = it.get("document")
        if not doc:
            continue
        name = doc.get("name", "")
        doc_id = name.split("/")[-1] if name else generate()
        fields = doc.get("fields", {})
        parsed = {k: _val(fields[k]) for k in fields}
        parsed["id"] = doc_id
        items[doc_id] = parsed

    if req.include_organization:
        body_org = {
            "structuredQuery": {
                "from": [{"collectionId": "frameworks"}],
                "where": {
                    "fieldFilter": {
                        "field": {"fieldPath": "publishedToOrganization"},
                        "op": "EQUAL",
                        "value": {"booleanValue": True},
                    }
                },
                "limit": req.limit,
            }
        }
        r2 = _requests.post(
            url, headers=headers, params=params, json=body_org, timeout=60
        )
        if r2.status_code != 200:
            raise HTTPException(status_code=500, detail=r2.text)
        for it in r2.json():
            doc = it.get("document")
            if not doc:
                continue
            name = doc.get("name", "")
            doc_id = name.split("/")[-1] if name else generate()
            fields = doc.get("fields", {})
            parsed = {k: _val(fields[k]) for k in fields}
            parsed["id"] = doc_id
            items[doc_id] = parsed

    uploaded = 0
    for doc_id, obj in items.items():
        exists = (
            db.query(SyncedVectorItem)
            .filter(SyncedVectorItem.doc_id == doc_id, SyncedVectorItem.vs_id == vs_id)
            .first()
        )
        if exists:
            continue

        fn = f"framework_{doc_id}.json"

        # get attributes
        is_public = obj.get("isPublic", False)
        tenant_id = obj.get("tenantId", "")

        attrs = {
            "visibility": "public" if is_public else "private",
            "domain": "valorie.ai",
            "tenantId": tenant_id,
        }

        # upload Vector Store
        provider.upload_json(
            vector_store_id=vs_id,
            filename=fn,
            content=json.dumps(obj, ensure_ascii=False),
            attributes=attrs,
        )

        # save record
        rec = SyncedVectorItem(
            doc_id=doc_id,
            vs_id=vs_id,
            source=("organization" if obj.get("publishedToOrganization") else "public"),
        )
        db.add(rec)
        try:
            db.commit()
        except Exception:
            db.rollback()
        uploaded += 1
    return {"success": True, "uploaded": uploaded}


@router.post("/log-event")
def log_event(
    req: EventLogRequest, user_id: str = Depends(get_current_user_id)
):
    vs_id = os.getenv("OPENAI_VECTOR_STORE_ACTIVITY")
    if not vs_id:
        raise HTTPException(
            status_code=500, detail="OPENAI_VECTOR_STORE_ACTIVITY missing"
        )
    provider = _legacy_vector_provider()
    now = datetime.utcnow().isoformat()
    payload = {
        "type": req.type,
        "frameworkId": req.framework_id,
        "tenantId": req.tenant_id,
        "userId": user_id,
        "timestamp": now,
        "data": req.payload or {},
    }
    fn = f"event_{generate()}.json"
    provider.upload_json(
        vector_store_id=vs_id,
        filename=fn,
        content=json.dumps(payload, ensure_ascii=False),
    )
    return {"success": True}


@router.post("/push-framework")
def push_framework(
    req: PushFrameworkRequest, current_user_id: str = Depends(get_current_user_id)
):
    print("=" * 60)
    print("🔧 DEBUG: push_framework called")
    print(f"   - Request data: {req}")
    print(f"   - Framework ID: {req.framework.get('id') if req.framework else 'None'}")
    print(f"   - Vector Store ID (req): {req.vector_store_id}")
    print(
        f"   - OPENAI_VECTOR_STORE_LIBRARY: {os.getenv('OPENAI_VECTOR_STORE_LIBRARY')}"
    )
    print(
        f"   - OPENAI_VECTOR_STORE_ACTIVITY: {os.getenv('OPENAI_VECTOR_STORE_ACTIVITY')}"
    )
    print(
        f"   - OPENAI_VECTOR_STORE_API_KEY: {'Set' if os.getenv('OPENAI_VECTOR_STORE_API_KEY') else 'Missing'}"
    )
    print("=" * 60)

    try:
        provider = _legacy_vector_provider()
        vs_id = (
            req.vector_store_id
            or os.getenv("OPENAI_VECTOR_STORE_LIBRARY")
            or os.getenv("OPENAI_VECTOR_STORE_ACTIVITY")
        )

        print(f"🔧 DEBUG: Final vs_id = {vs_id}")

        if not vs_id:
            print("❌ ERROR: vs_id is None!")
            raise HTTPException(status_code=400, detail="vector_store_id missing")

        fw = req.framework or {}
        doc_id = fw.get("id") or generate()
        fn = f"framework_{doc_id}.json"

        is_public = fw.get("isPublic", False)
        tenant_id = fw.get("tenantId", "")

        print(f"🔧 DEBUG: Framework metadata:")
        print(f"   - doc_id: {doc_id}")
        print(f"   - filename: {fn}")
        print(f"   - isPublic: {is_public}")
        print(f"   - tenantId: {tenant_id}")

        attrs = {
            "visibility": "public" if is_public else "private",
            "domain": "valorie.ai",
            "tenantId": tenant_id,
        }

        print(f"🔧 DEBUG: Uploading to Vector Store...")
        provider.upload_json(
            vector_store_id=vs_id,
            filename=fn,
            content=json.dumps(fw, ensure_ascii=False),
            attributes=attrs,
        )
        print(f"✅ DEBUG: Upload successful!")

        return {"success": True}

    except HTTPException as he:
        print(f"❌ ERROR (HTTPException): {he.detail}")
        raise
    except Exception as e:
        print(f"❌ ERROR (Exception): {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
