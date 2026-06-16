from datetime import datetime, timedelta

import httpx
import pytest
from fastapi import FastAPI

from app.api.frameworks import router as frameworks_router
from app.auth import create_access_token
from app.db import get_db
from app.models import Framework, User


BASE_TIME = datetime(2026, 1, 1, 12, 0, 0)


def auth_headers(user_id: str) -> dict[str, str]:
    token = create_access_token({"sub": user_id})
    return {"Authorization": f"Bearer {token}"}


def make_framework(
    framework_id: str,
    creator_id: str,
    *,
    title: str,
    family: str = "Other",
    created_offset: int = 0,
) -> Framework:
    now = BASE_TIME + timedelta(seconds=created_offset)
    return Framework(
        id=framework_id,
        title=title,
        version="1.0.0",
        family=family,
        confidence=80.0,
        pov="owner-pov",
        creator_id=creator_id,
        metadata_json={"title": title, "version": "1.0.0"},
        steps_json=[{"id": "step-1", "name": "Step"}],
        artefacts_json={
            "additional": [{"name": "Brief", "description": "Native JSON artefact"}]
        },
        risks_json=[{"id": "risk-1"}],
        escalation_json=[{"id": "esc-1"}],
        raw_framework_json={"pov": "owner-pov"},
        raw_metadata_json={"source": "test"},
        created_at=now,
        updated_at=now,
    )


def make_user(user_id: str) -> User:
    return User(
        id=user_id,
        email=f"{user_id}@example.com",
        username=user_id,
        password_hash="not-used-in-this-test",
        is_disabled=False,
        disabled_at=None,
        created_at=BASE_TIME,
    )


class FakeFrameworkQuery:
    def __init__(self, frameworks: list[Framework]):
        self.frameworks = frameworks

    def filter(self, *conditions):
        for condition in conditions:
            key = getattr(getattr(condition, "left", None), "key", None)
            expected = getattr(getattr(condition, "right", None), "value", None)
            if key is None:
                continue
            self.frameworks = [
                framework
                for framework in self.frameworks
                if getattr(framework, key) == expected
            ]
        return self

    def order_by(self, *_args):
        self.frameworks = sorted(
            self.frameworks,
            key=lambda framework: framework.created_at,
            reverse=True,
        )
        return self

    def all(self):
        return list(self.frameworks)

    def first(self):
        return self.frameworks[0] if self.frameworks else None


class FakeFrameworkDB:
    def __init__(self, frameworks: list[Framework] | None = None):
        self.frameworks = {framework.id: framework for framework in frameworks or []}
        creator_ids = {framework.creator_id for framework in frameworks or []}
        self.users = {user_id: make_user(user_id) for user_id in creator_ids}
        self.added: list[Framework] = []
        self.deleted: list[str] = []
        self.commits = 0

    def query(self, model):
        if model is Framework:
            return FakeFrameworkQuery(list(self.frameworks.values()))
        if model is User:
            return FakeFrameworkQuery(list(self.users.values()))
        raise AssertionError(f"Unexpected model query: {model}")

    def add(self, framework):
        self.frameworks[framework.id] = framework
        self.added.append(framework)

    def commit(self):
        self.commits += 1

    def refresh(self, _framework):
        pass

    def delete(self, framework):
        self.deleted.append(framework.id)
        self.frameworks.pop(framework.id, None)


@pytest.fixture
def fake_db() -> FakeFrameworkDB:
    return FakeFrameworkDB(
        [
            make_framework(
                "fw_user_a",
                "user_a",
                title="A Framework",
                family="Technology",
                created_offset=10,
            ),
            make_framework(
                "fw_user_b",
                "user_b",
                title="B Framework",
                family="Financial",
            ),
        ]
    )


@pytest.fixture
def app(fake_db):
    app = FastAPI()
    app.include_router(frameworks_router)
    app.dependency_overrides[get_db] = lambda: fake_db
    return app


