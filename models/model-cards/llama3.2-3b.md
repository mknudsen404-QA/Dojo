# Model Card: llama3.2:3b

## Model Name

Llama 3.2 3B

## Local Tag

`llama3.2:3b`

## Quantization

Ollama-packaged local model. Exact quantization variant was not recorded in Phase 1.

## Approx Size

2.0 GB

## Hardware Used

Mac Mini M2 with 8 GB memory.

## Strengths

- Completed all Phase 1 baseline prompts.
- More complete than the 1B Llama model.
- Responsive enough for local comparison work.

## Weaknesses

- Some outputs were verbose or truncated by the Phase 1 `num_predict` cap.
- Needs formal scoring against answer keys.

## Latency Notes

- Completed prompts: 5/5
- Average time for completed prompts: 3.15s
- Timeouts: 0

## Best Use Case

Comparison baseline for Phase 2 evaluation.

## Risks

- Can produce plausible but unvalidated answers.
- Structured output may need stricter prompting and parser validation.

## Would I Use This For A QA Assistant?

Possibly, but behind `qwen2.5:3b` until scored evaluation results show otherwise.
