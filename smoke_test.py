#!/usr/bin/env python3
"""Quick smoke test for the instrumented HTTP wrapper in serve.py."""

import json
import sys
import urllib.error
import urllib.request

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000"


def _req(path: str, payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if data is not None else {}
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read().decode("utf-8"))


def main():
    print("1. GET /health ->", _req("/health"))
    print(
        "2. POST /ask (valid) ->",
        _req("/ask", {"question": "How many hours per week outside of class should students expect to spend on CS 210?"}),
    )
    print(
        "3. POST /ask (out-of-scope) ->",
        _req("/ask", {"question": "What is the capital of Mongolia?"}),
    )
    print("4. POST /ask (empty 400) ->", _req("/ask", {}))
    status, log_data = _req("/logs?limit=5")
    print(f"5. GET /logs -> status={status}, entries_logged={log_data.get('count')}")


if __name__ == "__main__":
    main()