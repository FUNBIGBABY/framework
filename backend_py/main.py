import re
import asyncio
import os
from pathlib import Path

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

from app.db import SessionLocal
from app.api.materials import router as materials_router
from app.api.frameworks import router as frameworks_router
from app.api.users import router as users_router
from app.api.frameworks import sync_library, SyncLibraryRequest


app = FastAPI(title="Valorie Framework Builder API")

# ================= 🆕 Custom CORS configuration (multi-domain support) =================
ALLOWED_ORIGINS = [
    r"^https://expert\.valorie\.ai$",
    r"^https://[\w-]+\.valorie\.ai$",
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
]


def is_valid_origin(origin: str) -> bool:
    if not origin:
        return False
    for pattern in ALLOWED_ORIGINS:
        if re.match(pattern, origin):
            return True
    return False


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
                            "Content-Type, Authorization, X-Tenant-ID"
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


@app.on_event("startup")
async def schedule_library_sync():
    async def job():
        while True:
            try:
                legacy_vector_enabled = os.getenv(
                    "OPENAI_VECTOR_STORE_ENABLED", "false"
                ).lower() in {"1", "true", "yes", "on"}
                if not legacy_vector_enabled:
                    await asyncio.sleep(60)
                    continue
                req = SyncLibraryRequest(
                    project_id=os.getenv("FIREBASE_PROJECT_ID"),
                    api_key=os.getenv("VITE_FIREBASE_API_KEY")
                    or os.getenv("FIREBASE_API_KEY"),
                    vector_store_id=os.getenv("OPENAI_VECTOR_STORE_LIBRARY"),
                    limit=1000,
                    include_organization=True,
                )
                db = SessionLocal()
                try:
                    sync_library(req, current_user_id="startup-sync", db=db)
                finally:
                    db.close()
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("Library sync failed:", e)
            await asyncio.sleep(60)

    asyncio.create_task(job())
