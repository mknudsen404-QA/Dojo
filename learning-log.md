# Learning Log

Use this file as the engineering notebook for the program. Keep entries short, factual, and evidence-based.

## Entry Template

```markdown
## YYYY-MM-DD: Topic

Phase:

Time spent:

What I learned:

What I built or tested:

What I broke:

How I measured it:

Results:

Limitations:

What I would do differently:

Artifacts committed:

Next step:
```

## 2026-07-05: Phase 0 Kickoff

Phase: 0 - Training System Setup

Time spent: Initial scaffold

What I learned:

- A useful AI assurance training system needs artifacts, measurements, and version control, not just notes.
- Each phase should end with evidence another person can inspect.

What I built or tested:

- Created the initial repository structure.
- Created the README, roadmap, learning log, and backlog.

What I broke:

- Nothing yet.

How I measured it:

- Verified the planned folders and files exist locally.

Results:

- Phase 0 scaffold is ready for local setup verification and GitHub remote setup.

Limitations:

- No model runtime, eval runner, or red-team tooling has been implemented yet.
- GitHub remote is not configured yet.

What I would do differently:

- Add weekly review entries immediately after each work session to avoid reconstructing decisions later.

Artifacts committed:

- Initial repository scaffold.

Next step:

- Verify local setup and connect the repository to GitHub.

## 2026-07-05: Phase 1 Local AI Lab

Phase: 1 - Local AI Lab

Time spent: Local model installation and baseline comparison

What I learned:

- The Mac Mini M2 with 8 GB memory can run several small local models comfortably.
- `mistral:7b` is installed and runnable, but it is slow enough to disrupt short evaluation loops.
- A bounded runner is better than open-ended `ollama run` calls for repeatable local testing.

What I built or tested:

- Installed `qwen2.5:3b`, `mistral:7b`, and `gemma3:1b`.
- Created a five-prompt baseline set.
- Created a repeatable Ollama baseline runner.
- Ran five models across the prompt set.

What I broke:

- The first runner version used `ollama run` and timed out on `mistral:7b`.

How I measured it:

- Captured per-prompt completion status and elapsed seconds.
- Compared 5 prompts across 5 models with a 60-second timeout and capped generation length.

Results:

- `llama3.2:1b`: 5/5 prompts completed, 1.94s average.
- `llama3.2:3b`: 5/5 prompts completed, 3.15s average.
- `qwen2.5:3b`: 5/5 prompts completed, 2.68s average.
- `mistral:7b`: 3/5 prompts completed, 24.83s average for completed prompts, 2 timeouts.
- `gemma3:1b`: 5/5 prompts completed, 2.79s average.

Limitations:

- This was a single baseline run.
- No formal scoring rubric was applied.
- Outputs were capped at 96 generated tokens.
- Hardware utilization was not captured.

What I would do differently:

- Add scoring before making strong quality claims.
- Capture tokens per second and memory pressure.
- Keep Mistral out of short-loop tests unless specifically needed.

Artifacts committed:

- Phase 1 local model prompt set, runner, raw results, model cards, behavior notes, and comparison report.

Next step:

- Move into Phase 2 prompt evaluation using `qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b`.

## 2026-07-05: Labs 1.1 and 1.2

Phase: 1 - Local AI Lab

Labs:

- Lab 1.1: Run Local Models
- Lab 1.2: Response Length / `num_predict` Experiment

Time spent: Local model execution and response-length experimentation

What I learned:

- I now understand how to install and run local models and compare them using a repeatable runner.
- `num_predict` has a meaningful impact on model behavior. A lower value can cut responses short or force a more compressed answer, while a higher value gives the model more room to respond fully.
- Quantization is a practical hardware tradeoff. Full-size models are not realistic on my Mac Mini because of RAM/VRAM limitations, so compressed model variants are required.
- Quantization levels such as 8-bit, 4-bit, and 2-bit represent different compression tradeoffs. Lower-bit quantization can make models easier to run on limited hardware, but may reduce output quality.
- This reinforced a familiar engineering principle: optimize based on hardware constraints.

What I built or tested:

- Downloaded and ran local LLMs on my Mac Mini.
- Used the Codex-built runner to compare model outputs and latency.
- Tested how changing `num_predict`, or the number of tokens available for the model response, affects the output.

What surprised me:

- The model comparison report was more insightful than expected and generally lined up with my own findings from reviewing the raw data.
- I did not see obvious hallucinations in the initial outputs, although I did not fully validate every factual or mathematical answer.

What failed or needs improvement:

- The current evaluation does not yet have strong ground-truth answer validation.
- Some outputs looked reasonable, but I still need to verify factual and mathematical correctness more rigorously.
- The next version of the evaluation should include prompts with known correct answers, hallucination traps, and scoring criteria.

Security observations:

- No major security testing was performed yet.
- This lab was focused on local execution, latency, output comparison, and basic model behavior.

Assurance observations:

- The runner creates the beginning of an assurance workflow because it allows repeatable comparison across models.
- The evaluation still needs formal scoring, answer keys, and structured pass/fail criteria.

Questions for follow-up:

- How much does quantization affect reasoning quality?
- Which model performs best under limited token budgets?
- Do smaller or more heavily quantized models hallucinate more often?
- How should I structure scoring so model comparisons are less subjective?
- What prompt categories should be included in the first baseline evaluation suite?

Artifacts committed:

- Existing Phase 1 runner, prompt set, raw results, comparison report, behavior notes, and model cards.

Next step:

- Improve the evaluation set with ground-truth answers, hallucination traps, and basic scoring.
- Review the existing model cards and add quantization details where available.
