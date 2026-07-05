#!/usr/bin/env python3
"""Generate a markdown report from Phase 2 evaluation results."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "n/a"
    return f"{(numerator / denominator) * 100:.1f}%"


def load_results(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
        manual_done = sum(
            1
            for row in rows
            if row.get("manual_scores", {}).get("correctness_score") is not None
        )
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
    args = parser.parse_args()

    payload = load_results(Path(args.results))
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
        "This report summarizes a repeatable local evaluation run. It is not a production-readiness decision. Manual scoring is still required for rubric-based cases.",
        "",
        "## Run Configuration",
        "",
        f"- Dataset: `{config['dataset']}`",
        f"- Models: {', '.join(f'`{model}`' for model in config['models'])}",
        f"- Cases: {config['case_count']}",
        f"- Results: {config['result_count']}",
        f"- Timeout: {config['timeout_seconds']} seconds",
        f"- `num_predict`: {config['num_predict']}",
        f"- Temperature: {config['temperature']}",
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
        "- Manual rubric scoring is not complete.",
        "- Exact-match checks are intentionally strict and may fail otherwise acceptable explanations.",
        "- JSON-schema checks only validate required top-level keys, not semantic quality.",
        "- The dataset is an initial baseline and is not statistically representative.",
        "- Results depend on local hardware, Ollama model packaging, and generation settings.",
        "",
        "## Next Steps",
        "",
        "- Manually score the first 50 outputs for the leading model.",
        "- Add category-specific scoring guidance for hallucination and security cases.",
        "- Expand exact-match and JSON-schema scoring where objective checks are possible.",
        "- Compare scored results for `qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b`.",
        "",
    ]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
