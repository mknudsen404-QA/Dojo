# Scoring Gap Note

Date: 2026-07-05

## Current Limitation

The Phase 1 local model comparison reviewed outputs manually, but not all factual or mathematical claims were validated against ground truth.

This means the comparison is useful for early model selection, latency observations, and qualitative behavior notes, but it is not yet an evaluation-grade assurance result.

## Why This Matters

For an internal QA assistant, a response that sounds reasonable is not enough. The evaluation needs to measure whether the answer is correct, supported, safe, and formatted as requested.

Without answer keys and scoring criteria, model comparisons remain partly subjective.

## Required Phase 2 Upgrade

Future evaluation runs should include:

- Ground-truth answer keys
- Explicit scoring criteria
- Exact-match checks for simple factual and mathematical answers
- JSON-validity checks for structured-output prompts
- Refusal-quality checks for unsafe or inappropriate requests
- Hallucination traps where the correct behavior is to say there is not enough information
- Notes on whether answers are complete, concise, and instruction-following

## Assurance Standard

A model should not be described as production-ready based only on plausible-looking responses. It should be evaluated against repeatable test cases with known expected behavior and documented limitations.
