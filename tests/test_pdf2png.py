import subprocess
import sys
from pathlib import Path

import pytest

pymupdf = pytest.importorskip("pymupdf")

SCRIPT = Path(__file__).resolve().parents[1] / "postdeck" / "scripts" / "pdf2png.py"


def test_rasterizes_each_page(tmp_path):
    doc = pymupdf.open()
    for _ in range(3):
        page = doc.new_page(width=300, height=400)
        page.insert_text((40, 40), "postdeck")
    pdf = tmp_path / "deck.pdf"
    doc.save(pdf)
    doc.close()

    out = tmp_path / "pages"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(pdf), str(out), "1.0"],
        check=True,
        capture_output=True,
    )

    pngs = sorted(out.glob("page-*.png"))
    assert len(pngs) == 3
    import struct

    for p in pngs:
        data = p.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        w, h = struct.unpack(">II", data[16:24])
        assert (w, h) == (300, 400)


def test_usage_error_without_args():
    proc = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True)
    assert proc.returncode == 1
    assert b"usage:" in proc.stdout
