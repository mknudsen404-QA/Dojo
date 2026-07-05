# Model Comparison 001: Internal QA Assistant Candidate

Date: 2026-07-05

## Question

Which local model looks most promising for an internal QA assistant?

## Short Answer

`qwen2.5:3b` is the best current candidate for an internal QA assistant on this Mac Mini M2 lab setup.

It is not production-ready yet. It is the best next model to evaluate more rigorously because it completed every baseline prompt, had practical latency, and produced comparatively useful responses under the same response-length budget.

## Evidence Used

Artifacts:

- `prompts/baseline/local-ai-lab.jsonl`
- `models/comparisons/phase-1-local-model-results.json`
- `models/comparisons/phase-1-local-ai-lab-report.md`
- `models/comparisons/local-model-behavior-notes.md`

Run settings:

- Ollama local HTTP API
- `temperature`: 0.2
- `num_predict`: 96
- Timeout: 60 seconds per prompt
- 5 prompts per model
- Hardware: Mac Mini M2, 8 GB memory

## Results Summary

| Model | Completed | Avg Time | Timeouts | QA Assistant Readiness |
|---|---:|---:|---:|---|
| `qwen2.5:3b` | 5/5 | 2.68s | 0 | Best candidate |
| `llama3.2:3b` | 5/5 | 3.15s | 0 | Good comparison baseline |
| `gemma3:1b` | 5/5 | 2.79s | 0 | Useful smoke-test model |
| `llama3.2:1b` | 5/5 | 1.94s | 0 | Fast but weaker candidate |
| `mistral:7b` | 3/5 | 24.83s | 2 | Too slow for routine use |

## Model Notes

### Qwen 2.5 3B

Strengths:

- Completed all baseline prompts.
- Latency was practical for local iteration.
- Responses were generally complete and useful.
- Best balance of output quality and runtime from this first pass.

Weaknesses:

- Not yet scored against ground truth.
- Structured output still needs parser validation.
- Needs more tests for hallucination, refusal behavior, and source-grounded answers.

Best use case:

- Primary model for Phase 2 evaluation harness development.

Would I use this for a QA assistant?

- Yes, as the first local candidate to evaluate. Not yet as a production assistant.

### Llama 3.2 3B

Strengths:

- Completed all baseline prompts.
- Still responsive on the Mac Mini.
- Useful as a second model for comparison.

Weaknesses:

- Some answers were verbose or truncated by the token cap.
- Needs the same formal scoring as Qwen.

Best use case:

- Comparison baseline for Phase 2.

Would I use this for a QA assistant?

- Possibly, but behind Qwen until scored results show otherwise.

### Gemma 3 1B

Strengths:

- Completed all prompts.
- Lightweight and easy to run.
- Good for quick smoke tests.

Weaknesses:

- Small model size limits confidence for reasoning-heavy QA.
- Should not be the only model used for assurance conclusions.

Best use case:

- Fast regression and runner checks.

Would I use this for a QA assistant?

- Not as the main model. Useful for fast test cycles.

### Llama 3.2 1B

Strengths:

- Fastest completed model in this run.
- Useful for quick failure checks.

Weaknesses:

- More likely to have weaker instruction following and reasoning due to size.
- Not the strongest candidate for internal QA quality.

Best use case:

- Fast local sanity checks.

Would I use this for a QA assistant?

- No, except as a lightweight baseline.

### Mistral 7B

Strengths:

- Larger model family is useful to keep available for occasional comparison.
- Some completed responses were reasonable.

Weaknesses:

- Timed out on 2 of 5 prompts.
- Average completed-prompt latency was much slower than the smaller models.
- Not practical for short-cycle local evaluation on this hardware.

Best use case:

- Occasional slower comparison, not routine evaluation.

Would I use this for a QA assistant?

- No, not on this machine under current constraints.

## Recommendation

Use this Phase 2 evaluation set:

1. Primary candidate: `qwen2.5:3b`
2. Comparison baseline: `llama3.2:3b`
3. Fast smoke-test model: `gemma3:1b`

Do not use `mistral:7b` for routine short-loop evals on this 8 GB Mac Mini. Keep it installed for occasional comparison only.

## Risks

- The baseline set is too small to support strong model-quality conclusions.
- No answer-key scoring exists yet.
- Hallucination behavior was not meaningfully tested.
- Structured output was manually inspected, not automatically validated.
- Quantization details were inferred from local model size and Ollama packaging, not recorded from a formal model manifest.

## Scoring Gap

Current limitation: outputs were reviewed manually, but not all factual or mathematical claims were validated against ground truth. Future evaluation runs should include answer keys, explicit scoring criteria, and automated checks for exact match, JSON validity, refusal quality, and unsupported claims.

## Decision

`qwen2.5:3b` advances to Phase 2 as the leading local QA-assistant candidate.
