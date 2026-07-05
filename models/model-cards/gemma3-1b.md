# Model Card: gemma3:1b

## Model Name

Gemma 3 1B

## Local Tag

`gemma3:1b`

## Quantization

Ollama-packaged local model. Exact quantization variant was not recorded in Phase 1.

## Approx Size

815 MB

## Hardware Used

Mac Mini M2 with 8 GB memory.

## Strengths

- Completed all Phase 1 baseline prompts.
- Lightweight and easy to run locally.
- Useful for fast smoke tests.

## Weaknesses

- Small model size limits confidence for reasoning-heavy QA.
- Should not be the only model used for assurance conclusions.

## Latency Notes

- Completed prompts: 5/5
- Average time for completed prompts: 2.79s
- Timeouts: 0

## Best Use Case

Fast regression checks and runner smoke tests.

## Risks

- May underperform on nuanced internal QA tasks.
- Fast responses can create false confidence if they are not scored.

## Would I Use This For A QA Assistant?

Not as the main model. Useful as a fast test-cycle model.
