# ============================================
# Stage 1: Build Frontend
# ============================================
FROM node:18-alpine AS frontend_builder

WORKDIR /frontend_build

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy all frontend source code
COPY frontend/ ./

# Build arguments for environment variables
ARG VITE_API_BASE_URL

# Set environment variables for build
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Build frontend
RUN npm run build

# ============================================
# Stage 2: Python Backend + Frontend Static Files
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend_py/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend_py/ .

# Copy frontend build from stage 1
COPY --from=frontend_builder /frontend_build/dist /app/static/frontend

# Copy entrypoint script
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
