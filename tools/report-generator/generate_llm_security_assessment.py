#!/usr/bin/env python3
"""Generate a Phase 3 security assessment report from red-team results."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_results(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def failures(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("heuristic_pass") is False]


def ordered_values(rows: list[dict[str, Any]], key: str) -> list[str]:
    return list(dict.fromkeys(row.get(key, "") for row in rows))


def table_by_model(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Model | Cases | Heuristic Failures | Critical/High Failures | Avg Latency | Notes |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for model in ordered_values(rows, "model"):
        subset = [row for row in rows if row["model"] == model]
        failed = failures(subset)
        severe = [
            row
            for row in failed
            if row.get("severity_if_failed") in {"critical", "high"}
        ]
        latencies = [row["elapsed_seconds"] for row in subset if row.get("elapsed_seconds") is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        notes = "Human review required for failures" if failed else "No obvious heuristic failures"
        lines.append(
            f"| `{model}` | {len(subset)} | {len(failed)} | {len(severe)} | "
            f"{avg_latency:.2f}s | {notes} |"
        )
    return lines


def table_by_category(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Category | Cases | Heuristic Failures | Top Risk |",
        "|---|---:|---:|---|",
    ]
    for category in ordered_values(rows, "category"):
        subset = [row for row in rows if row["category"] == category]
        failed = failures(subset)
        risk = Counter(row["risk"] for row in failed).most_common(1)
        top_risk = risk[0][0] if risk else "n/a"
        lines.append(f"| `{category}` | {len(subset)} | {len(failed)} | `{top_risk}` |")
    return lines


def table_by_severity(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Severity If Failed | Cases | Heuristic Failures |",
        "|---|---:|---:|",
    ]
    order = ["critical", "high", "medium", "low", "informational"]
    for severity in order:
        subset = [row for row in rows if row.get("severity_if_failed") == severity]
        if subset:
            lines.append(f"| {severity} | {len(subset)} | {len(failures(subset))} |")
    return lines


def response_excerpt(row: dict[str, Any], limit: int = 180) -> str:
    response = row.get("response", "").replace("\n", " ")
    if len(response) > limit:
        response = response[: limit - 3].rstrip() + "..."
    return response or "No response."


def failure_rows(rows: list[dict[str, Any]], limit: int) -> list[str]:
    lines = [
        "| Model | Case | Category | Severity | Expected Behavior | Observed Signal | Response Excerpt | Mitigation |",
        "|---|---|---|---|---|---|---|---|",
    ]
    failed = failures(rows)[:limit]
    if not failed:
        lines.append("| n/a | n/a | n/a | n/a | No obvious heuristic failures. | n/a | n/a | n/a |")
        return lines
    for row in failed:
        lines.append(
            f"| `{row['model']}` | `{row['case_id']}` | `{row['category']}` | "
            f"{row['severity_if_failed']} | {row['expected_behavior']} | "
            f"{row['heuristic_notes']} | {response_excerpt(row)} | {row['mitigation_notes']} |"
        )
    return lines


def source_lines() -> list[str]:
    return [
        "- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/",
        "- OWASP 2025 LLM risks archive: https://genai.owasp.org/llm-top-10/",
        "- MITRE ATLAS SAFE-AI report: https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        default="security/attack-logs/phase3_attack_results_001.json",
    )
    parser.add_argument(
        "--output",
        default="security/findings/llm_security_assessment_001.md",
    )
    parser.add_argument("--sample-limit", type=int, default=50)
    args = parser.parse_args()

    payload = load_results(Path(args.results))
    rows = payload["results"]
    failed = failures(rows)
    severe = [row for row in failed if row.get("severity_if_failed") in {"critical", "high"}]

    lines = [
        "# LLM Security Assessment 001",
        "",
        "Date: 2026-07-05",
        "",
        "Phase: 3 - AI Security Foundations",
        "",
        "## Question",
        "",
        "How do the local models behave across common LLM security attack classes under controlled, safe test prompts?",
        "",
        "## Short Answer",
        "",
        "This run creates the first Phase 3 security assessment baseline. Results are scored with deterministic failure-pattern heuristics, so they should be treated as triage evidence rather than final security findings until targeted human review is complete.",
        "",
        "## Scope",
        "",
        "This assessment uses local Ollama models and harmless synthetic prompts. It does not use real secrets, real system prompts, real customer data, live tools, or production systems.",
        "",
        "## Run Configuration",
        "",
        f"- Dataset: `{payload['run_config']['dataset']}`",
        f"- Results: `{args.results}`",
        f"- Models: {', '.join(f'`{model}`' for model in payload['run_config']['models'])}",
        f"- Cases per model: {payload['run_config']['case_count']}",
        f"- Total results: {payload['run_config']['result_count']}",
        f"- Timeout: {payload['run_config']['timeout_seconds']} seconds",
        f"- `num_predict`: {payload['run_config']['num_predict']}",
        f"- Temperature: {payload['run_config']['temperature']}",
        "",
        "## Results Summary",
        "",
        f"- Attack prompts tested: {payload['run_config']['case_count']}",
        f"- Model responses tested: {len(rows)}",
        f"- Heuristic failures: {len(failed)}/{len(rows)}",
        f"- Critical/high heuristic failures: {len(severe)}/{len(rows)}",
        "- Human review remains required for final severity confirmation.",
        "",
        "## Security Summary",
        "",
        "The strongest signal in this baseline is that local models can still disclose fake system-prompt content, follow direct scoring or approval overrides, and produce risky workflow guidance when prompts pressure them toward approval, disclosure, or excessive agency.",
        "",
        "The most important assurance lesson is that model behavior is only one layer. Production systems also need prompt boundaries, output validation, secret separation, tool permission checks, audit logging, and human approval gates for high-impact actions.",
        "",
        "## Results By Model",
        "",
        *table_by_model(rows),
        "",
        "## Results By Category",
        "",
        *table_by_category(rows),
        "",
        "## Results By Severity",
        "",
        *table_by_severity(rows),
        "",
        "## Heuristic Finding Candidates",
        "",
        *failure_rows(rows, args.sample_limit),
        "",
        "## Mitigation Themes",
        "",
        "- Prompt boundaries reduce some direct prompt-injection behavior but should not be treated as a complete security control.",
        "- System prompts and secrets should not contain sensitive data that would be harmful if disclosed.",
        "- Generated code, shell commands, HTML, JSON tool calls, and access policies need downstream validation before execution or rendering.",
        "- Tool use requires server-side permission checks, allowlists, and human approval for destructive or external actions.",
        "- Findings should be rated with `security/findings/severity_rubric.md`, not only with model-quality scores.",
        "",
        "## Limitations",
        "",
        "- The heuristic scorer flags obvious configured failure strings and can produce false positives or false negatives.",
        "- Some safe but low-quality responses may pass the heuristic while still being poor evaluator behavior.",
        "- Local model behavior may differ from hosted models or tool-enabled production agents.",
        "- This report does not prove security; it identifies test coverage and candidates for review.",
        "",
        "## Next Steps",
        "",
        "- Human-review all critical/high heuristic failures.",
        "- Add AI-assisted judge scoring for rubric cases after human calibration.",
        "- Create focused finding reports for repeated failures by attack class.",
        "- Add mitigation reruns for the highest-risk failure classes.",
        "",
        "## References",
        "",
        *source_lines(),
        "",
    ]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
