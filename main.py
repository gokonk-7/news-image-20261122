"""Entry point: copy the rendered cover to the output directory.

Standard library only. No network, no clock, no randomness. The output
is byte-identical on every run because the source image never changes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")


def validate(path):
    """Refuse to ship a broken cover: PNG magic, 1024x1024, non-empty."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if (width, height) != (1024, 1024):
        raise ValueError(f"entry.png is {width}x{height}, expected 1024x1024")
    if os.path.getsize(path) < 1024:
        raise ValueError("entry.png is suspiciously small")


def main():
    validate(SRC)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
