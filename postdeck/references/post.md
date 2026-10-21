# Post

Read when publishing and wrapping up. All external-visibility rules live here.

## The posting adapter

The mechanism was chosen at Intake. Three shapes:

- **Platform CLI/API** — post through it in its most private mode (draft / private / only-me). Verify the result through the same tool.
- **Draft-only** — create the artifact where the platform keeps drafts (or as far as the mechanism reaches), then stop.
- **Handoff** — no usable mechanism: bundle `pages/*.png` + `note.txt` (title, body, topics) into one folder and report that publishing is manual.

Whatever the shape, the rule holds: **nothing goes fully public from this skill.** Public is the human flipping a switch after review, or an approved delete-and-repost.

## Rust CLI adapters

Use the maintained [OpenMedia-Lab](https://github.com/OpenMedia-Lab) clients: `xhs-cli` (`xhs`), `zhihu-cli` (`zhihu`), and `x-cli` (`x native …`). Their command-level capabilities differ; check `--help` on the installed version. These CLIs allow explicit public writes, but this skill retains its preview-first boundary.

### Xiaohongshu

Auth first:

```bash
xhs status --json  # verify the returned profile belongs to the expected account
xhs my-notes  # optional: confirm recent notes for context
```

For reading reference notes, keep the signed URL or pass the returned `xsec_token` with `xhs read NOTE_ID --xsec-token TOKEN`; a bare ID may be insufficient. Use `xhs detail` for the current account's editable note representation.

Post — note the flag shapes, they are easy to get wrong:

```bash
xhs post \
  --title "标题" \
  --body "$(cat body.txt)" \
  --images p1.png --images p2.png \
  --topic 大模型 --topic 深度学习 \
  --private
```

- Repeat `--images` and `--topic` per item. The Rust client also accepts multiple paths after `--images`.
- `--topic` resolves exact names or IDs before posting; unknown topics fail rather than silently disappearing.
- `--private` is mandatory on every post this skill makes. There is no "publish public" path.

## Verify and report

After posting, confirm visibility through the mechanism itself:

```bash
xhs detail NOTE_ID  # creator representation: privacy.type must be 1
```

Report the post id, title, image count, and the local paths of the deck source + PNGs. State clearly: **the note is live but private/draft; going public is a human action** — flip visibility in the app, or approve a delete + repost.

### Zhihu

Use `zhihu status`, `zhihu search`, `zhihu my-articles`, and `zhihu read` for source/reference retrieval. Create an article draft with `zhihu article "标题" --content-file body.html -i page-01.png`; repeat `-i` for other images. Read it with `zhihu draft ARTICLE_ID` and return its edit URL. Omit `--publish` in this skill. Images can take time to appear in draft reads; do not append duplicates while waiting.

### X

Use `x native me`, `search`, `timeline`, and `read` for reference retrieval. `x native post` publishes immediately and offers no draft mode. Hand off images and copy for review; do not invoke it as a preview operation. Split a deck according to the platform's per-post media limit. `post` and `reply` can form a thread after the human separately authorizes public posting. Reading long posts does not establish X Article publishing support.

## Revisions

Fix the card source, re-render, and re-inspect first. Prefer an in-place update of the existing preview:

```bash
xhs edit NOTE_ID --title "修订标题" --body "$(cat body.txt)" --images p1.png --images p2.png
xhs detail NOTE_ID
```

Omitted fields, including visibility, are preserved. Supplying images replaces the image list; omitting them preserves existing images. Confirm the same note ID, expected text/image IDs, and `privacy.type == 1` after editing. Do not recreate the note to work around an edit error without explaining the failure.

For Zhihu use `zhihu edit-article ARTICLE_ID --title "修订标题" --content-file body.html`, then read the same draft again. `--image` appends; to replace existing card images, rebuild the complete HTML body with the desired uploaded image URLs and pass `--content-file`. Keep `--publish` omitted. If the installed mechanism truly lacks edits, fall back to a new preview and report both IDs; delete a stale preview only with the human's authorization.

## Cleanup contract

At Report, delete intermediates: vendored dep trees (KaTeX `package/`), `*.pdf`, scratch venvs, one-off raster scripts, tarballs. Keep the deck's HTML source and the final `pages/` PNGs unless the human says otherwise — they're the record of what's live and the starting point for any revision.
