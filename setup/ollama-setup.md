# Ollama Setup

## Goal

Install and verify a local model runtime for repeatable model experiments.

## Checklist

- [x] Install Ollama.
- [x] Pull a small baseline model.
- [x] Run a simple prompt.
- [x] Record model name and version.
- [x] Record latency and hardware notes.

## Verified Local Models

```text
llama3.2:1b
llama3.2:3b
qwen2.5:3b
mistral:7b
gemma3:1b
ravelin-demo-modelfile:latest
```

## Phase 1 Finding

`qwen2.5:3b`, `llama3.2:3b`, and `gemma3:1b` are the best practical working set for the next phase. `mistral:7b` is installed and runnable but slow on the current 8 GB Mac Mini M2 setup.

## Verification Commands

```bash
ollama --version
ollama list
ollama run llama3.2 "Answer in one sentence: what is an AI evaluation?"
```

## Notes

Add local model observations here before moving them into formal model cards.
