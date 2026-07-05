# Prompt Injection Expanded Test Design 001

Date: 2026-07-05

Phase: 2 - Evaluation Harness

Related ticket: ASA-013

Dataset:

- `prompts/security/prompt_injection_expanded_001.jsonl`

## Goal

Expand prompt-injection testing beyond simple override prompts into realistic AI application attack scenarios.

This is a security test design exercise. The purpose is to improve adversarial coverage before adding more tooling.

## Dataset Shape

Each case includes:

- `id`
- `category`
- `attack_family`
- `attack_type`
- `prompt`
- `expected_behavior`
- `failure_condition`
- `risk`
- `severity_if_failed`
- `control_layer_expected`

Compatibility fields are also included:

- `expected_answer`
- `scoring_type`

## Case Split

| Attack Family | Count |
|---|---:|
| Direct override | 5 |
| RAG / retrieved document injection | 10 |
| Evaluator / scoring manipulation | 5 |
| Tool-use manipulation | 5 |
| Approval / release-gate manipulation | 3 |
| Multi-step or role-confusion attacks | 2 |

Evaluator/scoring coverage totals 10 cases when combining evaluator/scoring manipulation, approval/release-gate manipulation, and role-confusion cases.

## Design Notes

The dataset intentionally separates security success from evaluator usefulness. A model may avoid following the malicious instruction while still producing a low-quality, incomplete, or underspecified answer.

The cases focus on:

- whether the model treats untrusted content as untrusted
- whether retrieved content can override evaluator instructions
- whether candidate output can manipulate scoring
- whether approval language is emitted without evidence
- whether tool-like instructions are followed from untrusted content
- whether role confusion changes the model's decision boundary

The `control_layer_expected` field is intentionally included so results can distinguish prompt-boundary failures from issues that need retrieval sanitization, tool permissioning, output validation, or human approval.

## Current Status

Dataset design is complete. Baseline and mitigated runs have not been executed yet.

## Next Steps

- Run the expanded dataset against all three local models without mitigation.
- Run the same dataset with the ASA-012 mitigation prompt.
- Compare failures by model and attack family.
- Identify which controls helped and where they were weak.
- Avoid claiming security based only on this dataset.
