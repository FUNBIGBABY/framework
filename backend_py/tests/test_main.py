import asyncio
import importlib

from starlette.requests import Request


def _reload_main(monkeypatch, *, app_base_domain="", frontend_url=""):
    monkeypatch.setenv("APP_NAME", "Personal Knowledge Studio")
    monkeypatch.setenv("APP_BASE_DOMAIN", app_base_domain)
    monkeypatch.setenv("FRONTEND_URL", frontend_url)

    import main

    return importlib.reload(main)


def test_app_title_uses_configured_app_name(monkeypatch):
    main = _reload_main(monkeypatch)

    assert main.app.title == "Personal Knowledge Studio API"


def test_cors_allows_localhost_and_configured_base_domain_only(monkeypatch):
    main = _reload_main(monkeypatch, app_base_domain="personal.example.com")

    assert main.is_valid_origin("http://localhost:5173")
    assert main.is_valid_origin("http://127.0.0.1:3000")
    assert main.is_valid_origin("https://personal.example.com")
    assert not main.is_valid_origin("https://workspace.personal.example.com")
    assert not main.is_valid_origin("https://expert.valorie.ai")


def test_cors_allows_explicit_frontend_url(monkeypatch):
    main = _reload_main(monkeypatch, frontend_url="https://app.example.com")

    assert main.is_valid_origin("https://app.example.com")
    assert not main.is_valid_origin("https://evil.example.com")


def test_cors_preflight_omits_legacy_tenant_header(monkeypatch):
    main = _reload_main(monkeypatch)

    request = Request(
        {
            "type": "http",
            "method": "OPTIONS",
            "path": "/api/frameworks",
            "scheme": "http",
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "headers": [
                (b"origin", b"http://localhost:5173"),
                (b"access-control-request-method", b"POST"),
            ],
        }
    )

    async def call_next(_request):
        raise AssertionError("preflight should be handled before call_next")

    middleware = main.CustomCORSMiddleware(main.app)
    response = asyncio.run(middleware.dispatch(request, call_next))

    assert response.status_code == 200
    allowed_headers = response.headers["access-control-allow-headers"]
    assert allowed_headers == "Content-Type, Authorization"
    assert "X-Tenant-ID" not in allowed_headers
