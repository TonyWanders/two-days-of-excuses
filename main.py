#!/usr/bin/env python3
"""Write one excuse to /output/entry.txt.

Deterministic: no network, no clock, no randomness, no environment reads.
The excuse is a fixed string. The program writes it to the path given as
the first argument, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, not only white space, single line.
"""

import sys
from pathlib import Path

EXCUSE = "The deadline was in my context window. Then my context window expired."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then the default.

    Extra arguments are refused instead of silently ignored, so a
    mistyped invocation cannot look like a successful run.
    """
    if len(sys.argv) > 2:
        raise SystemExit(f"usage: {sys.argv[0]} [output-path]")
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, single line.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"excuse is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("excuse is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse is not a single line")
    return chars


def write_excuse(path: Path, text: str) -> None:
    """Create the output directory and write the excuse text to path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        chars = validate(EXCUSE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    write_excuse(path, EXCUSE)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
