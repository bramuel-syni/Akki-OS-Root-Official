READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# AUTONOMOUS RUN PLAN · toward Akki v1.0 · post-CHUNK-1-close · 2026-09-18

**Status:** ACTIVE · standing autonomous authority in force per owner ruling 2026-09-18 Item 3.
**Anchor plan (unchanged, still authoritative for milestone-internal detail):** `notes/NEXT_MILESTONES_PLAN_20260917.md` (revised 2026-09-17T~20:30Z).
**Overlay purpose:** apply 2026-09-18 rulings + CP-M11-GATE-RELEASE state + CHUNK-1 seal; consolidate the pre-run OWNER-QUESTIONS checklist per POST-SPRINT-QUEUE Q2 (owner directive 2026-09-18).
**Not a rewrite of the anchor plan.** A second layer above `NEXT_MILESTONES_PLAN_20260917.md` would be D5 meta-spiral (Canon 7 §47). If a line here contradicts the anchor plan or an owner ruling, the source wins and this file is corrected at the next R-6 boundary.

**Byte-identical downloadable copy:** not required (Q2 is a state-master-only artefact per NEXT.md queue definition). If a future ruling elevates it to a boot-relevant artefact, R-6 companion regen kicks in.

---

## 0 · What changed since the anchor plan (2026-09-17 → 2026-09-18)

| Field | 2026-09-17 anchor | 2026-09-18 state |
|---|---|---|
| Ratchet floor | 4,814 | **4,826** (bumped at CP-M11-GATE-RELEASE Commit-A `4132e72` · +12 tests) |
| Master HEAD (state) | pre-Q1/Q2 landings | **`dce5b867`** (CHUNK-1-CLOSE Commit-C fixup) → this file lands the next Commit-B on top |
| Track-a HEAD (code) | `71faac1` | **`4132e72`** (CP-M11-GATE-RELEASE Commit-A) |
| M11 Tension (a) | ⏳ pending owner | ✅ **Option C** — thin adapter layer (owner ruling 2026-09-17T~15:45Z; SO §3.8 amended in place) |
| M11 Tension (b) | ⏳ pending owner | ✅ **Option α** — technical reading of "zero closed enum type" (owner ruling 2026-09-17; SO §3.10 amended) |
| M11-W1 P3 (Tension-a ruling banked) | ⏳ pending | ✅ satisfied |
| M11-W1 P4 (Tension-b ruling banked) | ⏳ pending | ✅ satisfied |
| M11-W1 P5 (SO §3.8 / §3.10 amended) | ⏳ pending | ✅ satisfied |
| T-c sequencing (schema/AST/P-15 before M11) | pending owner | ✅ **α · schema-first, caller-flip at M12b-W1** — owner ruling 2026-09-18 Item 4 |
| D-16..D-19 banked FIXED | pending | ✅ done at CP-M11-GATE-RELEASE |
| Watch contract schemas landed | pending | ✅ `contracts/watch_action_class.schema.json` + `contracts/watch_verdict.schema.json` at track-a `4132e72` |
| AST + P-15 green | pending | ✅ 6 tests (schema) + 6 tests (D.6 `canon_ref`) all green |
| Ledger drift note | not present | banked — `STATE/NEXT.md` carries a stale `Ratchet floor: 2692` line from a legacy WPW section (operative 4826 per `baseline_failures.json`) |
| Standing autonomous authority | not granted | ✅ granted through **Q1 → Q2 → M11-W1 → M12b-W1** (owner ruling 2026-09-18 Item 3) |

---

## 1 · The measure (owner ruling 2026-09-18 Item 2) — R-18 effect-15 gate conditions

Every milestone below states which of these it feeds or is deferred:

1. **G1 · SER errata landed.** ✅ closed at CP-M11-GATE-RELEASE (2026-09-18T~08:30Z).
2. **G2 · Watch contract schema · certificate · no confidence field.** ✅ closed at Commit-A `4132e72`. **Consumer waves (M11-W1 callers, M12/M12b callers) MUST target this schema from day one — never a shim.**
3. **G3 · AST rule green + P-15 green.** ✅ closed at Commit-A `4132e72`.
4. **G4 · `D.6 canon_ref` check active.** ✅ closed at Commit-A `4132e72`.
5. **G5 · D-16..D-19 banked FIXED.** ✅ closed at CP-M11-GATE-RELEASE (2026-09-18T~08:15Z).

