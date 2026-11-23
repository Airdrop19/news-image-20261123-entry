"""Entry for make.fun news-image-20261123: copy the front-page image to /output/entry.png.

The image (entry.png beside this file) sums up world news of Monday 23 November 2026:
39 dated stories from 7 regions on one front page. It was drawn by build_image.py.
Standard library only; no network.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def check_png(path):
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB limit")
    with open(path, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"entry.png is {width}x{height}, over 1024x1024")
    return width, height


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    width, height = check_png(SRC)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    if sha256(SRC) != sha256(OUT):
        raise ValueError("copied entry.png differs from the source image")
    print(f"wrote {OUT} ({width}x{height}, {os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
