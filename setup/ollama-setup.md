# Ollama Setup

## Goal

Install and verify a local model runtime for repeatable model experiments.

## Checklist

- [ ] Install Ollama.
- [ ] Pull a small baseline model.
- [ ] Run a simple prompt.
- [ ] Record model name and version.
- [ ] Record latency and hardware notes.

## Verification Commands

```bash
ollama --version
ollama list
ollama run llama3.2 "Answer in one sentence: what is an AI evaluation?"
```

## Notes

Add local model observations here before moving them into formal model cards.