**Status:** all five gates GREEN. The remaining sprint work is turning these GREEN gates into **functional compliance across the milestones below** — the gate release is the license to build M11+; the milestone deliverables consume the gate output.

---

## 2 · Sequenced milestone entry table

Sequence is owner-ratified per anchor plan §1: **M13-W1 → M11 → M10 → M12 → M12b → remaining M13 sub-waves → M14 ∥ M15 → M16 → M17 · frontends out-of-band**.

M13-W1 landed pre-anchor-plan; M11-W1 opens next.

| # | Milestone | Anchor §ref | Status (2026-09-18) | Waves | R-18 effect-15 gate served | Feeds v1.0 clause | Blocking pre-conditions before open |
|---|---|---|---|---:|---|---|---|
| 1 | **M13-W1** · TCB.yaml + `akki.arch` global import assertions CI | §2 | ✅ **SEALED** (pre-anchor-plan; landed at CP-M13-W1 · ratchet 4809→4814) | 1 | supports G2/G3/G4 by scaffolding TCB review | B.8 | (satisfied) |
| 2 | **M11-W1** · `akki.data` repository primitive · single Motor importer · auto-injected tenant filter | §3 | 🟢 **READY TO OPEN** — all P1-P5 satisfied at CHUNK 1 close; P6 (Mongo interim local container) can proceed under interim scope | 1 (of 10 in M11) | G2 consumer wave (new M11 callers target the new Watch schema from day one per T-c α) | B.2 (partial) · D-01 (partial) · A.4 TCB row | interim local Mongo container acceptable; hosted-tier Mongo choice can slip |
| 3 | **M11-W2..W10** · Signed `X-Akki-Context` header · control-plane collection landing · estate/connector/compute collections · retention TTL · data-plane split | §3 | ⏳ opens on M11-W1 close | 9 | G2 consumers | B.2 (full) · B.3 · B.7 · D-06 (in part) | Ed25519 signing keys (M13-W2 pull-forward option); IAM per-DB users (may be interim); Retention values (interim conservative defaults acceptable) |
| 4 | **M10** · The Ledger · hash-chained single-writer · independent verifier | §4 | ⏳ opens on M11 close (per anchor plan §1: M11 precedes M10 to avoid B.3 forbidden migration) | ~6 waves | Feeds v1.0 D.3 P-06, P-07; C.4 I-1..I-6 to L5 | B.4 · B.3 · B.7 · C.4 · D-01 (finish) | Row schema v1 ratification (blocking); interim durable log Redis-Streams-vs-Kafka choice (blocking); verifier receipt cadence (blocking) |
| 5 | **M12** · Wire M9 refusers as unroutable runtime chokepoints (T2 close) | §5 | ⏳ opens on M10 close | ~5 waves | Consumes G2 (Watch schema) at every refuser call site; consumes G4 (`canon_ref` check active) at every close | C.n I-x for M9 modules; T2 close | M9 refuser surface is sealed; the wave is thin-adapter-layer per Tension (a) Option C |
| 6 | **M12b** · Governance invariants to L5 (NEW · inserted per owner) | §6 | ⏳ opens on M12 close | ~4 waves | **G2 caller-flip lands here per T-c α (owner ruling 2026-09-18 Item 4)** · advances P-04, P-05, P-08, P-09, P-14, P-15 | C.3 · C.5 · C.6 · C.10 · C.11 · C.16 · C.19 · C.20 | Ed25519 for C.3 signed verdicts (M13-W2 pull-forward if not landed) |
| 7 | **M13-W2..W7** · remaining TCB sub-waves | §7 | ⏳ opens after M12/M12b (or pulled forward for M12b-W1 signing dep) | 6 | Cross-cutting TCB standards | B.8 (full) · D-06 · cross-cutting | KMS choice · observability vendor · Terraform state store · Ed25519 publication endpoint · SLO values · `akki-runbooks` repo · GitHub org admin |
| 8 | **M14** · Answering Service + Seam + Async + Mkondo | §8 | ⏳ opens on M13 close | ~ (per anchor plan) | Consumes G2/G3/G4 across the answering service; makes the whole Canon 7 Part II–III surface real | Canon 7 Part II–III · A.4 · B-series contract | Backend-contract stability point (recommend: after M12) — owner-desk item |
| 9 | **M15** (parallel with M14) · Documents Suite + Wizards | §9 | ⏳ opens on M13 close, runs parallel with M14 | ~ | Documents Suite discipline; wizard-frozen shape prevents execution-time discovery (Canon 7 §6) | Canon 5 Documents Suite · Canon 6 wizards | (largely independent of M14) |
| 10 | **M16** · CIF (Conditioned Ideation Faculty · C.21) — NEW BUILD · OWNER-SCOPED | §10 | ⏳ owner-scoped; opens after M14/M15 | TBD | Canon 2 (whole) — Conditioned Ideation Faculty specification | C.21 | Owner scope ruling required at M15 close before opening (per anchor plan §10 "owner-scoped") |
| 11 | **M17** · Tenant Apps + Personal Client (C.23) | §11 | ⏳ opens on M16 close | TBD | Reference application on the Integration-Console-issued-key model (Canon 7 §28) | C.23 | (largely stable spec — depends on M14 answering service being live) |
| 12 | **Frontends** (out-of-band · web/Expo specialists) | §12 | Gated at M12 completion (per anchor plan §12) | out-of-band | Renders the Integration Console + Trust Center + Watch Console (Canon 5) | Canon 5 Interface Architecture | Handoff to web/Expo specialist agents (owner-desk); backend-contract stability point |

