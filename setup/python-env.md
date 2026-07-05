# Python Environment

## Goal

Create a reproducible Python environment for evaluation runners, scoring scripts, and report generation.

## Checklist

- [ ] Create a virtual environment.
- [ ] Install baseline dependencies.
- [ ] Freeze dependencies.
- [ ] Run a smoke test.

## Suggested Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip freeze > requirements.txt
python -c "print('python environment ok')"
```

## Notes

Keep dependency additions intentional. Every package should support an experiment, evaluation, or report.
