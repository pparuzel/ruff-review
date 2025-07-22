# ruff-review
🔎📝Setup ruff with reviewdog to incrementally enforce ruff rules

## Dependencies

### ruff
```bash
pip install ruff
```

### reviewdog
[Read how to install reviewdog](https://github.com/reviewdog/reviewdog?tab=readme-ov-file#installation)

## Usage

To run an incremental code review, use the provided script:

```bash
scripts/review.py [--ci-mode] [--diff-range HEAD~1] [--verbose]
```

For full help and options, run:

```bash
scripts/review.py -h
```
