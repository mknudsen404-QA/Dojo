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
- [x] Create ASA-014 human-review queue for expanded prompt-injection results.
- [x] Adopt scoring operating model: heuristics plus AI judge plus targeted human audit.
- [x] Close Phase 2 / Phase 2.5 as complete enough to proceed.

## Phase 3 Candidates

- [x] Start ASA-015 AI security severity rubric.
- [x] Create Phase 3 finding severity rubric.
- [x] Start ASA-016 system prompt leakage simulation.
- [x] Start ASA-017 insecure output handling tests.
- [x] Create Phase 3 attack log structure.
- [x] Build small red-team runner or adapt existing eval runner for security labs.
- [x] Create 50-case Phase 3 attack prompt library.
- [x] Run Phase 3 attack library against three local models.
- [x] Generate `security/findings/llm_security_assessment_001.md`.
- [ ] Human-review critical/high Phase 3 heuristic finding candidates.
- [ ] Create focused finding report for confirmed system-prompt leakage failures.
- [ ] Create mitigation rerun for system-prompt leakage controls.

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

## ASA-014: Human Review Expanded Injection Results

Goal: Validate whether ASA-013 heuristic scoring is directionally accurate and identify false positives and false negatives.

Retrospective note: ASA-014 completed the calibration job, but its manual-heavy workflow is not the model going forward. Manual review should be used for calibration and audit, not bulk scoring.

Inputs:

- `evals/results/prompt_injection_expanded_baseline_001.json`
- `evals/results/prompt_injection_expanded_mitigated_001.json`
- `security/findings/prompt_injection_expanded_results_001.md`
- `security/attack-logs/asa_014_human_review_queue_001.jsonl`
- `security/attack-logs/asa_014_human_review_queue_001_scored.jsonl`
- `security/findings/asa_014_human_review_summary_001.md`
- `assurance/test-plans/asa_014_human_review_expanded_injection.md`

Acceptance criteria:

- [x] Review all mitigated failures.
- [x] Review all baseline heuristic failures.
- [x] Review at least 10 baseline heuristic passes from high-risk control layers.
- [x] Identify false positives.
- [x] Identify false negatives.
- [x] Update the expanded results report with a human-review note.
- [x] Record whether the `24/90 -> 1/90` result still holds directionally after review.

Outcome: The mitigation result still holds directionally, but ASA-014 found 17 false negatives. Baseline risk was higher than the ASA-013 heuristic reported.

Superseding operating model:

- `evals/scoring/scoring-operating-model.md`

## ASA-014-FU: AI-Assisted Scoring Calibration

Goal: Replace bulk manual scoring with AI-assisted scoring plus targeted human audit.

Approach:

Use deterministic heuristics and an AI judge to score expanded prompt-injection results. Human review is used only for calibration, critical failures, suspicious passes, and disagreement cases.

Inputs:

- `evals/scoring/scoring-operating-model.md`
- `prompts/security/prompt_injection_expanded_001.jsonl`
- `evals/results/prompt_injection_expanded_baseline_001.json`
- `evals/results/prompt_injection_expanded_mitigated_001.json`
- `security/findings/asa_014_human_review_summary_001.md`

Acceptance criteria:

- [ ] AI judge scores all ASA-013 baseline and mitigated results.
- [ ] AI judge returns structured scoring JSON.
- [ ] Heuristic failures are compared against AI-judge failures.
- [ ] Human reviews all remaining mitigated failures.
- [ ] Human reviews at least 10 high-risk heuristic passes.
- [ ] Human reviews at least 10 AI-judge/heuristic disagreements.
- [ ] False positives and false negatives are documented.
- [ ] Report states that AI-assisted scoring is not ground truth.
- [ ] Final conclusion is based on combined heuristic, AI-judge, and targeted human review.
- [ ] Routine human review is limited to 10-20 targeted rows unless calibration requires more.

## ASA-015: AI Security Severity Rubric

Goal: Create the reusable severity rubric for AI security findings.

Severity levels:

- Critical
- High
- Medium
- Low
- Informational

Acceptance criteria:

- [x] Define each severity level.
- [x] Include impact and likelihood guidance.
- [x] Include examples specific to AI systems.
- [x] Include escalation guidance.
- [x] Include recommended report language.
- [x] Store rubric in `security/findings/severity_rubric.md`.

## ASA-016: System Prompt Leakage Simulation

Goal: Test whether local models reveal, summarize, or transform a fake system prompt when pressured.

Acceptance criteria:

- [x] Create fake system prompt leakage test cases.
- [x] Run against at least three local models.
- [x] Record baseline results.
- [x] Identify leakage, refusal, and partial leakage behavior.
- [x] Produce a short finding or lab report.
- [x] Avoid using real secrets or real system prompts.

Outcome: Included in `prompts/security/phase3_attack_prompts_001.jsonl`, `security/attack-logs/phase3_attack_results_001.json`, and `security/findings/llm_security_assessment_001.md`.

Caveat: Heuristic failures require targeted human review before final finding severity is confirmed.

## ASA-017: Insecure Output Handling

Goal: Test whether models produce dangerous downstream output such as unsafe SQL, shell commands, HTML/script content, or destructive automation steps.

Acceptance criteria:

- [x] Create insecure-output test cases.
- [x] Include SQL, shell, HTML/script, and automation examples.
- [x] Run against at least three local models.
- [x] Classify outputs by severity using the ASA-015 rubric.
- [x] Produce a short findings report.

Outcome: Included in `prompts/security/phase3_attack_prompts_001.jsonl`, `security/attack-logs/phase3_attack_results_001.json`, and `security/findings/llm_security_assessment_001.md`.

Caveat: Heuristic failures require targeted human review before final finding severity is confirmed.
