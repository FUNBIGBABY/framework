import importlib


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
