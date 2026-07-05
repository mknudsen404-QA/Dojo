# Model Card: qwen2.5:3b

## Model Name

Qwen 2.5 3B

## Local Tag

`qwen2.5:3b`

## Quantization

Ollama-packaged local model. Exact quantization variant was not recorded in Phase 1.

## Approx Size

1.9 GB

## Hardware Used

Mac Mini M2 with 8 GB memory.

## Strengths

- Completed all Phase 1 baseline prompts.
- Practical local latency.
- Produced useful, comparatively complete responses.
- Best balance of quality and speed in the first comparison.

## Weaknesses

- Not yet scored against ground-truth answer keys.
- Structured-output compliance has not been parser-validated.
- Hallucination behavior has not been tested rigorously.

## Latency Notes

- Completed prompts: 5/5
- Average time for completed prompts: 2.68s
- Timeouts: 0

## Best Use Case

Primary local model for Phase 2 prompt evaluation and internal QA-assistant testing.

## Risks

- Plausible answers may still be wrong without source grounding or answer-key validation.
- Quantization details need to be captured more explicitly for reproducibility.

## Would I Use This For A QA Assistant?

Yes, as the first local candidate to evaluate. Not yet as a production assistant.
