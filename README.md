# Expert Framework Builder

A full-stack application for creating, editing, and managing expert evaluation frameworks using AI assistance.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Project Structure](#project-structure)
- [Documentation](#documentation)

---

## 🔧 Prerequisites
# For more specific info, please read Project-Startup-and-Operation-Flow.md
### Required Software
- **Node.js**: 22.12.0 or higher (use nvm: `nvm use`)
- **Python**: 3.11 or higher (`python --version`)
- **Docker**: Latest version (for containerized deployment)
- **Ollama**: For local LLM support (optional)

### Installation
```bash
# Install Node.js using nvm
nvm install 22.12.0
nvm use 22.12.0

# Verify Python
python --version

# Install Docker
# Visit: https://docs.docker.com/get-docker/
```

---

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up --build
docker-compose up -d
# Access the application
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development
```bash
# Terminal 1: Frontend
cd frontend
npm install
npm run dev
# Access: http://localhost:5173

# Terminal 2: Backend
cd backend_py
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Access: http://localhost:8000
```

---

## 💻 Development Setup

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file (if needed)
cp .env.example .env

# Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:5173`

**Environment Variables** (`.env`):
- `VITE_API_BASE_URL`: Backend API URL
- Firebase configuration (API key, auth domain, etc.)

### Backend Setup
```bash
cd backend_py

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run development server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

**Environment Variables** (`.env`):
- `OPENAI_API_KEY`: OpenAI API key for framework generation
- `ANTHROPIC_API_KEY`: Anthropic API key (optional)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to Firebase credentials

### Local LLM Setup (Optional)
For privacy-protected framework generation:
```bash
# Install Ollama
# Visit: https://ollama.ai/download

# Pull the model
ollama pull llama3.1:8b

# Start Ollama service
ollama serve
```

---

##  Testing

We maintain comprehensive test coverage for both frontend and backend components.

### Test Summary
- **Total Tests**: 31
- **Backend Tests**: 18 (pytest)
- **Frontend Tests**: 13 (vitest)
- **Pass Rate**: 100% ✅

### Backend Tests (18 tests)

**Test Coverage**:
- File processing and validation
- Data structure integrity
- Business logic validation
- Error handling
- Mock external dependencies (Firebase, OpenAI)

**Run tests**:
```bash
cd backend_py

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html  # Mac
# or
start htmlcov/index.html  # Windows
```

**Test Files**:
- `tests/test_file_processing.py` - File handling and data validation (16 tests)
- `tests/test_main.py` - Basic functionality (2 tests)

**Coverage**: 99% for test modules

### Frontend Tests (13 tests)

**Test Coverage**:
- Component rendering verification
- User interaction handling (clicks, inputs, checkboxes)
- Form validation logic
- Conditional rendering
- State management

**Run tests**:
```bash
cd frontend

# Run all tests
npm test

# Run tests with UI
npm run test:ui

# Run tests in watch mode
npm run test:watch
```

**Test Files**:
- `src/App.test.jsx` - Core component tests (13 tests)

**Coverage**: 100% for test files

### Testing Approach

Our testing strategy follows industry best practices:

1. **Unit Testing**: Individual functions and components tested in isolation
2. **Mocking**: External dependencies (Firebase, OpenAI, file systems) are mocked to ensure:
   - Fast, reliable test execution
   - No dependency on external services
   - Consistent, repeatable results
3. **Coverage**: Both happy path and error cases tested
4. **Separation**: Backend uses pytest, frontend uses Vitest + React Testing Library

### Test Installation

If tests are not working, install dependencies:

```bash
# Backend testing dependencies
cd backend_py
pip install pytest pytest-cov --break-system-packages

# Frontend testing dependencies
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest @vitest/ui jsdom
```

### CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Backend Tests
  run: |
    cd backend_py
    pip install -r requirements.txt
    pytest tests/ -v --cov

- name: Run Frontend Tests
  run: |
    cd frontend
    npm install
    npm test
```

---

##  Docker Deployment

### Build and Run
```bash
# Build images
docker-compose build --no-cache

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Configuration

**Services**:
- `frontend`: React + Vite application (port 3000)
- `backend`: FastAPI application (port 8000)

**Volumes**:
- Frontend source mounted for hot reload
- Backend source mounted for development

**Networks**:
- Services communicate via internal Docker network

### Production Deployment

For production deployment (e.g., GCP):
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose down
docker-compose build --no-cache

# Start with production settings
docker-compose up -d

# Monitor
docker-compose logs -f
```

---

##  Project Structure

```
capstone-project/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts (Auth, etc.)
│   │   ├── lib/             # Utility libraries
│   │   ├── App.test.jsx     # Frontend tests
│   │   └── main.jsx         # Entry point
│   ├── vitest.config.js     # Test configuration
│   └── package.json
│
├── backend_py/              # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── frameworks.py  # Main framework API
│   │   ├── services/       # Business logic
│   │   └── models.py       # Data models
│   ├── tests/              # Backend tests
│   │   ├── test_file_processing.py
│   │   └── test_main.py
│   ├── llm_global.py       # OpenAI integration
│   ├── llm_local.py        # Local LLM integration
│   ├── main.py             # FastAPI app entry
│   └── requirements.txt
│
├── docker-compose.yml       # Docker orchestration
├── .env.example            # Environment template
└── README.md               # This file
```

---

##  Documentation

### Quick Links
- **Installation Guide**: See above sections
- **API Documentation**: `http://localhost:8000/docs` (when backend is running)
- **Project Flow**: See `Project-Startup-and-Operation-Flow.md` for detailed workflow

### Key Features
-  **AI-Powered Generation**: Create frameworks from text or files using OpenAI
-  **Privacy Protection**: Optional local LLM for sensitive data
-  **Framework Editor**: Rich editing experience with auto-save
-  **Framework Merging**: AI-powered or manual framework combination
-  **Export**: Download as Word (.docx) or Markdown (.md)
-  **Multi-Tenant**: Organization support with invitations
-  **Library & Marketplace**: Share and discover frameworks

### Technology Stack

**Frontend**:
- React 18
- Vite
- Tailwind CSS
- Firebase (Authentication, Firestore)
- React Router

**Backend**:
- FastAPI
- Python 3.11+
- OpenAI API
- Firebase Admin SDK
- SQLAlchemy

**Testing**:
- Backend: pytest, pytest-cov
- Frontend: Vitest, React Testing Library

**Deployment**:
- Docker & Docker Compose
- Google Cloud Platform (GCP)

---

## 🔍 Code Quality

### Linting
```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend_py
black .
pylint main.py
```

### Building
```bash
# Frontend production build
cd frontend
npm run build

# Output will be in: frontend/dist/
```

---

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using the port
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process or change port in docker-compose.yml
```

**Docker build fails:**
```bash
# Clean Docker cache
docker system prune -a
docker-compose build --no-cache
```

**Tests failing:**
```bash
# Reinstall dependencies
cd backend_py
pip install -r requirements.txt --break-system-packages

cd frontend
rm -rf node_modules
npm install
```

**Firebase connection issues:**
- Verify `.env` file has correct Firebase credentials
- Check network connectivity
- Ensure Firebase project is properly configured

---