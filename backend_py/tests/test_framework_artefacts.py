from datetime import datetime, timedelta

import httpx
import pytest
from fastapi import FastAPI

from app.api.frameworks import router as frameworks_router
from app.auth import ACCESS_COOKIE_NAME, create_access_token
from app.db import get_db
from app.models import Artefact, Framework, User


BASE_TIME = datetime(2026, 1, 1, 12, 0, 0)


def auth_headers(user_id: str) -> dict[str, str]:
    token = create_access_token({"sub": user_id})
    return {"Cookie": f"{ACCESS_COOKIE_NAME}={token}"}


def make_framework(framework_id: str, creator_id: str) -> Framework:
    return Framework(
        id=framework_id,
        title=f"{framework_id} title",
        version="1.0.0",
        family="Technology",
        confidence=80.0,
        creator_id=creator_id,
        metadata_json={"title": framework_id},
        steps_json=[],
        artefacts_json={},
        risks_json=[],
        escalation_json=[],
        created_at=BASE_TIME,
        updated_at=BASE_TIME,
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


def make_artefact(
    artefact_id: str,
    framework_id: str,
    *,
    name: str,
    ord: int = 0,
    offset: int = 0,
) -> Artefact:
    now = BASE_TIME + timedelta(seconds=offset)
    return Artefact(
        id=artefact_id,
        framework_id=framework_id,
        name=name,
        artefact_type="custom",
        content_json={"body": name},
        metadata_json={"source": "seed"},
        ord=ord,
        created_at=now,
        updated_at=now,
    )


def _condition_matches(row, condition) -> bool:
    key = getattr(getattr(condition, "left", None), "key", None)
    operator_name = getattr(getattr(condition, "operator", None), "__name__", "")
    expected = getattr(getattr(condition, "right", None), "value", None)

    if key is None:
        return True
    if operator_name == "eq":
        return getattr(row, key) == expected
    return True


class FakeQuery:
    def __init__(self, rows):
        self.rows = list(rows)

    def filter(self, *conditions):
        self.rows = [
            row
            for row in self.rows
            if all(_condition_matches(row, condition) for condition in conditions)
        ]
        return self

    def order_by(self, *_args):
        if self.rows and isinstance(self.rows[0], Artefact):
            self.rows = sorted(
                self.rows,
                key=lambda artefact: (
                    artefact.ord,
                    artefact.created_at or datetime.min,
                    artefact.id,
                ),
            )
        return self

    def all(self):
        return list(self.rows)

    def first(self):
        return self.rows[0] if self.rows else None


class FakeArtefactDB:
    def __init__(self):
        self.frameworks = {
            "fw_owner": make_framework("fw_owner", "user_a"),
            "fw_owner_second": make_framework("fw_owner_second", "user_a"),
            "fw_other": make_framework("fw_other", "user_b"),
        }
        self.users = {
            "user_a": make_user("user_a"),
            "user_b": make_user("user_b"),
        }
        self.artefacts = {
            "art_owner_early": make_artefact(
                "art_owner_early",
                "fw_owner",
                name="Owner Early",
                ord=2,
                offset=1,
            ),
            "art_owner_late": make_artefact(
                "art_owner_late",
                "fw_owner",
                name="Owner Late",
                ord=5,
                offset=2,
            ),
            "art_owner_second": make_artefact(
                "art_owner_second",
                "fw_owner_second",
                name="Second Framework",
                ord=1,
                offset=3,
            ),
            "art_other": make_artefact(
                "art_other",
                "fw_other",
                name="Other User",
                ord=1,
                offset=4,
            ),
        }
        self.added: list[Artefact] = []
        self.deleted: list[str] = []
        self.commits = 0

    def query(self, model):
        if model is Framework:
            return FakeQuery(self.frameworks.values())
        if model is Artefact:
            return FakeQuery(self.artefacts.values())
        if model is User:
            return FakeQuery(self.users.values())
        raise AssertionError(f"Unexpected model query: {model}")

    def add(self, obj):
        if isinstance(obj, Artefact):
            self.artefacts[obj.id] = obj
            self.added.append(obj)
            return
        raise AssertionError(f"Unexpected add: {obj}")

    def commit(self):
        self.commits += 1

    def refresh(self, _obj):
        pass

    def delete(self, obj):
        if isinstance(obj, Artefact):
            self.deleted.append(obj.id)
            self.artefacts.pop(obj.id, None)
            return
        raise AssertionError(f"Unexpected delete: {obj}")


@pytest.fixture
def fake_db():
    return FakeArtefactDB()


@pytest.fixture
def app(fake_db):
    app = FastAPI()
    app.include_router(frameworks_router)
    app.dependency_overrides[get_db] = lambda: fake_db
    return app


@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        ("get", "/api/frameworks/fw_owner/artefacts", {}),
        ("post", "/api/frameworks/fw_owner/artefacts", {"json": {"name": "New"}}),
        ("get", "/api/frameworks/fw_owner/artefacts/art_owner_early", {}),
        (
            "put",
            "/api/frameworks/fw_owner/artefacts/art_owner_early",
            {"json": {"name": "Updated"}},
        ),
        ("delete", "/api/frameworks/fw_owner/artefacts/art_owner_early", {}),
    ],
)
@pytest.mark.asyncio
async def test_artefact_routes_require_auth(app, method, path, kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await getattr(client, method)(path, **kwargs)

    assert response.status_code in {401, 403}


@pytest.mark.asyncio
async def test_owner_can_create_list_get_update_and_delete_artefacts(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        create_response = await client.post(
            "/api/frameworks/fw_owner/artefacts",
            json={
                "name": "Created Artefact",
                "content_json": [{"section": "native list"}],
                "metadata_json": {"kind": "native dict"},
            },
            headers=auth_headers("user_a"),
        )
        created_id = create_response.json()["id"]
        assert create_response.status_code == 201
        created = fake_db.added[0]
        assert created.framework_id == "fw_owner"
        assert created.artefact_type == "custom"
        assert created.ord == 0
        assert created.content_json == [{"section": "native list"}]
        assert created.metadata_json == {"kind": "native dict"}
        assert not isinstance(created.content_json, str)
        assert not isinstance(created.metadata_json, str)

        list_response = await client.get(
            "/api/frameworks/fw_owner/artefacts",
            headers=auth_headers("user_a"),
        )
        get_response = await client.get(
            f"/api/frameworks/fw_owner/artefacts/{created_id}",
            headers=auth_headers("user_a"),
        )
        update_response = await client.put(
            f"/api/frameworks/fw_owner/artefacts/{created_id}",
            json={
                "name": "Updated Artefact",
                "artefact_type": "brief",
                "content_json": {"blocks": [{"text": "native dict"}]},
                "metadata_json": [{"tag": "native list"}],
                "ord": 3,
            },
            headers=auth_headers("user_a"),
        )
        assert update_response.status_code == 200
        updated = fake_db.artefacts[created_id]
        assert updated.name == "Updated Artefact"
        assert updated.artefact_type == "brief"
        assert updated.content_json == {"blocks": [{"text": "native dict"}]}
        assert updated.metadata_json == [{"tag": "native list"}]
        assert updated.ord == 3
        assert not isinstance(updated.content_json, str)
        assert not isinstance(updated.metadata_json, str)

        delete_response = await client.delete(
            f"/api/frameworks/fw_owner/artefacts/{created_id}",
            headers=auth_headers("user_a"),
        )

    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [
        created_id,
        "art_owner_early",
        "art_owner_late",
    ]
    assert get_response.status_code == 200
    assert get_response.json()["content_json"] == [{"section": "native list"}]

    assert delete_response.status_code == 200
    assert created_id not in fake_db.artefacts
    assert fake_db.deleted == [created_id]


@pytest.mark.asyncio
async def test_non_owner_cannot_access_or_mutate_framework_artefacts(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        list_response = await client.get(
            "/api/frameworks/fw_owner/artefacts",
            headers=auth_headers("user_b"),
        )
        create_response = await client.post(
            "/api/frameworks/fw_owner/artefacts",
            json={"name": "Blocked", "content_json": {"x": 1}},
            headers=auth_headers("user_b"),
        )
        get_response = await client.get(
            "/api/frameworks/fw_owner/artefacts/art_owner_early",
            headers=auth_headers("user_b"),
        )
        update_response = await client.put(
            "/api/frameworks/fw_owner/artefacts/art_owner_early",
            json={"name": "Blocked Update"},
            headers=auth_headers("user_b"),
        )
        delete_response = await client.delete(
            "/api/frameworks/fw_owner/artefacts/art_owner_early",
            headers=auth_headers("user_b"),
        )

    assert list_response.status_code == 404
    assert create_response.status_code == 404
    assert get_response.status_code == 404
    assert update_response.status_code == 404
    assert delete_response.status_code == 404
    assert fake_db.added == []
    assert fake_db.deleted == []
    assert fake_db.artefacts["art_owner_early"].name == "Owner Early"


@pytest.mark.asyncio
async def test_artefact_id_must_match_path_framework_id(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        get_response = await client.get(
            "/api/frameworks/fw_owner_second/artefacts/art_owner_early",
            headers=auth_headers("user_a"),
        )
        update_response = await client.put(
            "/api/frameworks/fw_owner_second/artefacts/art_owner_early",
            json={"name": "Cross Framework Update"},
            headers=auth_headers("user_a"),
        )
        delete_response = await client.delete(
            "/api/frameworks/fw_owner_second/artefacts/art_owner_early",
            headers=auth_headers("user_a"),
        )

    assert get_response.status_code == 404
    assert update_response.status_code == 404
    assert delete_response.status_code == 404
    assert fake_db.artefacts["art_owner_early"].framework_id == "fw_owner"
    assert fake_db.artefacts["art_owner_early"].name == "Owner Early"
    assert fake_db.deleted == []


@pytest.mark.parametrize("forbidden_field", ["user_id", "creator_id", "framework_id"])
@pytest.mark.asyncio
async def test_artefact_body_does_not_accept_identity_or_parent_fields(
    app, fake_db, forbidden_field
):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        create_response = await client.post(
            "/api/frameworks/fw_owner/artefacts",
            json={"name": "Blocked", forbidden_field: "attacker"},
            headers=auth_headers("user_a"),
        )
        update_response = await client.put(
            "/api/frameworks/fw_owner/artefacts/art_owner_early",
            json={forbidden_field: "attacker"},
            headers=auth_headers("user_a"),
        )

    assert create_response.status_code == 422
    assert update_response.status_code == 422
    assert fake_db.added == []
    assert fake_db.artefacts["art_owner_early"].name == "Owner Early"


def test_artefact_delete_cascade_contract_is_configured_on_model():
    framework_id_fk = next(
        fk for fk in Artefact.__table__.foreign_keys if fk.parent.name == "framework_id"
    )
    assert framework_id_fk.ondelete == "CASCADE"
    assert "delete-orphan" in Framework.artefact_rows.property.cascade
