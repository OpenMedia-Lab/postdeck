# Post

Read when publishing and wrapping up. All external-visibility rules live here.

## The posting adapter

The mechanism was chosen at Intake. Three shapes:

- **Platform CLI/API** — post through it in its most private mode (draft / private / only-me). Verify the result through the same tool.
- **Draft-only** — create the artifact where the platform keeps drafts (or as far as the mechanism reaches), then stop.
- **Handoff** — no usable mechanism: bundle `pages/*.png` + `note.txt` (title, body, topics) into one folder and report that publishing is manual.

Whatever the shape, the rule holds: **nothing goes fully public from this skill.** Public is the human flipping a switch after review, or an approved delete-and-repost.

## Reference: the xhs CLI

Xiaohongshu is the worked example — the patterns below generalize to any CLI-shaped mechanism.

Auth first:

```bash
xhs status    # authenticated: true for the expected account
xhs my-notes  # optional: confirm recent notes for context
```

Post — note the flag shapes, they are easy to get wrong:

```bash
xhs post \
  --title "≤20 chars" \
  --body "$(cat body.txt)" \
  --images p1.png --images p2.png … \   # repeated flag, NOT a list
  --topic 大模型 --topic 深度学习 … \     # repeated flag, resolved by search
  --private
```

- `--images` / `--topic` are single-value flags: repeat them per item.
- `--topic` searches and attaches; unknown topics may attach nothing — verify on the posted note if it matters.
- `--private` is mandatory on every post this skill makes. There is no "publish public" path.

## Verify and report

After posting, confirm visibility through the mechanism itself:

```bash
xhs my-notes    # the new note shows permission_msg: 仅自己可见
```

Report the post id, title, image count, and the local paths of the deck source + PNGs. State clearly: **the note is live but private/draft; going public is a human action** — flip visibility in the app, or approve a delete + repost.

## Revisions

If the human's review asks for changes: edit the deck source, re-render, re-inspect, re-post the preview. A stale preview from a previous round should be deleted only with the human's ok.

## Cleanup contract

At Report, delete intermediates: vendored dep trees (KaTeX `package/`), `*.pdf`, scratch venvs, one-off raster scripts, tarballs. Keep the deck's HTML source and the final `pages/` PNGs unless the human says otherwise — they're the record of what's live and the starting point for any revision.
