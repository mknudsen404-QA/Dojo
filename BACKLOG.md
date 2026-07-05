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
- [ ] Manually score the first 50 outputs.
- [ ] Finalize `evals/results/model_eval_report_001.md` after manual scoring.
