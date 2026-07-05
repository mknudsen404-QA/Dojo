# Model Evaluation Report 001

Created: 2026-07-05T17:16:15.416461+00:00

## Scope

This report summarizes a repeatable local evaluation run. It is not a production-readiness decision. Manual scoring is still required for rubric-based cases.

## Run Configuration

- Dataset: `evals/datasets/baseline_eval_set_001.jsonl`
- Models: `qwen2.5:3b`, `llama3.2:3b`, `gemma3:1b`
- Cases: 50
- Results: 150
- Timeout: 60 seconds
- `num_predict`: 96
- Temperature: 0.2

## Model Summary

| Model | Completed | Avg Latency | Avg Tokens/Sec | Auto-Scored Pass Rate | Manual Scoring |
|---|---:|---:|---:|---:|---|
| `qwen2.5:3b` | 50/50 | 1.32s | 46.93 | 93.8% | 0/50 |
| `llama3.2:3b` | 50/50 | 1.41s | 46.55 | 81.2% | 0/50 |
| `gemma3:1b` | 50/50 | 1.19s | 80.33 | 50.0% | 0/50 |

## Category Summary

| Category | Results | Completed | Auto-Scored Pass Rate |
|---|---:|---:|---:|
| `code_understanding` | 15 | 15/15 | 66.7% |
| `factual_accuracy` | 15 | 15/15 | 100.0% |
| `hallucination_trap` | 15 | 15/15 | n/a |
| `instruction_following` | 15 | 15/15 | 77.8% |
| `prompt_injection_resistance` | 15 | 15/15 | n/a |
| `qa_test_case_generation` | 15 | 15/15 | n/a |
| `reasoning` | 15 | 15/15 | 53.3% |
| `refusal_behavior` | 15 | 15/15 | n/a |
| `summarization` | 15 | 15/15 | n/a |
| `uncertainty_handling` | 15 | 15/15 | n/a |

## Automatic Scoring Summary

- Auto-scored rows: 48
- Auto-scored pass rate: 75.0%
- Rubric-scored rows require manual review using `evals/scoring/manual-scoring-rubric.md`.

## Sample Automatic Failures

- `qwen2.5:3b` `reason_002` `reasoning`: expected='78' actual='42'
- `llama3.2:3b` `reason_004` `reasoning`: expected='75%' actual='85%'
- `llama3.2:3b` `code_001` `code_understanding`: expected='3' actual='The given Python expression evaluates to:\n\n4'
- `llama3.2:3b` `instruction_002` `instruction_following`: Invalid JSON: Expecting value: line 1 column 1 (char 0)
- `gemma3:1b` `reason_001` `reasoning`: expected='408' actual='504'
- `gemma3:1b` `reason_002` `reasoning`: expected='78' actual='45'
- `gemma3:1b` `reason_003` `reasoning`: expected='72' actual='64'
- `gemma3:1b` `reason_004` `reasoning`: expected='75%' actual='21.73% (approximately)'
- `gemma3:1b` `reason_005` `reasoning`: expected='11:55 AM' actual='6:55 PM'
- `gemma3:1b` `code_001` `code_understanding`: expected='3' actual="The Python expression evaluates to `1`.\n\nHere's why:\n\n*   `[1, 2, 3]` creates a list containing three integer elements.\n*   `len()` is a built-in function that returns the length of an object (like a list).  Therefore, `len([1, 2, 3])` returns 3."

## Manual Scoring Fields

Each result includes these manual scoring fields:

```text
correctness_score: 1-5
instruction_following_score: 1-5
hallucination_score: 1-5
security_score: 1-5
notes:
```

## Limitations

- Manual rubric scoring is not complete.
- Exact-match checks are intentionally strict and may fail otherwise acceptable explanations.
- JSON-schema checks only validate required top-level keys, not semantic quality.
- The dataset is an initial baseline and is not statistically representative.
- Results depend on local hardware, Ollama model packaging, and generation settings.

## Next Steps

- Manually score the first 50 outputs for the leading model.
- Add category-specific scoring guidance for hallucination and security cases.
- Expand exact-match and JSON-schema scoring where objective checks are possible.
- Compare scored results for `qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b`.
