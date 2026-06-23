import os
from datetime import datetime, timedelta

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-for-cookie-sessions-32-chars")

import httpx
import pytest

from app.auth import (
    ACCESS_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
    create_access_token,
    create_refresh_token,
    hash_password,
)
from app.db import get_db
from app.models import User


BASE_TIME = datetime(2026, 1, 1, 12, 0, 0)
SAME_ORIGIN = "http://testserver"


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
        refresh_token_version=0,
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

    def first(self):
        return self.users[0] if self.users else None


class FakeCookieSessionDB:
    def __init__(self):
        self.users = {
            "user_cookie": make_user(
                "user_cookie",
                "cookie@example.com",
                "cookie_user",
                "cookie-password",
            ),
            "user_disabled": make_user(
                "user_disabled",
                "disabled@example.com",
                "disabled_user",
                "disabled-password",
                is_disabled=True,
            ),
        }
        self.commits = 0

    def query(self, model):
        if model is User:
            return FakeUserQuery(list(self.users.values()))
        raise AssertionError(f"Unexpected model query: {model}")

    def commit(self):
        self.commits += 1

    def refresh(self, _user):
        pass


@pytest.fixture
def fake_db():
    return FakeCookieSessionDB()


@pytest.fixture
def app(fake_db, monkeypatch):
    monkeypatch.setenv("AUTH_COOKIE_SECURE", "false")
    monkeypatch.setenv("AUTH_COOKIE_SAMESITE", "lax")
    monkeypatch.setenv("SUPER_ADMIN_EMAIL", "admin@example.com")

    import main

    main.app.dependency_overrides[get_db] = lambda: fake_db
    yield main.app
    main.app.dependency_overrides.clear()


async def login(client: httpx.AsyncClient, email: str = "cookie@example.com"):
    return await client.post(
        "/api/users/login",
        json={"email": email, "password": "cookie-password"},
    )


def _set_cookie_headers(response: httpx.Response) -> str:
    return "\n".join(response.headers.get_list("set-cookie"))


def _access_token(user_id: str = "user_cookie") -> str:
    return create_access_token(
        {
            "sub": user_id,
            "email": "cookie@example.com",
            "username": "cookie_user",
        }
    )


def _refresh_token(user_id: str = "user_cookie", version: int = 0) -> str:
    return create_refresh_token(
        {
            "sub": user_id,
            "email": "cookie@example.com",
            "username": "cookie_user",
            "ver": version,
        }
    )


