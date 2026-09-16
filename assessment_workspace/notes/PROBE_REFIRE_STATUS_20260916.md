READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PROBE_REFIRE_STATUS_20260916.md · post-credential-drop probe re-fire attempt · 2026-09-16T~19:15Z

**Origin.** Owner directive at compaction handoff (verbatim): *"Probe re-fire with updated binds: CD/Visitors → new MySQL endpoints → NAS audio shares → radio → transcription. PASSes fold into census supplement + unblock banked lanes."*

**Result.** Zero probes fired; four blocked, one already-successful (Huawei OBS). Detail below. **Absence is a finding per SO §1** — surfaced rather than silently degraded.

---

## §1 · Probe class matrix

| # | Target | Access pattern | From-disk bind state | This-shift result | Blocker source |
|--:|---|---|---|---|---|
| 1 | Huawei OBS `google-transcripts` | direct-from-pod via SDK · env-injected AK/SK | huawei_credentials.csv present (F.1 flags 2nd absent · this file alone sufficient for validation) | ✅ **PASS** · status 200 · 1+ objects in bucket · endpoint `obs.af-south-1.myhuaweicloud.com` confirmed · receipt at `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json` | none |
| 2 | CD MySQL `159.138.164.103:3306` | from JUMP (SG allow-list scoped to `159.138.173.250`) | admin_bind JSON UNCHANGED (sha256 `a7a616be...` matches ADMIN_BINDS §A pin) | ⛔ **BLOCKED** · JUMP path SEC-HALTED pending root-pw rotation (SEC-2026-09-15-06) · direct-from-pod would fail on SG | JUMP root pw rotation pending (owner-side) |
| 3 | Visitors MySQL `110.238.75.83:3306` | from JUMP (same SG scoping) | admin_bind JSON UNCHANGED | ⛔ **BLOCKED** · same JUMP-halt as row 2 | JUMP root pw rotation pending |
| 4 | NAS audio shares (`10.10.55.x` subnet) | via JUMP-to-internal-subnet route | no bind on disk (INBOUND-BIND-PENDING per ADMIN_BINDS §B) | ⛔ **BLOCKED** · admin has not delivered `10.10.55.x` IP-set as of last drop | admin-side IP-set delivery pending |
| 5 | Radio subnet | via JUMP-to-internal-subnet route | no bind on disk | ⛔ **BLOCKED** · same as row 4 | admin-side IP-set delivery pending |
| 6 | Transcription server | via JUMP-to-internal-host | no bind on disk (SEC-BIND-01 per ADMIN_BINDS §C) | ⛔ **BLOCKED** · owner drop-in pending for host + creds | owner-side drop-in pending |

**Aggregate:** 1 PASS · 5 BLOCKED · 0 FAIL · 0 attempted-and-network-failed (no wire-time on any blocked target).

---

## §2 · SEC-HALT preservation on rows 2–3

The SEC halt (JUMP root pw leaked to agent-tool STDOUT via bad `sed` redaction · SEC-2026-09-15-06) is UNCHANGED at boot ritual: NEXT pin explicit "SEC HALT probes NOTE-SKIPPED pending JUMP rotation." Rows 2–3 preserve that halt disposition; this-shift ingestion **did not** land a JUMP rotation, so the halt stands.

Rotation-land or explicit-owner-order-with-opt-in remain the two unlocks per ADMIN_BINDS §D + owner ruling 2026-09-16T~08:10Z verbatim: *"probe-class distinction preserved (SEC-suspended JUMP-path probes NOTE-SKIPPED · mysql-path CD/Visitors probes fire only on rotation-land or explicit owner order with `--allow-csv-custody` opt-in)."*

The this-shift owner directive ("probe re-fire ... CD/Visitors → new MySQL endpoints") does not carry the `--allow-csv-custody` opt-in token, so the mysql-path probe under the JUMP halt is **not this-shift-fireable** without explicit owner opt-in. Surface and hold.

---

## §3 · What DID land this-shift

- **Huawei OBS bounded validation ✅** — full-network round-trip · zero AK/SK bytes crossed stdout · zero object keys crossed stdout · sha-prefixed shape metadata only. Receipt: `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json`.
- **Credential-drop manifest** ✅ — 12 custody files pinned · bind-delta authored. `phase0/credential_drop_manifests/20260916T1910Z_drop_manifest.json` + `notes/CREDENTIAL_DROP_BIND_DELTA_20260916.md`.

## §4 · What did NOT land + why

- **New MySQL endpoints:** no new endpoint appears in the on-disk custody set. Existing binds (CD `159.138.164.103:3306` · Visitors `110.238.75.83:3306`) are recorded in ADMIN_BINDS §A and remain UNCHANGED per bind-delta reconciliation. If the owner has "new MySQL endpoints" not yet on-disk, they need to land on the pod filesystem before this-shift probe class can activate.
- **NAS audio shares · radio · transcription:** three admin/owner-side inputs still pending per ADMIN_BINDS §B/§C. No advance possible without the missing bind(s).

---

## §5 · Next actions per §A pre-declared dependency-order walk

W8 tier-lift ✅ (this-shift · 4419) → **CP-M7-W9-UPGRADE-1** (Path B `corpus_deliverable_v1` upgrade shape · newly-unblocked by Ruling #5's `transfer_basis=derivative-only`) → M6 SEAL → CP-M8-CSD-1 → M8 SEAL + OVERALL BUILD STATUS.

Probe-class advance is BLOCKED-on-owner/admin-inputs (JUMP rotation · new endpoints · IP-set · transcription drop). Continue seal walk while waiting.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
