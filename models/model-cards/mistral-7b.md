# Model Card: mistral:7b

## Model Name

Mistral 7B

## Local Tag

`mistral:7b`

## Quantization

Ollama-packaged local model. Exact quantization variant was not recorded in Phase 1.

## Approx Size

4.4 GB

## Hardware Used

Mac Mini M2 with 8 GB memory.

## Strengths

- Larger model family is useful to keep available for comparison.
- Some completed responses were reasonable.

## Weaknesses

- Too slow for routine short-loop evaluation on this machine.
- Timed out on 2 of 5 Phase 1 baseline prompts.

## Latency Notes

- Completed prompts: 3/5
- Average time for completed prompts: 24.83s
- Timeouts: 2

## Best Use Case

Occasional slower comparison when larger-model behavior is specifically useful.

## Risks

- High latency can interrupt evaluation workflow.
- Longer timeouts may make comparisons less practical and less consistent.
- May require more memory or different quantization to be useful locally.

## Would I Use This For A QA Assistant?

No, not on this machine under current constraints.
