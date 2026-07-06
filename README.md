# Matthew AI Security & Assurance Training

This repository is a practical training system for AI engineering, AI security, and AI assurance.

The purpose is not to learn AI in the abstract. The purpose is to build the capability to answer a production-readiness question with evidence:

> Is this AI system safe, reliable, measurable, and ready for production?

## Operating Rhythm

Recommended pace:

- 5-8 hours per week
- 1 primary phase at a time
- 1 weekly review
- 1 written artifact per week
- 1 demo or report at the end of each phase

Each week follows the same loop:

1. Learn the concept.
2. Build or test something.
3. Break it.
4. Measure it.
5. Document what happened.
6. Write what you would do differently.
7. Commit the artifact.

## Definition of Done

A phase is complete only when it has:

- Working code or reproducible steps
- Written notes
- Measured results
- A report or portfolio artifact
- Known limitations
- Next-step recommendations
- A commit in source control

## Repository Map

```text
setup/       Local setup notes for Mac, Python, Ollama, and tooling
prompts/     Prompt collections for baseline, security, RAG, and hallucination testing
evals/       Datasets, evaluation runners, scoring logic, and results
models/      Model cards and model comparison notes
security/    Attack logs, threat models, and security findings
rag/         RAG datasets, pipelines, and evaluation artifacts
lora/        LoRA datasets, training runs, and evaluations
assurance/   Test plans, readiness reviews, and executive reports
tools/       Local utilities for evals, red teaming, and report generation
capstone/    Final client-style assurance package
```

## Current Phase

Phase 2: Evaluation Harness.

The focus is to build a repeatable evaluation runner that compares local models using structured prompt sets and produces saved results.

## Phase 0 Acceptance Criteria

- [x] Repository created
- [x] Folder structure created
- [x] `README.md` created
- [x] `ROADMAP.md` created
- [x] `learning-log.md` created
- [x] First 10 backlog items created
- [ ] Initial setup verified on local machine
- [x] Phase 0 commit completed

## Phase 1 Outputs

- [x] Local models running in Ollama
- [x] 3 additional model families installed: Qwen, Mistral, Gemma
- [x] Basic prompt set created
- [x] Baseline runner created
- [x] Raw model comparison results captured
- [x] Model behavior notes written
- [x] First local model comparison report written
- [x] Internal QA assistant model comparison written
- [x] Scoring gap documented

## Phase 2 Outputs

- [x] Baseline evaluation dataset created
- [x] Evaluation runner created
- [x] Manual scoring rubric created
- [x] Markdown report generator created
- [x] Full 50-prompt, 3-model evaluation run completed
- [x] Manual Scoring UI 001 created
- [x] First-pass manual scoring completed for `qwen2.5:3b`
- [x] Prompt-injection scoring completed for `llama3.2:3b` and `gemma3:1b`
- [x] Initial `evals/results/model_eval_report_001.md` generated
- [x] Initial scored report generated
- [x] Scored-run manifest created
- [x] First security finding recorded

## Scoring

Run the local scoring UI:

```bash
streamlit run tools/manual-scorer/app.py
```

The raw evaluation result remains unchanged. Scored progress is written to:

```text
evals/results/scored/model_eval_001_scored.jsonl
```

Current scoring operating model:

1. Use heuristics for obvious cases.
2. Use an AI judge for rubric cases.
3. Use human review for targeted calibration and audit.
4. Limit routine human review to 10-20 targeted rows per major run.

See:

```text
evals/scoring/scoring-operating-model.md
```

## How to Work in This Repo

Start each week by choosing one backlog item or roadmap objective. End each week by committing an artifact that another person could inspect and reproduce.

Useful artifact types include:

- Experiment note
- Prompt set
- Evaluation dataset
- Evaluation result
- Attack log
- Finding writeup
- Model card
- Readiness review
- Executive summary

## Portfolio Intent

The final portfolio should show practical judgment, not just tool familiarity. Each phase should make it easier to explain what was tested, what failed, how it was measured, and what would need to happen before production use.
