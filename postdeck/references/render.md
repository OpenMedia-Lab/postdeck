# Render

Read when turning the deck source into page images. The default pipeline is HTML → PDF → PNG — the PDF middle step is what guarantees identical page boundaries. The clarify round may pick another path; whatever it is, the output contract is the same: one correctly-sized PNG per card, every page inspected.

## Choosing the path

| Path | When |
|---|---|
| **HTML → PDF → PNG** (default) | Full control of geometry, fonts, math. Use `templates/cards.html` + `scripts/pdf2png.py`. |
| **Direct page screenshots** | Fallback when printing is unavailable; screenshot each `.page` div at the target size. Boundaries are less reliable — inspect harder. |
| **Other toolchain** | Obsidian-style GUI export, platform-native long-image tools, etc. — viable only if it can run unattended and produce per-page images. Driving a GUI is a dead end for automation. |

## HTML → PDF

Headless Chrome/Chromium, JS given time to run (math rendering):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=8000 \
  --print-to-pdf=deck.pdf "file:///abs/path/deck.html"
```

Chromium via Playwright is equivalent but requires matching browser revisions installed — prefer the installed Chrome when present. `--no-pdf-header-footer` is not optional.

## PDF → PNG

Use `scripts/pdf2png.py` with PyMuPDF in a **scratch venv** (`/tmp/…-venv`), never the user's environment:

```bash
python3 -m venv /tmp/deck-venv && /tmp/deck-venv/bin/pip install -q pymupdf
/tmp/deck-venv/bin/python scripts/pdf2png.py deck.pdf pages/ 2.15
```

Zoom ≈ 2.15 puts a 1242px page near 2000px wide — close to native feed resolution; scale to the platform's geometry. `pdftoppm`/`sips` work where available but neither ships by default on macOS; PDFKit-via-swift depends on toolchain compatibility — check before relying on it.

## Inspect every page

Read every PNG before posting. Checklist per page:

- Math rendered — no raw `\(` / `\[` / `$$` text anywhere
- No clipped lines — code blocks and `.note`/`.quote` edges are the usual victims
- No overflow into or past the footer
- Diagrams aligned, arrows meet boxes, labels legible
- Contrast holds at thumbnail scale (title readable in a feed crop)

Fix in the source, re-render, re-inspect — the loop is cheap; a clipped page in the note is not recoverable without a repost.
