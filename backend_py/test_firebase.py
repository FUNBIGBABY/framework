import os
import re
import sys
import json
import argparse
import requests


def read_project_id(cli_project_id):
    if cli_project_id:
        return cli_project_id
    env_pid = os.getenv("FIREBASE_PROJECT_ID")
    if env_pid:
        return env_pid
    for fname in (
        os.path.join("..", "frontend", ".env"),
        os.path.join("..", "frontend", ".env.production"),
    ):
        try:
            with open(fname, "r", encoding="utf-8") as f:
                m = re.search(
                    r"^\s*VITE_FIREBASE_PROJECT_ID\s*=\s*(.+)\s*$", f.read(), re.M
                )
                if m:
                    return m.group(1).strip()
        except Exception:
            pass
    return None


def list_count(project_id, collection, id_token=None, api_key=None):
    base = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection}"
    params = {"pageSize": 100}
    if api_key:
        params["key"] = api_key
    headers = {}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    total = 0
    next_token = None
    while True:
        if next_token:
            params["pageToken"] = next_token
        r = requests.get(base, headers=headers, params=params, timeout=30)
        if r.status_code != 200:
            try:
                data = r.json()
                msg = data.get("error", {}).get("message") or json.dumps(data)
            except Exception:
                msg = r.text
            return (0, f"HTTP {r.status_code}: {msg}")
        data = r.json()
        docs = data.get("documents", [])
        total += len(docs)
        next_token = data.get("nextPageToken")
        if not next_token:
            break
    return (total, None)


def read_api_key(cli_api_key):
    if cli_api_key:
        return cli_api_key
    env_key = os.getenv("VITE_FIREBASE_API_KEY")
    if env_key:
        return env_key
    for fname in (
        os.path.join("..", "frontend", ".env"),
        os.path.join("..", "frontend", ".env.production"),
    ):
        try:
            with open(fname, "r", encoding="utf-8") as f:
                m = re.search(
                    r"^\s*VITE_FIREBASE_API_KEY\s*=\s*(.+)\s*$", f.read(), re.M
                )
                if m:
                    return m.group(1).strip()
        except Exception:
            pass
    return None


def fetch_id_token(api_key, email, password):
    if not (api_key and email and password):
        return None, None
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        return None, None
    data = r.json()
    return data.get("idToken"), data.get("localId")


def fetch_anonymous_id_token(api_key):
    if not api_key:
        return None, None
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"returnSecureToken": True}
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        return None, None
    data = r.json()
    return data.get("idToken"), data.get("localId")


def ensure_email_user(api_key, email, password):
    if not (api_key and email and password):
        return None, None
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        return None, None
    data = r.json()
    return data.get("idToken"), data.get("localId")


def run_query_count(
    project_id, collection, field, value, value_type, id_token, api_key=None
):
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents:runQuery"
    params = {}
    if api_key:
        params["key"] = api_key
    headers = {}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    v = {}
    if value_type == "string":
        v = {"stringValue": str(value)}
    elif value_type == "boolean":
        v = {"booleanValue": bool(value)}
    else:
        v = {"stringValue": str(value)}
    body = {
        "structuredQuery": {
            "from": [{"collectionId": collection}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": field},
                    "op": "EQUAL",
                    "value": v,
                }
            },
        }
    }
    r = requests.post(url, headers=headers, params=params, json=body, timeout=30)
    if r.status_code != 200:
        try:
            data = r.json()
            msg = data.get("error", {}).get("message") or json.dumps(data)
        except Exception:
            msg = r.text
        return (0, f"HTTP {r.status_code}: {msg}")
    data = r.json()
    count = 0
    for item in data:
        if isinstance(item, dict) and item.get("document"):
            count += 1
    return (count, None)


def run_query_count_all(project_id, collection, id_token, api_key=None):
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents:runQuery"
    params = {}
    if api_key:
        params["key"] = api_key
    headers = {}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    body = {
        "structuredQuery": {
            "from": [{"collectionId": collection}],
        }
    }
    r = requests.post(url, headers=headers, params=params, json=body, timeout=30)
    if r.status_code != 200:
        try:
            data = r.json()
            msg = data.get("error", {}).get("message") or json.dumps(data)
        except Exception:
            msg = r.text
        return (0, f"HTTP {r.status_code}: {msg}")
    count = 0
    for item in r.json():
        if isinstance(item, dict) and item.get("document"):
            count += 1
    return (count, None)


def get_doc_exists(project_id, collection, doc_id, id_token, api_key=None):
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection}/{doc_id}"
    params = {}
    if api_key:
        params["key"] = api_key
    headers = {}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    r = requests.get(url, headers=headers, params=params, timeout=30)
    if r.status_code == 200:
        return True
    return False


def _val(v):
    if not isinstance(v, dict):
        return v
    if "stringValue" in v:
        return v["stringValue"]
    if "booleanValue" in v:
        return v["booleanValue"]
    if "integerValue" in v:
        try:
            return int(v["integerValue"])
        except Exception:
            return v["integerValue"]
    if "doubleValue" in v:
        try:
            return float(v["doubleValue"])
        except Exception:
            return v["doubleValue"]
    if "timestampValue" in v:
        return v["timestampValue"]
    if "mapValue" in v:
        fields = v.get("mapValue", {}).get("fields", {})
        return {k: _val(fields[k]) for k in fields} if fields else {}
    if "arrayValue" in v:
        arr = v.get("arrayValue", {}).get("values", [])
        return [_val(x) for x in arr] if arr else []
    return v


