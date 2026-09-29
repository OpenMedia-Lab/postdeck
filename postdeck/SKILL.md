---
name: postdeck
description: A gated pipeline that turns a technical blog post into a swipe-deck social-media note. Clarify platform, style references, render path, and posting mechanism up front; distill the article into card pages; render; inspect every page; then post as private/draft (or hand off) so the human reviews the real thing — going public is always the human's call. Xiaohongshu via the xhs CLI is the classic worked example. Triggers on converting posts to swipe-card notes — "发到小红书/知乎/公众号", "写成图文笔记", "swipe deck", "card carousel".
---

# postdeck

A blog post and a swipe-deck note are different media: the post rewards depth, the feed rewards the first card. Pasted paragraphs become a wall nobody reads; screenshots of the rendered article are illegible on a phone. postdeck treats the conversion as a **redesign** — the article is distilled into a card deck, and the human controls the calls that matter: **the platform, the style, the render path, and the public flip**.

Works with agents that load `SKILL.md`, a headless browser for PDF printing, and PyMuPDF (or equivalent) for rasterizing pages. Posting needs whatever mechanism the target platform offers — a CLI (e.g. `xhs`), an API, or a manual handoff of the finished deck.

## Intake → Adapt → Layout → Render → Inspect → Post → Report

| Stage | Produces | Human decides |
|---|---|---|
| **Intake** | task card: source, platform, style refs, render path, post mechanism, mode | every choice on the card — via a clarify round |
| **Adapt** | page plan + note copy (title, body, topics) | approve / revise plan & copy |
| **Layout** | paged HTML deck: cover, one idea per page, closing CTA | — (visual deviations only) |
| **Render** | PDF + per-page PNGs, or the chosen equivalent | — |
| **Inspect** | per-page QA report; fixes already applied | acceptance depth |
| **Post** | private/draft note live, or a handoff bundle | going public — always |
| **Report** | post id / artifact manifest, cleanup confirmation | — |

## Clarify first, then build

Every run starts with a short clarify round — batched multiple-choice questions, each with options plus Other, asked once and never again mid-pipeline:

1. **Platform** — where the note lands. Xiaohongshu is the classic case; the deck adapts to whatever the user names.
2. **Style references** — whose voice to imitate: the account's own published posts, user-supplied example links, skill defaults, or none.
3. **Render path** — HTML → PDF → PNG (default), direct page screenshots, or another toolchain the user prefers.
4. **Post mechanism** — platform CLI/API, or a manual handoff of images + copy.

Answers already in the prompt are reused, not re-asked; anything unanswered gets a marked default rather than a stall. Details and question phrasing live in `references/intake.md`.

## Preview-first posting

Where the platform supports it, posting is private/draft-only — cheap, reversible, and reviewable in the real app. That makes the default gate density lighter than it looks:

- **Hard gate, always:** nothing ever goes fully public. Going public means the human flips visibility themselves, or approves a delete-and-repost — only after seeing the preview.
- **Soft gate, mode-dependent:** the Adapt plan (page list + copy draft) is presented for approval in `align first` mode; in the default `autonomous until preview` mode the agent proceeds straight to a private/draft post and the human rules on the real thing.
- **No publishable platform?** The Post stage hands off a clean bundle — PNGs + `note.txt` — and reports that publishing is manual.

When revisions are requested, fix and re-post the preview. Repeat until the human approves.

## Read only what is needed now

| Reference | Load when |
|---|---|
| [Intake](references/intake.md) | Starting any task; clarify questions, source, modes, authorization |
| [Adapt](references/adapt.md) | Distilling the article into a page plan and note copy |
| [Layout](references/layout.md) | Building the paged HTML deck |
| [Render](references/render.md) | HTML → PDF → PNG and the per-page inspection loop |
| [Post](references/post.md) | Posting mechanisms, preview verification, cleanup |

Do not preload the directory. Follow the current stage only.

## Assets

- `templates/cards.html` — the card-deck base template: 3:4 fixed pages, vendored-math hooks, the component vocabulary (kicker / formula / quote / chips / code / diagram), footer numbering.
- `scripts/pdf2png.py` — rasterize a PDF to per-page PNGs via PyMuPDF (`python pdf2png.py in.pdf outdir [zoom]`). Install PyMuPDF into a scratch venv; never pollute the user's environment.

## Defaults

- Task modes: **full note** / **cards only** / **copy only** / **restyle existing deck** — partial modes enter mid-pipeline via Intake routing.
- Voice comes from evidence — the account's own posts or user-supplied references — never invented. No references means the skill's neutral house style, flagged as such.
- Page budget follows the platform's limit; target ≤12 for a ~5k-word post. Cover + one idea per page + closing page that links back to the source.
- Card geometry follows the platform (3:4 portrait, 1242×1656 CSS px, is the Xiaohongshu classic); export ~2000px wide PNGs. Body text must stay legible at phone width.
- Math and fonts are vendored — nothing the render needs may come from a live CDN.
- Inspect **every** page image before posting: clipped lines, raw TeX, overflow, misaligned diagrams. "Probably fine" is not inspection.
- The note body carries the source link; the cards carry a closing CTA page — readers who want the full derivation know where to go.
- Intermediates (vendored deps, PDFs, scratch venvs, one-off scripts) are deleted at Report; the card source and final PNGs are kept unless the human says otherwise.
