# QUARANTINE · `repos/Akki-Executive-Final/` · read-only · 2026-09-18

**Authority:** Owner ruling 2026-09-18 (post-Q1+Q2 close · banked verbatim in `STATE/DECISIONS.md`):

> "The anomaly repo (Akki-Executive-Final): quarantine read-only, out of scope, not a source for anything until ruled otherwise."

## Provenance of the anomaly

- The problem statement (CHUNK 1) names four repos: `RMS-IQ-Core-2`, `Akki-OS-V1`, `Extraction-Akki`, `Akki-Executive-Core`.
- `repos/Akki-Executive-Final/` exists in the workspace and is **NOT** one of those four.
- Task B (repo inventory · `notes/chunk1_20260918/chunk1_task_b_repo_inventory.md`) and Task C (cross-repo overlap · `notes/chunk1_20260918/chunk1_task_c_cross_repo_overlap.md` + `_matrix.json`) both banked it as anomaly-scope data.

## Quarantine terms (from owner ruling)

1. **READ-ONLY.** No writes to `repos/Akki-Executive-Final/` from any wave, seal, or agent.
2. **Out of scope.** Not counted against any CHUNK, milestone, gate, or ratchet.
3. **Not a source for anything.** No file inside is authoritative for any decision, mapping, or reference in any downstream artefact — including future Chunk-3 REUSE_ASSESSMENT.md, the G5 mapping, or any milestone charter — until the owner rules otherwise.
4. **Existing Task-C references** to `Akki-Executive-Final` (banked in `chunk1_task_c_matrix.json` under anomaly-scope) remain as anomaly-scope data points but MUST NOT be promoted to primary-scope findings.

## Operational effect

- **Analysis scripts** under `/app/assessment_workspace/tools/` that scan repos MUST exclude `repos/Akki-Executive-Final/` from primary-scope output.
- **Future chunk artefacts** MUST NOT cite `repos/Akki-Executive-Final/` as a source for reuse/modify/re-point/build/retire classifications.
- **Grep/find/glob** helpers used by main-agent workflows SHOULD prefer patterns that omit this path unless the search is expressly investigating the quarantine (e.g. auditing that nothing inside has been read).

## Exit criteria

Owner ratifies one of:

- **UNQUARANTINE** — the repo is admitted to primary scope as a fifth reference repo. Would require an amendment to the problem statement.
- **DELETE** — the folder is removed from the workspace tree. Would require an owner-approved delete ceremony.
- **RETAIN AS QUARANTINED** — status quo continues indefinitely.

Until then, this note is the only authoritative disposition.

## Cross-references

- `notes/chunk1_20260918/chunk1_task_b_repo_inventory.md` — anomaly first surfaced in repo inventory.
- `notes/chunk1_20260918/chunk1_task_c_cross_repo_overlap.md` — anomaly-scope overlap data.
- `STATE/DECISIONS.md` — owner ruling 2026-09-18 banking this quarantine.
- `STATE/AUTONOMOUS_RUN_PLAN.md §5` — quarantine referenced in the sequenced-milestone context.
