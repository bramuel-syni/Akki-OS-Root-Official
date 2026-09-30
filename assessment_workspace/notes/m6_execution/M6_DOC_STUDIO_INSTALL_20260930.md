# M6 — doc-studio v1.1 installed as Akki's primary production skill · 2026-09-30

Owner approval (verbatim rulings 1–4, conditions A–D) received 2026-09-30 after the owner uploaded `files (21).zip`
(SHA256 `8f920f9f70c771a4e4edabf9ab85e142aa6b5ab1554de094818f3039cba56840`; inner `doc-studio.zip`
`4348b074dbae7a5bb27dca74c4673ad01b81df3d35a9b3f18a53f623045b0d9f`). Package read line for line: SKILL.md, 7 references,
6 schemas, 11 scripts, 1 theme, 2 voices, 2 fixtures, evals, the shipped build manifest and four Northline outputs.

## Rulings → what was done

| Ruling | Implementation |
|---|---|
| 1 LibreOffice now, version pinned | `libreoffice-calc/impress/writer` 7.4.7.2 + `poppler-utils` installed via apt; `freeze.py` records it in every build manifest; `/api/studio/skill` shows the environment of record. |
| 2 Deck engine kept read-only; doc-studio = DRE reference implementation | `/api/decks/*` untouched (14 offline tests still pass; recorded deck re-renderable). Install manifest `role` field records doc-studio as the Deck Rendering Engine's reference implementation (DR-R1–R14). No new producer targets `deck_engine`. |
| 3 Direction stage | `frames.py`: standing frame `FR-strategy-decide-v1` with candidates from `references/taxonomy.md`; operator = confirmer for routine commissions. Non-routine briefs raise `LookupError` ("CIF's ideas endpoint is not mounted") — no LLM/chokepoint path exists or is planned for this stage. |
| 4 Defaults | `house-neutral`, "Tenant confidential", `FR-strategy-decide-v1`. Seed = `content_id/purpose.kind/commission-date` (producer-derived). `build_stamp` set once at commission creation; copied into every spec; revisions keep it. RMS house theme deferred. |

## Conditions → compliance

- **A Helper paths.** One edit only: `scripts/build.py` and `scripts/qa.py` read `DOC_STUDIO_TOOLS_DIR` (build.py also imports `os`).
  In-repo stand-ins live at `services/transform_forms/doc_studio/tools/{xlsx/scripts/recalc.py, pptx|docx/scripts/office/validate.py}`
  (headless-LibreOffice recalc + cached-value error scan; package/relationship/reopen checks — not an OOXML schema validator, stated
  in the manifest). `INSTALL_MANIFEST.json`: v1.0 (owner zip) and v1.1 (installed) per-file SHA256; `changed_from_v1_0 = [scripts/build.py, scripts/qa.py]`; `edit_within_approval = true`. Test `test_install_manifest_edit_is_within_approval` asserts the other 37 files are byte-identical to the owner's package.
- **B Commission producer.** `manifest_template.py` generates M1–M6 from the brief (M2/M3 branch on `read_unattended`/`printed`; M6 only when options exist). `producer_estate.py` never reads a fixture. Test asserts the generated manifest differs from the fixture's.
- **C Verification.** No testing agent. `pytest tests/m6_doc_studio -n 0` → **19 passed** (evals 1–3 in-pod, install/template/frames/producer/receipts, offline lifecycle on a temp store, live `/api/studio/*` reads/refusals). `tests/m6_decks` → 14 passed (regression).
- **D Commission store.** File-backed under `AKKI_STUDIO_STORE_DIR=/app/assessment_workspace/phase0/doc_studio_state/<tenant>/<commission>/` (`record.json`, `v<N>/`, `builds/<id>/{a,b,exports}`). No Mongo writes; no Ledger rows.

## Evals 1–3 in-pod (environment of record: Python 3.11.16 · python-pptx 1.0.2 · python-docx 1.2.0 · openpyxl 3.1.5 · matplotlib 3.11.2 · LibreOffice 7.4.7.2)

