# news-image-20261123 entrypoint.
# Copies the Monday 23 November 2026 front page (entry.png, 39 stories,
# 7 regions) to the output directory after checking it fits the limits.
# Standard library only, no network, deterministic.
import hashlib
import os
import struct
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.png")
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(TARGET_DIR, "entry.png")
LIMIT_BYTES = 1 << 20
LIMIT_SIDE = 1024


def png_dimensions(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png does not start with a PNG signature")
    return struct.unpack(">II", head[16:24])


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(1 << 16)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def run():
    if os.path.getsize(SOURCE) > LIMIT_BYTES:
        raise SystemExit("entry.png is larger than 1 MiB")
    w, h = png_dimensions(SOURCE)
    if w > LIMIT_SIDE or h > LIMIT_SIDE:
        raise SystemExit(f"entry.png is {w}x{h}, over the 1024 limit")
    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(SOURCE, "rb") as src, open(TARGET, "wb") as dst:
        dst.write(src.read())
    if digest(SOURCE) != digest(TARGET):
        raise SystemExit("the copy does not match the source image")
    print(f"entry.png ready: {w}x{h}, {os.path.getsize(TARGET)} bytes — Monday 23 November 2026, 39 stories")


if __name__ == "__main__":
    run()
    sys.exit(0)
