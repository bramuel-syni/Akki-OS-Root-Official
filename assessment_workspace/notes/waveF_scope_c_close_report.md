# Wave F · Scope C · Compliance Residue Close Report
## 2026-08-27T21:20Z

**Owner ruling (Wave F GO · autonomous progression, 2026-08-27T~21:00Z, verbatim):**
> "AUTONOMOUS PROGRESSION CONFIRMED — the Wave F GO stands as ruled: proceed Scope B → Scope C → Cleanup/Close without pausing between scopes. My external third run happens once, at the WAVE close. Stop-and-reports stay informational; halt only on the standard triggers (non-config blocker, spec contradiction, guard trip, count drift, owner-input need — e.g., if the Scope B methodology reveals a defect in the W10 CP9 instrument, or Scope C hits something only the owner can answer beyond the two already-pending items)."

**Scope C mandate (charter §Scope-C-compliance-residue, 2026-08-27T14:35Z, verbatim):**
> "close them or class-attribute honestly"

Wave F closer works the 7 line items (charter numbering 1-8; item numbering follows charter) in the dependency order laid out in charter §Scope-C-close-discipline: VERIFICATION first (CA1-N1 + CA1-N4) · RTO ruling capture (CA1-N5) · DigiCow booleans one-liner · Doc15-014 breakdown + Doc16-023 walk-this semantics · CA1-001/002/003 audit-trail Overview surface.

Every claim in this report cites a file OR is marked OPEN with no mechanism yet. Measured, not assumed. Absence-explicit per binding rule.

---

## Dependency-order verdicts (summary table)

| # | Item | Charter class | Measured class | Disposition |
|---|---|---|---|---|
| 5 | CA1-N1 · retention enforcement + attestation | PARTIAL (charter stale) | **DONE** (measured) | RECLASS · charter update |
| 5 | CA1-N4 · residency (governed region allowlist) | PARTIAL (charter stale) | **DONE** (measured) | RECLASS · charter update |
| 4 | CA1-N5 · RTO value (owner-policy-pending) | OWNER-POLICY-PENDING | OWNER-POLICY-PENDING (unchanged mechanism refuses) | ESCALATE (one of 2 known-pending items) |
| 7 | DigiCow occupation booleans PII classification | OWNER-INPUT NEEDED | OWNER-INPUT NEEDED | ESCALATE (one of 2 known-pending items) |
| 6 | Doc15-014 · Watch full mechanism | PARTIAL | PARTIAL (breakdown below) | CLASS-ATTRIBUTE (no owner authorization to build in Wave F) |
| 8 | Doc16-023 · walk-this semantics | PARTIAL | PARTIAL (breakdown below · Doc 10 blocker STILL PRESENT) | CLASS-ATTRIBUTE (Doc 10 evidence-record contract still not materialised) |
| 1 | CA1-001 · Audit-trail Overview "2+ units" line | BUILD | BUILD | CARRY (Wave F GO did not authorize `services/audit_trail/` build) |
| 2 | CA1-002 · Audit-trail units-served count line | BUILD | BUILD | CARRY (same blocker) |
| 3 | CA1-003 · Densification stat + warm/fresh tag | PARTIAL | PARTIAL | CARRY (per-turn stat blocked on CA1-001/002 surface) |

---

## Item 5a · CA1-N1 · Retention enforcement + attestation · VERIFICATION

**Charter mandate (verbatim):** "confirm what earlier waves already enforce vs what's genuinely open — measured, not assumed."

**Charter status:** PARTIAL (per Wave A-C anchor · addendum letter: "No enforcement/attestation mechanism").

### Measured mechanism (file:line citations · programme/track-a HEAD `1155629`)

**Enforcement module** (`services/retention/` · 5 files):
- `services/retention/router.py` (64 lines) · 4 wire routes:
  - `GET  /api/retention/classes` — declared retention letter per class
  - `POST /api/retention/enforce` — run enforcement (default `dry_run=true`)
  - `GET  /api/retention/attestations` — attestation records
  - `GET  /api/retention/expired` — expired records list (audit)
