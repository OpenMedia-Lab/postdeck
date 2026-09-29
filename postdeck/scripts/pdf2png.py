#!/usr/bin/env python3
"""Rasterize a PDF to per-page PNGs via PyMuPDF.

usage: pdf2png.py <in.pdf> <out_dir> [zoom]

zoom ~2.15 lands near 2000px wide for a 1242px-CSS page printed to PDF.
Run inside a scratch venv: python3 -m venv /tmp/deck-venv &&
/tmp/deck-venv/bin/pip install pymupdf, then invoke with that interpreter.
"""
import sys
from pathlib import Path

import pymupdf


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    pdf_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 2.15

    doc = pymupdf.open(pdf_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        out = out_dir / f"page-{i + 1:02d}.png"
        pix.save(out)
        print(f"{out} {pix.width}x{pix.height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
