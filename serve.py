#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP, with structured logging.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app --workers 1           run it the way a host runs it
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time

from flask import Flask, jsonify, request

import config
import generate

app = Flask(__name__)

LOG_PATH = Path(os.getenv("RUN_LOG_PATH", "logs/runs.jsonl"))


def _write_log(record: dict) -> None:
    """Append one structured JSON record to LOG_PATH."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?"""
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.get("/logs")
def logs():
    """Return structured log records so they can be inspected/copied on Path A."""
    if not LOG_PATH.exists():
        return jsonify({"count": 0, "entries": []})

    limit = request.args.get("limit", default=50, type=int)
    lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    entries = []
    for line in lines[-limit:]:
        if line.strip():
            entries.append(json.loads(line))
    return jsonify({"count": len(entries), "entries": entries})


@app.post("/ask")
def ask():
    """One question in, one grounded answer out, with structured instrumentation."""
    from app import ask_pipeline

    started_at = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()

    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()

    if not question:
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        error_msg = (
            "Send JSON with a question in it, like "
            '{"question": "is the housing lottery random?"}'
        )
        _write_log(
            {
                "timestamp": started_at,
                "corpus": config.CORPUS,
                "question": "",
                "status": "bad_request",
                "http_status": 400,
                "refused": None,
                "answer": None,
                "sources": [],
                "best_distance": None,
                "latency_ms": latency_ms,
                "prompt_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "error": error_msg,
            }
        )
        return jsonify({"error": error_msg}), 400

    tokens_before = generate.token_counts()

    try:
        outcome = ask_pipeline(question, corpus=config.CORPUS)
    except Exception as exc:  # noqa: BLE001 — a reader gets this, not a traceback
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        tokens_after = generate.token_counts()
        error_msg = f"{type(exc).__name__}: {exc}"
        _write_log(
            {
                "timestamp": started_at,
                "corpus": config.CORPUS,
                "question": question,
                "status": "error",
                "http_status": 500,
                "refused": None,
                "answer": None,
                "sources": [],
                "best_distance": None,
                "latency_ms": latency_ms,
                "prompt_tokens": tokens_after["prompt"] - tokens_before["prompt"],
                "output_tokens": tokens_after["output"] - tokens_before["output"],
                "total_tokens": tokens_after["total"] - tokens_before["total"],
                "error": error_msg,
            }
        )
        return jsonify({"error": error_msg}), 500

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    tokens_after = generate.token_counts()
    prompt_tokens = tokens_after["prompt"] - tokens_before["prompt"]
    output_tokens = tokens_after["output"] - tokens_before["output"]
    total_tokens = tokens_after["total"] - tokens_before["total"]

    record = {
        "timestamp": started_at,
        "corpus": config.CORPUS,
        "question": question,
        "status": "refused" if outcome["refused"] else "ok",
        "http_status": 200,
        "refused": outcome["refused"],
        "answer": outcome["answer"],
        "sources": outcome["sources"],
        "best_distance": round(outcome["best_distance"], 4),
        "latency_ms": latency_ms,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "error": None,
    }
    _write_log(record)

    return jsonify(
        {
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
            "latency_ms": latency_ms,
            "tokens": {
                "prompt": prompt_tokens,
                "output": output_tokens,
                "total": total_tokens,
            },
        }
    )


def main():
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()