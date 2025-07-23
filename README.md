# ruff-review
🔎📝Setup ruff with reviewdog to incrementally enforce ruff rules

**What can it do?** Report Python code issues based on [ruff ruleset](https://docs.astral.sh/ruff/rules/).

**Why use it?** You need feedback based solely on the lines *you modified*.

**Why different ruleset for CI?** The rules defined by default may be strict, your CI may be less nitpicky. If you use vscode + ruff extension it can highlight potential issues (for a user to consider) without enforcing it in the CI.

To see it in action, check out [test: Add bad code to test GitHub Actions review](https://github.com/pparuzel/ruff-review/pull/2)

## Usage

To run an incremental code review, use the provided script:

```bash
scripts/review.py
```

For full help and options, run:

```bash
scripts/review.py -h
```

## Dependencies

### ruff
```bash
pip install ruff
```

### reviewdog
[Read how to install reviewdog](https://github.com/reviewdog/reviewdog?tab=readme-ov-file#installation)