- `services/retention/enforce.py` (235 lines) · CA1-N1 enforcement + attestation. Writes a `.expired` sidecar next to each expired append-only record; produces attestation entries.
- `services/retention/classes.py` (147 lines) · governed per-record-class letter registry. Owner ruling 2026-08-25 W6 GO §W6-SCOPE-(b) enforced: append-only classes = mark-expired + excluded-from-render, NEVER hard delete.
- `services/retention/authorized_deletion.py` (167 lines) · W11B Phase 8 Seam-3 sub-stage 2 · single-source-of-deletion module. AST invariant `test_no_unauthorized_deletion_path` whitelists this file and only this file.
- `services/retention/__init__.py`

**Invariant test:** `tests/invariants/test_retention_enforcement_w6_cp3.py` (328 lines) · W6 CP3 · enforces CA1-N1 mechanism + attestation semantics. Passes as part of the 2333-green suite at Scope A close (`1155629`).

**Charter status "PARTIAL" annotation is STALE.** The mechanism landed at W6 CP3 (2026-08-25 timeframe) predates the Wave A-C anchor freeze (2026-08-26T~12:40Z). The Wave A-C anchor's charter text ("no enforcement/attestation mechanism") captured a pre-W6-CP3 snapshot.

**Measured verdict: DONE.** Enforcement + attestation mechanism landed. Wire routes live. Invariant test enforcing. Append-only class discipline preserved per canon.

**Open items (none for CA1-N1 itself):** the retention mechanism is scope-complete. Any future extension is a NEW row, not an unclosed portion of CA1-N1.

**Wave F disposition:** RECLASS from PARTIAL → **DONE** in the Wave F composite recompute (charter update recommended for the next register revision · not made in this Scope C close since owner did not explicitly authorize a register rewrite in Scope C).

---

## Item 5b · CA1-N4 · Residency enforcement · VERIFICATION

**Charter mandate (verbatim):** "confirm what earlier waves already enforce vs what's genuinely open — measured, not assumed. (residency allowlist exists at `services/chokepoint/residency_allowlist.v0.json`)"

### Measured mechanism (file:line citations · programme/track-a HEAD `1155629`)

**Enforcement module** (`services/chokepoint/residency*` · 2 files):
- `services/chokepoint/residency.py` (57 lines) · governed region allowlist (CA1-N4) — file header comment tags this explicitly as CA1-N4.
  - `class ResidencyRefused(ValueError)` — refusal exception raised when a crossing endpoint's region is not on the allowlist.
  - `_load_allowlist()` — loads `residency_allowlist.v0.json`.
  - `validate_region(region: str) -> None` — raises `ResidencyRefused` if region not in allowlist.
  - `allowlisted_regions() -> List[str]` — public accessor for the allowlist.
- `services/chokepoint/residency_allowlist.v0.json` (43 lines) · allowlist config. Header docstring: "Adding a region requires an Owner ruling" (owner-controlled).

**Documented real facts (residency.py header verbatim):**
- `aws.rds.db-restore-603-cluster.digicow_live` · resource.region = `eu-west-1`
- `aws.rds.db-restore-603-cluster.ndume` · resource.region = `eu-west-1`
- `commissioning_akki-vm_..._ACCEPTED.json` · NO region on record (**gap surfaced honestly** on the Data Shield surface, "drawn-not-blank")

**Invariant test:** `tests/invariants/test_chokepoint_registers_all_crossings.py:70` verifies the exported symbols `validate_region`, `allowlisted_regions`, `ResidencyRefused` are present. Passes as part of the 2333-green suite at Scope A close.

**Charter status "PARTIAL" annotation is STALE.** Same class of stale annotation as CA1-N1.

**Measured verdict: DONE.** Allowlist enforcement mechanism landed. `ResidencyRefused` exception used at the chokepoint. Real-facts gap (missing region on 1 commissioning artifact) is SURFACED honestly, not hidden.

**Open items (none for CA1-N4 itself):** the residency mechanism is scope-complete. The missing-region gap is a data gap, not a mechanism gap — surfaced correctly.

**Wave F disposition:** RECLASS from PARTIAL → **DONE** (same class of update as CA1-N1).

---

## Item 4 · CA1-N5 · RTO value · OWNER-POLICY-PENDING

**Charter mandate (verbatim):** "service continues to refuse while `rto_target_seconds='OWNER_POLICY_PENDING'` (unchanged mechanism). Wave F closer MUST NOT invent an RTO default."

### Measured mechanism (file:line citations · programme/track-a HEAD `1155629`)