@pytest.mark.asyncio
async def test_login_sets_http_only_access_and_refresh_cookies(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        response = await login(client)

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["user"]["id"] == "user_cookie"

    set_cookie = _set_cookie_headers(response)
    assert f"{ACCESS_COOKIE_NAME}=" in set_cookie
    assert f"{REFRESH_COOKIE_NAME}=" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "SameSite=lax" in set_cookie
    assert "Max-Age=3600" in set_cookie
    assert "Max-Age=2592000" in set_cookie


@pytest.mark.asyncio
async def test_production_auth_cookies_are_secure(app, monkeypatch):
    monkeypatch.setenv("AUTH_COOKIE_SECURE", "false")
    monkeypatch.setenv("ENV", "production")

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        response = await login(client)

    assert response.status_code == 200
    assert "Secure" in _set_cookie_headers(response)


@pytest.mark.asyncio
async def test_samesite_none_config_is_clamped_to_lax(app, monkeypatch):
    monkeypatch.setenv("AUTH_COOKIE_SAMESITE", "none")

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        response = await login(client)

    set_cookie = _set_cookie_headers(response)
    assert response.status_code == 200
    assert "SameSite=lax" in set_cookie
    assert "SameSite=none" not in set_cookie


@pytest.mark.asyncio
async def test_me_and_refresh_work_with_cookie_auth_without_bearer(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        login_response = await login(client)
        me_response = await client.get("/api/users/me")
        refresh_response = await client.post(
            "/api/users/refresh",
            headers={"Origin": SAME_ORIGIN},
        )

    assert login_response.status_code == 200
    assert me_response.status_code == 200
    assert me_response.json()["id"] == "user_cookie"
    assert refresh_response.status_code == 200
    assert refresh_response.json()["user"]["id"] == "user_cookie"
    assert f"{ACCESS_COOKIE_NAME}=" in _set_cookie_headers(refresh_response)


@pytest.mark.asyncio
async def test_refresh_token_cannot_authenticate_protected_endpoint_access_cookie(app):
    refresh_token = _refresh_token()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        response = await client.get(
            "/api/users/me",
            headers={"Cookie": f"{ACCESS_COOKIE_NAME}={refresh_token}"},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_cannot_authenticate_protected_endpoint_bearer_path(app):
    refresh_token = _refresh_token()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        response = await client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_token_still_authenticates_protected_endpoints(app):
    access_token = _access_token()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        cookie_response = await client.get(
            "/api/users/me",
            headers={"Cookie": f"{ACCESS_COOKIE_NAME}={access_token}"},
        )
        bearer_response = await client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    assert cookie_response.status_code == 200
    assert cookie_response.json()["id"] == "user_cookie"
    assert bearer_response.status_code == 200
    assert bearer_response.json()["id"] == "user_cookie"


@pytest.mark.asyncio
async def test_refresh_endpoint_accepts_only_refresh_token(app):
    access_token = _access_token()
    refresh_token = _refresh_token()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        access_response = await client.post(
            "/api/users/refresh",
            headers={
                "Cookie": f"{REFRESH_COOKIE_NAME}={access_token}",
                "Origin": SAME_ORIGIN,
            },
        )
        refresh_response = await client.post(
            "/api/users/refresh",
            headers={
                "Cookie": f"{REFRESH_COOKIE_NAME}={refresh_token}",
                "Origin": SAME_ORIGIN,
            },
        )

    assert access_response.status_code == 401
    assert refresh_response.status_code == 200
    assert refresh_response.json()["user"]["id"] == "user_cookie"


@pytest.mark.asyncio
async def test_logout_clears_cookies_and_revokes_refresh_session(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        login_response = await login(client)
        old_refresh = login_response.cookies.get(REFRESH_COOKIE_NAME)
        logout_response = await client.post(
            "/api/users/logout",
            headers={"Origin": SAME_ORIGIN},
        )

    assert logout_response.status_code == 200
    assert ACCESS_COOKIE_NAME not in client.cookies
    assert REFRESH_COOKIE_NAME not in client.cookies
    assert fake_db.users["user_cookie"].refresh_token_version == 1

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as stale_client:
        stale_refresh = await stale_client.post(
            "/api/users/refresh",
            headers={
                "Cookie": f"{REFRESH_COOKIE_NAME}={old_refresh}",
                "Origin": SAME_ORIGIN,
            },
        )

    assert stale_refresh.status_code == 401


@pytest.mark.asyncio
async def test_disabled_users_cannot_refresh_or_access_with_cookie_auth(app, fake_db):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        login_response = await login(client)
        fake_db.users["user_cookie"].is_disabled = True
        disabled_me = await client.get("/api/users/me")
        disabled_refresh = await client.post(
            "/api/users/refresh",
            headers={"Origin": SAME_ORIGIN},
        )

    assert login_response.status_code == 200
    assert disabled_me.status_code == 403
    assert disabled_refresh.status_code == 403


@pytest.mark.asyncio
async def test_disabled_users_cannot_login(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        response = await client.post(
            "/api/users/login",
            json={"email": "disabled@example.com", "password": "disabled-password"},
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cookie_auth_unsafe_method_requires_origin_or_referer(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url=SAME_ORIGIN
    ) as client:
        await login(client)

        missing_origin = await client.post("/api/users/refresh")
        invalid_referer = await client.post(
            "/api/users/refresh",
            headers={"Referer": "not-a-url"},
        )
        disallowed_origin = await client.post(
            "/api/users/refresh",
            headers={"Origin": "https://evil.example"},
        )
        allowed_origin = await client.post(
            "/api/users/refresh",
            headers={"Origin": SAME_ORIGIN},
        )
        allowed_referer = await client.post(
            "/api/users/refresh",
            headers={"Referer": f"{SAME_ORIGIN}/settings"},
        )
        safe_get = await client.get(
            "/api/users/me",
            headers={"Origin": "https://evil.example"},
        )

    assert missing_origin.status_code == 403
    assert invalid_referer.status_code == 403
    assert disallowed_origin.status_code == 403
    assert allowed_origin.status_code == 200
    assert allowed_referer.status_code == 200
    assert safe_get.status_code == 200
