import importlib.util
from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI

from app.api import materials as materials_api
from app.auth import ACCESS_COOKIE_NAME, create_access_token
from app.db import get_db
from app.models import Material, User


def auth_headers(user_id: str) -> dict[str, str]:
    token = create_access_token({"sub": user_id})
    return {"Cookie": f"{ACCESS_COOKIE_NAME}={token}"}


def make_user(user_id: str) -> User:
    return User(
        id=user_id,
        email=f"{user_id}@example.com",
        username=user_id,
        password_hash="not-used-in-this-test",
        is_disabled=False,
        disabled_at=None,
    )


class FakeQuery:
    def __init__(self, rows):
        self.rows = list(rows)

    def filter(self, *conditions):
        for condition in conditions:
            key = getattr(getattr(condition, "left", None), "key", None)
            expected = getattr(getattr(condition, "right", None), "value", None)
            if key is None:
                continue
            self.rows = [row for row in self.rows if getattr(row, key) == expected]
        return self

    def first(self):
        return self.rows[0] if self.rows else None


class FakeMaterialDB:
    def __init__(self):
        self.users = {user_id: make_user(user_id) for user_id in ("user_a", "user_b")}
        self.materials: dict[str, Material] = {}

    def query(self, model):
        if model is User:
            return FakeQuery(self.users.values())
        if model is Material:
            return FakeQuery(self.materials.values())
        raise AssertionError(f"Unexpected model query: {model}")

    def add(self, material):
        self.materials[material.id] = material

    def commit(self):
        pass

    def refresh(self, _material):
        pass


@pytest.fixture
def fake_db() -> FakeMaterialDB:
    return FakeMaterialDB()


@pytest.fixture
def app(fake_db, monkeypatch):
    async def fake_save_bytes(_payload: bytes, _filename: str) -> str:
        return "memory://material"

    monkeypatch.setattr(materials_api, "save_bytes", fake_save_bytes)
    app = FastAPI()
    app.include_router(materials_api.router)
    app.dependency_overrides[get_db] = lambda: fake_db
    return app


@pytest.mark.parametrize("creation_path", ["upload-file", "ingest-text"])
@pytest.mark.asyncio
async def test_material_creation_and_retrieval_are_owner_isolated(
    app, fake_db, creation_path
):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        if creation_path == "upload-file":
            created_response = await client.post(
                "/materials/upload-file",
                files={"file": ("owned.txt", b"owned by user A", "text/plain")},
                headers=auth_headers("user_a"),
            )
        else:
            created_response = await client.post(
                "/materials/ingest-text",
                json={"text": "owned by user A"},
                headers=auth_headers("user_a"),
            )

        assert created_response.status_code == 200
        material_id = created_response.json()["id"]
        assert fake_db.materials[material_id].owner_id == "user_a"

        owner_response = await client.get(
            f"/materials/{material_id}", headers=auth_headers("user_a")
        )
        other_user_response = await client.get(
            f"/materials/{material_id}", headers=auth_headers("user_b")
        )
        missing_response = await client.get(
            "/materials/mat_missing", headers=auth_headers("user_b")
        )

    assert owner_response.status_code == 200
    assert owner_response.json()["id"] == material_id
    assert other_user_response.status_code == 404
    assert (
        other_user_response.json() == missing_response.json() == {"detail": "not found"}
    )


@pytest.mark.asyncio
async def test_ownerless_legacy_material_is_quarantined(app, fake_db):
    legacy = Material(
        id="mat_legacy",
        type="text",
        status="available",
        mime="text/plain",
        owner_id=None,
    )
    fake_db.materials[legacy.id] = legacy

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response_a = await client.get(
            "/materials/mat_legacy", headers=auth_headers("user_a")
        )
        response_b = await client.get(
            "/materials/mat_legacy", headers=auth_headers("user_b")
        )

    assert response_a.status_code == 404
    assert response_b.status_code == 404


def test_material_owner_migration_refuses_destructive_downgrade():
    migration_path = (
        Path(__file__).resolve().parents[1]
        / "alembic"
        / "versions"
        / "0005_material_owner.py"
    )
    spec = importlib.util.spec_from_file_location(
        "material_owner_migration", migration_path
    )
    assert spec and spec.loader
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)

    with pytest.raises(RuntimeError, match="irreversible"):
        migration.downgrade()
