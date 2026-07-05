import os
import re
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

# Load environment variables before importing app routers/auth modules that read
# JWT_SECRET_KEY at import time.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv(BASE_DIR / ".env")

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME
from app.api.admin_users import router as admin_users_router
from app.api.materials import router as materials_router
from app.api.frameworks import router as frameworks_router
from app.api.users import router as users_router


DEFAULT_APP_NAME = "Personal AI Framework Studio"
APP_NAME = os.getenv("APP_NAME", DEFAULT_APP_NAME).strip() or DEFAULT_APP_NAME

app = FastAPI(title=f"{APP_NAME} API")

# ================= Custom CORS configuration =================
LOCAL_DEV_ORIGIN_PATTERNS = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
]


def _split_env_values(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    return [value.strip() for value in raw_value.split(",") if value.strip()]


def _normalize_origin(raw_origin: str) -> str | None:
    value = raw_origin.strip().rstrip("/")
    if not value:
        return None
    if "://" not in value:
        value = f"https://{value}"

    try:
        parsed = urlsplit(value)
    except ValueError:
        return None

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return f"{parsed.scheme}://{parsed.netloc}"


def _build_allowed_origin_patterns() -> list[str]:
    exact_origins: set[str] = set()

    for raw_origin in _split_env_values(os.getenv("FRONTEND_URL")):
        origin = _normalize_origin(raw_origin)
        if origin:
            exact_origins.add(origin)

    for raw_domain in _split_env_values(os.getenv("APP_BASE_DOMAIN")):
        origin = _normalize_origin(raw_domain)
        if origin:
            exact_origins.add(origin)

    patterns = list(LOCAL_DEV_ORIGIN_PATTERNS)
    patterns.extend(rf"^{re.escape(origin)}$" for origin in sorted(exact_origins))
    return patterns


ALLOWED_ORIGIN_PATTERNS = _build_allowed_origin_patterns()


def is_valid_origin(origin: str) -> bool:
    if not origin:
        return False
    for pattern in ALLOWED_ORIGIN_PATTERNS:
        if re.match(pattern, origin):
            return True
    return False


def _request_origin(request: Request) -> str:
    scheme = request.url.scheme
    host = request.headers.get("host") or request.url.netloc
    return f"{scheme}://{host}"


def _origin_from_referer(referer: str) -> str | None:
    try:
        parsed = urlsplit(referer)
    except ValueError:
        return None
    if not parsed.scheme or not parsed.netloc:
        return None
    return f"{parsed.scheme}://{parsed.netloc}"


def _origin_allowed_for_request(origin: str, request: Request) -> bool:
    return origin == _request_origin(request) or is_valid_origin(origin)


class CookieCSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        unsafe_method = request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}
        has_auth_cookie = bool(
            request.cookies.get(ACCESS_COOKIE_NAME)
            or request.cookies.get(REFRESH_COOKIE_NAME)
        )

        if unsafe_method and has_auth_cookie:
            origin = request.headers.get("origin")
            referer = request.headers.get("referer")
            referer_origin = _origin_from_referer(referer) if referer else None

            if origin:
                allowed = _origin_allowed_for_request(origin, request)
            elif referer_origin:
                allowed = _origin_allowed_for_request(referer_origin, request)
            else:
                allowed = False

            if not allowed:
                return JSONResponse(
                    content={"detail": "CSRF origin check failed"},
                    status_code=403,
                )

        return await call_next(request)


class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")

        # OPTIONS preflight request
        if request.method == "OPTIONS":
            if origin and is_valid_origin(origin):
                return JSONResponse(
                    content={},
                    status_code=200,
                    headers={
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": (
                            "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                        ),
                        "Access-Control-Allow-Headers": (
                            "Content-Type, Authorization"
                        ),
                        "Access-Control-Allow-Credentials": "true",
                        "Access-Control-Max-Age": "3600",
                    },
                )

        # Normal request
        response = await call_next(request)

        if origin and is_valid_origin(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Vary"] = "Origin"

        return response


app.add_middleware(CookieCSRFMiddleware)
app.add_middleware(CustomCORSMiddleware)
# ================= 🆕 End =================

# ❌ Remove or comment out this old CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# ================= Health Check =================
@app.get("/health")
def health():
    return {"status": "healthy", "message": "Backend is running!", "version": "1.0.0"}


# ================= Register Routers =================
app.include_router(materials_router)
app.include_router(frameworks_router)
app.include_router(admin_users_router)
app.include_router(users_router)

# ================= Serve Frontend Static Files (Docker mode) =================
static_dir = Path("/app/static/frontend")
if static_dir.exists():
    app.mount(
        "/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets"
    )

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}

        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"detail": "Frontend not found"}

    print("Serving frontend from /app/static/frontend")
else:
    print("Frontend static files not found (development mode)")
