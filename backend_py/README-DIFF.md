# Project Run & Sync Testing Guide

This project includes both frontend and backend, and supports syncing framework data from Firebase Firestore to the OpenAI Vector Store. This document explains how to run the project, test vector database syncing, test Firebase connectivity, and the API & ID token logic. All paths below are relative.

## Prerequisites

- Required software:
  - Python 3.11+
  - Node.js 18+
  - PowerShell (Windows)
- Install backend dependencies:
  - `cd backend_py`
  - `pip install -r requirements.txt --break-system-packages`
- Install frontend dependencies:
  - `cd frontend`
  - `npm install`

### Environment Variables (PowerShell examples)

- OpenAI:
  - `setx OPENAI_API_KEY "sk-xxxx"`
  - `setx OPENAI_VECTOR_STORE_LIBRARY "vs_xxxx"`
  - `setx OPENAI_VECTOR_STORE_ACTIVITY "vs_xxxx"` (can be the same or different)
- Firebase:
  - `setx FIREBASE_PROJECT_ID "your-project-id"`
  - `setx VITE_FIREBASE_API_KEY "your-web-api-key"` (or `setx FIREBASE_API_KEY "your-web-api-key"`)
  - Optional: use non-anonymous tokens
    - `setx FIREBASE_USER_EMAIL "user@example.com"`
    - `setx FIREBASE_USER_PASSWORD "your_password"`

After setting, restart your terminal for variables to take effect.

## Start the Project

- Start backend:
  - `cd backend_py`
  - `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Start frontend:
  - `cd frontend`
  - `npm run dev`

After backend starts, it will automatically sync public/organization frameworks from Firestore to the Vector Store every minute (see "Sync Overview").

## Sync Overview

- Scheduled task: on backend startup, a job runs every 60 seconds to sync from Firestore into the OpenAI Vector Store.
  - Location: `backend_py/main.py:124`
- Sync endpoint:
  - `POST /api/frameworks/sync-library` (manual trigger when needed)
    - Location: `backend_py/app/api/frameworks.py:2625`
  - De-duplication model: `SyncedVectorItem` avoids re-uploading the same doc to the same vector store
    - Location: `backend_py/app/models.py:109`
- Events & single-item push:
  - `POST /api/frameworks/log-event` (behavior log into activity vector store) at `backend_py/app/api/frameworks.py:2713`
  - `POST /api/frameworks/push-framework` (push a single framework to vector store) at `backend_py/app/api/frameworks.py:2734`

## Test: Vector Database Sync (backend_py\test_vec_base.py)

This script verifies connection to the OpenAI Vector Store and lists/aggregates files.

- Prerequisites: ensure `OPENAI_API_KEY` and vector store ID are set (for Library tests, set `OPENAI_VECTOR_STORE_LIBRARY`).
- Run:
  - `cd backend_py`
  - `python .\test_vec_base.py --api-key $env:OPENAI_API_KEY --vs-id $env:OPENAI_VECTOR_STORE_LIBRARY`
- Expected output:
  - Successful connection (prints `Connected to Vector Store: id=..., name=...`)
  - Shows file count (`Files count` and `Files total count`)

## Test: Firebase Connectivity (backend_py\test_firebase.py)

This script uses REST APIs to validate Firestore reads and ID token acquisition.

- Prerequisites: set `FIREBASE_PROJECT_ID` and a Web API Key (`VITE_FIREBASE_API_KEY` or `FIREBASE_API_KEY`).
- Run:
  - `cd backend_py`
  - Anonymous token (default): `python .\test_firebase.py --collections frameworks,users,tenants`
  - With account token: `python .\test_firebase.py --email user@example.com --password your_password --collections frameworks,users,tenants`
- Expected output: collection counts; if project rules and credentials are correct, counts should be non-zero.

## Validate Publish & Sync Success (Recommended Flow)

Goal: after publishing a framework, Firestore total count increases; within at most 1 minute, the Vector Store count also increases.

- Step A: Publish a framework to the vector store (choose one of two methods)
  - Method 1 (script):
    - `cd backend_py`
    - `python .\test_update_publish.py --to-org` (optionally add `--organization your-org`)
    - The script calls `POST /api/frameworks/push-framework` and logs an event to the activity vector store.
  - Method 2 (direct API):
    - Request: `POST http://127.0.0.1:8000/api/frameworks/push-framework`
    - Example body:
      ```json
      {
        "framework": {
          "id": "fw_test_001",
          "title": "Publish Test",
          "version": "1.0",
          "isPublic": true,
          "category": "Technology",
          "tags": ["test", "auto"],
          "tenantId": "legacy"
        }
      }
      ```

- Step B: Verify Firestore updates
  - Run: `python .\test_firebase.py --collections frameworks`
  - Compare counts before/after; `frameworks` collection should increase.

- Step C: Verify Vector Store updates (≤ 1 minute)
  - Wait up to 60 seconds (backend schedule interval)
  - Run: `python .\test_vec_base.py --api-key $env:OPENAI_API_KEY --vs-id $env:OPENAI_VECTOR_STORE_LIBRARY`
  - Compare `Files total count` before/after; it should increase (a new `framework_*.json` file).

## API & ID Token Logic (Implementation References)

- Read Web API Key: `backend_py/app/api/frameworks.py:163`
  - Uses `req.api_key` or environment variables `VITE_FIREBASE_API_KEY` / `FIREBASE_API_KEY`
- Read Project ID: `backend_py/app/api/frameworks.py:171`
  - Uses `req.project_id` or environment variable `FIREBASE_PROJECT_ID`
- Get ID Token: `backend_py/app/api/frameworks.py:178`
  - Prefers `FIREBASE_ID_TOKEN` if present
  - If email/password provided, calls Google Identity Toolkit `accounts:signInWithPassword`
  - Otherwise performs anonymous `accounts:signUp` to obtain a token
- Write files to Vector Store: `backend_py/app/api/frameworks.py:152`
  - Uses OpenAI Files API to upload JSON to the Vector Store (`files.upload` or fallback `files.create`)
- Firestore query: `backend_py/app/api/frameworks.py:2625`
  - Calls `documents:runQuery` with conditions: `isPublic == true` and optionally `publishedToOrganization == true`
- Scheduled sync on startup: `backend_py/main.py:124`
  - Triggers `sync_library` every 60 seconds into `OPENAI_VECTOR_STORE_LIBRARY`

## Tips

- If the backend complains about missing `OPENAI_API_KEY` or vector store IDs, verify your environment variables and restart your shell.
- If Firebase queries fail, check your Firestore security rules, project ID, and Web API Key; if you lack an account, anonymous token mode works.
- Vector Store file counts may refresh within 1 minute—wait for the scheduled sync.

---

To switch to manual-only sync or adjust the sync frequency, edit the startup scheduled task configuration in `backend_py/main.py`.
