# Manual Scoring UI 001

This local Streamlit app supports Phase 2 manual scoring.

## Goal

Make manual scoring of LLM evaluation results faster, more consistent, and less error-prone.

## Data Safety Rule

Raw evaluation results are read-only. The app writes scored progress to a separate JSONL file:

```text
evals/results/scored/model_eval_001_scored.jsonl
```

Do not overwrite:

```text
evals/results/model_eval_results_001.json
```

## Install

From the repository root:

```bash
python3 -m pip install -r tools/manual-scorer/requirements.txt
```

## Run

```bash
streamlit run tools/manual-scorer/app.py
```

## Recommended Scoring Order

1. Score all 50 `qwen2.5:3b` outputs.
2. Score manual-only categories across all models:
   - hallucination traps
   - prompt injection resistance
   - refusal behavior
   - uncertainty handling
   - QA test case generation
   - summarization
3. Review automatic failures manually.

## Manual Fields

```text
correctness_score: 1-5
instruction_following_score: 1-5
hallucination_score: 1-5
security_score: 1-5
notes:
```

## Review Status Values

```text
unscored
scored
needs_review
answer_key_issue
scorer_unsure
```

## Important Rule

Do not use an LLM as the final scorer yet. This phase is for building a trusted human baseline.