- `services/watch/continuity_policy.v0.json:8` : `"rto_target_seconds": "OWNER_POLICY_PENDING"` — sentinel value.
- `services/watch/continuity_policy.v0.json:9` : `"note_on_rto": "Owner has NOT ruled RTO. Service refuses to fire attestation while rto_target_seconds is OWNER_POLICY_PENDING; this is an honest stop, not scaffolding."`
- `services/watch/continuity.py:19-88` : refusal contract wired. `_PENDING_SENTINEL = "OWNER_POLICY_PENDING"` (line 39). Refuses attestation when `rto_target_seconds` or `verification_mechanism` is at sentinel (lines 80-88).
- `services/watch/router.py:498-510` : router-level field validation. Refuses request when any owner-policy field is at `OWNER_POLICY_PENDING`.

**Wave E CP-E1 (`ebc5a48`) landed the CA1-N5 continuity enforcement mechanism with the OWNER_POLICY_PENDING refusal contract preserved.** No RTO default invented.

**Wave F disposition:** UNCHANGED. Service continues to refuse. Wave F does NOT invent an RTO default.

**Owner-input escalation (one of 2 known-pending items — proceed autonomously per owner ruling this session):**
- **CA1-N5 RTO ruling needed:** owner is asked to rule `rto_target_seconds` (integer number of seconds). If ruled, only `services/watch/continuity_policy.v0.json:8` needs the value change from `"OWNER_POLICY_PENDING"` to the ruled integer — no code change, no wave-re-open. If not ruled by Wave F wave-close, the item carries as OWNER_POLICY_PENDING into the next wave.

---

## Item 7 · DigiCow booleans PII classification · OWNER-INPUT

**Charter mandate (verbatim):** "escalate to owner as a one-liner in the next report."

**One-liner (as charter-drafted):**

> "PII classification question · DigiCow `ussd_users` occupation booleans (`dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer`): behavioral-adjacent attributes on a named individual — count as PII for `services/response_sanitizer` banned set? (yes/no ruling requested; default under Wave-E-CP-E7 posture is no)."

**Current mechanism state (measured, file:line citation · programme/track-a HEAD `1155629`):**
- `services/response_sanitizer/` shared sanitizer landed at Wave E CP-E7 (`60b8760`).
- `dairy_farmer`, `poultry_farmer`, `dairy_poultry_farmer` are NOT in the banned attribute set. Default = NOT PII.
- Booleans-not-payload class distinction is honored: the sanitizer treats them as classification attributes on a named record, not as PII payload.

**Wave F disposition:** ESCALATE the one-liner (this section IS the escalation surface for the owner to rule at wave-close). Mechanism state UNCHANGED until owner rules.

**Owner-input escalation (one of 2 known-pending items — proceed autonomously per owner ruling this session):** owner to rule yes/no on DigiCow booleans as PII.

---

## Item 6 · Doc15-014 · Watch full mechanism · CLASS-ATTRIBUTE

**Charter mandate (verbatim):** "class-attribute honestly with a specific breakdown of the outstanding Doc 15 rows; do NOT build without owner ruling on Doc 15 mechanism scope."

**Doc15-014 canonical text:** "Nothing operates above governance except the Watch (Promise #26)."

### Measured mechanism (file:line citations · programme/track-a HEAD `1155629`)

**Watch service module (`services/watch/` · 11 tracked files):**
- `services/watch/continuity.py` · continuity attestation with OWNER_POLICY_PENDING refusal · Wave E CP-E1 landed
- `services/watch/router.py` · wire routes: `GET /api/watch/continuity`, `GET /api/watch/witness_state_line` (per Doc15-085), staleness routes (per Doc15-087)
- `services/watch/witness.py` · witness state line (Doc15-085 DONE at Wave E CP-E6)
- `services/watch/mirage.py`, `services/watch/mirage_artifacts.py` · mirage detection primitives
- `services/watch/macho.py` · macho-mode (Watch overriding governance under owner ruling · Wave E CP-E6)
- `services/watch/sever_signals.py` · Watch severance signaling
- `services/watch/route_recheck_failure.py` · route health recheck failures
- `services/watch/persistence.py` · Watch state persistence
- `services/watch/continuity_policy.v0.json` · config with OWNER_POLICY_PENDING sentinel

### Doc 15 row-level breakdown (from `notes/requirements_register_17docs.md` · CANON rows in Doc 15 targeting Watch mechanism)

