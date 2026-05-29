import os
import sys
import argparse
from openai import OpenAI


def _get_vs(client):
    try:
        return client.vector_stores
    except AttributeError:
        return client.beta.vector_stores


def _retrieve(vs_api, vs_id):
    try:
        return vs_api.retrieve(vs_id)
    except TypeError:
        return vs_api.retrieve(vector_store_id=vs_id)


def _list_files(vs_api, vs_id):
    try:
        return vs_api.files.list(vector_store_id=vs_id)
    except TypeError:
        return vs_api.files.list(vs_id)


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


def _list_all_vs(vs_api):
    total = 0
    after = None
    while True:
        try:
            resp = vs_api.list(limit=100, after=after)
        except TypeError:
            try:
                resp = vs_api.list(limit=100)
            except TypeError:
                resp = vs_api.list()
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--vs-id", default=os.getenv("OPENAI_VECTOR_STORE_ID"))
    args = parser.parse_args()

    if not args.api_key:
        print("OPENAI_API_KEY missing. Set env or pass --api-key.")
        sys.exit(2)
    if not args.vs_id:
        print(
            "Vector Store ID missing. Set env OPENAI_VECTOR_STORE_ID or pass --vs-id."
        )
        sys.exit(2)

    client = OpenAI(api_key=args.api_key)
    vs_api = _get_vs(client)

    try:
        vs = _retrieve(vs_api, args.vs_id)
    except Exception as e:
        print(f"Retrieve failed: {e}")
        sys.exit(1)

    try:
        name = getattr(vs, "name", None)
        print(f"Connected to Vector Store: id={vs.id}, name={name}")
    except Exception:
        print("Connected but failed to read properties.")

    try:
        files = _list_files(vs_api, args.vs_id)
        data = getattr(files, "data", None)
        count = len(data) if isinstance(data, list) else 0
        print(f"Files count: {count}")
        total_files = _count_all_files(vs_api, args.vs_id)
        print(f"Files total count: {total_files}")
    except Exception as e:
        print(f"List files failed: {e}")

    try:
        total_vs = _list_all_vs(vs_api)
        print(f"Vector Stores count: {total_vs}")
    except Exception as e:
        print(f"List vector stores failed: {e}")

    sys.exit(0)


if __name__ == "__main__":
    main()


# python test_vec_base.py --api-key "$OPENAI_API_KEY" --vs-id "vs_..."
