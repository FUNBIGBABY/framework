import copy

import httpx
import pytest
from fastapi import FastAPI, HTTPException

from app.api import frameworks_shared
from app.api.frameworks import router as frameworks_router
from app.auth import create_access_token
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


def make_user(user_id: str) -> User:
    return User(
        id=user_id,
        email=f"{user_id}@example.com",
        username=user_id,
        password_hash="not-used-in-this-test",
        is_disabled=False,
        disabled_at=None,
    )


class FakeGenerationDB:
    def __init__(self):
        self.added = []
        self.commits = 0
        self.users = {
            user_id: make_user(user_id)
            for user_id in ["user_text", "user_file", "user_files"]
        }

    def query(self, model):
        if model is User:
            return FakeUserQuery(list(self.users.values()))
        raise AssertionError(f"Unexpected model query: {model}")

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.commits += 1

    def refresh(self, _obj):
        pass


@pytest.fixture
def fake_db():
    return FakeGenerationDB()


@pytest.fixture
def app(fake_db):
    app = FastAPI()
    app.include_router(frameworks_router)
    app.dependency_overrides[get_db] = lambda: fake_db
    return app


def auth_headers(user_id: str) -> dict[str, str]:
    token = create_access_token({"sub": user_id})
    return {"Authorization": f"Bearer {token}"}


def framework_payload(title: str, *, family: str = "Technology") -> dict:
    return {
        "metadata": {"title": title, "version": "1.0.0"},
        "steps": [{"id": "step-1", "name": "Plan"}],
        "artefacts": {"additional": [{"name": "Brief"}]},
        "risks": [{"id": "risk-1"}],
        "escalation": [{"id": "esc-1"}],
        "family": family,
        "confidence": 88.0,
        "pov": "operator",
    }


def install_fake_provider(monkeypatch, provider_result):
    captured = {}
    monkeypatch.setenv("ENV", "production")

    class FakeProvider:
        name = "deepseek"

        def generate_json(self, messages, **kwargs):
            captured["messages"] = list(messages)
            captured["kwargs"] = kwargs
            return copy.deepcopy(provider_result)

    monkeypatch.setattr(frameworks_shared, "get_llm_provider", lambda: FakeProvider())
    return captured


@pytest.mark.asyncio
async def test_generate_from_text_saves_owned_framework_and_returns_id(
    app, fake_db, monkeypatch
):
    captured = install_fake_provider(
        monkeypatch,
        framework_payload("Generated Text Framework"),
    )

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/frameworks/generate-from-text",
            json={
                "text": "Generated Text Framework\nStep one\nStep two",
                "creator_id": "attacker",
                "user_id": "attacker",
            },
            headers=auth_headers("user_text"),
        )

    assert response.status_code == 200
    body = response.json()
    saved = fake_db.added[0]

    assert body["success"] is True
    assert body["framework_id"] == saved.id
    assert body["framework_ids"] == [saved.id]
    assert body["framework"]["id"] == saved.id
    assert saved.creator_id == "user_text"
    assert saved.metadata_json == {"title": "Generated Text Framework", "version": "1.0.0"}
    assert saved.steps_json == [{"id": "step-1", "name": "Plan"}]
    assert saved.raw_metadata_json["title"] == "Generated Text Framework"
    assert not isinstance(saved.metadata_json, str)
    assert not isinstance(saved.steps_json, str)
    assert captured["kwargs"]["reasoning"] is False


@pytest.mark.asyncio
async def test_generate_from_file_deterministic_metadata_saves_framework(
    app, fake_db, monkeypatch
):
    install_fake_provider(monkeypatch, framework_payload("Generated File Framework"))

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/frameworks/generate-from-file",
            files={
                "file": (
                    "roadmap.txt",
                    b"Roadmap Planning Framework\nStep one\nStep two",
                    "text/plain",
                )
            },
            data={"creator_id": "attacker", "user_id": "attacker"},
            headers=auth_headers("user_file"),
        )

    assert response.status_code == 200
    body = response.json()
    saved = fake_db.added[0]

    assert body["framework_id"] == saved.id
    assert body["framework_ids"] == [saved.id]
    assert saved.creator_id == "user_file"
    assert saved.raw_metadata_json["extra"]["processing_mode"] == "direct_file_metadata"
    assert {"key": "processing_mode", "value": "direct_file_metadata"} in saved.raw_metadata_json[
        "key_values"
    ]
    assert not isinstance(saved.raw_metadata_json, str)
    assert not isinstance(saved.artefacts_json, str)


@pytest.mark.asyncio
async def test_generate_from_files_saves_all_frameworks_and_returns_ids(
    app, fake_db, monkeypatch
):
    install_fake_provider(
        monkeypatch,
        {
            "frameworks": [
                framework_payload("First Generated Framework", family="Operations"),
                framework_payload("Second Generated Framework", family="Strategy"),
            ]
        },
    )

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/frameworks/generate-from-files",
            files=[
                (
                    "files",
                    (
                        "first.txt",
                        b"First Uploaded Framework\nStep one",
                        "text/plain",
                    ),
                ),
                (
                    "files",
                    (
                        "second.txt",
                        b"Second Uploaded Framework\nStep two",
                        "text/plain",
                    ),
                ),
            ],
            data={"creator_id": "attacker"},
            headers=auth_headers("user_files"),
        )

    assert response.status_code == 200
    body = response.json()
    saved_ids = [framework.id for framework in fake_db.added]

    assert len(fake_db.added) == 2
    assert body["framework_id"] == saved_ids[0]
    assert body["framework_ids"] == saved_ids
    assert [framework["id"] for framework in body["frameworks"]] == saved_ids
    assert {framework.creator_id for framework in fake_db.added} == {"user_files"}
    assert all(not isinstance(framework.metadata_json, str) for framework in fake_db.added)
    assert all(isinstance(framework.steps_json, list) for framework in fake_db.added)
    assert fake_db.added[0].raw_metadata_json["extra"]["processing_mode"] == (
        "direct_file_metadata"
    )
    assert fake_db.added[0].raw_metadata_json["source_files"] == [
        "first.txt",
        "second.txt",
    ]


@pytest.mark.asyncio
async def test_generation_routes_require_auth(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        text_response = await client.post(
            "/api/frameworks/generate-from-text",
            json={"text": "hello"},
        )
        file_response = await client.post(
            "/api/frameworks/generate-from-file",
            files={"file": ("one.txt", b"hello", "text/plain")},
        )
        files_response = await client.post(
            "/api/frameworks/generate-from-files",
            files=[("files", ("one.txt", b"hello", "text/plain"))],
        )

    assert text_response.status_code in {401, 403}
    assert file_response.status_code in {401, 403}
    assert files_response.status_code in {401, 403}


def test_mock_generation_is_rejected_in_production_without_dry_run(monkeypatch):
    monkeypatch.setenv("ENV", "production")

    with pytest.raises(HTTPException) as exc:
        frameworks_shared.process_with_global_llm(
            {"title": "Production Input"},
            use_mock=True,
        )

    assert exc.value.status_code == 503
    assert "ENV=dev" in exc.value.detail


def test_mock_generation_is_allowed_for_explicit_dry_run(monkeypatch):
    monkeypatch.setenv("ENV", "production")

    result = frameworks_shared.process_with_global_llm(
        {"title": "Dry Run Input"},
        use_mock=True,
        dry_run=True,
    )

    assert result["metadata"]["title"] == "Dry Run Input"
    assert 60 <= result["confidence"] <= 95
