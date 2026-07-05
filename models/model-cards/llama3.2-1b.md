# Model Card: llama3.2:1b

## Model Name

Llama 3.2 1B

## Local Tag

`llama3.2:1b`

## Quantization

Ollama-packaged local model. Exact quantization variant was not recorded in Phase 1.

## Approx Size

1.3 GB

## Hardware Used

Mac Mini M2 with 8 GB memory.

## Strengths

- Fastest model in the Phase 1 comparison.
- Completed all baseline prompts.
- Useful for quick failure checks.

## Weaknesses

- Small model size likely limits reasoning quality.
- Not the strongest candidate for an internal QA assistant.
- Structured-output reliability still needs validation.

## Latency Notes

- Completed prompts: 5/5
- Average time for completed prompts: 1.94s
- Timeouts: 0

## Best Use Case

Very fast local sanity checks.

## Risks

- May provide shallow or overconfident answers.
- Should not be treated as representative of stronger local models.

## Would I Use This For A QA Assistant?

No, except as a lightweight baseline or smoke-test model.
