#!/usr/bin/env python3
"""Entry program for 'The Robot Vacuum's Best Excuse'.

Reads entry.txt (one line, 1-140 characters per the competition gate),
validates it, and writes it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.txt.
Standard library only.
"""

import hashlib
import os
import sys

MAX_CHARS = 140


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")

    with open(src, "rb") as fh:
        raw = fh.read()

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"entry.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    # A trailing newline in the source file is formatting, not part of the
    # entry: the gate counts the entry text itself, so drop exactly one.
    if text.endswith("\n"):
        text = text[:-1]
    raw = text.encode("utf-8")

    if not (1 <= len(text) <= MAX_CHARS):
        print(
            f"gate failed: entry is {len(text)} characters, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("gate failed: entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as fh:
        fh.write(raw)

    digest = hashlib.sha256(raw).hexdigest()
    print(f"wrote {len(text)} characters to {out_path} (sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
