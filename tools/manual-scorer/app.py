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


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def result_key(row: dict[str, Any]) -> str:
    return f"{row['model']}::{row['case_id']}"


def default_manual_scores(row: dict[str, Any]) -> dict[str, Any]:
    existing = row.get("manual_scores") or {}
    return {
        "correctness_score": existing.get("correctness_score"),
        "instruction_following_score": existing.get("instruction_following_score"),
        "hallucination_score": existing.get("hallucination_score"),
        "security_score": existing.get("security_score"),
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


def score_value(value: Any) -> int | None:
    if value in ("", None):
        return None
    return int(value)


def score_label(value: Any) -> str:
    return "" if value is None else str(value)


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
        return not is_manually_scored(row) and row.get("review_status") == "unscored"
    return row.get("review_status") == selected


def progress_summary(rows: list[dict[str, Any]]) -> tuple[int, int]:
    scored_count = sum(1 for row in rows if is_manually_scored(row))
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


def main() -> None:
    st.set_page_config(page_title="Manual Scoring UI 001", layout="wide")
    st.title("Manual Scoring UI 001")
    st.caption("Human scoring for Phase 2 model evaluation. Raw result files are read-only.")

    with st.sidebar:
        st.header("Files")
        raw_path_text = st.text_input(
            "Raw result file",
            value=str(DEFAULT_RAW_RESULTS.relative_to(REPO_ROOT)),
        )
        scored_path_text = st.text_input(
            "Scored output file",
            value=str(DEFAULT_SCORED_RESULTS.relative_to(REPO_ROOT)),
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

    with st.sidebar:
        st.header("Filters")
        default_models = ["qwen2.5:3b"] if "qwen2.5:3b" in models else models
        selected_models = st.multiselect("Model", models, default=default_models)
        selected_categories = st.multiselect("Category", categories, default=categories)
        status_filter = st.selectbox(
            "Manual status",
            ["All", "Unscored", "scored", "needs_review", "answer_key_issue", "scorer_unsure"],
        )
        auto_filter = st.selectbox(
            "Automatic score",
            ["All", "Auto pass", "Auto fail", "Manual only", "Model call failed"],
        )

    filtered = [
        row
        for row in rows
        if row["model"] in selected_models
        and row["category"] in selected_categories
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
        f"{index + 1}. {row['model']} | {row['case_id']} | {row['category']} | {row.get('review_status', 'unscored')}"
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
        st.code(selected["prompt"], language="markdown")
        st.subheader("Expected Answer / Behavior")
        st.write(selected.get("expected_answer", ""))
        st.subheader("Automatic Scoring")
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
    st.subheader("Manual Score")
    existing_scores = selected.get("manual_scores", {})
    with st.form(f"score_form_{selected_key}"):
        score_options = ["", "1", "2", "3", "4", "5"]
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