- **Eval 1** `build.py fixtures/board-pack --prove`: validate PASS, recalc success, QA PASS, **byte-identical across two builds: 4 outputs**.
  In-pod hashes: pptx `64b946b9768b18adfe0c02ea9bb1492d6377bb6246d2cfcc327922c7a573d9db` (**identical to the owner's shipped manifest** — same python-pptx),
  html `e3dc8bf2822afff334db11822d83313b63d494b4d0a3675392df93be3d7bfcea`, docx `05e5cc05ce0b49dbaaf2bf93224766c488969bf4f4dd7d5e2b9d80481a2b862d`,
  xlsx `59dcc8b9e183221c80ec246bb6a19832e03c5821c692be9c424dd8c06a74838f`. html/docx/xlsx differ from the shipped manifest (matplotlib 3.10.8→3.11.2, LibreOffice 24.2→7.4) — expected, not a defect.
- **Eval 2** revise `content.options.O2.capex=28.5`, `annual_saving=8.4`: content `@2`, `look_preserved: true`, no strikes, release clear, pptx/docx/xlsx changed.
- **Eval 3** revise `brief.setting.printed=false`: strike **M3** (flips `palette_field`, `full_bleed_disallowed`), release `blocked pending re-verdict`.

## Akki binding (`services/transform_forms/doc_studio/`, routes `/api/studio/*`)

- `skill_env.py` (scripts importable, tools dir from env) · `install.py` (manifest + state) · `store.py` · `frames.py` · `manifest_template.py` · `producer_estate.py` · `receipts.py` · `service.py` · `routers/studio.py`.
- Receipts carry `platform_ref` (eij-/cr-…) resolved by `deck_engine.validate.default_resolver` at build; unresolvable → blocker, no artefact. Declared (non-platform) receipts are allowed and marked `declared`.
- Producer output for census `eij-1b359b3cbd2e`: commission `com-a439e14b4e38` (idempotent per tenant/census/purpose/day), deck 12 slides + paper + review HTML; **no workbook** — the studio's `options_model`/`checks` sheet kinds are bound to the Northline option-model shape (renderer untouched per condition A; recorded as a limit).
- Released build `bld-189be273e643`: pptx `dc97c0e18f8b96e63abaac31a02ef62391b6ef1377f17df18a7095f0cbb14fb9`, docx `55d40386135e3ac15772f2c99624fbd4a84751421bef54d52ed90634133797e3`, html `bf8b935f965fae9552bbba89c96d293b3a8040364f3ea03e7de90d803a4ccdbb`; all five receipts platform-bound; validate/QA PASS; byte-identical across two builds.
- Revise → new version + rebuild + diff (look preserved / outputs changed); strike → build runs, release blocked; `reverdict` → new version, verdict re-instantiated from the frame with a manifest regenerated from the current brief (`-rN` id), rebuild. PDF export of the review page via the DRE's headless-browser pipeline (furniture check; outside the byte-identity contract).
- UI: WORKSTUDIO · Documents is the studio (commissions, builds with hash proof, validate blockers vs review questions, QA, look, environment, downloads, inline review page, revisions with strikes, revise form, re-verdict, direction/manifest/receipts, skill state). Estate Intelligence: "Commission board pack" → Open in Documents. Desktop and 390 px checked; no overflow.

## Visual QA finding (fixed before release)

Thumbnails of the first estate deck showed "Three strategies carry 317403.8% of the reclaimable bytes": cost strategies span OBS/NAS (TiB) while `reclaimable_bytes` is database-only. Fixed in the producer (denominator = bytes addressed by all strategies, F021); the development commission that carried the defect and test revisions was removed from the file store and re-commissioned clean. Not a skill defect.

## Not claimed

No CIF ideas endpoint exists yet (non-routine commissions are refused). No RMS house theme. No workbook for the estate commission. The
in-repo office tools are not the office skills' OOXML validators. PDF bytes are not part of the determinism proof. G6 remains open:
M6-T4 (skill really callable by an external caller) and M6-T5 (async/late refusal/withdrawal) were not exercised in this wave.

## Addendum · v1.2 and the four follow-on directives (2026-09-30, later the same day)

- **v1.2 (owner ruling 3a):** `scripts/render_xlsx.py` accepts option-model rows and checks declared in the workbook spec (default = the
  fixture's option shape, fixtures byte-identical), `scripts/studio.py` passes the declared rows through, `schemas/workbook.schema.json`
  documents the optional fields. `INSTALL_MANIFEST.json` lists five approved edits; the other 34 files are byte-identical to the owner
  package (asserted by `test_install_manifest_edit_is_within_approval`). The estate commission now ships a **workbook** with a live option
  model (bytes addressed / monthly saving per strategy, K001–K004 cross-checks).
- **Commission-close producer** (`producer_close.py`, `POST /api/studio/producers/commission-close/{eij}`): the accepted census result
  becomes a decide pack (close or hold the commission). Live: `com-c3d53a38d18f`, build `bld-0c5ad1cefa90` released, byte-identical,
  pptx · docx · html · xlsx, 11 page thumbnails.
- **Page thumbnails:** every released deck is rendered pptx → PDF (LibreOffice) → PNG (poppler, 60 dpi) at build time; served per page at
  `GET …/builds/{id}/thumbnail/{n}` (tenant-bound, `no-store`). Documents shows the grid with an enlarged page view (prev/next) so reviewers
  answer the review questions without downloading. Outside the byte-identity contract, stated in the UI.
- **Verification (condition C):** `tests/m6_doc_studio` **20 passed**, `tests/m6_decks` 14 passed, `tests/m6_callable_skill` 11 passed
  (see `M6_T4_CALLABLE_SKILL_BOUNDARY_20260930.md`). Desktop 1920×800 and 390×844 checked; no page overflow.
