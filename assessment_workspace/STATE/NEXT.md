# NEXT.md — Exact next actions

**Last updated:** 2026-08-14 · fixture-arrival cycle CLOSED, corrections committed on assessment-repo `master`, two SOP conflicts ESCALATED awaiting owner ruling.

## Cycle status (2026-08-14)

- BUILD_STRATEGY.md re-assembled — 2447 lines / 250,939 bytes. Three Build-Order-01 corrections applied: §10.F stale placeholder gone; XL count 9→7 reconciled (roster fixed at assembly-tool source); Canon 5 §10 phrasing updated to "five consoles" throughout (FL-OQ-04 CLOSED, retained historical paraphrase-defect note in ledger row).
- Every interface item's `FIXTURE PENDING` marker flipped to `FIXTURE CLEARED @ transcription grade` with citation to `fixtures/binding_acceptance_criteria.md` (BAC-1..BAC-13). `test_four_questions_topline_present` added to every console item's new-invariants list.
- Audits at cycle close: **104/104 file · 1772/1772 canon · 0 failed**; completeness **PASS**.
- Fixtures on disk with sha256:
  - `Akki_Prototype_v7_Design_Brief.md` — `063f2b47…9717b4` (file-cleared).
  - `AISCA_GPU_Access_Guide.pdf` — `0f6b6e0f…157f3` (file-cleared, SOP conflicts A/B ESCALATED).
  - `reference_screenshot_transcription.md` — `d3ae9a6c…02fc949` (transcription-cleared, Q1(c)).
- Pod egress IP re-verified: **`34.16.56.64`** (4/4 curl services agree; no IPv6).

## Blocked (awaiting owner rulings)

- **FL-P2-03** — AISCA SOP SKU mismatch (1×H200 documented vs 4×H200 required by Order §6). Blocks: Phase-0 `acceptance.sh` execution against a vendor SKU; commissioning-checklist SKU line; VM provisioning day cannot start until owner rules the provisioning path.
- **FL-P2-04** — AISCA SOP credential-handoff procedural gap (SOP hands password; Order §6 requires key-only, password-dead-before-data). Blocks: whether `acceptance.sh` extends to cover credential hardening, or owner-side hands run it before seam admission.

## Cold-reader-executable next actions

### 1. Deliver cycle-close report to owner (this reply)

Corrections committed on assessment-repo `master` (SHA computed at commit); audits clean; fixture arrival + hashes recorded; SOP conflicts escalated per Q2(a); pod egress IP `34.16.56.64` for the VM SSH allowlist.

### 2. On receipt of FL-P2-03 / FL-P2-04 rulings

- Update `fixtures/aisca_sop_extraction.md` §5 to reflect the ruling.
- Update `phase0/acceptance.sh` + `commissioning_checklist.md` per the ruled provisioning path.
- Close FL-P2-03 / FL-P2-04 in the ledger with the ruling verbatim.
- Re-run audits, refresh snapshot, commit on `master`.

### 3. On receipt of VM SSH credentials + host IP

- Populate `backend/.env` on `programme/track-a` with `SSH_PRIVATE_KEY_PATH`, `VM_HOST`, `VM_USER`, `SSH_ALLOWLIST_EGRESS_IPS`. Never commit key material; never place it in `STATE/` or any Markdown.
- Run `tools/report_egress_ip.sh` to confirm allowlist target still matches `34.16.56.64`.
- Execute compute-seam preflight (`ssh -o BatchMode`) via seam; run `acceptance.sh` through the seam once Phase-0 SKU/HSS/hardening are resolved.
- Ledger the commissioning record per `phase0/commissioning_record_template.md`.
- Pin actual UTC deadline for the +14d checkpoint in `STATE/PINS.md`.

### 4. Commit Phase-1 A0/A1 code on `programme/track-a`

Currently 7 staged-but-uncommitted files under `repos/Extraction-Akki/backend/`. Independent cycle (Q3 scope this cycle was assessment-repo `master` only). To commit: switch to `Extraction-Akki` clone on `programme/track-a` (baseline `b150c21` preserved), commit test files first with their gating-test-fails-for-right-reason evidence pinned, then commit implementation files. STATE/ update on completion.

### 5. Track-A phase 2 (the Slice)

Once Phase-0 acceptance clean AND Phase-1 committed:
- Hash manifest of archive source before first byte moves.
- Admit representative slice (few hundred hours audio) end-to-end.
- FL-P1-02 focused read lands here (voice-audit custody path A confirmation).
- Deliverable: slice report — timings, throughput, GPU utilisation, evidence-based checkpoint targets as Canon-4 §33 quality-matrix rows.

### 6. Verify audits clean at cycle-close HEAD

```bash
cd /app/assessment_workspace
python3 tools/citation_audit.py 2>&1 | grep -E "File citations|Canon citations|failed"
python3 tools/completeness_audit.py 2>&1 | tail -3
```

Expected: 104/104 file · 1772/1772 canon · 0 failed; completeness PASS.

### 7. Snapshot refresh discipline

`/app/backend/deliverables/BUILD_STRATEGY.md` mirror already refreshed (new sha256 `182ef43…f152d`, 250,939 bytes). `server.py` snapshot commit literal updated post-commit to the new master SHA. Refresh again on every subsequent BUILD_STRATEGY.md change (copy from `/app/assessment_workspace/` to `/app/backend/deliverables/` + update commit literal in server.py and STATE/CONTEXT.md).

### 8. No push, ever

Owner Clarification 1: local commits are the record. Do not solicit push credentials.
