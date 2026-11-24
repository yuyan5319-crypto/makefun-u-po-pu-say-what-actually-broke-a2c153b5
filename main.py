#!/usr/bin/env python3
"""Say What Actually Broke — one blunt, honest error line.

Writes a single-line error message to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output, then ./output). The line names the real
failure in plain words instead of apologising in generalities.
"""

import os
import sys

MAX_CHARS = 200

SENTENCE = (
    "The upload failed: your file is 4.2 GB, the limit is 10 MB, "
    "and optimism is not a compression algorithm."
)


def resolve_output_dir():
    """Pick the output directory: env var, then /output, then ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    try:
        os.makedirs("/output", exist_ok=True)
        return "/output"
    except OSError:
        return os.path.join(os.getcwd(), "output")


def validate(text):
    """The gate: 1-200 chars, non-empty, a single line, no trailing newline."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not text.endswith("."):
        raise ValueError("entry must be a complete sentence ending with a period")
    return text


def main():
    sentence = validate(SENTENCE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(sentence)
    print(f"Wrote {len(sentence)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