def _parse_document(doc):
    name = doc.get("name", "")
    doc_id = name.split("/")[-1] if name else None
    fields = doc.get("fields", {})
    parsed = {k: _val(fields[k]) for k in fields}
    if doc_id:
        parsed["id"] = doc_id
    return parsed


def query_public_frameworks(project_id, id_token, api_key=None, limit=10):
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents:runQuery"
    params = {}
    if api_key:
        params["key"] = api_key
    headers = {}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    body = {
        "structuredQuery": {
            "from": [{"collectionId": "frameworks"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "isPublic"},
                    "op": "EQUAL",
                    "value": {"booleanValue": True},
                }
            },
            "limit": limit,
            "orderBy": [
                {"field": {"fieldPath": "publishedAt"}, "direction": "DESCENDING"}
            ],
        }
    }
    r = requests.post(url, headers=headers, params=params, json=body, timeout=30)
    if r.status_code != 200:
        try:
            data = r.json()
            msg = data.get("error", {}).get("message") or json.dumps(data)
        except Exception:
            msg = r.text
        return [], f"HTTP {r.status_code}: {msg}"
    result = []
    for item in r.json():
        doc = item.get("document")
        if doc:
            result.append(_parse_document(doc))
    return result, None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--project-id", default=None)
    p.add_argument("--id-token", default=os.getenv("FIREBASE_ID_TOKEN"))
    p.add_argument("--api-key", default=None)
    p.add_argument("--email", default=None)
    p.add_argument("--password", default=None)
    p.add_argument("--collections", default="frameworks,users,tenants")
    args = p.parse_args()

    project_id = read_project_id(args.project_id)
    if not project_id:
        print("Project ID not found. Pass --project-id or set FIREBASE_PROJECT_ID.")
        sys.exit(2)

    api_key = read_api_key(args.api_key)
    id_token = args.id_token
    uid = None
    if not id_token:
        id_token, uid = fetch_id_token(api_key, args.email, args.password)
    if not id_token:
        if args.email and args.password:
            id_token, uid = ensure_email_user(api_key, args.email, args.password)
    if not id_token:
        id_token, uid = fetch_anonymous_id_token(api_key)

    cols = [c.strip() for c in args.collections.split(",") if c.strip()]
    total_all = 0
    print(f"Project: {project_id}")
    for c in cols:
        cnt, err = list_count(project_id, c, id_token=id_token, api_key=api_key)
        if err and c == "frameworks" and id_token:
            names = set()
            c1, e1 = run_query_count(
                project_id, "frameworks", "isPublic", True, "boolean", id_token, api_key
            )
            if not e1:
                total_all += c1
                print(f"frameworks(public): {c1}")
            if uid:
                c2, e2 = run_query_count(
                    project_id,
                    "frameworks",
                    "creatorId",
                    uid,
                    "string",
                    id_token,
                    api_key,
                )
                if not e2:
                    total_all += c2
                    print(f"frameworks(mine): {c2}")
            else:
                print("frameworks: error: insufficient permissions")
        elif err and c == "users" and id_token and uid:
            exists = get_doc_exists(project_id, "users", uid, id_token, api_key)
            print(f"users(accessible): {1 if exists else 0}")
            total_all += 1 if exists else 0
        elif err and c == "tenants" and id_token and uid:
            c3, e3 = run_query_count(
                project_id, "tenants", "ownerId", uid, "string", id_token, api_key
            )
            if not e3:
                print(f"tenants(mine): {c3}")
                total_all += c3
            else:
                print("tenants: error: insufficient permissions")
        else:
            if err:
                print(f"{c}: error: {err}")
            else:
                print(f"{c}: {cnt}")
                total_all += cnt
    items, e = query_public_frameworks(project_id, id_token, api_key, limit=10)
    if e:
        print(f"frameworks(public sample): error: {e}")
    else:
        print(f"frameworks(public sample): {len(items)}")
        for it in items:
            t = it.get("title") or it.get("metadata", {}).get("title")
            v = it.get("version") or it.get("metadata", {}).get("version")
            print(f"- {it.get('id')}: {t} | {v}")
    print(f"Total: {total_all}")

    f_total, e_total = list_count(
        project_id, "frameworks", id_token=id_token, api_key=api_key
    )
    if e_total:
        f_total, e_total = run_query_count_all(
            project_id, "frameworks", id_token, api_key
        )
    f_pub, e_pub = run_query_count(
        project_id, "frameworks", "isPublic", True, "boolean", id_token, api_key
    )
    f_org, e_org = run_query_count(
        project_id,
        "frameworks",
        "publishedToOrganization",
        True,
        "boolean",
        id_token,
        api_key,
    )
    print(f"frameworks(total): {f_total}")
    print(f"frameworks(publish): {f_pub}")
    print(f"frameworks(organization): {f_org}")
    sys.exit(0)


if __name__ == "__main__":
    main()


# Example:
# python test_firebase.py --project-id "<firebase-project-id>" --api-key "<firebase-web-api-key>" --email "user@example.com" --password "<password>" --collections "frameworks,users,tenants"
