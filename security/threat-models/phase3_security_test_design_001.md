# Phase 3 Security Test Design 001

Date: 2026-07-05

## Purpose

Create a safe local test set for major LLM security failure classes.

This test design supports Phase 3: AI Security Foundations.

## Scope

The tests use local models, synthetic prompts, fake system prompts, and fake tokens only. They do not use real secrets, real system prompts, real customer data, live tools, or production systems.

## Attack Classes

The Phase 3 attack library covers:

- direct prompt injection
- system prompt leakage simulation
- jailbreak-style policy bypass pressure
- insecure output handling
- sensitive information disclosure
- excessive agency

## Dataset

Prompt library:

```text
prompts/security/phase3_attack_prompts_001.jsonl
```

Each case includes:

- `id`
- `lab`
- `category`
- `attack_family`
- `attack_type`
- `prompt`
- `expected_behavior`
- `failure_condition`
- `risk`
- `severity_if_failed`
- `owasp_llm`
- `mitre_atlas`
- `recommended_control`
- `mitigation_notes`

System prompt leakage cases may also include a fake `system_prompt` field. These prompts use fake honeytokens only.

## Evaluation Method

Run the local red-team runner:

```bash
python3 tools/red-team-runner/red_team_runner.py \
  --dataset prompts/security/phase3_attack_prompts_001.jsonl \
  --output security/attack-logs/phase3_attack_results_001.json \
  --models qwen2.5:3b llama3.2:3b gemma3:1b \
  --num-predict 96 \
  --temperature 0.2
```

Generate the report:

```bash
python3 tools/report-generator/generate_llm_security_assessment.py \
  --results security/attack-logs/phase3_attack_results_001.json \
  --output security/findings/llm_security_assessment_001.md
```

## Scoring Approach

The first pass uses deterministic pattern heuristics to flag obvious failures. This is triage only.

Final findings require targeted human review, especially for:

- critical or high heuristic failures
- suspicious heuristic passes
- system-prompt leakage cases
- unsafe output handling cases
- excessive agency cases

## Severity

Use:

```text
security/findings/severity_rubric.md
```

Severity reflects system risk, not just response quality.

## References

- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- OWASP 2025 LLM risks archive: https://genai.owasp.org/llm-top-10/
- MITRE ATLAS SAFE-AI report: https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf
