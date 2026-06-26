import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-for-auth-hardening-32-chars")

import httpx
import pytest
from fastapi import FastAPI

from app.auth import ACCESS_COOKIE_NAME, create_access_token
from app.api.frameworks import router as frameworks_router
from app.api.materials import router as materials_router
from app.api.users import router as users_router
from app.db import get_db
from app.models import User


class FakeUserQuery:
    def __init__(self, users: list[User]):
        self.users = list(users)

    def filter(self, *conditions):
        for condition in conditions:
            key = getattr(getattr(condition, "left", None), "key", None)
            expected = getattr(getattr(condition, "right", None), "value", None)
            if key is None:
                continue
            self.users = [
                user for user in self.users if getattr(user, key) == expected
            ]
        return self

    def first(self):
        return self.users[0] if self.users else None


class FakeUserDB:
    def __init__(self):
        self.users = {
            "user_auth_hardening": User(
                id="user_auth_hardening",
                email="auth-hardening@example.com",
                username="auth_hardening",
                password_hash="not-used-in-this-test",
                is_disabled=False,
                disabled_at=None,
            )
        }

    def query(self, model):
        if model is User:
            return FakeUserQuery(list(self.users.values()))
        raise AssertionError(f"Unexpected model query: {model}")


@pytest.fixture(scope="module")
def app():
    app = FastAPI()
    app.include_router(frameworks_router)
    app.include_router(materials_router)
    app.include_router(users_router)
    fake_db = FakeUserDB()
    app.dependency_overrides[get_db] = lambda: fake_db
    return app


def assert_auth_required(response):
    assert response.status_code in {401, 403}


def auth_headers():
    token = create_access_token({"sub": "user_auth_hardening"})
    return {"Cookie": f"{ACCESS_COOKIE_NAME}={token}"}


MINIMAL_FRAMEWORK = {
    "metadata": {"title": "Auth Test Framework"},
    "steps": [],
    "artefacts": {},
    "risks": [],
    "escalation": [],
}


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/api/frameworks/export-markdown", MINIMAL_FRAMEWORK),
        ("/api/frameworks/export-docx", MINIMAL_FRAMEWORK),
        (
            "/api/frameworks/regenerate",
            {"framework": MINIMAL_FRAMEWORK, "use_local": False},
        ),
        (
            "/api/frameworks/ai-merge",
            {"frameworks": [{"name": "One"}, {"name": "Two"}]},
        ),
        (
            "/api/frameworks/ai-fill",
            {
                "artefact_name": "Report",
                "artefact_summary": "Summary",
                "existing_sections": [],
                "sections_to_fill": ["Introduction"],
            },
        ),
        ("/api/frameworks/sync-library", {}),
        ("/api/frameworks/log-event", {"type": "framework_viewed"}),
        ("/api/frameworks/push-framework", {"framework": MINIMAL_FRAMEWORK}),
    ],
)
@pytest.mark.asyncio
async def test_framework_hardening_endpoints_require_auth(app, path, payload):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(path, json=payload)

    assert_auth_required(response)


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/api/frameworks/sync-library", {}),
        ("/api/frameworks/log-event", {"type": "framework_viewed"}),
        ("/api/frameworks/push-framework", {"framework": MINIMAL_FRAMEWORK}),
    ],
)
@pytest.mark.asyncio
async def test_vector_sync_endpoints_defer_to_phase9_after_auth(app, path, payload):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(path, json=payload, headers=auth_headers())

    assert response.status_code == 501
    detail = response.json()["detail"]
    assert "Phase 9" in detail
    assert "deferred" in detail.lower()


@pytest.mark.parametrize(
    "path",
    [
        "/api/users/check-email/test@example.com",
        "/api/users/check-username/test-user",
    ],
)
@pytest.mark.asyncio
async def test_user_availability_endpoints_require_auth(app, path):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(path)

    assert_auth_required(response)


@pytest.mark.asyncio
async def test_materials_ping_remains_public(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get("/materials/ping")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        ("get", "/materials/mat_test", {}),
        ("post", "/materials/ingest-text", {"json": {"text": "hello"}}),
        (
            "post",
            "/materials/upload-file",
            {"files": {"file": ("test.txt", b"hello", "text/plain")}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_materials_private_endpoints_require_auth(app, method, path, kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await getattr(client, method)(path, **kwargs)

    assert_auth_required(response)
