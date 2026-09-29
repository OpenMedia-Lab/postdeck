# Intake

Read when a task starts. Intake pins down everything that varies between runs — the source, the platform, the voice, the render path, the posting mechanism — so later stages never have to guess.

## The clarify round

Ask once, up front, as **one batch of multiple-choice questions** — each with ready options plus Other, so the user can pick, override, or free-type. This is the main gate of the whole pipeline; everything downstream keys off these answers.

| Question | Options to offer | Default |
|---|---|---|
| **Target platform?** | Xiaohongshu (classic) · 知乎想法/文章 · 公众号图文 · X/Twitter image thread · Other | Whatever the prompt implies; Xiaohongshu if unstated |
| **Style references?** | My account's own past posts (fetch them) · URLs I provide · Skill's neutral house style · None needed | Account's own posts when a fetch path exists |
| **Render path?** | HTML → PDF → PNG (recommended) · Direct page screenshots · Other toolchain | HTML → PDF → PNG |
| **Post mechanism?** | Platform CLI / API (e.g. `xhs`) · Draft-only, I'll publish myself · Just hand me the files | CLI/API when one is configured; otherwise handoff |
| **Authorization mode?** | Autonomous until preview (default) · Align first — approve plan before rendering | Autonomous until preview |

Rules for the round:

- Skip questions the prompt already answers — "发到小红书，风格参考我的两条笔记" answers platform and refs; don't re-ask.
- Present marked defaults; a user who just hits enter gets a coherent run.
- Other is always a real path, not an error — a platform or toolchain the skill hasn't met becomes the spec for the run, recorded on the task card.
- One round, one batch. Do not drip questions across stages.

## Determine the task mode

| Mode | Route |
|---|---|
| **Full note** | Whole pipeline: Adapt → … → Post |
| **Cards only** | Adapt → Layout → Render → Inspect → Report (no post) |
| **Copy only** | Adapt (copy half) → Report — title / body / topics, no images |
| **Restyle existing deck** | Layout → Render → Inspect → Post — source HTML/PNGs already exist |

If the request is ambiguous, propose the most likely mode rather than silently choosing one.

## Build the task card

After the clarify round, assemble:

- **Source** — post URL, local file, or dev-server address. Fetch the *full* text (fetches truncate — get the whole body). Nav menus and footers are not content.
- **Platform** — name, image count limit, aspect ratio, and what "preview" means there (xhs: `--private` → 仅自己可见; elsewhere: draft / local review / handoff).
- **Style references** — resolved per the clarify answer: fetch the account's posts (e.g. `xhs my-notes`, `xhs read`) or read the provided URLs. Record title habits, body skeleton, link placement, emoji/shortcode usage, image geometry and count.
- **Render path** — confirmed toolchain and where intermediates live.
- **Post mechanism** — the exact command/API/handoff format, verified reachable (e.g. `xhs status` → `authenticated: true` for the expected account) *before* anything is written for it.
- **Goal** — what the note is *for*: series episode pointer, standalone digest, announcement. This decides how much survives Adapt.
- **Authorization mode** — from the clarify round.

## Rules

- Small choices (chip wording, one heading's phrasing) follow convention and are flagged in the final report — never gated.
- Irreversible or external-visibility moves (posting publicly, deleting an existing note) always ask, regardless of mode.
- Output the card as a short summary table, confirm it, then enter the routed stage.