@pytest.mark.asyncio
async def test_create_framework_uses_jwt_owner_and_native_json(app, fake_db):
    payload = {
        "title": "Created From REST",
        "version": "2.0.0",
        "confidence": 91,
        "metadata": {"title": "Created From Metadata", "version": "2.0.0"},
        "steps": [{"id": "step-1", "name": "Plan"}],
        "artefacts": {
            "additional": [{"name": "Brief", "description": "Native JSONB value"}]
        },
        "risks": [{"id": "risk-1", "name": "Risk"}],
        "escalation": [{"id": "esc-1", "trigger": "Escalate"}],
        "_raw": {"pov": "operator", "nested": {"items": [1, 2]}},
        "creatorId": "user_b",
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/frameworks",
            json=payload,
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 200
    created_id = response.json()["framework_id"]
    created = fake_db.frameworks[created_id]
    assert created.creator_id == "user_a"
    assert created.family == "Other"
    assert created.metadata_json == payload["metadata"]
    assert created.steps_json == payload["steps"]
    assert created.artefacts_json == payload["artefacts"]
    assert created.risks_json == payload["risks"]
    assert created.escalation_json == payload["escalation"]
    assert created.raw_framework_json == payload["_raw"]
    assert not isinstance(created.metadata_json, str)
    assert not isinstance(created.steps_json, str)
    assert not isinstance(created.raw_framework_json, str)


@pytest.mark.parametrize("owner_field", ["user_id", "creator_id"])
@pytest.mark.asyncio
async def test_create_framework_rejects_snake_case_owner_fields(
    app,
    owner_field,
):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/frameworks",
            json={
                "metadata": {"title": "Forbidden Owner Field"},
                owner_field: "user_b",
            },
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_current_user_list_and_by_family_are_owner_scoped(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        list_response = await client.get(
            "/api/frameworks/my-frameworks?user_id=user_b",
            headers=auth_headers("user_a"),
        )
        family_response = await client.get(
            "/api/frameworks/my-frameworks/by-family?user_id=user_b",
            headers=auth_headers("user_a"),
        )

    assert list_response.status_code == 200
    assert [framework["id"] for framework in list_response.json()] == ["fw_user_a"]
    assert family_response.status_code == 200
    assert family_response.json() == {
        "Technology": [
            {
                "id": "fw_user_a",
                "title": "A Framework",
                "version": "1.0.0",
                "family": "Technology",
                "confidence": 80.0,
                "created_at": fake_datetime_iso(10),
                "updated_at": fake_datetime_iso(10),
                "preview_artefacts": [
                    {
                        "name": "Brief",
                        "description": "Native JSON artefact",
                    }
                ],
            }
        ]
    }


def fake_datetime_iso(created_offset: int) -> str:
    return (BASE_TIME + timedelta(seconds=created_offset)).isoformat()


@pytest.mark.asyncio
async def test_get_binding_update_and_delete_require_owner(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        forbidden_get = await client.get(
            "/api/frameworks/fw_user_a",
            headers=auth_headers("user_b"),
        )
        forbidden_binding = await client.get(
            "/api/frameworks/fw_user_a/binding",
            headers=auth_headers("user_b"),
        )
        forbidden_update = await client.put(
            "/api/frameworks/fw_user_a",
            json={"metadata": {"title": "Stolen"}},
            headers=auth_headers("user_b"),
        )
        forbidden_delete = await client.delete(
            "/api/frameworks/fw_user_a",
            headers=auth_headers("user_b"),
        )
        assert fake_db.frameworks["fw_user_a"].title == "A Framework"

        owner_detail = await client.get(
            "/api/frameworks/fw_user_a",
            headers=auth_headers("user_a"),
        )
        owner_binding = await client.get(
            "/api/frameworks/fw_user_a/binding",
            headers=auth_headers("user_a"),
        )
        owner_update = await client.put(
            "/api/frameworks/fw_user_a",
            json={
                "metadata": {"title": "Updated Native", "version": "3.0.0"},
                "steps": [{"id": "step-2", "name": "Updated"}],
                "artefacts": {"additional": [{"name": "Updated Brief"}]},
                "risks": [],
                "escalation": [],
                "_raw": '{"pov":"updated-pov"}',
            },
            headers=auth_headers("user_a"),
        )

    assert forbidden_get.status_code == 404
    assert forbidden_binding.status_code == 404
    assert forbidden_update.status_code == 404
    assert forbidden_delete.status_code == 404

    assert owner_detail.status_code == 200
    assert owner_detail.json()["metadata"] == {
        "title": "A Framework",
        "version": "1.0.0",
    }
    assert owner_binding.status_code == 200
    assert owner_binding.json()["pov"] == "owner-pov"

    assert owner_update.status_code == 200
    updated = fake_db.frameworks.get("fw_user_a")
    assert updated is not None
    assert updated.title == "Updated Native"
    assert updated.version == "3.0.0"
    assert updated.metadata_json == {"title": "Updated Native", "version": "3.0.0"}
    assert updated.steps_json == [{"id": "step-2", "name": "Updated"}]
    assert updated.artefacts_json == {"additional": [{"name": "Updated Brief"}]}
    assert updated.raw_framework_json == {"pov": "updated-pov"}
    assert not isinstance(updated.metadata_json, str)
    assert not isinstance(updated.steps_json, str)
    assert not isinstance(updated.raw_framework_json, str)

    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        owner_delete = await client.delete(
            "/api/frameworks/fw_user_a",
            headers=auth_headers("user_a"),
        )

    assert owner_delete.status_code == 200
    assert "fw_user_a" not in fake_db.frameworks
