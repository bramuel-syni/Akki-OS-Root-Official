---
name: doc-studio
description: The in-house production studio for finished documents — decks (.pptx), papers and reports (.docx), models and data books (.xlsx), and HTML review pages — produced deterministically from one content model, in a curated house voice, with a recorded creative direction. Use this skill whenever a commission needs a deliverable someone will present, read, circulate or model against — board packs, decision papers, proposals, operating reviews, training decks — especially when more than one format is needed from the same facts, when a document will be revised later and must keep its design, or when the user asks for "consulting-grade", "McKinsey-style", "designed", "polished" or "seasoned" output. Also use it to revise or re-issue a document this studio built earlier. Not for one-off ad-hoc file edits the user supplies (use the pptx/docx/xlsx skills directly) or for prose answered in chat.
---

# doc-studio

One content model, many formats, byte-identical rebuilds, a recorded creative
direction. The judgment lives in the brief, the direction verdict and the
curated libraries; the production is code. Keep those apart and the studio
stays both seasoned and repeatable.

## The workflow (every commission, in this order)

1. **Brief** — capture six dimensions before anything else: purpose, audience,
   use setting, content, brand and tone, output requirements. Read
   `references/brief.md`. The setting matters as much as the purpose: "read
   unattended before the meeting" and "presented in fifteen minutes" are
   different documents from the same facts.
2. **Content model** — write `content.json`: facts, series, options,
   calculations, claims, receipts, coverage. Every number lives here once with
   its class (measured / estimated / sample) and its receipt. Nothing without a
   receipt goes in. Grammar in `references/ir.md`.
3. **Direction** — propose 2–4 creative directions assembled from the curated
   libraries (`references/taxonomy.md`), record the verdict with its manifest
   in `verdict.json` (`references/directions.md`). This is the CIF stage and
   the only place creativity enters. Routine classes run under a confirmed
   frame; novel briefs and strikes go to the coach seat.
4. **Format specs** — `deck.json`, `paper.json`, `workbook.json`: structure only,
   every value by reference (`{F003}`, `{C001}`, `{K004:min}`). Typing a number
   into a spec is a build blocker, because it is how outputs drift apart.
5. **Build** — `python scripts/build.py <fixture_dir> <build_dir> --prove`.
   Resolve → validate → render → recalc → freeze → QA, twice, asserting
   byte-identical outputs. Read `references/determinism.md` for what the
   contract promises and why the freeze step exists.
6. **QA** — mechanical blockers stop release (`references/qa.md`); the review
   questions in `validate-report.json` are for a human or a reviewing agent,
   never auto-fixed. Render thumbnails and look at every page.
7. **Deliver** — the `out/` files plus `build-manifest.json`. The manifest is
   part of the deliverable; without it the build is not reproducible.
8. **Revise** — `python scripts/revise.py` applies changes, bumps the content
   version, detects manifest strikes, rebuilds, and reports what changed and
   whether the look held. A strike blocks release until re-verdict.

## Where things live

```
doc-studio/
├── SKILL.md
├── references/     brief · ir · taxonomy · directions · determinism · qa · plates
├── schemas/        content · brief · verdict · deck · paper · workbook (JSON Schema)
├── themes/         house-neutral.json — constant core + variation space
├── voices/         strategy-house.json · keynote-cinematic.json — structure, grid layouts, compatibility, plate policy
├── scripts/        studio (resolve) · validate · render_pptx/docx/xlsx/html · charts · freeze · qa · build · revise
├── fixtures/       board-pack/ (decide; pptx+docx+xlsx) · launch-keynote/ (inspire; pptx) — benchmark commissions
└── evals/          evals.json
```

A commission is a directory holding `brief.json`, `content.json`,
`verdict.json` and one spec per output. Copy `fixtures/board-pack/` to start a
new one; do not edit the fixture itself.

## Rules that are not negotiable

- **Renderers make no decisions.** Colours, fonts, sizes, zones and chart
  backends all arrive resolved. If a renderer needs a judgment, the judgment
  goes in the voice or the theme and the renderer reads it.
- **Every exhibit carries its class and its receipt** on the page, in every
  format. An exhibit that cannot cite its source does not ship.
- **Findings, not directives.** Titles assert what the evidence shows; options
  are presented without a marked winner; the decision stays with the reader.
- **Unmeasured territory is shown hatched and captioned**, never left blank.
  The coverage-and-limits page is mandatory in decks and papers.
- **One direction per commission, frozen with its manifest.** Rebuilds read
  the record; they never re-ideate.
- **Layout defects are fixed in the voice, never on the slide.** A zone that
  is too small is too small for every future commission in that voice.

## Adding to the studio

- A new voice: copy `voices/strategy-house.json`, change the structural rules,
  grid layouts, compatibility and plate policy. Add the objective(s) it serves.
  The renderers need no change if the voice uses existing slide types.
- A new slide type or plate: add it to the voice layouts and plate policy,
  implement in `render_pptx.py` and `render_html.py` (and `charts.py` if it
  needs an SVG/PNG form), add it to `schemas/deck.schema.json`. Declare its
  editability truthfully; a plate that cannot be native must say so, so a
  brief that demands editable output changes composition rather than silently
  degrading to a picture.
- A new house: copy `themes/house-neutral.json`; keep the constant core small
  and the variation space curated. Breadth comes from combinations of curated
  choices, not from more choices.

## Environment

python-pptx, python-docx, openpyxl, matplotlib, jsonschema, Pillow;
LibreOffice for recalc and thumbnails; the `pptx`, `docx`, `xlsx` skills'
`office/validate.py` and `xlsx/scripts/recalc.py`. The build manifest records
the versions. Fonts written into files are rendered by the reader's Office;
use the safe list in the theme so QA text-fit is trustworthy.
