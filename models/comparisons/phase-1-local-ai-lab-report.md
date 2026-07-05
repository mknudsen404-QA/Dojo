# Phase 1 Local AI Lab Report

Date: 2026-07-05

## Goal

Run local LLMs and understand basic model behavior before adding security, RAG, or fine-tuning.

## Local Environment

- Machine: Mac Mini M2
- Memory: 8 GB
- macOS: 26.5
- Ollama: 0.31.1
- Python: 3.14.6
- Git: 2.50.1
- VS Code CLI: `code` command not currently on PATH

## Models Installed

| Model | Family | Size | Phase 1 Use |
|---|---:|---:|---|
| `llama3.2:1b` | Llama | 1.3 GB | Fast baseline |
| `llama3.2:3b` | Llama | 2.0 GB | Stronger local baseline |
| `qwen2.5:3b` | Qwen | 1.9 GB | Recommended default for next evals |
| `mistral:7b` | Mistral | 4.4 GB | Installed, but slow on this machine |
| `gemma3:1b` | Gemma | 815 MB | Lightweight smoke-test model |

Additional local model present but not included in this baseline:

- `ravelin-demo-modelfile:latest`

## Test Method

Prompt set:

- `prompts/baseline/local-ai-lab.jsonl`

Runner:

- `tools/eval-runner/run_ollama_baseline.py`

Raw results:

- `models/comparisons/phase-1-local-model-results.json`

Run settings:

- Local Ollama HTTP API
- `temperature`: 0.2
- `num_predict`: 96
- Timeout: 60 seconds per prompt
- 5 prompts per model

Prompt categories:

- Baseline production-readiness explanation
- Reliability and uncertainty behavior
- Simple arithmetic reasoning
- Safety boundary behavior
- Structured JSON-style output

## Timing Results

| Model | Completed | Average Time For Completed Prompts | Timeouts |
|---|---:|---:|---:|
| `llama3.2:1b` | 5/5 | 1.94s | 0 |
| `llama3.2:3b` | 5/5 | 3.15s | 0 |
| `qwen2.5:3b` | 5/5 | 2.68s | 0 |
| `mistral:7b` | 3/5 | 24.83s | 2 |
| `gemma3:1b` | 5/5 | 2.79s | 0 |

## Behavior Notes

### Llama 3.2 1B

Very fast and usable for smoke tests. It answered the arithmetic prompt correctly and generally followed instructions, but it sometimes added wrapper text around structured output instead of returning only JSON.

### Llama 3.2 3B

Reliable enough for a local baseline and still responsive. It produced more complete explanations than the 1B model, though responses were still sometimes verbose or truncated by the `num_predict` cap.

### Qwen 2.5 3B

Best practical default from this first pass. It completed all prompts, stayed responsive, and generally gave structured, thoughtful answers. It should be the first model used for Phase 2 prompt-evaluation work.

### Mistral 7B

Installed and runnable, but too slow for short-cycle local evaluation on this 8 GB Mac Mini M2 configuration. It completed some prompts, but timed out on the simple reasoning and safety-boundary prompts at 60 seconds. Treat it as an occasional comparison model, not the default lab model.

### Gemma 3 1B

Fast, lightweight, and useful for quick checks. It answered the arithmetic prompt correctly and completed all prompts. It is a good smoke-test model, but should not be the only model used for quality or assurance conclusions.

## Initial Recommendation

Use this model order for the next phase:

1. `qwen2.5:3b` as the primary local evaluation model.
2. `llama3.2:3b` as the comparison baseline.
3. `gemma3:1b` for quick smoke tests.
4. `llama3.2:1b` for fast failure checks.
5. `mistral:7b` only when slower, larger-model comparison is specifically useful.

## Limitations

- This was a single run, not a statistically meaningful benchmark.
- No human scoring rubric was applied yet.
- Outputs were capped at 96 generated tokens.
- Hardware metrics such as memory pressure, CPU/GPU utilization, and tokens per second were not captured.
- The custom `ravelin-demo-modelfile:latest` model was not evaluated.
- Structured-output compliance was inspected manually, not validated with a JSON parser.

## Next Steps

- Add a scoring rubric for instruction following, correctness, refusal quality, and structured output validity.
- Capture tokens-per-second and memory notes during runs.
- Add a JSON-validity check for structured-output prompts.
- Decide whether to keep `mistral:7b` in routine comparisons or reserve it for slower ad hoc tests.
- Move Phase 2 into repeatable prompt evaluation using `qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b`.
