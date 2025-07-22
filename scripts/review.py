#!/usr/bin/env python

import argparse
import logging
import subprocess
import sys
from pprint import pformat
from textwrap import dedent

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def review(runners: list[str], diff_range: str = "HEAD~1") -> int:
    """Runs code review diagnostics tool on the specified git diff range.

    Args:
        runners (list[str]): List of reviewdog runners to use.
        diff_range (str): The git diff range to review. Defaults to last commit.

    Returns:
        int: The return code from the reviewdog process.

    """
    reviewdog_args = [
        "-filter-mode=added",
        f"-diff=git diff {diff_range}",
        "-conf=.reviewdog.yml",
        # We could possibly parse `rdjsonl` output in the future to produce a
        # more detailed report, but for now we just use the local reporter.
        # This option also supports `gerrit-change-review` as well as
        # `github-pr-review`.
        "-reporter=local",
        "-fail-level=any",
        "-runners=" + ",".join(runners),
    ]
    logger.debug("Running reviewdog with args:\n%s", pformat(reviewdog_args, indent=2))

    review_proc = subprocess.run(
        ["reviewdog", *reviewdog_args],
        check=False,
        capture_output=True,
        text=True,
    )

    code = review_proc.returncode
    logger.debug("Reviewdog process completed with code: %d", code)

    # If reviewdog returns an unexpected code, we should raise an exception.
    if code not in (0, 1):
        logger.error(review_proc.stderr)
        review_proc.check_returncode()

    if stderr := review_proc.stderr.rstrip():
        logger.info(stderr)
    if stdout := review_proc.stdout.rstrip():
        logger.info(stdout)

    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="Run in CI mode, using 'ruff-ci' runner instead of 'ruff'",
    )
    parser.add_argument(
        "--diff-range",
        type=str,
        default="HEAD~1",
        help="Git diff range to review (default: HEAD~1)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    # Continuous Integration mode uses a set of less strict rules.
    ci_mode: bool = args.ci_mode
    # Runners are specified in `.reviewdog.yml` file
    runner: list[str] = ["ruff-ci" if ci_mode else "ruff"]
    diff_range: str = args.diff_range
    verbose: bool = args.verbose

    if verbose:
        logger.setLevel(logging.DEBUG)

    code = review(runner, diff_range)
    if code == 1:
        msg = """

        🚨🚨🚨
        Your code can be improved. See `ruff` suggestions
        and use it to assist with making the necessary changes.
        🚨🚨🚨

        """
        logger.warning(dedent(msg))
    elif code != 0:
        msg = f"reviewdog returned an unexpected code={code}"
        logger.error(msg)
    else:
        msg = """
        Code review passed successfully! 🎉
        """
        logger.info(dedent(msg))
    sys.exit(code)
