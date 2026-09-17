READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ORCH_BOOT.md — Anti-forget boot manifest

**Owner ruling (verbatim, 2026-09-17T~20:45Z, banked in STATE/DECISIONS.md):**

> "Add a machine-checkable boot manifest whose ratchet field can never
>  silently drift, and whose HEAD fields cannot race with the §3.3 commit
>  protocol.  This file MUST be regenerated at every seal boundary (R-6)."

This file is the CANONICAL boot state for the orchestrator.  A byte-identical
downloadable copy is served at `/app/frontend/public/audit/ORCH_BOOT.md`.

The invariant test at
`repos/Extraction-Akki/backend/tests/invariants/test_orch_boot.py` enforces:

1. Both copies exist and are byte-identical.
2. `ratchet.passed_floor` equals live `baseline_failures.json.passed_floor`
   (drift-and-burn priority guard · always-on hard assertion).
3. `ratchet.baseline_failures_sha256` equals live sha256 of that file
   (paired byte-fingerprint · always-on hard assertion).
4. `heads_last_sealed.*.head` are well-formed 40-hex AND banked in
   STATE/DECISIONS.md or STATE/NEXT.md (last-sealed HEADs, NOT live
   `git rev-parse HEAD` — freshness is enforced by R-6 boundary
   regeneration, not by an always-on equality-to-live-HEAD test, per
   owner ruling refinement to avoid racing §3.3 Commit-A/B/C ordering).

Regenerate this file (both copies, byte-identically) at every §3.3
Commit-C fixup, at every owner ruling that mutates ratchet / HEADs /
STATE files, and on any boot ritual that detects drift.

---

```yaml
schema_version: 1
generated_at_utc: 2026-09-17T15:48:00Z
generator: main-agent Autopilot (Owner-Ruling-2026-09-17T~15:45Z · state-only 2-commit · R-6 boundary regen at Commit-C fixup)
regeneration_reason: r6-boundary-regen-at-owner-ruling-2026-09-17T15-45Z-commit-c-fixup-banking-master-commit-b-sha

ratchet:
  passed_floor: 4814
  counts_at_baseline_passed: 4814
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: 06050dbf1298037c993a59add0235b75e13cf5b90e4b694a46a9d54a15275237

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: 31908fedb5e7afb5a1b46674dff3bdc821e67874
    sealed_at_utc: 2026-09-17T15:47:00Z
    seal_kind: "OWNER RULING 2026-09-17T~15:45Z · state Commit-B · Tension (a)=Option C + Tension (b)=Option α + SO §3.8/§3.10 verbatim + RMS ESTATE BRIEF + Watch-vocabulary finding (Commit-C fixup banks this SHA)"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 71faac1cd9c5bd6fe1db1ec6ca340485a34c251a
    sealed_at_utc: 2026-09-17T13:42:00Z
    seal_kind: "CP-M13W1 · Commit-A · TCB.yaml + tools/akki_arch/* + test_akki_arch_import_assertions.py + ratchet 4810 -> 4814 (+4)"

boot_sequence:
  - Read STATE/STANDING_ORDERS.md end-to-end.
  - Read last 300 lines of STATE/DECISIONS.md and all of STATE/NEXT.md.
  - Verify HEADs against `git rev-parse` for informational purposes only — this file's HEADs are LAST-SEALED, not live.
  - Verify ratchet floor + baseline sha256 against baseline_failures.json (hard-asserted by test_orch_boot.py).
  - Resume the in-flight work order at the top of STATE/NEXT.md.

regeneration_triggers_r6:
  - After Commit-C fixup of every §3.3 3-commit seal (CP boundary).
  - After any owner ruling that mutates ratchet, HEADs, or STATE files.
  - On every boot ritual when STANDING_ORDERS §1 boot verification detects drift.

authoritative_downloadable_copy_path: /app/frontend/public/audit/ORCH_BOOT.md
```

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
