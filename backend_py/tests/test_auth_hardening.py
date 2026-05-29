import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-for-auth-hardening-32-chars")

import httpx
import pytest
from fastapi import FastAPI

from app.api.frameworks import router as frameworks_router
from app.api.users import router as users_router


@pytest.fixture(scope="module")
def app():
    app = FastAPI()
    app.include_router(frameworks_router)
    app.include_router(users_router)
    return app


def assert_auth_required(response):
    assert response.status_code in {401, 403}


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
