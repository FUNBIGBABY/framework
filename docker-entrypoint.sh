#!/bin/bash
set -e

echo "=========================================="
echo "Starting ${APP_NAME:-Personal AI Framework Studio}"
echo "=========================================="

echo "Environment Configuration:"
echo "  - APP_NAME: ${APP_NAME:-Personal AI Framework Studio}"
echo "  - LLM_PROVIDER: ${LLM_PROVIDER:-not set}"
echo "  - DEEPSEEK_BASE_URL: ${DEEPSEEK_BASE_URL:-not set}"
echo "  - ENABLE_LEGACY_LLM: ${ENABLE_LEGACY_LLM:-false}"
echo "  - PORT: ${PORT:-8000}"

if [ "${ENABLE_LEGACY_LLM:-false}" = "true" ]; then
    echo "Warning: legacy local/cloud LLM path is enabled. Keep this disabled for the personal DeepSeek API migration."
fi

if [ -d "/app/static/frontend" ]; then
    FILE_COUNT=$(find /app/static/frontend -type f | wc -l)
    echo "Frontend static files found ($FILE_COUNT files)"
else
    echo "Warning: Frontend static files not found at /app/static/frontend"
fi

echo "=========================================="
echo "Starting FastAPI server on port ${PORT:-8000}"
echo "=========================================="

exec uvicorn main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --workers "${WORKERS:-1}" \
    --log-level info
