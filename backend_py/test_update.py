import os
import sys
import time
import json
import argparse
import requests
from openai import OpenAI


def _vs_api(client):
    try:
        return client.vector_stores
    except AttributeError:
        return client.beta.vector_stores


def _list_files(vs_api, vs_id, limit=100):
    try:
        resp = vs_api.files.list(vector_store_id=vs_id, limit=limit)
    except TypeError:
        resp = vs_api.files.list(vector_store_id=vs_id)
    data = getattr(resp, "data", [])
    if not isinstance(data, list):
        return []
    return data


def _file_content(client, file_id):
    try:
        r = client.files.content(file_id)
        try:
            return r.read().decode("utf-8", errors="ignore")
        except Exception:
            return r.text
    except Exception:
        try:
            r = client.files.retrieve(file_id)
            return json.dumps(r.model_dump(), ensure_ascii=False)
        except Exception:
            return None


def _get_id_token(api_key, email, password):
    if not api_key:
        return None
    if email and password:
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            r = requests.post(
                url,
                json={"email": email, "password": password, "returnSecureToken": True},
                timeout=30,
            )
            if r.status_code == 200:
                return r.json().get("idToken")
        except Exception:
            pass
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
            r = requests.post(
                url,
                json={"email": email, "password": password, "returnSecureToken": True},
                timeout=30,
            )
            if r.status_code == 200:
                return r.json().get("idToken")
        except Exception:
            pass
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
        r = requests.post(url, json={"returnSecureToken": True}, timeout=30)
        if r.status_code == 200:
            return r.json().get("idToken")
    except Exception:
        pass
    return None


def _sync_library(backend, project_id, api_key, vs_id, id_token, limit):
    body = {
        "project_id": project_id,
        "api_key": api_key,
        "vector_store_id": vs_id,
        "id_token": id_token,
        "limit": limit,
    }
    try:
        r = requests.post(
            f"{backend}/api/frameworks/sync-library", json=body, timeout=60
        )
        if r.status_code == 200:
            d = r.json()
            return d.get("uploaded")
    except Exception:
        pass
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY"))
    p.add_argument("--library-vs-id", default=os.getenv("OPENAI_VECTOR_STORE_LIBRARY"))
    p.add_argument(
        "--activity-vs-id", default=os.getenv("OPENAI_VECTOR_STORE_ACTIVITY")
    )
    p.add_argument(
        "--backend", default=os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    )
    p.add_argument("--project-id", default=os.getenv("FIREBASE_PROJECT_ID"))
    p.add_argument(
        "--firebase-api-key",
        default=os.getenv("VITE_FIREBASE_API_KEY") or os.getenv("FIREBASE_API_KEY"),
    )
    p.add_argument("--email", default=None)
    p.add_argument("--password", default=None)
    p.add_argument("--do-sync", action="store_true")
    args = p.parse_args()

    if not args.api_key:
        print("OPENAI_API_KEY missing")
        sys.exit(2)
    if not args.library_vs_id:
        print("library vs id missing")
        sys.exit(2)
    if not args.activity_vs_id:
        args.activity_vs_id = args.library_vs_id

    client = OpenAI(api_key=args.api_key)
    vs_api = _vs_api(client)

    lib_files = _list_files(vs_api, args.library_vs_id, limit=100)
    print(f"Library files: {len(lib_files)}")
    lib_samples = []
    for f in lib_files[-10:]:
        i = getattr(f, "id", None)
        fn = getattr(f, "filename", None)
        lib_samples.append((i, fn))
        if len(lib_samples) >= 5:
            break
    print("Library samples:")
    for i, fn in lib_samples:
        print(f"- {i}: {fn}")

    if args.do_sync and args.project_id and args.firebase_api_key:
        token = _get_id_token(args.firebase_api_key, args.email, args.password)
        uploaded = _sync_library(
            args.backend,
            args.project_id,
            args.firebase_api_key,
            args.library_vs_id,
            token,
            limit=50,
        )
        if uploaded is not None:
            print(f"Sync uploaded: {uploaded}")
        time.sleep(2)

    act_before = _list_files(vs_api, args.activity_vs_id, limit=100)
    before_count = len(act_before)
    marker = f"marker-{int(time.time())}"
    try:
        payload = {
            "type": "test",
            "framework_id": "_",
            "tenant_id": "_",
            "user_id": "_",
            "payload": {"marker": marker},
        }
        r = requests.post(
            f"{args.backend}/api/frameworks/log-event", json=payload, timeout=20
        )
    except Exception:
        r = None
    time.sleep(2)
    act_after = _list_files(vs_api, args.activity_vs_id, limit=100)
    after_count = len(act_after)
    print(f"Activity files before: {before_count}")
    print(f"Activity files after: {after_count}")
    found = False
    for f in act_after[-10:]:
        c = _file_content(client, f.id)
        if c and marker in c:
            print(f"Activity latest: {f.id} contains marker")
            found = True
            break
    print(f"Realtime event written: {found}")
    sys.exit(0)


if __name__ == "__main__":
    main()
