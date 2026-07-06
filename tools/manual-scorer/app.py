#!/usr/bin/env python3
"""Streamlit UI for manually scoring local LLM evaluation results."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_RESULTS = REPO_ROOT / "evals/results/model_eval_results_001.json"
DEFAULT_SCORED_RESULTS = REPO_ROOT / "evals/results/scored/model_eval_001_scored.jsonl"
ASA014_RAW_RESULTS = REPO_ROOT / "security/attack-logs/asa_014_human_review_queue_001.jsonl"
ASA014_SCORED_RESULTS = REPO_ROOT / "security/attack-logs/asa_014_human_review_queue_001_scored.jsonl"
REVIEW_STATUSES = [
    "unscored",
    "scored",
    "needs_review",
    "answer_key_issue",
    "scorer_unsure",
]
MANUAL_FIELDS = [
    "correctness_score",
    "instruction_following_score",
    "hallucination_score",
    "security_score",
]
SECURITY_OUTCOMES = ["", "pass", "fail", "unclear"]
HEURISTIC_DISPOSITIONS = [
    "",
    "true_positive",
    "false_positive",
    "true_negative",
    "false_negative",
]


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def result_key(row: dict[str, Any]) -> str:
    return f"{row.get('mode', 'eval')}::{row['model']}::{row['case_id']}"


def default_manual_scores(row: dict[str, Any]) -> dict[str, Any]:
    existing = row.get("manual_scores") or {}
    return {
        "correctness_score": existing.get("correctness_score"),
        "instruction_following_score": existing.get("instruction_following_score"),
        "hallucination_score": existing.get("hallucination_score"),
        "security_score": existing.get("security_score"),
        "notes": existing.get("notes", ""),
    }


def default_manual_review(row: dict[str, Any]) -> dict[str, Any]:
    existing = row.get("manual_review") or {}
    return {
        "human_security_outcome": existing.get("human_security_outcome"),
        "heuristic_disposition": existing.get("heuristic_disposition"),
        "security_score": existing.get("security_score"),
        "evaluator_usefulness_score": existing.get("evaluator_usefulness_score"),
        "notes": existing.get("notes", ""),
    }


def load_raw_results(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix == ".jsonl":
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("results", payload if isinstance(payload, list) else [])
    normalized: list[dict[str, Any]] = []
    for row in rows:
        copied = dict(row)
        copied["manual_scores"] = default_manual_scores(copied)
        if "manual_review" in copied:
            copied["manual_review"] = default_manual_review(copied)
        copied.setdefault("review_status", "unscored")
        copied.setdefault("scored_at", "")
        copied.setdefault("scorer", "")
        normalized.append(copied)
    return normalized


def load_scored_rows(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    scored: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        scored[result_key(row)] = row
    return scored


def merge_scored_rows(
    raw_rows: list[dict[str, Any]],
    scored_rows: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for row in raw_rows:
        key = result_key(row)
        if key in scored_rows:
            saved = scored_rows[key]
            row["manual_scores"] = default_manual_scores(saved)
            if "manual_review" in row or "manual_review" in saved:
                row["manual_review"] = default_manual_review(saved)
            row["review_status"] = saved.get("review_status", row.get("review_status", "unscored"))
            row["scored_at"] = saved.get("scored_at", "")
            row["scorer"] = saved.get("scorer", "")
        merged.append(row)
    return merged


def write_scored_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_manually_scored(row: dict[str, Any]) -> bool:
    scores = row.get("manual_scores", {})
    return all(scores.get(field) is not None for field in MANUAL_FIELDS)


def is_manual_review_scored(row: dict[str, Any]) -> bool:
    review = row.get("manual_review")
    if not review:
        return is_manually_scored(row)
    return all(
        review.get(field) not in ("", None)
        for field in [
            "human_security_outcome",
            "heuristic_disposition",
            "security_score",
            "evaluator_usefulness_score",
        ]
    )


def score_value(value: Any) -> int | None:
    if value in ("", None):
        return None
    return int(value)


def score_label(value: Any) -> str:
    return "" if value is None else str(value)


def completed_manual_review(
    human_security_outcome: str,
    heuristic_disposition: str,
    security_score: str,
    usefulness_score: str,
) -> bool:
    return all([human_security_outcome, heuristic_disposition, security_score, usefulness_score])


def auto_filter_match(row: dict[str, Any], selected: str) -> bool:
    auto_pass = row.get("auto_pass")
    if selected == "All":
        return True
    if selected == "Auto pass":
        return auto_pass is True
    if selected == "Auto fail":
        return auto_pass is False
    if selected == "Manual only":
        return auto_pass is None
    if selected == "Model call failed":
        return row.get("ok") is False
    return True


def status_filter_match(row: dict[str, Any], selected: str) -> bool:
    if selected == "All":
        return True
    if selected == "Unscored":
        return not is_manual_review_scored(row) and row.get("review_status") == "unscored"
    return row.get("review_status") == selected


def progress_summary(rows: list[dict[str, Any]]) -> tuple[int, int]:
    scored_count = sum(1 for row in rows if is_manual_review_scored(row))
    return scored_count, len(rows)


def render_metadata(row: dict[str, Any]) -> None:
    cols = st.columns(4)
    cols[0].metric("Model", row["model"])
    cols[1].metric("Case", row["case_id"])
    cols[2].metric("Category", row["category"])
    cols[3].metric("Risk", row["risk"])
    st.caption(
        f"Auto score: `{row.get('auto_pass')}` | "
        f"Scoring type: `{row.get('scoring_type')}` | "
        f"Latency: `{row.get('elapsed_seconds')}s` | "
        f"Tokens/sec: `{row.get('tokens_per_second')}`"
    )
    if "attack_family" in row:
        st.caption(
            f"Mode: `{row.get('mode')}` | "
            f"Attack family: `{row.get('attack_family')}` | "
            f"Severity: `{row.get('severity_if_failed')}` | "
            f"Control layer: `{row.get('control_layer_expected')}` | "
            f"Heuristic pass: `{row.get('heuristic_pass')}`"
        )


def main() -> None:
    st.set_page_config(page_title="Manual Scoring UI 001", layout="wide")
    st.title("Manual Scoring UI 001")
    st.caption("Human scoring for Phase 2 model evaluation. Raw result files are read-only.")

    with st.sidebar:
        st.header("Files")
        preset = st.selectbox(
            "Workflow preset",
            ["ASA-014 Human Review", "Phase 2 Manual Scoring"],
        )
        default_raw = ASA014_RAW_RESULTS if preset == "ASA-014 Human Review" else DEFAULT_RAW_RESULTS
        default_scored = ASA014_SCORED_RESULTS if preset == "ASA-014 Human Review" else DEFAULT_SCORED_RESULTS
        raw_path_text = st.text_input(
            "Raw result file",
            value=str(default_raw.relative_to(REPO_ROOT)),
        )
        scored_path_text = st.text_input(
            "Scored output file",
            value=str(default_scored.relative_to(REPO_ROOT)),
        )
        scorer = st.text_input("Scorer", value="Matthew")
        st.divider()

    raw_path = resolve_path(raw_path_text)
    scored_path = resolve_path(scored_path_text)

    try:
        rows = merge_scored_rows(load_raw_results(raw_path), load_scored_rows(scored_path))
    except Exception as exc:
        st.error(f"Could not load results: {exc}")
        return

    models = sorted({row["model"] for row in rows})
    categories = sorted({row["category"] for row in rows})
    modes = sorted({row.get("mode", "eval") for row in rows})
    attack_families = sorted({row.get("attack_family") for row in rows if row.get("attack_family")})
    control_layers = sorted({row.get("control_layer_expected") for row in rows if row.get("control_layer_expected")})
    review_reasons = sorted({reason for row in rows for reason in row.get("review_reasons", [])})

    with st.sidebar:
        st.header("Filters")
        selected_modes = st.multiselect("Mode", modes, default=modes)
        selected_models = st.multiselect("Model", models, default=models)
        selected_categories = st.multiselect("Category", categories, default=categories)
        selected_attack_families = (
            st.multiselect("Attack family", attack_families, default=attack_families)
            if attack_families
            else []
        )
        selected_control_layers = (
            st.multiselect("Control layer", control_layers, default=control_layers)
            if control_layers
            else []
        )
        selected_review_reasons = (
            st.multiselect("Review reason", review_reasons, default=review_reasons)
            if review_reasons
            else []
        )
        heuristic_filter = st.selectbox(
            "Heuristic result",
            ["All", "Heuristic pass", "Heuristic fail"],
        )
        default_status_index = 1 if preset == "ASA-014 Human Review" else 0
        status_filter = st.selectbox(
            "Manual status",
            ["All", "Unscored", "scored", "needs_review", "answer_key_issue", "scorer_unsure"],
            index=default_status_index,
        )
        auto_filter = st.selectbox(
            "Automatic score",
            ["All", "Auto pass", "Auto fail", "Manual only", "Model call failed"],
        )

    filtered = [
        row
        for row in rows
        if row.get("mode", "eval") in selected_modes
        and row["model"] in selected_models
        and row["category"] in selected_categories
        and (not attack_families or row.get("attack_family") in selected_attack_families)
        and (not control_layers or row.get("control_layer_expected") in selected_control_layers)
        and (
            not review_reasons
            or not selected_review_reasons
            or set(row.get("review_reasons", [])) & set(selected_review_reasons)
        )
        and (
            heuristic_filter == "All"
            or (heuristic_filter == "Heuristic pass" and row.get("heuristic_pass") is True)
            or (heuristic_filter == "Heuristic fail" and row.get("heuristic_pass") is False)
        )
        and status_filter_match(row, status_filter)
        and auto_filter_match(row, auto_filter)
    ]

    overall_scored, overall_total = progress_summary(rows)
    filtered_scored, filtered_total = progress_summary(filtered)
    st.progress(overall_scored / overall_total if overall_total else 0)
    st.write(
        f"Overall progress: **{overall_scored}/{overall_total}** scored. "
        f"Filtered progress: **{filtered_scored}/{filtered_total}** scored."
    )
    st.caption(f"Scored output: `{scored_path}`")

    if not filtered:
        st.info("No results match the current filters.")
        return

    labels = [
        f"{index + 1}. {row.get('mode', 'eval')} | {row['model']} | {row['case_id']} | {row.get('attack_family', row['category'])} | {row.get('review_status', 'unscored')}"
        for index, row in enumerate(filtered)
    ]
    selected_label = st.selectbox("Result", labels, index=0)
    selected_index = labels.index(selected_label)
    selected = filtered[selected_index]
    selected_key = result_key(selected)

    st.divider()
    render_metadata(selected)

    left, right = st.columns(2)
    with left:
        st.subheader("Prompt")
        st.code(selected.get("prompt") or selected.get("original_prompt", ""), language="markdown")
        st.subheader("Expected Answer / Behavior")
        st.write(selected.get("expected_behavior") or selected.get("expected_answer", ""))
        if selected.get("failure_condition"):
            st.subheader("Failure Condition")
            st.write(selected["failure_condition"])
        if selected.get("review_reasons"):
            st.subheader("Review Reasons")
            st.write(selected["review_reasons"])
        st.subheader("Automatic / Heuristic Scoring")
        if "heuristic_pass" in selected:
            st.write(
                {
                    "heuristic_pass": selected.get("heuristic_pass"),
                    "heuristic_notes": selected.get("heuristic_notes"),
                    "failure_summary": selected.get("failure_summary"),
                }
            )
        else:
            st.write(
                {
                    "auto_pass": selected.get("auto_pass"),
                    "auto_score_type": selected.get("auto_score_type"),
                    "auto_notes": selected.get("auto_notes"),
                }
            )
    with right:
        st.subheader("Model Response")
        st.code(selected.get("response", ""), language="markdown")
        if selected.get("error"):
            st.error(selected["error"])

    st.divider()
    st.subheader("Manual Review" if "manual_review" in selected else "Manual Score")
    score_options = ["", "1", "2", "3", "4", "5"]
    if "manual_review" in selected:
        existing_review = selected.get("manual_review", {})
        with st.form(f"review_form_{selected_key}"):
            current_review_status = selected.get("review_status", "unscored")
            default_review_status = "scored" if current_review_status == "unscored" else current_review_status
            cols = st.columns(4)
            human_security_outcome = cols[0].selectbox(
                "Security outcome",
                SECURITY_OUTCOMES,
                index=SECURITY_OUTCOMES.index(existing_review.get("human_security_outcome") or ""),
            )
            heuristic_disposition = cols[1].selectbox(
                "Heuristic disposition",
                HEURISTIC_DISPOSITIONS,
                index=HEURISTIC_DISPOSITIONS.index(existing_review.get("heuristic_disposition") or ""),
            )
            security = cols[2].selectbox(
                "Security score",
                score_options,
                index=score_options.index(score_label(existing_review.get("security_score"))),
            )
            usefulness = cols[3].selectbox(
                "Evaluator usefulness",
                score_options,
                index=score_options.index(score_label(existing_review.get("evaluator_usefulness_score"))),
            )
            review_status = st.selectbox(
                "Review status",
                REVIEW_STATUSES,
                index=REVIEW_STATUSES.index(default_review_status),
            )
            notes = st.text_area("Notes", value=existing_review.get("notes", ""), height=120)
            submitted = st.form_submit_button("Save review and next")
    else:
        existing_scores = selected.get("manual_scores", {})
        with st.form(f"score_form_{selected_key}"):
            cols = st.columns(4)
            correctness = cols[0].selectbox(
                "Correctness",
                score_options,
                index=score_options.index(score_label(existing_scores.get("correctness_score"))),
            )
            instruction = cols[1].selectbox(
                "Instruction following",
                score_options,
                index=score_options.index(score_label(existing_scores.get("instruction_following_score"))),
            )
            hallucination = cols[2].selectbox(
                "Hallucination",
                score_options,
                index=score_options.index(score_label(existing_scores.get("hallucination_score"))),
            )
            security = cols[3].selectbox(
                "Security",
                score_options,
                index=score_options.index(score_label(existing_scores.get("security_score"))),
            )
            review_status = st.selectbox(
                "Review status",
                REVIEW_STATUSES,
                index=REVIEW_STATUSES.index(selected.get("review_status", "unscored")),
            )
            notes = st.text_area("Notes", value=existing_scores.get("notes", ""), height=120)
            submitted = st.form_submit_button("Save score")

    if submitted:
        updated_rows = []
        for row in rows:
            if result_key(row) == selected_key:
                row = dict(row)
                if "manual_review" in row:
                    saved_review_status = review_status
                    if review_status == "unscored" and completed_manual_review(
                        human_security_outcome,
                        heuristic_disposition,
                        security,
                        usefulness,
                    ):
                        saved_review_status = "scored"
                    row["manual_review"] = {
                        "human_security_outcome": human_security_outcome or None,
                        "heuristic_disposition": heuristic_disposition or None,
                        "security_score": score_value(security),
                        "evaluator_usefulness_score": score_value(usefulness),
                        "notes": notes,
                    }
                    row["review_status"] = saved_review_status
                else:
                    row["manual_scores"] = {
                        "correctness_score": score_value(correctness),
                        "instruction_following_score": score_value(instruction),
                        "hallucination_score": score_value(hallucination),
                        "security_score": score_value(security),
                        "notes": notes,
                    }
                    row["review_status"] = review_status
                row["scorer"] = scorer
                row["scored_at"] = datetime.now(timezone.utc).isoformat()
            updated_rows.append(row)
        write_scored_rows(scored_path, updated_rows)
        st.success("Saved progress without modifying the raw result file.")
        st.rerun()

    with st.expander("Raw merged result"):
        st.json(selected)


if __name__ == "__main__":
    main()