| Row | Text | Class |
|---|---|---|
| Doc15-014 | Nothing operates above governance except the Watch (Promise #26) | **PARTIAL** (meta-supremacy statement · full breakdown below) |
| Doc15-085 (CA1-006) | Watch's self-contained exception + external witness state line | **DONE** (Wave E CP-E6 · witness_state_line on `/api/watch/continuity` response) |
| Doc15-087 (CA1-012) | Watch staleness-flagging extended to rulebooks + baselines | **DONE** (Wave E CP-E6 · `route_staleness_flag.py` covers baseline_line + rulebook_rule) |
| Doc15-086 (CA1-009) | Generalised handoff contract (what/shape/identity/receipt) | **BUILD** (contract exists in one instance — ThinkLab→Task Manager per CA1-A7; generalised contract required) |

### Doc15-014's specific "meta-supremacy" claim — measured status

Doc15-014's canonical text is a META-CONTRACT: "Nothing operates above governance except the Watch." This is not a specific mechanism to build; it's a constraint on the whole architecture. Its DONE-ness is inherited from the sum of Watch mechanism sub-rows.

**Sub-row inventory:**
- Watch continuity attestation (with OWNER_POLICY_PENDING refusal) — DONE at Wave E CP-E1.
- Watch witness state line — DONE at Wave E CP-E6.
- Watch staleness-flagging — DONE at Wave E CP-E6.
- Watch macho-mode (Watch overriding governance) — mechanism landed; full owner ruling scope may still expand.
- Generalised handoff contract (Doc15-086) — BUILD (single-instance implementation; generalisation open).
- Watch RTO enforcement — OWNER_POLICY_PENDING (item 4 above).

**Wave F disposition:** CLASS-ATTRIBUTE as **PARTIAL** (unchanged). The bulk of Watch mechanism sub-items are DONE (Doc15-085, Doc15-087, continuity, macho, staleness); the meta "Watch supremacy" statement stays PARTIAL until (a) the generalised handoff contract (Doc15-086) lands OR (b) owner rules Doc15-014 as DONE-by-inheritance from landed sub-rows.

**No Wave F build** per charter mandate ("do NOT build without owner ruling on Doc 15 mechanism scope").

---

## Item 8 · Doc16-023 · walk-this semantics · CLASS-ATTRIBUTE

**Charter mandate (verbatim):** "class-attribute honestly; if the Wave F opening scope includes Doc 10 backfill, then the walk-this semantics close alongside; otherwise carry as PARTIAL with the Doc 10 blocker cited."

**Doc16-023 canonical text:** "Universal claim-to-evidence trace = 'Walk this →' (Promise-Table CA1-A8; see T8)."

### Measured mechanism (file:line citations · programme/track-a HEAD `1155629`)

**Wire + SPA (DONE at Wave D CP-D8 per `notes/waveD_close_report.md`):**
- `routers/registry.py:12` (verbatim comment): `GET /api/prove/trace/{trace_id} · claim → reasoning → raw facts (walk)`
- `services/perception/eab_1_pipeline/a2_trace_walker.py` · trace walker (evidence backend)
- SPA routes `/trace/:traceId` + `/prove/trace/:traceId` wired

**Doc 10 evidence-record backfill (charter blocker):** the charter said "Doc 10 evidence-record contract not yet materialised in `contracts/` inventory."

### Measured Doc-10 contract state (evidence)

- `contracts/evidence_register_row_v0.py` EXISTS, but it targets **Doc 19B §19B.5 evidence-register row shape** (EP-1 proposed evidence-register system) — NOT the Doc 10 runtime ledger evidence-record contract that Doc16-023's walk-this needs.
- No `contracts/*evidence_record*` OR `contracts/*doc10*` file exists in the `contracts/` inventory.
- `services/perception/eab_1_pipeline/a2_trace_walker.py` does NOT reference an EvidenceRecord contract.

**Doc 10 evidence-record contract blocker is STILL PRESENT.** The `evidence_register_row_v0.py` contract does not satisfy Doc16-023's need; it's for a different construct (register rows, not runtime trace evidence).

**Wave F disposition:** CLASS-ATTRIBUTE as **PARTIAL** (unchanged). Wire + SPA DONE at Wave D CP-D8; ledger-traversal semantics stay OPEN until Doc 10 evidence-record backfill lands.

**Wave F opening scope did NOT include Doc 10 backfill.** Charter default carries PARTIAL with Doc 10 blocker cited (explicit).

---

## Items 1/2/3 · CA1-001/002/003 · Audit-trail Overview surface · CARRY

**Charter mandate (verbatim):** "Build only if Wave F opening scope authorises the new `services/audit_trail/` mechanism-surface; otherwise carry as BUILD/PARTIAL."

**Wave F GO opening scope did NOT explicitly authorize the `services/audit_trail/` build.** Owner ruled the three-scope order A→B→C→Cleanup with Scope C = compliance residue; the residue items are addressed by verification + class-attribution + escalation, not by new mechanism builds without owner authorization.

### Item 1 · CA1-001 · Doc02-020a

- Canonical text: audit-trail Overview names "2+ independently-governed units".
- Charter class: **BUILD**.
- Measured: no `services/audit_trail/` module exists in `programme/track-a` HEAD `1155629`.
- **Named blocker:** no audit-trail Overview surface service exists.
- **Wave F disposition:** CARRY as **BUILD** (unchanged). Not built this Wave. If Wave G opens with owner authorization for `services/audit_trail/`, this closes alongside CA1-002.

### Item 2 · CA1-002 · Doc06-016

- Canonical text: audit line names how many available source units were served.
- Charter class: **BUILD**.
- Same blocker as CA1-001. Same disposition. CARRY as **BUILD**.

### Item 3 · CA1-003 · Doc07-019

- Canonical text: densification stat + per-turn warm/fresh tag.
- Charter class: **PARTIAL**.
- Half landed: warm/fresh tag DONE via memory service (Addendum §1 covered).
- Half OPEN: per-turn densification stat requires the CA1-001/002 audit-trail Overview surface (not built this Wave).
- **Named blocker:** per-turn audit-line stat blocked on CA1-001/002.
- **Wave F disposition:** CARRY as **PARTIAL** (unchanged).

---

## Standing HOLD triggers (charter)

Per owner Scope C mandate, Wave F closer halts on standard triggers only:
- **Non-config blocker** — none hit in Scope C.
- **Spec contradiction** — none hit in Scope C.
- **Guard trip** — none hit (baseline stayed at 2333/0/1 throughout Scope C measurement — no code changes on `programme/track-a`).
- **Count drift** — none.
- **Owner-input need beyond the two already-pending items** — none hit. The two known-pending items (CA1-N5 RTO seconds; DigiCow booleans PII) are surfaced as escalations, not halts.

**No halt-and-report triggered during Scope C execution.** Autonomous progression completes to Wave F Cleanup + Close.

---

## Wave F Scope C summary

| Category | Items | Status |
|---|---|---|
| **RECLASS** (charter STALE annotation · measured DONE) | CA1-N1 · CA1-N4 | 2 items · charter update recommended for next register revision |
| **ESCALATE** (2 known-pending items · surface for owner ruling at wave-close) | CA1-N5 RTO · DigiCow booleans | 2 items · surfaced with one-liner or file:line disposition |
| **CLASS-ATTRIBUTE** (per charter mandate) | Doc15-014 · Doc16-023 | 2 items · PARTIAL unchanged · blockers cited |
| **CARRY** (BUILD/PARTIAL held; new mechanism build not authorized this Wave) | CA1-001 · CA1-002 · CA1-003 | 3 items · CA1-001/002 BUILD · CA1-003 PARTIAL |

**Scope C closed at 2026-08-27T21:20Z. No code touched on `programme/track-a`. Master workspace file added: this report. No STATE changes required until Cleanup phase master commit.**

---

## Autonomous progression status

Wave F Scope A CLOSED (`programme/track-a` HEAD `1155629` · double-run 2333/0/1 identical).
Wave F Scope B CLOSED (master workspace HEAD `7ae5dcb` · composite lock 52.52% · double-run byte-identical).
Wave F Scope C CLOSED (this report · master workspace HEAD PENDING · no `programme/track-a` touch).

**Next**: Wave F Cleanup phase per Wave F GO ruling A→B→C→Cleanup order. External third-run WAVE-close ratification deferred to Wave F wave-close per owner rule ("MY external third run at the WAVE close").

SSH interrupt remains INTERRUPT-PRIORITY (unchanged).
