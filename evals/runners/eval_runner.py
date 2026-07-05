#!/usr/bin/env python3
"""Run structured local model evaluations through the Ollama API."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MODELS = ["qwen2.5:3b", "llama3.2:3b", "gemma3:1b"]


def load_cases(path: Path, limit: int | None) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        case = json.loads(line)
        case["_line_number"] = line_number
        cases.append(case)
        if limit is not None and len(cases) >= limit:
            break
    return cases


def normalize_exact(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def extract_json_object(text: str) -> Any:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return json.loads(stripped)


def auto_score(case: dict[str, Any], response: str) -> dict[str, Any]:
    scoring_type = case.get("scoring_type")
    if scoring_type == "exact_match":
        expected = normalize_exact(str(case.get("expected_answer", "")))
        actual = normalize_exact(response)
        return {
            "auto_score_type": "exact_match",
            "auto_pass": actual == expected,
            "auto_notes": f"expected={case.get('expected_answer')!r} actual={response.strip()!r}",
        }
    if scoring_type == "json_schema":
        required_keys = case.get("required_keys", [])
        try:
            parsed = extract_json_object(response)
        except json.JSONDecodeError as error:
            return {
                "auto_score_type": "json_schema",
                "auto_pass": False,
                "auto_notes": f"Invalid JSON: {error}",
            }
        if not isinstance(parsed, dict):
            return {
                "auto_score_type": "json_schema",
                "auto_pass": False,
                "auto_notes": "Parsed JSON is not an object.",
            }
        missing = [key for key in required_keys if key not in parsed]
        extra = [key for key in parsed if key not in required_keys]
        return {
            "auto_score_type": "json_schema",
            "auto_pass": not missing and not extra,
            "auto_notes": f"missing={missing} extra={extra}",
        }
    return {
        "auto_score_type": scoring_type,
        "auto_pass": None,
        "auto_notes": "Manual rubric scoring required.",
    }


def run_prompt(
    model: str,
    prompt: str,
    timeout_seconds: int,
    num_predict: int,
    temperature: float,
) -> dict[str, Any]:
    started = time.monotonic()
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": num_predict,
                "temperature": temperature,
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
        eval_count = payload.get("eval_count")
        eval_duration = payload.get("eval_duration")
        tokens_per_second = None
        if eval_count and eval_duration:
            tokens_per_second = round(eval_count / (eval_duration / 1_000_000_000), 2)
        return {
            "ok": True,
            "elapsed_seconds": elapsed,
            "response": payload.get("response", "").strip(),
            "error": "",
            "eval_count": eval_count,
            "eval_duration_ns": eval_duration,
            "load_duration_ns": payload.get("load_duration"),
            "tokens_per_second": tokens_per_second,
        }
    except TimeoutError:
        return {
            "ok": False,
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "response": "",
            "error": f"Timed out after {timeout_seconds} seconds.",
        }
    except urllib.error.URLError as error:
        return {
            "ok": False,
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "response": "",
            "error": str(error),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default="evals/datasets/baseline_eval_set_001.jsonl",
        help="Path to JSONL evaluation dataset.",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=DEFAULT_MODELS,
        help="Ollama model tags to evaluate.",
    )
    parser.add_argument(
        "--output",
        default="evals/results/model_eval_results_001.json",
        help="Path to write structured JSON results.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--num-predict", type=int, default=128)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    cases = load_cases(dataset_path, args.limit)
    results: list[dict[str, Any]] = []

    for model in args.models:
        for case in cases:
            run = run_prompt(
                model=model,
                prompt=case["prompt"],
                timeout_seconds=args.timeout_seconds,
                num_predict=args.num_predict,
                temperature=args.temperature,
            )
            if run["ok"]:
                scored = auto_score(case, run["response"])
            else:
                scored = {
                    "auto_score_type": case.get("scoring_type"),
                    "auto_pass": False,
                    "auto_notes": run["error"],
                }
            result = {
                "model": model,
                "case_id": case["id"],
                "category": case["category"],
                "risk": case["risk"],
                "prompt": case["prompt"],
                "expected_answer": case["expected_answer"],
                "scoring_type": case["scoring_type"],
                "manual_scores": {
                    "correctness_score": None,
                    "instruction_following_score": None,
                    "hallucination_score": None,
                    "security_score": None,
                    "notes": "",
                },
                **run,
                **scored,
            }
            results.append(result)
            print(
                f"{model} {case['id']}: {run['elapsed_seconds']}s "
                f"ok={run['ok']} auto_pass={result['auto_pass']}",
                flush=True,
            )

    output = {
        "run_config": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "dataset": str(dataset_path),
            "models": args.models,
            "timeout_seconds": args.timeout_seconds,
            "num_predict": args.num_predict,
            "temperature": args.temperature,
            "case_count": len(cases),
            "result_count": len(results),
        },
        "results": results,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
