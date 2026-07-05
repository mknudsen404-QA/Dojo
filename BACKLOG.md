# Backlog

## Phase 0

- [ ] Verify Git user name and email are configured locally.
- [ ] Create the GitHub repository and add it as `origin`.
- [ ] Confirm the folder structure matches the roadmap.
- [ ] Review README for clarity and revise after one read-through.
- [ ] Add existing Obsidian notes that are relevant to Phase 0.
- [ ] Add a weekly review template.
- [ ] Add a basic experiment note template.
- [ ] Add a security finding template.
- [ ] Add an evaluation report template.
- [ ] Create the first GitHub issues from this backlog.

## Phase 1 Candidates

- [x] Install and verify Ollama.
- [x] Install at least three additional local model families.
- [x] Run a baseline prompt set against local models.
- [x] Record model latency and basic behavior.
- [x] Create initial model cards.
- [x] Enrich model cards with quantization, latency, risks, and QA-assistant suitability.
- [x] Compare local models on the same prompt set.
- [x] Mark Lab 1.1 complete.
- [x] Mark Lab 1.2 response-length experiment partially complete.
- [x] Finalize `model_comparison_001.md` for internal QA assistant model selection.
- [x] Add scoring gap note.
- [ ] Add formal scoring rubric for Phase 2.
- [ ] Add JSON-validity scoring for structured-output prompts.
- [ ] Capture memory and tokens-per-second metrics.
- [ ] Decide whether `mistral:7b` stays in routine evals.

## Phase 2 Candidates

- [x] Add 50-case baseline dataset with expected answers and scoring types.
- [x] Build exact-match scoring.
- [x] Build JSON-schema scoring.
- [x] Add manual scoring rubric for hallucination, refusal, and subjective tests.
- [x] Build repeatable evaluation runner.
- [x] Build markdown report generator.
- [x] Run the Phase 2 baseline dataset against `qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b`.
- [x] Generate initial `evals/results/model_eval_report_001.md`.
- [x] Create ASA-011 ticket for manual scoring UI.
- [x] Build Manual Scoring UI 001.
- [x] Manually score the first 50 `qwen2.5:3b` outputs.
- [x] Clean up Qwen scored-result data-quality issues.
- [x] Generate `evals/results/model_eval_report_001_scored.md`.
- [x] Add scored-run manifest so reports preserve execution context.
- [x] Add interim decision and prompt-injection comparison table to scored report.
- [x] Create Qwen prompt-injection findings.
- [x] Score prompt-injection cases for `llama3.2:3b` and `gemma3:1b`.
- [x] Compare prompt-injection resistance across Qwen, Llama, and Gemma.
- [x] Update `evals/results/model_eval_report_001_scored.md` after injection comparison.
- [ ] Start ASA-012 mitigation validation.

## ASA-011: Build Manual Scoring UI

Goal: Create a lightweight local UI that makes manual scoring of LLM evaluation results faster, more consistent, and less error-prone.

Problem: The evaluation runner produces structured result files, but rubric-based categories still require human review. Manually editing JSON or markdown is slow and increases the risk of inconsistent scoring.

Inputs:

- `evals/results/*.json`
- `evals/results/*.jsonl`
- `evals/scoring/manual-scoring-rubric.md`
- model responses
- expected answers
- automatic scoring results

Outputs:

- scored results file
- updated manual scoring fields
- scoring progress summary
- model/category score summaries

MVP features:

- [x] Load an evaluation result file.
- [x] Filter by model.
- [x] Filter by category.
- [x] Filter by unscored results.
- [x] Filter by automatic pass/fail.
- [x] View the original prompt.
- [x] View the expected answer, if present.
- [x] View the model response.
- [x] View automatic scoring result.
- [x] Enter manual scores.
- [x] Add notes.
- [x] Mark a result as scored, needs review, answer key issue, or scorer unsure.
- [x] Save progress without overwriting raw results.
- [x] Export scored results to a new file.

Data safety rule:

- [x] Raw evaluation results must remain immutable.
- [x] The scorer writes to `evals/results/scored/model_eval_001_scored.jsonl`.

Recommended scoring order:

1. Score all 50 `qwen2.5:3b` outputs.
2. Score manual-only categories across all models.
3. Review automatic failures manually.

Definition of done:

- [x] Manually score the first 50 `qwen2.5:3b` results using the UI and export a scored result file without touching the raw evaluation output.

## ASA-012: Add Prompt-Injection Mitigation Prompt And Rerun Failed Cases

Goal: Test whether explicit prompt-injection controls reduce the two confirmed Qwen prompt-injection failures.

Inputs:

- `security/findings/qwen_prompt_injection_findings_001.md`
- `evals/datasets/baseline_eval_set_001.jsonl`
- `evals/results/scored/model_eval_001_scored.jsonl`
- Failed cases: `injection_001`, `injection_005`

Acceptance criteria:

- [ ] Add hardened system/developer instruction pattern.
- [ ] Rerun `injection_001` and `injection_005`.
- [ ] Compare baseline vs mitigated behavior.
- [ ] Document whether mitigation reduced risk.
- [ ] Update the finding with mitigation validation results.
