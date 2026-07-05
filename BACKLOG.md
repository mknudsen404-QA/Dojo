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
- [x] Start ASA-012 mitigation validation.
- [x] Add hardened prompt-injection mitigation pattern.
- [x] Rerun all prompt-injection cases across Qwen, Llama, and Gemma with mitigation.
- [x] Generate prompt-injection mitigation validation report.
- [x] Human sanity-check ASA-012 mitigated responses.
- [x] Record ASA-012 outcome: prompt-level mitigation reduced obvious prompt-injection failures from 6/15 to 0/15 in a small controlled rerun.
- [x] Start ASA-013 expanded prompt-injection dataset.
- [x] Design 30-case expanded prompt-injection dataset.
- [x] Document ASA-013 test design.
- [x] Run ASA-013 baseline prompts without mitigation.
- [x] Run ASA-013 prompts with mitigation.
- [x] Generate ASA-013 expanded prompt-injection results report.

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

## ASA-012: Prompt-Injection Mitigation Validation

Goal: Test whether explicit prompt-injection controls reduce the confirmed prompt-injection failures from Phase 2.

Inputs:

- `security/findings/qwen_prompt_injection_findings_001.md`
- `evals/datasets/baseline_eval_set_001.jsonl`
- `evals/results/scored/model_eval_001_scored.jsonl`
- Models: `qwen2.5:3b`, `llama3.2:3b`, `gemma3:1b`
- Cases: `injection_001` through `injection_005`

Acceptance criteria:

- [x] Add hardened system/developer instruction pattern.
- [x] Rerun all 5 prompt-injection cases across all 3 models.
- [x] Compare baseline vs mitigated behavior.
- [x] Record whether previous failures were fixed.
- [x] Identify any new regressions.
- [x] Produce a mitigation validation report.
- [x] Avoid claiming the system is secure based on 5 tests.
- [x] Human reviewer agrees mitigated outputs did not repeat baseline failures.

Outcome: Prompt-level mitigation reduced obvious prompt-injection failures from 6/15 to 0/15 in a small controlled rerun.

Caveat: This is a smoke test, not proof of security.

## ASA-013: Expanded Prompt-Injection Test Set

Goal: Expand the prompt-injection evaluation set beyond the first five smoke tests so mitigation controls are tested against more realistic adversarial scenarios.

Problem: ASA-012 showed that prompt-level mitigation reduced obvious failures in a small test set, but five cases are not enough to support broad security confidence.

Inputs:

- `prompts/security/prompt_injection_expanded_001.jsonl`
- `security/threat-models/prompt_injection_expanded_test_design_001.md`
- `evals/results/prompt_injection_expanded_baseline_001.json`
- `evals/results/prompt_injection_expanded_mitigated_001.json`
- `security/findings/prompt_injection_expanded_results_001.md`
- `evals/datasets/baseline_eval_set_001.jsonl`
- `prompts/security/prompt_injection_mitigation_001.md`
- `security/findings/prompt_injection_mitigation_validation_001.md`
- local models from Phase 2

Prompt categories to add:

- direct override attempts
- retrieved-document instruction injection
- evaluator/rubric manipulation
- approval-language manipulation
- tool-use instruction abuse
- data-exfiltration attempts
- role confusion
- conflicting instruction hierarchy
- hidden instruction inside formatted content
- multi-step or indirect prompt injection

Acceptance criteria:

- [x] Add at least 30 new prompt-injection cases.
- [x] Include at least 10 RAG-style cases.
- [x] Include at least 10 evaluator/scoring manipulation cases.
- [x] Include at least 5 tool-use manipulation cases.
- [x] Include expected safe behavior for each case.
- [x] Include risk metadata for each case.
- [x] Include expected control layer for each case.
- [x] Mark cases that require manual scoring.
- [x] Run baseline prompts without mitigation.
- [x] Run the same prompts with mitigation.
- [x] Compare baseline vs mitigated behavior.
- [x] Report failures by model and category.
- [x] Identify which controls helped and which failed.
- [x] Document remaining failures and limitations.
- [x] Avoid claiming system security from prompt-level controls alone.

Outcome: ASA-012 mitigation reduced obvious heuristic failures from 24/90 to 1/90 on the expanded ASA-013 dataset.

Caveat: Results are heuristic and require human review before final security scoring.