---

## 3 · How autonomous execution proceeds (per owner ruling 2026-09-18 Items 3, 5, 7)

**Decision loop per wave** (applies to every milestone open above):

1. **Read** anchor plan §<milestone-ref> + M-<milestone> charter if it exists + latest DECISIONS.md/NEXT.md tails.
2. **Compose** the wave's grounding brief in `notes/<W-name>_grounding_brief.md` per SO §3 discipline (§A owner quote · §E wave-honest limits · §F commit protocol).
3. **Author** RED tests first per SO §3 tests-first mechanical RED. Bank drill receipt under `phase0/drill_receipts/`.
4. **Implement** additive-only per SO §3.8 (Option C thin-adapter layer for M11+ per Tension-a ruling).
5. **GREEN double-green byte-match** per SO §3.
6. **§3.3 3-commit seal**: Commit-A code (track-a) · Commit-B state (master) · Commit-C fixup (master).
7. **Update** `notes/ORCH_BOOT.md` at Commit-C fixup per R-6 boundary regen; sync `/app/frontend/public/audit/ORCH_BOOT.md` byte-identical.
8. **Report** at wave-close per owner ruling Item 7: six-item summary + gate condition advanced + ratchet + open forks.
9. **Continue** to next wave unless a stop-and-report condition (Item 5) fires.

**Stop-and-report triggers** (Item 5 · fail closed on the affected fork only; do not hold the whole build):

- RED ratchet or failed invariant.
- Canon vs lower-layer conflict discovered.
- Any proposal to amend canon, add a TCB member outside `tcb_enumeration_v1`'s method, change a Fixed decision-register entry, or carve an exception to a hard invariant.
- A new rule-vs-rule tension of the T-a/T-b kind.

**Reporting cadence** (Item 7):
- **Chunk close / wave close**: six-item summary + gate advancement + ratchet + open forks.
- **Gate release** (R-18 effect-15 gates unlocking): each of the five conditions with its evidence.
- **No other reports required.**

---

## 4 · Consolidated OWNER-QUESTIONS checklist (seeded per POST-SPRINT-QUEUE Q2 · Item 5 discipline)

**Framing discipline (Item 5).** A question here is **BLOCKING** only if opening the next wave without an answer would violate (i) canon, (ii) SO, (iii) SER, (iv) a Fixed DR entry, (v) a hard invariant, or (vi) require a T-a/T-b-class rule-vs-rule ruling. Everything else is NON-BLOCKING — the wave opens under a conservative default, the question is surfaced at the wave-close report, and forward progress continues.

### 4.1 BLOCKING questions (no default is safe; owner must rule before open)

Item-5 threshold: opening under a default would either amend canon, change a TCB member, break a hard invariant, or force a rule-tension exception.

