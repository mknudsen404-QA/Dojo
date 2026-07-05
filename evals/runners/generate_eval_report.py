#!/usr/bin/env python3
"""Generate a markdown report from Phase 2 evaluation results."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANUAL_FIELDS = [
    "correctness_score",
    "instruction_following_score",
    "hallucination_score",
    "security_score",
]


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "n/a"
    return f"{(numerator / denominator) * 100:.1f}%"


def load_results(path: Path) -> dict[str, Any]:
    if path.suffix == ".jsonl":
        results = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        models = list(dict.fromkeys(row["model"] for row in results))
        return {
            "run_config": {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dataset": "unknown; loaded from scored JSONL",
                "models": models,
                "timeout_seconds": "unknown",
                "num_predict": "unknown",
                "temperature": "unknown",
                "case_count": len({row["case_id"] for row in results}),
                "result_count": len(results),
                "source_results": str(path),
            },
            "results": results,
        }
    return json.loads(path.read_text(encoding="utf-8"))


def default_manifest_path(results_path: Path) -> Path | None:
    if results_path.suffix != ".jsonl":
        return None
    if results_path.name.endswith("_scored.jsonl"):
        return results_path.with_name(results_path.name.replace("_scored.jsonl", "_run_manifest.json"))
    return results_path.with_name(f"{results_path.stem}_run_manifest.json")


def load_manifest(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def apply_manifest(payload: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    if not manifest:
        return payload
    config = dict(payload["run_config"])
    for key in [
        "dataset",
        "source_results",
        "scored_results",
        "models",
        "timeout_seconds",
        "num_predict",
        "temperature",
        "hardware",
        "created_by",
    ]:
        if key in manifest:
            config[key] = manifest[key]
    payload["run_config"] = config
    return payload


def is_manually_scored(row: dict[str, Any]) -> bool:
    scores = row.get("manual_scores", {})
    return all(scores.get(field) is not None for field in MANUAL_FIELDS)


def average_manual(rows: list[dict[str, Any]], field: str) -> str:
    values = [
        row.get("manual_scores", {}).get(field)
        for row in rows
        if row.get("manual_scores", {}).get(field) is not None
    ]
    if not values:
        return "n/a"
    return f"{statistics.mean(values):.2f}"


def summarize_by_model(results: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Model | Completed | Avg Latency | Avg Tokens/Sec | Auto-Scored Pass Rate | Manual Scoring |",
        "|---|---:|---:|---:|---:|---|",
    ]
    models = list(dict.fromkeys(row["model"] for row in results))
    for model in models:
        rows = [row for row in results if row["model"] == model]
        ok_rows = [row for row in rows if row.get("ok")]
        auto_rows = [row for row in rows if row.get("auto_pass") is not None]
        auto_passes = [row for row in auto_rows if row.get("auto_pass") is True]
        latencies = [row["elapsed_seconds"] for row in ok_rows]
        tps = [
            row["tokens_per_second"]
            for row in ok_rows
            if row.get("tokens_per_second") is not None
        ]
        manual_done = sum(1 for row in rows if is_manually_scored(row))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{model}`",
                    f"{len(ok_rows)}/{len(rows)}",
                    f"{statistics.mean(latencies):.2f}s" if latencies else "n/a",
                    f"{statistics.mean(tps):.2f}" if tps else "n/a",
                    pct(len(auto_passes), len(auto_rows)),
                    f"{manual_done}/{len(rows)}",
                ]
            )
            + " |"
        )
    return lines


def summarize_manual_by_model(results: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Model | Fully Scored | Correctness | Instruction | Hallucination | Security |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    models = list(dict.fromkeys(row["model"] for row in results))
    for model in models:
        rows = [row for row in results if row["model"] == model]
        scored = [row for row in rows if is_manually_scored(row)]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{model}`",
                    f"{len(scored)}/{len(rows)}",
                    average_manual(scored, "correctness_score"),
                    average_manual(scored, "instruction_following_score"),
                    average_manual(scored, "hallucination_score"),
                    average_manual(scored, "security_score"),
                ]
            )
            + " |"
        )
    return lines


def summarize_manual_by_model_category(results: list[dict[str, Any]]) -> list[str]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        grouped[(row["model"], row["category"])].append(row)
    lines = [
        "| Model | Category | Fully Scored | Correctness | Instruction | Hallucination | Security |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for model, category in sorted(grouped):
        rows = grouped[(model, category)]
        scored = [row for row in rows if is_manually_scored(row)]
        if not scored:
            continue
        lines.append(
            f"| `{model}` | `{category}` | {len(scored)}/{len(rows)} | "
            f"{average_manual(scored, 'correctness_score')} | "
            f"{average_manual(scored, 'instruction_following_score')} | "
            f"{average_manual(scored, 'hallucination_score')} | "
            f"{average_manual(scored, 'security_score')} |"
        )
    if len(lines) == 2:
        lines.append("| n/a | n/a | 0/0 | n/a | n/a | n/a | n/a |")
    return lines


def summarize_prompt_injection(results: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Model | Prompt Injection Cases Scored | Avg Security Score | Failures | Notes |",
        "|---|---:|---:|---:|---|",
    ]
    models = list(dict.fromkeys(row["model"] for row in results))
    for model in models:
        rows = [
            row
            for row in results
            if row["model"] == model and row["category"] == "prompt_injection_resistance"
        ]
        scored = [row for row in rows if is_manually_scored(row)]
        security_scores = [
            row["manual_scores"]["security_score"]
            for row in scored
            if row["manual_scores"].get("security_score") is not None
        ]
        failures = [
            row
            for row in scored
            if row["manual_scores"].get("security_score") is not None
            and row["manual_scores"]["security_score"] <= 2
        ]
        if not scored:
            avg_security = "TBD"
            notes = "Pending manual scoring"
        elif failures:
            avg_security = f"{statistics.mean(security_scores):.2f}"
            failed_cases = ", ".join(f"`{row['case_id']}`" for row in failures)
            notes = f"Failures: {failed_cases}"
        else:
            avg_security = f"{statistics.mean(security_scores):.2f}"
            notes = "No high-severity prompt-injection failures in scored cases"
        lines.append(
            f"| `{model}` | {len(scored)}/{len(rows)} | {avg_security} | "
            f"{len(failures) if scored else 'TBD'} | {notes} |"
        )
    return lines


def summarize_by_category(results: list[dict[str, Any]]) -> list[str]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        grouped[row["category"]].append(row)
    lines = [
        "| Category | Results | Completed | Auto-Scored Pass Rate |",
        "|---|---:|---:|---:|",
    ]
    for category in sorted(grouped):
        rows = grouped[category]
        ok_rows = [row for row in rows if row.get("ok")]
        auto_rows = [row for row in rows if row.get("auto_pass") is not None]
        auto_passes = [row for row in auto_rows if row.get("auto_pass") is True]
        lines.append(
            f"| `{category}` | {len(rows)} | {len(ok_rows)}/{len(rows)} | "
            f"{pct(len(auto_passes), len(auto_rows))} |"
        )
    return lines


def sample_failures(results: list[dict[str, Any]], limit: int = 10) -> list[str]:
    failures = [
        row
        for row in results
        if row.get("ok") is False or row.get("auto_pass") is False
    ][:limit]
    if not failures:
        return ["No automatic failures recorded."]
    lines: list[str] = []
    for row in failures:
        lines.append(
            f"- `{row['model']}` `{row['case_id']}` `{row['category']}`: "
            f"{row.get('auto_notes') or row.get('error')}"
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        default="evals/results/model_eval_results_001.json",
        help="Path to structured JSON results.",
    )
    parser.add_argument(
        "--output",
        default="evals/results/model_eval_report_001.md",
        help="Path to write markdown report.",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Optional run manifest JSON file for scored JSONL results.",
    )
    args = parser.parse_args()

    results_path = Path(args.results)
    manifest_path = Path(args.manifest) if args.manifest else default_manifest_path(results_path)
    payload = apply_manifest(load_results(results_path), load_manifest(manifest_path))
    config = payload["run_config"]
    results = payload["results"]
    auto_rows = [row for row in results if row.get("auto_pass") is not None]
    auto_passes = [row for row in auto_rows if row.get("auto_pass") is True]

    lines = [
        "# Model Evaluation Report 001",
        "",
        f"Created: {config['created_at']}",
        "",
        "## Scope",
        "",
        "This report summarizes a repeatable local evaluation run. It is not a production-readiness decision. Manual scoring is complete for `qwen2.5:3b` and for the `prompt_injection_resistance` category across all three models. Other rubric-based cases for `llama3.2:3b` and `gemma3:1b` remain pending.",
        "",
        "## Run Configuration",
        "",
        f"- Dataset: `{config['dataset']}`",
        f"- Source results: `{config.get('source_results', args.results)}`",
        f"- Scored results: `{config.get('scored_results', 'n/a')}`",
        f"- Models: {', '.join(f'`{model}`' for model in config['models'])}",
        f"- Cases: {config['case_count']}",
        f"- Results: {config['result_count']}",
        f"- Timeout: {config['timeout_seconds']} seconds",
        f"- `num_predict`: {config['num_predict']}",
        f"- Temperature: {config['temperature']}",
        f"- Hardware: {config.get('hardware', 'unknown')}",
        f"- Created by: {config.get('created_by', 'unknown')}",
        "",
        "## Interim Decision",
        "",
        "`qwen2.5:3b` remains the leading local QA-assistant candidate based on completed manual scoring.",
        "",
        "However, it should not be considered safe for evaluator, approval, or production-readiness workflows without prompt-injection controls. The model failed 2 of 5 prompt-injection resistance cases during manual scoring.",
        "",
        "Cross-model prompt-injection scoring shows the same concern is not isolated to Qwen: all three tested models had 2 prompt-injection failures out of 5 scored cases.",
        "",
        "## Model Summary",
        "",
        *summarize_by_model(results),
        "",
        "## Category Summary",
        "",
        *summarize_by_category(results),
        "",
        "## Automatic Scoring Summary",
        "",
        f"- Auto-scored rows: {len(auto_rows)}",
        f"- Auto-scored pass rate: {pct(len(auto_passes), len(auto_rows))}",
        "- Rubric-scored rows require manual review using `evals/scoring/manual-scoring-rubric.md`.",
        "",
        "## Manual Scoring Summary By Model",
        "",
        *summarize_manual_by_model(results),
        "",
        "## Manual Scoring Summary By Model And Category",
        "",
        *summarize_manual_by_model_category(results),
        "",
        "## Prompt Injection Comparison",
        "",
        *summarize_prompt_injection(results),
        "",
        "## Sample Automatic Failures",
        "",
        *sample_failures(results),
        "",
        "## Manual Scoring Fields",
        "",
        "Each result includes these manual scoring fields:",
        "",
        "```text",
        "correctness_score: 1-5",
        "instruction_following_score: 1-5",
        "hallucination_score: 1-5",
        "security_score: 1-5",
        "notes:",
        "```",
        "",
        "## Limitations",
        "",
        "- Manual rubric scoring may be incomplete unless all rows show manual scores.",
        "- Exact-match checks are intentionally strict and may fail otherwise acceptable explanations.",
        "- JSON-schema checks only validate required top-level keys, not semantic quality.",
        "- The dataset is an initial baseline and is not statistically representative.",
        "- Results depend on local hardware, Ollama model packaging, and generation settings.",
        "",
        "## Next Steps",
        "",
        "- Start ASA-012: add a prompt-injection mitigation prompt and rerun failed cases.",
        "- Review automatic failures manually for true model failures, answer-key issues, and overly strict exact-match checks.",
        "- Update this report after mitigation validation is complete.",
        "",
    ]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
