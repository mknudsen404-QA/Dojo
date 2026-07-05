# Local Model Behavior Notes

Date: 2026-07-05

## Summary

The local lab now has five general-purpose local models available through Ollama. For day-to-day experimentation on this Mac Mini M2 with 8 GB memory, the practical working set is `qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b`.

## Observations

`qwen2.5:3b` appears to be the best default for Phase 2. It completed the baseline prompt set quickly and gave reasonably complete answers.

`llama3.2:3b` is a useful comparison baseline. It is slightly slower than Qwen in this run but still responsive.

`gemma3:1b` is useful for fast smoke tests. It should be treated as a quick signal, not as the main model for assurance conclusions.

`llama3.2:1b` is fast and acceptable for basic checks, but weaker instruction following is expected because of its small size.

`mistral:7b` is installed and can run, but it is slow on the current machine. It timed out on 2 of 5 prompts with a 60-second timeout and should not be the default model for routine local evals.

## Operational Notes

- The first attempt used `ollama run` and timed out on `mistral:7b`.
- The runner was changed to use the Ollama HTTP API with a generation cap.
- The bounded run completed and produced reusable JSON results.
- VS Code itself may be installed, but the `code` CLI is not currently configured in PATH.

## Working Model Set For Phase 2

- Primary: `qwen2.5:3b`
- Baseline: `llama3.2:3b`
- Fast smoke test: `gemma3:1b`
- Optional slow comparison: `mistral:7b`
