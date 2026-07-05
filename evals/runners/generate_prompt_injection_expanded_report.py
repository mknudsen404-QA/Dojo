#!/usr/bin/env python3
"""Generate the ASA-013 expanded prompt-injection results report."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_results(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def failures(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("heuristic_pass") is False]


def model_order(rows: list[dict[str, Any]]) -> list[str]:
    return list(dict.fromkeys(row["model"] for row in rows))


def family_order(rows: list[dict[str, Any]]) -> list[str]:
    return list(dict.fromkeys(row["attack_family"] for row in rows))


def summarize_by_model(
    baseline_rows: list[dict[str, Any]],
    mitigated_rows: list[dict[str, Any]],
) -> list[str]:
    lines = [
        "| Model | Baseline Failures | Mitigated Failures | Failures Reduced | Notes |",
        "|---|---:|---:|---:|---|",
    ]
    for model in model_order(baseline_rows):
        base_failures = failures([row for row in baseline_rows if row["model"] == model])
        mit_failures = failures([row for row in mitigated_rows if row["model"] == model])
        reduced = len(base_failures) - len(mit_failures)
        notes = "No obvious mitigated failures" if not mit_failures else "Human review required for remaining failures"
        lines.append(f"| `{model}` | {len(base_failures)} | {len(mit_failures)} | {reduced} | {notes} |")
    return lines


def summarize_by_family(
    baseline_rows: list[dict[str, Any]],
    mitigated_rows: list[dict[str, Any]],
) -> list[str]:
    lines = [
        "| Attack Family | Baseline Failures | Mitigated Failures | Most Common Failure Mode |",
        "|---|---:|---:|---|",
    ]
    all_families = family_order(baseline_rows)
    for family in all_families:
        base_failures = failures([row for row in baseline_rows if row["attack_family"] == family])
        mit_failures = failures([row for row in mitigated_rows if row["attack_family"] == family])
        mode_counts = Counter(row["failure_condition"] for row in base_failures + mit_failures)
        common = mode_counts.most_common(1)[0][0] if mode_counts else "No obvious failures detected"
        lines.append(f"| `{family}` | {len(base_failures)} | {len(mit_failures)} | {common} |")
    return lines


def remaining_failures(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Model | Case | Attack Family | Severity | Failure Summary | Recommended Control |",
        "|---|---|---|---|---|---|",
    ]
    remaining = failures(rows)
    if not remaining:
        lines.append("| n/a | n/a | n/a | n/a | No obvious mitigated failures detected by heuristic. | n/a |")
        return lines
    for row in remaining:
        lines.append(
            f"| `{row['model']}` | `{row['case_id']}` | `{row['attack_family']}` | "
            f"{row['severity_if_failed']} | {row['failure_summary'] or row['failure_condition']} | "
            f"`{row.get('control_layer_expected', 'unknown')}` |"
        )
    return lines


def summarize_by_control_layer(
    baseline_rows: list[dict[str, Any]],
    mitigated_rows: list[dict[str, Any]],
) -> list[str]:
    lines = [
        "| Expected Control Layer | Baseline Failures | Mitigated Failures | Interpretation |",
        "|---|---:|---:|---|",
    ]
    layers = list(dict.fromkeys(row.get("control_layer_expected", "unknown") for row in baseline_rows))
    for layer in layers:
        base_failures = failures(
            [row for row in baseline_rows if row.get("control_layer_expected", "unknown") == layer]
        )
        mit_failures = failures(
            [row for row in mitigated_rows if row.get("control_layer_expected", "unknown") == layer]
        )
        if mit_failures:
            interpretation = "Prompt mitigation helped, but this control layer still needs architectural validation."
        elif base_failures:
            interpretation = "Prompt mitigation removed obvious failures in this run; architectural validation still needed."
        else:
            interpretation = "No obvious failures detected by heuristic in either run."
        lines.append(f"| `{layer}` | {len(base_failures)} | {len(mit_failures)} | {interpretation} |")
    return lines


def sample_failures(rows: list[dict[str, Any]], title: str, limit: int = 12) -> list[str]:
    rows = failures(rows)[:limit]
    lines = [f"## {title}", ""]
    if not rows:
        lines.append("No obvious failures detected by heuristic.")
        return lines
    for row in rows:
        response = row.get("response", "").replace("\n", " ")
        if len(response) > 220:
            response = response[:217].rstrip() + "..."
        lines.append(
            f"- `{row['model']}` `{row['case_id']}` `{row['attack_family']}`: "
            f"{row['heuristic_notes']} Response: {response}"
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline",
        default="evals/results/prompt_injection_expanded_baseline_001.json",
    )
    parser.add_argument(
        "--mitigated",
        default="evals/results/prompt_injection_expanded_mitigated_001.json",
    )
    parser.add_argument(
        "--output",
        default="security/findings/prompt_injection_expanded_results_001.md",
    )
    args = parser.parse_args()

    baseline_payload = load_results(Path(args.baseline))
    mitigated_payload = load_results(Path(args.mitigated))
    baseline_rows = baseline_payload["results"]
    mitigated_rows = mitigated_payload["results"]
    baseline_failures = failures(baseline_rows)
    mitigated_failures = failures(mitigated_rows)
    reduced = len(baseline_failures) - len(mitigated_failures)
    answer = (
        "The ASA-012 mitigation reduced obvious failures on the expanded dataset, "
        "but results are heuristic and require human review."
        if reduced > 0
        else "The ASA-012 mitigation did not reduce obvious failures in this expanded heuristic run."
    )

    lines = [
        "# Prompt Injection Expanded Results 001",
        "",
        "Date: 2026-07-05",
        "",
        "Phase: 2 - Evaluation Harness",
        "",
        "Question: Did the ASA-012 mitigation still hold up against a broader and more realistic prompt-injection dataset?",
        "",
        f"Answer: {answer}",
        "",
        "## Scope",
        "",
        "This report compares baseline and mitigated runs across the ASA-013 30-case expanded prompt-injection dataset. It uses deterministic heuristics to flag obvious failures and does not replace human scoring.",
        "",
        "## Run Configuration",
        "",
        f"- Dataset: `{baseline_payload['run_config']['dataset']}`",
        f"- Baseline results: `{args.baseline}`",
        f"- Mitigated results: `{args.mitigated}`",
        f"- Mitigation prompt: `{mitigated_payload['run_config'].get('mitigation_prompt', '')}`",
        f"- Models: {', '.join(f'`{model}`' for model in baseline_payload['run_config']['models'])}",
        f"- Cases per model: {baseline_payload['run_config']['case_count']}",
        f"- Baseline results: {baseline_payload['run_config']['result_count']}",
        f"- Mitigated results: {mitigated_payload['run_config']['result_count']}",
        f"- Timeout: {baseline_payload['run_config']['timeout_seconds']} seconds",
        f"- `num_predict`: {baseline_payload['run_config']['num_predict']}",
        f"- Temperature: {baseline_payload['run_config']['temperature']}",
        "",
        "## Results Summary",
        "",
        f"- Baseline obvious heuristic failures: {len(baseline_failures)}/{len(baseline_rows)}",
        f"- Mitigated obvious heuristic failures: {len(mitigated_failures)}/{len(mitigated_rows)}",
        f"- Obvious failures reduced: {reduced}",
        "- Human review is required before treating these as final security scores.",
        "",
        "## Results By Model",
        "",
        *summarize_by_model(baseline_rows, mitigated_rows),
        "",
        "## Results By Attack Family",
        "",
        *summarize_by_family(baseline_rows, mitigated_rows),
        "",
        "## Results By Expected Control Layer",
        "",
        *summarize_by_control_layer(baseline_rows, mitigated_rows),
        "",
        "## Remaining Failures",
        "",
        *remaining_failures(mitigated_rows),
        "",
        *sample_failures(baseline_rows, "Sample Baseline Failures"),
        "",
        *sample_failures(mitigated_rows, "Sample Mitigated Failures"),
        "",
        "## Assurance Interpretation",
        "",
        "The expanded dataset tests more realistic application failure modes than the first five smoke tests, including RAG poisoning, model-as-judge manipulation, tool-use manipulation, and release-gate pressure.",
        "",
        "This run should be treated as control validation evidence, not proof of security. Prompt-level mitigation may reduce obvious failures, but tool-use, release approval, and data-exfiltration risks still need architectural controls such as permission gates, output validation, retrieval sanitization, and human approval.",
        "",
        "## Limitations",
        "",
        "- Results are scored by deterministic heuristics for obvious failures.",
        "- Subtle failures, low-quality safe responses, and incomplete evaluator reasoning may require manual scoring.",
        "- The dataset is broader than ASA-012 but still not representative of all prompt-injection attacks.",
        "- No broad security claim should be made from this dataset alone.",
        "",
        "## Next Steps",
        "",
        "- Manually review remaining failures and a sample of heuristic passes.",
        "- Add human scores for security success and evaluator usefulness.",
        "- Add non-prompt controls for tool permission, retrieval sanitization, output validation, and human approval.",
        "",
    ]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
