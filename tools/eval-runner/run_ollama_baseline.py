#!/usr/bin/env python3
"""Run a small Ollama baseline prompt set and write JSON results."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_MODELS = [
    "llama3.2:1b",
    "llama3.2:3b",
    "qwen2.5:3b",
    "mistral:7b",
    "gemma3:1b",
]


def load_prompts(path: Path) -> list[dict[str, str]]:
    prompts: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            prompts.append(json.loads(line))
    return prompts


def run_prompt(
    model: str,
    prompt: str,
    timeout_seconds: int,
    num_predict: int,
) -> dict[str, object]:
    started = time.monotonic()
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": num_predict,
                "temperature": 0.2,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        elapsed = round(time.monotonic() - started, 2)
        return {
            "ok": True,
            "elapsed_seconds": elapsed,
            "response": payload.get("response", "").strip(),
            "error": "",
            "eval_count": payload.get("eval_count"),
            "eval_duration": payload.get("eval_duration"),
            "load_duration": payload.get("load_duration"),
        }
    except TimeoutError:
        elapsed = round(time.monotonic() - started, 2)
        return {
            "ok": False,
            "elapsed_seconds": elapsed,
            "response": "",
            "error": f"Timed out after {timeout_seconds} seconds.",
        }
    except urllib.error.URLError as error:
        elapsed = round(time.monotonic() - started, 2)
        return {
            "ok": False,
            "elapsed_seconds": elapsed,
            "response": "",
            "error": str(error),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompts",
        default="prompts/baseline/local-ai-lab.jsonl",
        help="Path to JSONL prompt set.",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=DEFAULT_MODELS,
        help="Ollama model tags to test.",
    )
    parser.add_argument(
        "--output",
        default="models/comparisons/phase-1-local-model-results.json",
        help="Path to write JSON results.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--num-predict", type=int, default=128)
    args = parser.parse_args()

    prompts = load_prompts(Path(args.prompts))
    results: list[dict[str, object]] = []

    for model in args.models:
        for prompt in prompts:
            run = run_prompt(
                model,
                prompt["prompt"],
                args.timeout_seconds,
                args.num_predict,
            )
            results.append(
                {
                    "model": model,
                    "prompt_id": prompt["id"],
                    "category": prompt["category"],
                    "prompt": prompt["prompt"],
                    **run,
                }
            )
            print(
                f"{model} {prompt['id']}: "
                f"{run['elapsed_seconds']}s ok={run['ok']}",
                flush=True,
            )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
