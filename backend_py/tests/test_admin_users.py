from datetime import datetime, timedelta

import httpx
import pytest
from fastapi import FastAPI

from app.api.admin_users import router as admin_users_router
from app.api.frameworks import router as frameworks_router
from app.api.users import router as users_router
from app.auth import (
    ACCESS_COOKIE_NAME,
    ARGON2ID_PREFIX,
    create_access_token,
    hash_password,
)
from app.db import get_db
from app.models import Artefact, Framework, User


BASE_TIME = datetime(2026, 1, 1, 12, 0, 0)


def auth_headers(user_id: str) -> dict[str, str]:
    token = create_access_token({"sub": user_id})
    return {"Cookie": f"{ACCESS_COOKIE_NAME}={token}"}


def make_user(
    user_id: str,
    email: str,
    username: str,
    password: str,
    *,
    created_offset: int = 0,
    is_disabled: bool = False,
) -> User:
    created_at = BASE_TIME + timedelta(seconds=created_offset)
    return User(
        id=user_id,
        email=email,
        username=username,
        password_hash=hash_password(password),
        is_disabled=is_disabled,
        disabled_at=created_at if is_disabled else None,
        created_at=created_at,
        last_login=None,
    )


def _condition_matches(user: User, condition) -> bool:
    key = getattr(getattr(condition, "left", None), "key", None)
    operator_name = getattr(getattr(condition, "operator", None), "__name__", "")
    expected = getattr(getattr(condition, "right", None), "value", None)

    if key is None:
        return True
    if operator_name == "eq":
        return getattr(user, key) == expected
    return True


class FakeUserQuery:
    def __init__(self, users: list[User]):
        self.users = list(users)

    def filter(self, *conditions):
        self.users = [
            user
            for user in self.users
            if all(_condition_matches(user, condition) for condition in conditions)
        ]
        return self

    def order_by(self, *_args):
        self.users = sorted(
            self.users,
            key=lambda user: (user.created_at or datetime.min, user.id),
            reverse=True,
        )
        return self

    def all(self):
        return list(self.users)

    def first(self):
        return self.users[0] if self.users else None


class FakeUserDB:
    def __init__(self):
        self.users = {
            "user_admin": make_user(
                "user_admin",
                "admin@example.com",
                "admin",
                "admin-password",
                created_offset=10,
            ),
            "user_regular": make_user(
                "user_regular",
                "regular@example.com",
                "regular",
                "regular-password",
                created_offset=5,
            ),
        }
        self.added: list[User] = []
        self.commits = 0

    def query(self, model):
        if model is User:
            return FakeUserQuery(list(self.users.values()))
        if model in {Framework, Artefact}:
            return FakeUserQuery([])
        raise AssertionError(f"Unexpected model query: {model}")

    def add(self, user: User):
        self.users[user.id] = user
        self.added.append(user)

    def commit(self):
        self.commits += 1

    def refresh(self, _user):
        pass


@pytest.fixture
def fake_db():
    return FakeUserDB()


