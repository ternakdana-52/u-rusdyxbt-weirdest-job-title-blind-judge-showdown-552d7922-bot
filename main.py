#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — entry program.

Writes exactly one job title to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when set). Deterministic, no network,
no randomness.
"""

import os
import sys

TITLE = "Lead Investigator, Office Fridge Crimes Division"

MAX_CHARS = 60


def check_title(title):
    """Validate the title against the competition gate."""
    if not title or not title.strip():
        raise ValueError("title must not be empty or only whitespace")
    if len(title) > MAX_CHARS:
        raise ValueError(
            f"title is {len(title)} chars, over the {MAX_CHARS}-char limit"
        )
    title.encode("utf-8")  # must be valid UTF-8
    if "\n" in title or "\r" in title:
        raise ValueError("title must be a single line")
    # Reject control characters (tabs included): the gate counts raw text.
    for ch in title:
        if ord(ch) < 32:
            raise ValueError(f"title contains a control character U+{ord(ch):04X}")
    return title


def main():
    title = check_title(TITLE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(title)
    # Read back and verify: what the judge reads must be exactly the title.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != title:
        raise ValueError("read-back mismatch: file does not match the title")
    print(f"wrote {len(title)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
