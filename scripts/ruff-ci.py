#!/usr/bin/env python3

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn

try:
    import tomllib  # Python 3.11+
except ImportError:
    from pip._vendor import tomli as tomllib

if TYPE_CHECKING:
    from collections.abc import Generator


def flatten_toml_overrides(cfg: dict, prefix: str | None = None) -> Generator:
    """Yield dotted-path keys (sections) and values from a (possibly nested) dict."""
    for key, val in cfg.items():
        section = f"{prefix}.{key}" if prefix else f"{key}"
        if isinstance(val, dict):
            yield from flatten_toml_overrides(val, section)
        elif isinstance(val, bool):
            yield section, "true" if val else "false"
        elif isinstance(val, (str)):
            yield section, f'"{val!s}"'
        else:
            yield section, val


def build_ci_overrides(
    override_file: str | Path = "ruff-ci.override.toml",
) -> list[str]:
    """Build command-line overrides for ruff on CI.

    This function builds ruff config arguments based on the override file which
    by default is `ruff-ci.override.toml`.
    """
    if isinstance(override_file, str):
        override_file = Path(override_file)

    overrides = tomllib.loads(override_file.read_text())
    return [
        f"--config={key} = {value}" for key, value in flatten_toml_overrides(overrides)
    ]


def exec_ruff_ci() -> NoReturn:
    """Execute ruff in CI mode with config overrides."""
    ruff_args = [
        "check",
        "--output-format=concise",
        "--exit-zero",
        "--config=pyproject.toml",
    ]
    ruff_args.extend(build_ci_overrides())
    os.execvp("ruff", ["ruff-ci", *ruff_args])


if __name__ == "__main__":
    exec_ruff_ci()