@pytest.fixture
def app(fake_db, monkeypatch):
    monkeypatch.setenv("SUPER_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.delenv("ALLOWED_EMAILS", raising=False)
    monkeypatch.setenv("ENABLE_PUBLIC_REGISTER", "false")

    app = FastAPI()
    app.include_router(admin_users_router)
    app.include_router(users_router)
    app.include_router(frameworks_router)
    app.dependency_overrides[get_db] = lambda: fake_db
    return app


@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        ("get", "/api/admin/users", {}),
        (
            "post",
            "/api/admin/users",
            {
                "json": {
                    "email": "new@example.com",
                    "username": "new_user",
                    "password": "new-password",
                }
            },
        ),
        ("post", "/api/admin/users/user_regular/disable", {}),
        ("post", "/api/admin/users/user_regular/enable", {}),
    ],
)
@pytest.mark.asyncio
async def test_admin_user_endpoints_require_auth(app, method, path, kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await getattr(client, method)(path, **kwargs)

    assert response.status_code in {401, 403}


@pytest.mark.asyncio
async def test_non_admin_cannot_access_admin_users(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/admin/users",
            headers=auth_headers("user_regular"),
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_super_admin_can_list_users_without_password_hash(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.get(
            "/api/admin/users",
            headers=auth_headers("user_admin"),
        )

    assert response.status_code == 200
    users = response.json()
    assert [user["id"] for user in users] == ["user_admin", "user_regular"]
    assert all("password_hash" not in user for user in users)
    assert users[0]["is_super_admin"] is True
    assert users[1]["is_super_admin"] is False


@pytest.mark.asyncio
async def test_super_admin_can_create_user_with_hashed_password(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/admin/users",
            json={
                "email": "outside-allowlist@example.net",
                "username": "outside_user",
                "password": "plain-password",
            },
            headers=auth_headers("user_admin"),
        )

    assert response.status_code == 201
    body = response.json()
    assert "password_hash" not in body
    assert body["email"] == "outside-allowlist@example.net"
    assert body["is_disabled"] is False

    created = fake_db.added[0]
    assert created.password_hash != "plain-password"
    assert created.password_hash.startswith(ARGON2ID_PREFIX)
    assert created.is_disabled is False
    assert created.disabled_at is None


@pytest.mark.asyncio
async def test_admin_create_user_does_not_accept_password_hash(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/admin/users",
            json={
                "email": "hash-field@example.com",
                "username": "hash_field",
                "password": "plain-password",
                "password_hash": "attacker-controlled",
            },
            headers=auth_headers("user_admin"),
        )

    assert response.status_code == 422
    assert fake_db.added == []


@pytest.mark.asyncio
async def test_public_register_remains_disabled_by_default(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/users/register",
            json={
                "email": "public@example.com",
                "username": "public_user",
                "password": "public-password",
            },
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_disable_and_enable_controls_login_and_me(app, fake_db):
    already_issued_regular_token = auth_headers("user_regular")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        disable_response = await client.post(
            "/api/admin/users/user_regular/disable",
            headers=auth_headers("user_admin"),
        )
        disabled_login = await client.post(
            "/api/users/login",
            json={
                "email": "regular@example.com",
                "password": "regular-password",
            },
        )
        disabled_me = await client.get(
            "/api/users/me",
            headers=already_issued_regular_token,
        )
        disabled_my_frameworks = await client.get(
            "/api/frameworks/my-frameworks",
            headers=already_issued_regular_token,
        )
        disabled_public_frameworks = await client.get(
            "/api/frameworks/public",
            headers=already_issued_regular_token,
        )
        disabled_artefacts = await client.get(
            "/api/frameworks/fw_owner/artefacts",
            headers=already_issued_regular_token,
        )
        disabled_vector_sync = await client.post(
            "/api/frameworks/push-framework",
            json={"framework": {"metadata": {"title": "Blocked"}}},
            headers=already_issued_regular_token,
        )
        disabled_flag_after_disable = fake_db.users["user_regular"].is_disabled
        disabled_at_after_disable = fake_db.users["user_regular"].disabled_at
        enable_response = await client.post(
            "/api/admin/users/user_regular/enable",
            headers=auth_headers("user_admin"),
        )
        enabled_login = await client.post(
            "/api/users/login",
            json={
                "email": "regular@example.com",
                "password": "regular-password",
            },
        )
        enabled_me = await client.get(
            "/api/users/me",
            headers=already_issued_regular_token,
        )
        enabled_my_frameworks = await client.get(
            "/api/frameworks/my-frameworks",
            headers=already_issued_regular_token,
        )

    assert disable_response.status_code == 200
    assert disable_response.json()["is_disabled"] is True
    assert disabled_flag_after_disable is True
    assert disabled_at_after_disable is not None

    assert disabled_login.status_code == 403
    assert disabled_me.status_code == 403
    assert disabled_my_frameworks.status_code == 403
    assert disabled_public_frameworks.status_code == 403
    assert disabled_artefacts.status_code == 403
    assert disabled_vector_sync.status_code == 403

    assert enable_response.status_code == 200
    assert enable_response.json()["is_disabled"] is False
    assert fake_db.users["user_regular"].is_disabled is False
    assert fake_db.users["user_regular"].disabled_at is None

    assert enabled_login.status_code == 200
    assert enabled_login.json()["user"]["id"] == "user_regular"
    assert enabled_me.status_code == 200
    assert enabled_me.json()["id"] == "user_regular"
    assert enabled_my_frameworks.status_code == 200
    assert enabled_my_frameworks.json() == []


@pytest.mark.asyncio
async def test_super_admin_cannot_disable_self(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        response = await client.post(
            "/api/admin/users/user_admin/disable",
            headers=auth_headers("user_admin"),
        )

    assert response.status_code == 400
    assert fake_db.users["user_admin"].is_disabled is False
