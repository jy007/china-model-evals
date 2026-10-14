"""Ask each model for the 18 numbers via OpenRouter, save everything, score it.

Usage: uv run python -m cme.run --data data/msft-fy2025 --out runs/2026-10-14 [--repeats 3]
Needs OPENROUTER_API_KEY in the environment.
"""

import argparse
import json
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

from cme.parse import extract_json
from cme.score import classify, to_number
from cme.truth import FIELDS

MODELS = [
    "deepseek/deepseek-v4.1-flash",
    "qwen/qwen3.8-max-0902",
    "moonshotai/kimi-k3",
    "z-ai/glm-5.3",
]
URL = "https://openrouter.ai/api/v1/chat/completions"

PROMPT = """Below is Microsoft Corporation's Form 10-K annual report for the fiscal year ended June 30, 2025.

Extract the following figures for fiscal year 2025 (the year ended June 30, 2025) exactly as reported in the consolidated financial statements.
Report dollar amounts in millions of US dollars, and diluted EPS in US dollars per share. Use plain numbers (no commas, no currency symbols); use null if you cannot find a figure.

Fields:
{fields}

Return only a JSON object with exactly these keys.

=== DOCUMENT START ===
{document}
=== DOCUMENT END ==="""


def build_prompt(document: str) -> str:
    fields = "\n".join(f"- {name}" for name, _, _ in FIELDS)
    return PROMPT.format(fields=fields, document=document)


def call(client: httpx.Client, model: str, prompt: str) -> dict:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 16000,
        "usage": {"include": True},
    }
    started = time.time()
    r = client.post(URL, json=body)
    r.raise_for_status()
    data = r.json()
    data["_elapsed_s"] = round(time.time() - started, 1)
    return data


def score(answer: dict | None, truth: dict) -> dict:
    answer = answer or {}
    return {
        f: {"answer": to_number(answer.get(f)), "truth": t["value"], "result": classify(to_number(answer.get(f)), t)}
        for f, t in truth.items()
    }


def run_one(client, model, prompt, truth, out: Path, i: int, bust_cache: bool = False) -> dict:
    path = out / model.replace("/", "__") / f"run{i}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    # Prompt caches match on the prefix, so a unique first line forces a full-price, uncached call.
    nonce = uuid.uuid4().hex if bust_cache else None
    if nonce:
        prompt = f"Request id: {nonce}\n\n{prompt}"
    try:
        resp = call(client, model, prompt)
        text = resp["choices"][0]["message"].get("content") or ""
        error = None
    except (httpx.HTTPError, KeyError, IndexError) as e:
        resp, text, error = None, "", f"{type(e).__name__}: {e}"
    scored = score(extract_json(text), truth)
    record = {"model": model, "run": i, "nonce": nonce, "error": error, "response": resp, "scored": scored}
    path.write_text(json.dumps(record, indent=1, ensure_ascii=False))
    correct = sum(v["result"] == "correct" for v in scored.values())
    print(f"{model} run{i}: {correct}/{len(scored)} correct" + (f" ERROR {error}" if error else ""), flush=True)
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--models", nargs="*", default=MODELS)
    ap.add_argument("--bust-cache", action="store_true", help="prefix each prompt with a unique id so no call hits a prompt cache")
    args = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY is not set")
    truth = json.loads((args.data / "truth.json").read_text())
    prompt = build_prompt((args.data / "doc.txt").read_text())
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "prompt.txt").write_text(prompt)

    headers = {"Authorization": f"Bearer {key}", "X-Title": "china-model-evals"}
    with httpx.Client(headers=headers, timeout=600) as client, ThreadPoolExecutor(8) as pool:
        jobs = [pool.submit(run_one, client, m, prompt, truth, args.out, i, args.bust_cache)
                for m in args.models for i in range(1, args.repeats + 1)]
        records = [j.result() for j in jobs]
    (args.out / "results.json").write_text(json.dumps(
        [{k: r[k] for k in ("model", "run", "error", "scored")} | {"usage": (r["response"] or {}).get("usage")} for r in records],
        indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
