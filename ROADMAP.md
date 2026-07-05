# Roadmap

This roadmap organizes the training plan into phases. Work one phase at a time, and treat each phase as complete only when its artifact is written, measured, and committed.

## Phase 0: Training System Setup

Goal: Create the repo, operating rhythm, folder structure, and learning log.

Outputs:

- GitHub-ready repository
- `README.md`
- `ROADMAP.md`
- `learning-log.md`
- Folder structure
- First backlog

Portfolio artifact:

- README and roadmap

Status:

- Automated run complete; manual scoring pending

## Phase 1: Local AI Lab

Goal: Run local LLMs and understand basic model behavior before adding security, RAG, or fine-tuning.

Example work:

- Install and verify Ollama or another local runtime
- Run baseline prompts against at least three models
- Capture latency, quality, failure modes, and resource notes
- Write a model comparison

Portfolio artifact:

- Local model comparison report

Outputs:

- Local models running
- Model behavior notes
- Basic prompt set
- First model comparison report

Status:

- Lab 1.1 complete; Lab 1.2 partially complete; ready for Phase 2 scoring work

## Phase 2: Prompt Evaluation Basics

Goal: Build a repeatable evaluation runner that compares models using structured prompt sets and produces saved results.

Example work:

- Build a baseline evaluation dataset
- Create an eval runner
- Define scoring criteria
- Compare baseline prompts against revised prompts
- Write measured results

Portfolio artifact:

- `evals/results/model_eval_report_001.md`

Outputs:

- `eval-runner`
- Baseline evaluation dataset
- Result files
- Markdown report generator

Status:

- In progress

## Phase 3: AI Security Foundations

Goal: Test common adversarial behaviors and document security findings.

Example work:

- Build a red-team prompt set
- Test prompt injection, jailbreak attempts, data exfiltration patterns, and policy bypass attempts
- Record attack logs
- Classify findings by severity and reproducibility
- Recommend mitigations

Portfolio artifact:

- AI security findings report

## Phase 4: RAG System Evaluation

Goal: Build and evaluate a small retrieval-augmented generation pipeline.

Example work:

- Create or collect a small document dataset
- Build a retrieval pipeline
- Measure retrieval quality and answer faithfulness
- Test hallucination and source-grounding failure modes
- Document limitations

Portfolio artifact:

- RAG evaluation report

## Phase 5: Hallucination and Reliability Testing

Goal: Measure reliability under ambiguity, missing context, and adversarial phrasing.

Example work:

- Create hallucination test cases
- Evaluate abstention behavior
- Measure unsupported claims
- Compare model and prompt variants
- Recommend reliability controls

Portfolio artifact:

- Hallucination and reliability assessment

## Phase 6: Fine-Tuning or LoRA Experiment

Goal: Understand the lifecycle, risks, and measurable outcomes of a small adaptation run.

Example work:

- Prepare a small dataset
- Run or simulate a LoRA training workflow
- Evaluate pre/post behavior
- Document overfitting, data quality, and safety risks

Portfolio artifact:

- LoRA experiment report

## Phase 7: Assurance and Production Readiness

Goal: Convert technical testing into an assurance package suitable for engineering and leadership review.

Example work:

- Create an AI test plan
- Write a readiness review
- Summarize known risks
- Define launch gates and monitoring recommendations
- Produce an executive report

Portfolio artifact:

- Production readiness review

## Phase 8: Capstone

Goal: Produce a client-style assessment of an AI system.

Deliverables:

- `client-brief.md`
- `architecture-review.md`
- `security-assessment.md`
- `evaluation-report.md`
- `final-recommendation.md`

Portfolio artifact:

- Complete AI assurance package
