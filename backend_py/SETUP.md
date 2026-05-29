# Backend Startup Guide (Minimal Version)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend_py
pip install fastapi uvicorn python-multipart
```

Or use requirements.txt：
```bash
pip install -r requirements.txt
```

### 2. Start the Backend
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Running Frontend & Backend Together

### Open two terminals in VSCode：

**Terminal 1 (Backend):**
```bash
cd backend_py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

see `Application startup complete.` means success！

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