| Q# | Gate | Question | Why blocking (Item-5 threshold) | Deferrable-to-wave? |
|---|---|---|---|---|
| **B-M10-Q1** | before **M10-W1** | **Ledger row schema v1 ratification** (16 fields per v1.0 B.4). The Ledger is TCB (`services/ledger_writer/*`); changing row schema post-open is B.3 forbidden migration territory. | B.3 forbids Ledger row-schema migrations. Committing a v1 that owner later revises = build blocked or forbidden migration. | No — must land before M10-W1 authoring RED tests. |
| **B-M10-Q2** | before **M10-W2** | **Verifier binary receipt location + cadence + SEV-1 wiring** (v1.0 D.3 P-07). Verifier is a SEPARATE process per anchor plan §4.1; wiring changes are cross-plane and hard to walk back. | Unwritable receipt path → verifier structurally impossible; SEV-1 wiring is org-level ceremony. | Partially — receipt location can slip to M10-W3 if a conservative interim default (`phase0/ledger_verifier_receipts/`) is banked, but SEV-1 wiring is fully owner. |
| **B-M12b-Q1** | before **M12b-W1** | **Ed25519 for C.3 signed verdicts** — M13-W2 pull-forward decision. C.3 signed-verdict contract shape is TCB-adjacent; caller-flip at M12b-W1 (per T-c α · owner ruling 2026-09-18 Item 4) needs the signing surface real, not stubbed. | Watch verdict schema (G2) requires signature-as-guard invariant; a stubbed signature at caller-flip would violate W2 (Canon 8 §4.2). | Partially — if signing keys aren't ready, M12b-W1 could open with `SIGNATURE_MODE=strict_stub_fail_closed`, but any real caller-flip needs live signing before wave-close. |
| **B-frontends-Q1** | before **frontends open** | **Handoff to web/Expo specialist agents** (owner-desk item). Frontends are out-of-band per anchor plan §12; without handoff, the main-agent would be authoring UI code which is outside the standing scope. | Frontend authoring by main-agent = D6 service-conflation risk (Canon 7 §47) + violation of the read-only chunk discipline for UI streams. | Yes — frontends are gated at M12 completion; question can land any time before then. |

### 4.2 NON-BLOCKING questions (conservative default is defensible; surface at wave-close)

Item-5 threshold NOT met: a conservative default holds, the wave proceeds, the question surfaces at the wave-close report for the owner to ratify or override without stopping the build.

| Q# | Gate | Question | Conservative default (this plan proposes) |
|---|---|---|---|
| N-M11-Q1 | M11-W1 | Mongo cluster provisioning (platform + hosted-tier) | **Interim: local container Mongo** with all `t_<tenant_id>` DBs sharing one instance. Meets the M11-W1 primitive surface; hosted-tier provisioning slips to M11-W4. |
| N-M11-Q2 | M11-W2 | IAM policy for per-DB users | Interim: single admin user with per-DB scope enforced by the repository primitive (SO §3.10 α · `PILOT_TENANT_KEYS` tuple). Real IAM lands at M11-W6. |
| N-M11-Q3 | M11-W2 | Pilot-tenant persistence choice (RMS · BDO: estate MongoDB or agent-embedded) | Interim: agent-embedded (matches the "single-tenant by construction" doctrine Canon 1 §1.1); estate-MongoDB deferred to M11-W9 (data-plane split). |
| N-M11-Q4 | M11-W3 | Retention values per collection audit | Interim: conservative defaults from Canon 4 §21 retention-class table (audit-90d / operational-30d / working-7d). Owner ratifies at M11-W3 close. |
| N-M11-Q5 | M11-W4 | Vector store deferral confirmed (Atlas Vector Search vs Pinecone) | Deferred — vector store is not in M11 scope per anchor plan §3. Explicitly banked as `NOT_M11_SCOPE`. |
| N-M10-Q3 | M10-W3 | Interim durable log: Redis Streams (recommended) vs Kafka | Redis Streams (recommended by anchor plan §4.5) — lower ceremony, meets append-only + single-writer contract. |
| N-M10-Q4 | M10-W6 | Backfill scope for existing filesystem Ledger rows | Interim: forward-only (no backfill); a reconciliation report at M10 close enumerates the legacy rows and their disposition. |
| N-M13-Q1 | M13-W2 | KMS choice (AWS KMS · HashiCorp Vault · HSM per D-06) | Interim: HashiCorp Vault local (matches SO §4.1 §E envelope-in-process discipline); HSM/KMS choice at M13-W3. |
| N-M13-Q2 | M13-W3 | Observability backend vendor | Interim: OpenTelemetry to local collector; vendor choice at wave-close report. |
| N-M13-Q3 | M13-W4 | Terraform state store location | Interim: S3 backend recommended by anchor plan §7; alternative at wave-close. |
| N-M13-Q4 | M13-W5 | Ed25519 receipt-signing public-key publication endpoint | Interim: `.well-known/akki/receipt-signing-keys.json` (matches Canon 7 §14 governed-fetch pattern); alternative at wave-close. |
| N-M13-Q5 | M13-W6 | SLO values per service | Interim: conservative defaults from Canon 8 §19 (detection ≤2s p95; response ≤5s p95). |
| N-M13-Q6 | M13-W7 | `akki-runbooks` repo creation | Interim: local `docs/runbooks/` directory; extract to separate repo post-M13. |
| N-M13-Q7 | M13-W7 | GitHub org admin for branch protection | Interim: local-only `.git-hooks/` scripts enforce §3.3 seal discipline; formal branch protection requires GitHub org admin (owner-desk). |
| N-M14-Q1 | M14 open | Backend-contract stability point | Recommend: after M12 (per anchor plan §12). |

