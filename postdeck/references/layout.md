# Layout

Read when building the paged deck. The default path is HTML cards — start from `templates/cards.html`, which encodes the geometry and component vocabulary; fill it, don't redesign it. If the clarify round picked another render path, this stage produces whatever that path consumes (e.g. a Markdown doc for an Obsidian-style export) — the principles below still apply.

## Geometry

- Aspect follows the platform: **1242×1656 CSS px (3:4 portrait)** is the Xiaohongshu classic; other platforms may want 4:5, 1:1, or 16:9 — set it once in `@page` and `.page`, per the task card.
- With HTML → PDF: `@page { size: 1242px 1656px; margin: 0 }` and one fixed-size `.page` per card with `page-break-after: always`.
- Padding ~72px sides, footer strip with `工作作坊 · 标题` left and `n / N` right.
- Legibility rule: body ≥ ~26px at this width — the export is ~1.6×, and readers see it on a phone. If a page doesn't fit, cut content; never shrink below the floor.

## Vendor everything the render needs

- **KaTeX**: download the npm tarball (`registry.npmmirror.com` or registry.npmjs.org), extract `dist/`, reference `katex.min.css` + `katex.min.js` + `contrib/auto-render.min.js` locally. A CDN link that fails at print time produces raw `\( \)` on every page — Inspect will catch it, but vendor instead.
- **Fonts**: system CJK stack (`PingFang SC`, `Hiragino Sans GB`) + `SF Mono`/`Menlo` for code. KaTeX carries its own math fonts.
- No external images; diagrams are CSS/SVG inline.

## Component vocabulary

Reuse the template's classes — they exist so pages stay consistent:

- `.kicker` + `.pagetitle` — section eyebrow + page title
- `.formula` — display math block; inline math inside prose
- `.quote` (accent) — the question or takeaway the page answers
- `.note` (warm) — caveats, "注意" boxes
- `.chips` — reference works, keywords
- `.code` — dark block, manually spanned highlights (`kw`/`fn`/`cm`)
- `.diagram` + `.fbox`/`.farrow`/`.expert` — flow boxes; diagrams are boxes + arrows, not ASCII art
- `table.cmp` — comparisons; keep to ≤4 rows

Accent color: pull the blog's theme hue when identifiable (e.g. hue-250 violet); warn color is a complementary tone for `.note` and "shared"-style highlights.

## Density

A page with 40% whitespace at the bottom is fine; a page whose footer overflows is not. Whitespace reads as confidence in the feed — overcrowding reads as a screenshot.
