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


def _count_all_files(vs_api, vs_id):
    total = 0
    after = None
    while True:
        try:
            resp = vs_api.files.list(vector_store_id=vs_id, limit=100, after=after)
        except TypeError:
            try:
                resp = vs_api.files.list(vector_store_id=vs_id, limit=100)
            except TypeError:
                resp = vs_api.files.list(vector_store_id=vs_id)
        data = getattr(resp, "data", [])
        total += len(data) if isinstance(data, list) else 0
        has_more = getattr(resp, "has_more", False)
        if not has_more:
            break
        after = getattr(resp, "last_id", None)
        if not after:
            break
    return total


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY"))
    p.add_argument(
        "--vs-id",
        default=os.getenv("OPENAI_VECTOR_STORE_ACTIVITY")
        or os.getenv("OPENAI_VECTOR_STORE_LIBRARY"),
    )
    p.add_argument(
        "--backend", default=os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    )
    p.add_argument("--framework-id", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--tenant-id", default=None)
    p.add_argument("--user-id", default=None)
    p.add_argument("--category", default="Technology")
    p.add_argument("--tags", default="test,auto")
    p.add_argument("--version", default="1.0")
    p.add_argument("--to-org", action="store_true")
    p.add_argument("--organization", default=None)
    args = p.parse_args()

    if not args.api_key:
        print("OPENAI_API_KEY missing")
        sys.exit(2)
    if not args.vs_id:
        print("vector store id missing")
        sys.exit(2)

    client = OpenAI(api_key=args.api_key)
    vs_api = _vs_api(client)

    before = _count_all_files(vs_api, args.vs_id)

    fid = args.framework_id or f"fw_{int(time.time())}"
    title = args.title or f"Publish Test {int(time.time())}"
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    payload = {
        "id": fid,
        "title": title,
        "version": args.version,
        "isPublic": True,
        "category": args.category,
        "tags": tags,
        "tenantId": args.tenant_id,
    }
    if args.to_org:
        payload["publishedToOrganization"] = True
        if args.organization:
            payload["organization"] = args.organization

    r1 = requests.post(
        f"{args.backend}/api/frameworks/push-framework",
        json={"framework": payload, "vector_store_id": args.vs_id},
        timeout=30,
    )
    r2 = requests.post(
        f"{args.backend}/api/frameworks/log-event",
        json={
            "type": "publish_org" if args.to_org else "publish",
            "framework_id": fid,
            "tenant_id": args.tenant_id,
            "user_id": args.user_id,
            "payload": {
                "category": args.category,
                "tags": tags,
                "version": args.version,
                "organization": args.organization,
            },
        },
        timeout=30,
    )

    time.sleep(2)
    after = _count_all_files(vs_api, args.vs_id)
    print(f"Publish simulated: id={fid}, title={title}")
    print(f"Files before: {before}")
    print(f"Files after: {after}")
    print(f"Delta: {after - before}")
    print(f"push-framework status: {getattr(r1, 'status_code', None)}")
    print(f"log-event status: {getattr(r2, 'status_code', None)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