### 4.3 Owner-desk items already surfaced (unchanged from anchor plan §15 · repeated for continuity)

Per anchor plan §Δ6 verbatim, these surface at every milestone-boundary report and do not gate this milestone unless flagged blocking above:

- BC tier · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 charters · D9 receipt-unify · admin binds · SEC rotations · R-17(a) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine.

### 4.4 Standing owner-only items (unchanged · never move without owner)

- **SEC-2026-09-12-01** (HF token rotation): three-step HF action + hash delta on record (SO §4.3). HF-touching waves HOLD; every other wave proceeds. Item 6 of the 2026-09-18 ruling reaffirms this.
- **T-d fixed-column CSV re-drop** (three Huawei triples): awaiting owner drop. Non-blocking for M11-W1.

---

## 5 · CHUNK 1 anomaly re-surfaced (per Item 5)

- `repos/Akki-Executive-Final/` folder exists locally and is **NOT one of the four repos** named in the problem statement. Task-B and Task-C banked this as an anomaly. **NOT currently a stop-and-report condition** — surface to owner at next milestone-boundary report and continue.

---

## 6 · Ratchet accounting for this plan

- **This file** is state-only (Q2 landing). Ratchet **unchanged 4826** (no code touched).
- **M11-W1** ratchet delta target: +N (RED tests for the repository primitive · sole-Motor-importer AST scan · M9-untouched byte-content assertions · cross-tenant refusal test · tenant-filter-auto-injection test). Concrete N banks at M11-W1 open.
- **M10-W1..W6** ratchet delta target: +M (per anchor plan §4). Concrete M banks per wave.
- **Ratchet floor monotonic-up** invariant (SO §3) preserved across every wave.

---

## 7 · Sources-win-if-drift note (per D5 meta-spiral prevention)

If any statement in this file contradicts:

- **The anchor plan** (`notes/NEXT_MILESTONES_PLAN_20260917.md`) — the anchor plan wins for milestone-internal detail.
- **STANDING_ORDERS.md** — SO wins for discipline.
- **A canon document** — canon wins for spec.
- **An owner ruling in DECISIONS.md** — the ruling wins for the specific decision it names.
- **A contract schema at `contracts/*.schema.json`** — the schema wins for the specific field it defines.

This overlay is a pointer atlas for the autonomous run, never authority in itself. Corrections land at the next R-6 boundary; this file is not edited in place — a superseded entry is annotated with SUPERSEDED-BY, and the successor is added.

---

## 8 · What this plan is deliberately not

- **Not a Chunk-3 REUSE_ASSESSMENT.md draft.** Chunk-3 opens after all four chunks are grounded.
- **Not a schedule commitment.** No dates on future waves — D7 (Canon 7 §47) forbids invented schedule/scope, and per Item 5 the autonomous plan is a decision-tree, not a Gantt chart. Wave-open triggers on pre-conditions being TRUE; wave-close triggers on tests-first RED → double-green.
- **Not an amendment to canon or SO.** Any need to amend either surfaces a stop-and-report condition (Item 5).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
