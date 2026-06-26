from datetime import datetime, timedelta

import httpx
import pytest
from fastapi import FastAPI

from app.api.frameworks import router as frameworks_router
from app.auth import ACCESS_COOKIE_NAME, create_access_token
from app.db import get_db
from app.models import Framework, User


BASE_TIME = datetime(2026, 1, 1, 12, 0, 0)


def auth_headers(user_id: str) -> dict[str, str]:
    token = create_access_token({"sub": user_id})
    return {"Cookie": f"{ACCESS_COOKIE_NAME}={token}"}


def make_framework(
    framework_id: str,
    creator_id: str,
    *,
    title: str,
    is_public: bool = False,
    category: str | None = None,
    tags: list[str] | None = None,
    published_offset: int | None = None,
    family: str = "Other",
) -> Framework:
    now = BASE_TIME + timedelta(seconds=published_offset or 0)
    return Framework(
        id=framework_id,
        title=title,
        version="1.0.0",
        family=family,
        confidence=82.5,
        pov="owner-pov",
        is_public=is_public,
        category=category,
        tags_json=tags or [],
        published_at=now if published_offset is not None else None,
        creator_id=creator_id,
        metadata_json={"title": title, "version": "1.0.0", "private": "hidden"},
        steps_json=[{"id": "step-1", "name": "Step"}],
        artefacts_json={
            "additional": [
                {"name": "Brief", "description": "Public preview artefact"},
                {"name": "Raw", "description": "Second preview"},
            ]
        },
        risks_json=[{"id": "risk-1"}],
        escalation_json=[{"id": "esc-1"}],
        raw_framework_json={"secret": "do not expose"},
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


def _condition_expected(condition):
    right = getattr(condition, "right", None)
    if str(right).lower() == "true":
        return True
    return getattr(right, "value", None)


def _condition_matches(framework: Framework, condition) -> bool:
    operator_name = getattr(getattr(condition, "operator", None), "__name__", "")

    if operator_name == "and_":
        return all(_condition_matches(framework, clause) for clause in condition.clauses)
    if operator_name == "or_":
        return any(_condition_matches(framework, clause) for clause in condition.clauses)

    key = getattr(getattr(condition, "left", None), "key", None)
    expected = _condition_expected(condition)
    if key is None:
        return True

    value = getattr(framework, key)
    if operator_name == "eq":
        return value == expected
    if operator_name in {"is_", "is"}:
        return bool(value) is bool(expected)
    if operator_name in {"is_not", "isnot"}:
        return value is not None
    if operator_name == "lt":
        return value < expected
    return True


class FakeFrameworkQuery:
    def __init__(self, frameworks: list[Framework]):
        self.frameworks = frameworks
        self.limit_value: int | None = None

    def filter(self, *conditions):
        for condition in conditions:
            self.frameworks = [
                framework
                for framework in self.frameworks
                if _condition_matches(framework, condition)
            ]
        return self

    def order_by(self, *_args):
        self.frameworks = sorted(
            self.frameworks,
            key=lambda framework: (
                framework.published_at or datetime.min,
                framework.id,
            ),
            reverse=True,
        )
        return self

    def limit(self, limit_value: int):
        self.limit_value = limit_value
        return self

    def all(self):
        if self.limit_value is None:
            return list(self.frameworks)
        return list(self.frameworks[: self.limit_value])

    def first(self):
        return self.frameworks[0] if self.frameworks else None


class FakeFrameworkDB:
    def __init__(self, frameworks: list[Framework] | None = None):
        self.frameworks = {framework.id: framework for framework in frameworks or []}
        creator_ids = {framework.creator_id for framework in frameworks or []}
        self.users = {user_id: make_user(user_id) for user_id in creator_ids}
        self.commits = 0

    def query(self, model):
        if model is Framework:
            return FakeFrameworkQuery(list(self.frameworks.values()))
        if model is User:
            return FakeFrameworkQuery(list(self.users.values()))
        raise AssertionError(f"Unexpected model query: {model}")

    def commit(self):
        self.commits += 1

    def refresh(self, _framework):
        pass


@pytest.fixture
def fake_db() -> FakeFrameworkDB:
    return FakeFrameworkDB(
        [
            make_framework(
                "fw_public_new",
                "user_a",
                title="Newest Public Framework",
                is_public=True,
                category="Technology",
                tags=["ai", "planning"],
                published_offset=20,
                family="Technology",
            ),
            make_framework(
                "fw_unpublished",
                "user_a",
                title="Private Draft Framework",
                is_public=False,
                family="Research",
            ),
            make_framework(
                "fw_public_old",
                "user_b",
                title="Older Public Framework",
                is_public=True,
                category="Financial",
                tags=["finance"],
                published_offset=5,
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
async def test_public_library_requires_auth(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get("/api/frameworks/public")

    assert response.status_code in {401, 403}


@pytest.mark.asyncio
async def test_authenticated_public_library_returns_only_published_simplified_items(
    app,
):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/frameworks/public",
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body["items"]] == [
        "fw_public_new",
        "fw_public_old",
    ]
    assert body["limit"] == 20
    assert body["next_cursor"] is None

    first = body["items"][0]
    assert set(first) == {
        "id",
        "title",
        "version",
        "family",
        "confidence",
        "category",
        "tags",
        "published_at",
        "updated_at",
        "preview_artefacts",
    }
    assert first["category"] == "Technology"
    assert first["tags"] == ["ai", "planning"]
    assert first["preview_artefacts"] == [
        {"name": "Brief", "description": "Public preview artefact"},
        {"name": "Raw", "description": "Second preview"},
    ]
    assert "metadata" not in first
    assert "creator_id" not in first
    assert "raw_framework_json" not in first
    assert "fw_unpublished" not in [item["id"] for item in body["items"]]


@pytest.mark.asyncio
async def test_public_library_blank_limit_is_rejected(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/frameworks/public?limit=",
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_public_library_limit_above_max_is_rejected(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/frameworks/public?limit=51",
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_public_library_second_page_cursor(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        first_page = await client.get(
            "/api/frameworks/public?limit=1",
            headers=auth_headers("user_a"),
        )
        second_page = await client.get(
            "/api/frameworks/public",
            params={"limit": 1, "cursor": first_page.json()["next_cursor"]},
            headers=auth_headers("user_a"),
        )

    assert first_page.status_code == 200
    assert [item["id"] for item in first_page.json()["items"]] == ["fw_public_new"]
    assert first_page.json()["next_cursor"]

    assert second_page.status_code == 200
    assert [item["id"] for item in second_page.json()["items"]] == ["fw_public_old"]
    assert second_page.json()["next_cursor"] is None


@pytest.mark.asyncio
async def test_public_library_invalid_cursor_returns_400(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/frameworks/public",
            params={"cursor": "not-a-valid-cursor"},
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid public library cursor"


@pytest.mark.asyncio
async def test_owner_can_publish_framework_and_public_list_sees_it(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        publish_response = await client.post(
            "/api/frameworks/fw_unpublished/publish",
            json={
                "category": "Research",
                "tags": [" discovery ", "research", "research", ""],
                "version": "2.1.0",
            },
            headers=auth_headers("user_a"),
        )
        library_response = await client.get(
            "/api/frameworks/public",
            headers=auth_headers("user_a"),
        )

    assert publish_response.status_code == 200
    body = publish_response.json()
    framework = fake_db.frameworks["fw_unpublished"]

    assert body["framework_id"] == "fw_unpublished"
    assert body["is_public"] is True
    assert body["category"] == "Research"
    assert body["tags"] == ["discovery", "research"]
    assert framework.is_public is True
    assert framework.version == "2.1.0"
    assert framework.category == "Research"
    assert framework.tags_json == ["discovery", "research"]
    assert framework.published_at is not None
    assert fake_db.commits == 1

    assert library_response.status_code == 200
    assert "fw_unpublished" in [item["id"] for item in library_response.json()["items"]]


@pytest.mark.asyncio
async def test_owner_can_unpublish_framework_and_published_at_is_cleared(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        unpublish_response = await client.post(
            "/api/frameworks/fw_public_new/unpublish",
            headers=auth_headers("user_a"),
        )
        library_response = await client.get(
            "/api/frameworks/public",
            headers=auth_headers("user_a"),
        )

    assert unpublish_response.status_code == 200
    body = unpublish_response.json()
    framework = fake_db.frameworks["fw_public_new"]

    assert body["framework_id"] == "fw_public_new"
    assert body["is_public"] is False
    assert body["published_at"] is None
    assert framework.is_public is False
    assert framework.published_at is None
    assert framework.category == "Technology"
    assert framework.tags_json == ["ai", "planning"]
    assert fake_db.commits == 1

    assert library_response.status_code == 200
    assert "fw_public_new" not in [
        item["id"] for item in library_response.json()["items"]
    ]


@pytest.mark.asyncio
async def test_non_owner_cannot_publish_or_unpublish(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        publish_response = await client.post(
            "/api/frameworks/fw_unpublished/publish",
            json={"category": "Research", "tags": ["blocked"]},
            headers=auth_headers("user_b"),
        )
        unpublish_response = await client.post(
            "/api/frameworks/fw_public_new/unpublish",
            headers=auth_headers("user_b"),
        )

    assert publish_response.status_code == 404
    assert unpublish_response.status_code == 404
    assert fake_db.frameworks["fw_unpublished"].is_public is False
    assert fake_db.frameworks["fw_unpublished"].published_at is None
    assert fake_db.frameworks["fw_public_new"].is_public is True
    assert fake_db.frameworks["fw_public_new"].published_at is not None
    assert fake_db.commits == 0


@pytest.mark.asyncio
async def test_public_route_is_not_swallowed_by_framework_id_route(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/frameworks/public",
            headers=auth_headers("user_a"),
        )

    assert response.status_code == 200
    assert "items" in response.json()
