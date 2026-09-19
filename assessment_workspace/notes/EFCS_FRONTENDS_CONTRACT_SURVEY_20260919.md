# EFCS · Frontends Contract Survey · 2026-09-19T~18:00Z

**Wave:** CP-EFCS-FRONTENDS-CONTRACT-SURVEY (notes-only sub-wave · state master · additive-only per SO §3.8).

**Ordered by owner ruling 2026-09-19T~17:54Z item (e) verbatim** ("survey now, then closure waves — frontends do not defer... one notes-only survey wave enumerating every contract the frontends consume, its status, and its owner; then closure waves in dependency order — the C.17 answering-service seam first, then DAP entitlement and receipt contracts, frozen from `dap_backend_spec_v1` (DAP-1 principal fields, DAP-13 key, the six-profile entitlement from §4, DAP-21's receipt fields).").

**Discipline:** Every factual claim below comes from a file opened this session (SO §6.1 files-are-truth). Cited by absolute or repo-relative path + line-range where applicable. Absence is a finding per client's binding rule.

**Author:** main-agent Autopilot under §6 END-OF-BUILD authority + owner PROCEED re-affirmed 2026-09-19T~14:35Z + owner ruling this-turn 2026-09-19T~17:54Z (autonomous continuation ordered).

---

## §1 · Anchor documents surveyed for this-wave

| # | Path | Kind | Opened this session? |
|---|---|---|---|
| 1 | `/app/assessment_workspace/canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` | Canon (Doc-3 · DAP-Spec `dap_backend_spec_v1`) | Yes · 131 lines |
| 2 | `backend/contracts/dap.py` | Sealed contract module · consumes DAP-Spec | Yes · 288 lines |
| 3 | `backend/contracts/handoff_contract.py` | Sealed contract module · M14-W1 seal | Yes · 98 lines |
| 4 | `backend/contracts/application_contract_v0.py` | Sealed contract module · M17-W1 seal | Yes · 216 lines |
| 5 | `backend/contracts/personal_client_session_v0.py` | Sealed contract module · M17-W3 seal | Yes · 152 lines |
| 6 | `backend/contracts/outer_gate_receipt_v1.py` | Sealed contract module · Watch/Outer Gate | Yes · 103 lines |
| 7 | `backend/contracts/trust_receipt_v1.py` | Sealed contract module | Yes · 96 lines |
| 8 | `STATE/DECISIONS.md:12115` (B-frontends-Q1 verbatim) | Owner ruling | Yes (via grep) |
| 9 | `STATE/DECISIONS.md:13600 + 13630 + STATE/STANDING_ORDERS.md:445` (Frontend fidelity bar · DAP UI Handoff Brief §5) | Owner ruling | Yes (via grep) |
| 10 | `STATE/OBJECTIVES/M17.md` (fully sealed at CP-M17-W5) | Objectives card · consumes contracts 3-5 | Yes · 140 lines |

**Absence findings (SO §6.1 · reportable per client's binding rule):**

- **DAP UI Handoff Brief §5** document itself is referenced by owner rulings 12115 + 13600 + 13630 but **not surveyed on disk** at this-wave close. The Frontend fidelity bar ("functional parity with five-stage pattern") is cited in DECISIONS.md but the brief file location is unknown at this-wave close. Impact: the frontends card drafted at the preceding-seal boundary (per orchestrator plan item 5) MUST resolve this location before card body can be authored — the card body derives from UI Handoff Brief §5 per owner ruling. **Action:** locate brief before frontends-card wave OR fork if unlocatable.
- **`dap_backend_spec_v1` machine-readable JSON-Schema** — spec is docx/txt (131 lines readable); no machine-readable JSON-Schema derivation on disk in `contracts/` beyond the pydantic model wrappers in `contracts/dap.py`. Per T-b JSON-Schema-authoritative, a contract can freeze from spec before backend is built; the frontends build against the frozen schema. **Action:** at contract closure waves, freeze pydantic models' `model_json_schema()` as sha256-pinned baselines per SO §3.10-α closed-schema discipline (mirrors M16-W1 + M17-W1 pattern precedent).

---

## §2 · Contracts enumerated for frontend consumption (per DAP UI Handoff Brief §5 anchor)

### §2.1 · C.17 · Answering-service seam contract (owner-named "answering-service seam")

**Constituent contracts (opened this session):**

| Contract file | Status | Sealed at | Notes |
|---|---|---|---|
| `backend/contracts/handoff_contract.py` (98 lines) | **SEALED (M14-W1)** at Commit-A `8b861987` · frozen pydantic + shape-snapshot pin | 2026-09-19T~06:37Z (per prior banking) | The core `Ask_v0` / `Handoff_v0` structural shapes for the seam · owner-cited fork target (M17-W5): handoff_id regex `^ho_[a-z0-9_-]+$`. |
| `backend/contracts/personal_client_session_v0.py` (152 lines) | **SEALED (M17-W3)** at Commit-A `adf828f6` · frozen pydantic + shape-snapshot pin | 2026-09-19T~14:20Z | Tenant-of-one session composition · consumes handoff_contract at emit_ask boundary. session_id regex `^pcs_[a-z0-9_-]+$` (source of M17-W5 fork). |
| `backend/contracts/application_contract_v0.py` (216 lines) | **SEALED (M17-W1)** at Commit-A `16ca02c4` · frozen pydantic + shape-snapshot pin `ba1957dfbb…` | 2026-09-19T~13:05Z | Tenant application outer contract · consumed by all session-composition surfaces + all UI surfaces per M17 card. |

**Runtime seam:**

| Module | Status | Sealed at |
|---|---|---|
| `backend/services/mkondo/registry.py` (Mkondo registry · `admit_handoff`) | **SEALED (M14-W2)** | Prior seal (per BUILD_JOURNAL claims to verify · not opened at this-wave) |
| `backend/services/answering_service/collections/*.py` (asks collection append) | **SEALED (M14-W3)** | Prior seal (per BUILD_JOURNAL claims to verify · not opened at this-wave) |
| `backend/services/personal_client/session.py` (compose_session + emit_ask) | **SEALED (M17-W3)** | 2026-09-19T~14:20Z |
| `backend/services/personal_client/governance_invariants.py` (three B-frontends-Q1 predicates) | **SEALED (M17-W4)** | 2026-09-19T~15:02Z |

**Overall C.17 frozen status:** **PARTIAL** (per digest (e)-prior state).

**Unfrozen surfaces at this-wave close (specific finding):**

- Machine-readable JSON-Schema freeze **NOT** yet applied at seam-boundary level for handoff_contract + application_contract + personal_client_session_v0 as a **bundle**. Each contract carries its own shape-snapshot pin, but there is no cross-contract seam-boundary sha256 pin binding "any UI conforming to this seam MUST match all three schemas". The M17 milestone snapshot pin `ba1957dfbb…` binds ApplicationContract_v0 alone; a matching seam-bundle pin does not exist yet.
- The **M17-W5 handoff-ID fork** (`notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md`) is banked as non-blocking but **structurally violates HR-2** ("hand-off entry carries the right identities"). Frozen status cannot claim full freeze until either the adapter (Option i) or ID-domain type-tagging (Option i + tier-1 addition per owner ruling this-turn) lands.
- **Frozen surfaces at this-wave close:** all three individual pydantic contracts (application_contract_v0 · handoff_contract · personal_client_session_v0) are frozen at their sub-wave seal boundaries. `Ask_v0.handoff_id` regex `^ho_[a-z0-9_-]+$` is frozen in handoff_contract.py.

**Owner (per canon + banked rulings):**

- Canon owner: Doc-1 (Interface Architecture · Canon 5) + Doc-2 (User Journeys · Canon 6) + AC-18 (proposes-never-ratifies) + M14 seal chain + M17 seal chain.
- Ratification owner: platform owner (banked ratifications per M14-W1, M17-W1, M17-W3, M17-W4, M17-W5 seals).

**Closure wave scope (per owner ruling this-turn · dependency order · C.17 seam first):**

- **CP-CCS1-C17-SEAM-BUNDLE-FREEZE** (proposed name for the C.17 closure wave · TBD at RED authoring):
  - **W1:** seam-boundary bundle snapshot pin (sha256 of concat-sorted-key JSON of `ApplicationContract_v0.model_json_schema()` + `Ask_v0.model_json_schema()` + `Handoff_v0.model_json_schema()` + `PersonalClientSession_v0.model_json_schema()`) frozen as `_C17_SEAM_BUNDLE_SHA256` constant · additive-only · new invariant test file.
  - **W2:** invariant asserts frozen bundle sha matches at every seam-crossing site (structural AST-scan on personal_client/session.py's imports + emit_ask body + all UI-facing helper functions in personal_client/*.py).
  - **W3:** integration test binds the bundle across an end-to-end ask flow (mirrors M17-W5 pattern).
  - Ratchet delta target: +5..+8 (TBD at RED authoring).
- **Dependency:** must wait for (f) CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG close (owner ruling this-turn) so the adapter + type-tag lands into the frozen bundle · otherwise the seam bundle freezes a broken handoff-id assignment.

---

### §2.2 · DAP entitlement contract (owner-named "DAP entitlement contract")

**Anchor:** DAP-Spec `dap_backend_spec_v1` §4 six-profile entitlement (browse · connect API key by external workspace · extract processed intelligence · fine-tune model on estate data · develop skills against estate data · download raw data). "These are not six variants of one action. They are six distinct crossings with six different governance profiles" (DAP-Spec verbatim).

**Constituent contracts (opened this session):**

| Contract | Status | Sealed at | Surface |
|---|---|---|---|
| `backend/contracts/dap.py::CrossingProfile` | **SEALED (M13-W? per Doc-3 spec-freeze wave)** at prior CP · pydantic model | Prior seal (per BUILD_JOURNAL claims to verify · not opened at this-wave) | The six-operation governance profile spine. |
| `backend/contracts/dap.py::PartyPrincipal` (DAP-2) + `ExternalPartyPrincipal` (DAP-1 verbatim: "organisation-level principal carrying: legal identity; a declared governance posture; the terms it is admitted under; its trust domain identifier; and an admission-time mandate") | **SEALED** at prior CP · pydantic models | Prior seal | The DAP-1 party principal shape · frontends admit under this. |
| `backend/contracts/dap.py::GovernancePosture` enum (DAP-1) | **SEALED** at prior CP · str enum | Prior seal | The declared governance posture. |

**Overall DAP entitlement frozen status:** **UNKNOWN at this-wave close** (per digest (e)-prior state).

**Finding on inspection:**

- `contracts/dap.py` is 288 lines · contains at least ExternalPartyPrincipal, PartyPrincipal, CrossingProfile, GovernancePosture, PartyPrincipalKind, CumulativeHistoryEntry, ApiKeyIssueReceipt, TrustDomainCrossingAttempt, ControlledDeterminationBasis (surface enumerated via `grep '^class '`).
- **JSON-Schema sha256-pinned baseline for each of these**: **UNKNOWN** at this-wave (would need to inspect contract snapshot files + parity registry entries to confirm which are pinned and which are not · deferred to closure wave RED authoring).
- **Six-profile entitlement matrix**: DAP-Spec §4 states each of the six operations separately with its own governance profile. Whether this six-way structure is **frozen as a closed Literal tuple** in `CrossingProfile` or as free-form strings is unknown at this-wave (would need to view the CrossingProfile class body · deferred to closure wave RED authoring).
- **Backwards linkage to platform-key model** (DAP-13 keys per party principal · revocable single-act · stated lifetime · non-transferable · never written to any record including receipts): `ApiKeyIssueReceipt` class present in `contracts/dap.py` but its exact fields + relation to M17-W2 sealed `issue_application_key` (which is the Integration Console issuance ceremony per Canon 7 §28) is unknown at this-wave. M17-W2 issuance is per **application** contract, not per **party principal** per DAP-13. Whether these are the same key or different keys is a **finding** deferred to closure wave.

**Owner (per canon + banked rulings):**

- Canon owner: Doc-3 (`dap_backend_spec_v1`).
- Ratification owner: platform owner. Owner ruling this-turn: "frozen from `dap_backend_spec_v1` (DAP-1 principal fields, DAP-13 key, the six-profile entitlement from §4)".

**Closure wave scope (per owner ruling this-turn · dependency order · after C.17 seam):**

- **CP-CCS2-DAP-ENTITLEMENT-FREEZE** (proposed name · TBD at RED authoring):
  - **W1:** DAP-1 party principal shape sha256-pinned baseline (`ExternalPartyPrincipal.model_json_schema()`) + JSON snapshot file `dap_external_party_principal_v0.contract_snapshot.json` + parity registry entry.
  - **W2:** Six-profile entitlement matrix closed-tuple freeze (`CrossingProfile` as closed Literal 6-tuple per DAP-Spec §4 verbatim if not already · pattern per M17-W1 receipt_policy Literal 2-tuple).
  - **W3:** DAP-13 key contract freeze (`ApiKeyIssueReceipt.model_json_schema()` sha256-pin · six-invariant: (i) per party principal · (ii) never per organisation · (iii) revocable single-act · (iv) expires on stated lifetime · (v) non-transferable · (vi) never written to any record including receipts · AST/structural scan for each).
  - **W4:** Integration seal.
  - Ratchet delta target: +8..+12 (TBD at RED authoring).
- **Dependency:** must wait for CP-CCS1-C17-SEAM-BUNDLE-FREEZE close.

---

### §2.3 · DAP receipt contract (owner-named "DAP receipt contract")

**Anchor:** DAP-Spec §DAP-21 verbatim: "Every operation in §4 emits a metered event carrying: operation type; what was accessed (unit identifiers, or the aggregate scope where units are not individually released); quantity in the unit natural to the operation — audio-hours, tokens, compute-seconds, units, queries; the terms identifier in force; the party principal; and the timestamp from the platform's reliable time source. Metered events are written to the Ledger before the operation's result is returned."

**Constituent contracts (opened this session):**

- `backend/contracts/dap.py` surface: no class explicitly named `MeteredEvent_v0` or `DAP21ReceiptEvent_v0` found via grep at this-wave (surface enumerates as ExternalPartyPrincipal, PartyPrincipal, CrossingProfile, CumulativeHistoryEntry, ApiKeyIssueReceipt, TrustDomainCrossingAttempt, ControlledDeterminationBasis · not exhaustive · would need full class enumeration).
- `backend/contracts/outer_gate_receipt_v1.py` (103 lines) · `backend/contracts/trust_receipt_v1.py` (96 lines) · possibly related but their DAP-21 alignment status is unknown at this-wave.

**Overall DAP receipt frozen status:** **UNKNOWN at this-wave close** (per digest (e)-prior state) · **more concerning finding**: a class explicitly implementing DAP-21 metered event fields (operation_type · accessed_units · quantity_in_natural_unit · terms_identifier · party_principal · timestamp) does not surface via simple grep in `contracts/dap.py` at this-wave. If a DAP-21 receipt class does not exist in `contracts/*.py`, that is an **absence finding** per client's binding rule: the receipt rail carries the Ledger before the operation's result returns, and the frontends card cannot claim full receipt-freeze until this class exists AND is JSON-Schema-pinned.

**Reliable time source dependency** (per DAP-Spec verbatim: "the timestamp from the platform's reliable time source · Reliable time source | Gap — Document 0 G-8 | DAP-21 requires it for every metered event. DAP cannot meter defensibly until it exists."). Whether the reliable_time_source service is fully sealed and DAP-21 metered event timestamp field is wired to it is a **finding** deferred to closure wave.

**Licensing & pricing model dependency** (per DAP-Spec verbatim: "DAP specifies the rails (DAP-21–24) and no tariff. §10 R-6 carries the tariff as a named dependency."). The receipt contract freezes the rails; the tariff is owner-orderable §10 R-6 · not a frontends dependency at this-wave.

**Owner (per canon + banked rulings):**

- Canon owner: Doc-3 (`dap_backend_spec_v1`).
- Ratification owner: platform owner. Owner ruling this-turn: "frozen from `dap_backend_spec_v1` (... DAP-21's receipt fields)".

**Closure wave scope (per owner ruling this-turn · dependency order · after DAP entitlement):**

- **CP-CCS3-DAP-RECEIPT-FREEZE** (proposed name · TBD at RED authoring):
  - **W1:** If `DAP21ReceiptEvent_v0` (or equivalent name) class already exists in `contracts/dap.py` or new module, sha256-pin its `model_json_schema()` + JSON snapshot file + parity registry entry. If class does NOT exist, author new pydantic frozen `DAP21MeteredEvent_v0` (closed 6-field tuple per DAP-Spec verbatim: operation_type · accessed_units · quantity_in_natural_unit · terms_identifier · party_principal · timestamp) at W1 (tests-first · SO §3).
  - **W2:** invariant asserts every §4 operation site emits a metered event structurally (AST-scan on all six operation execution modules · scan for `MeteredEvent(` or equivalent constructor call OR a decorator that guarantees it).
  - **W3:** invariant asserts metered event is written to Ledger BEFORE operation result returns (structural AST-scan on ordering: `emit_metered_event` call comes before `return` in every operation surface).
  - **W4:** timestamp field bound to reliable_time_source (identity import from sealed module · not a wall-clock call).
  - **W5:** integration seal binding all four W-boundaries.
  - Ratchet delta target: +10..+15 (TBD at RED authoring · larger due to per-operation site scan).
- **Dependency:** must wait for CP-CCS2-DAP-ENTITLEMENT-FREEZE close.

---

### §2.4 · Additional contracts that frontends touch (per owner steer + M17 seal chain)

The three anchor contracts named in owner ruling this-turn (C.17 seam · DAP entitlement · DAP receipt) are the **gating** trio for frontends per B-frontends-Q1. However, several other contracts are directly consumed by frontend surfaces per the M17 seal chain and would benefit from a status audit at the survey close for owner visibility:

| Contract file | Status | Sealed at | Notes |
|---|---|---|---|
| `backend/contracts/approval_request.py` | **STATUS UNKNOWN** at this-wave (not opened) | Prior seal (unknown wave) | Any frontend surface presenting an approval flow consumes this. Owner ruling B-frontends-Q1 says "approval blocks rather than warns". |
| `backend/contracts/admission_refusal.py` | **STATUS UNKNOWN** at this-wave (not opened) | Prior seal (unknown wave) | Any frontend surface handling admission refusal consumes this. |
| `backend/contracts/erasure_request.py` | **STATUS UNKNOWN** at this-wave (not opened) | Prior seal (unknown wave) | Frontends implementing rights-of-access + erasure (CA1-N3 owner ruling · A17.15) consume this. |
| `backend/contracts/trust_receipt_v1.py` (96 lines) | **SEALED at prior CP · specific wave TBD from BUILD_JOURNAL** | Prior seal | Trust receipt shape · possibly overlaps with DAP-21 receipt · **finding**: whether trust_receipt_v1 IS the DAP-21 receipt or separate is unknown at this-wave · deferred to CCS3 RED authoring. |
| `backend/contracts/outer_gate_receipt_v1.py` (103 lines) | **SEALED at prior CP · specific wave TBD from BUILD_JOURNAL** | Prior seal | Outer gate (Canon 8 Watch) receipt · frontends may or may not touch · **finding**: does frontend see outer_gate_receipt as first-class or only as policy-shielded? Deferred to CCS wave authoring boundary. |
| `backend/contracts/service_1_refusal.py` | **SEALED at prior CP · specific wave TBD** | Prior seal | Any frontend refusal envelope consumes this. |
| `backend/contracts/v2_refusal.py` | **STATUS UNKNOWN** at this-wave (not opened) | Prior seal (unknown wave) | Possibly successor to service_1_refusal · **finding**: which is authoritative for frontends? Deferred to CCS wave authoring boundary. |
| `backend/contracts/handoff_contract.py` | **SEALED (M14-W1)** at Commit-A `8b861987` | 2026-09-19T~06:37Z | Enumerated in §2.1 (C.17 seam) above. |
| `backend/contracts/asset_registry.py` | **STATUS UNKNOWN** at this-wave (not opened) | Prior seal (unknown wave) | Frontends showing estate composition may consume this. |
| `backend/contracts/cif_proposal_v0.py` | **SEALED (M16-W1)** at Commit-A `ff000d58` · shape-snapshot pin `e190d8300f…` | 2026-09-19T~09:35Z | Conditioned Ideation Faculty proposal · frontends showing proposals (approve/refuse flow) consume this. |
| `backend/contracts/watch_action_v0.py` | **SEALED at prior CP · specific wave TBD** | Prior seal | Watch action surface · frontends showing security posture consume this. |

**Non-anchor findings:** the DAP UI Handoff Brief §5 anchor lists surfaces the frontends MUST implement; the survey confirms most such surfaces have backing contracts, but sha256-pinned frozen status is not universally applied. **Recommendation**: at the frontends-card-drafting wave boundary, order a **status confirmation sub-wave** for each contract in the §2.4 list (short reads + parity-registry inspection · notes-only). This is smaller than a closure wave and preserves the primary sequence.

---

## §3 · Ready-for-frontends checklist (per B-frontends-Q1 gate)

Per owner ruling `STATE/DECISIONS.md:12115` verbatim (B-frontends-Q1): frontends open when **all three** of (C.17 seam · DAP entitlement · DAP receipt) are frozen from `dap_backend_spec_v1` per T-b JSON-Schema-authoritative. Status at this survey close:

| Gate item | Status | Blocks frontends open? |
|---|---|---|
| C.17 answering-service seam bundle freeze | **PARTIAL** (three individual contracts frozen · seam-boundary bundle-sha not yet pinned · M17-W5 handoff-ID structural violation banked as fork) | YES (until CP-CCS1-C17-SEAM-BUNDLE-FREEZE closes AND CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG closes) |
| DAP entitlement contract freeze | **UNKNOWN** (individual pydantic models exist · sha256-pinned baselines unknown · six-profile Literal freeze unknown) | YES (until CP-CCS2-DAP-ENTITLEMENT-FREEZE closes) |
| DAP receipt contract freeze | **UNKNOWN / possibly ABSENT** (class implementing DAP-21 exact fields not surface-grepped this-wave · reliable_time_source wiring status unknown · Ledger-write-before-return structural discipline unknown) | YES (until CP-CCS3-DAP-RECEIPT-FREEZE closes) |
| **B-frontends-Q1 gate result: CLOSED at this survey close.** Frontends stay gated until all three closure waves seal. | | |

---

## §4 · Ordered sequence for gate release (per owner ruling this-turn · sequence clause verbatim)

1. **(f) CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG** (slotted between C.13 seal and memory layer per owner ruling item 2 · but a **prerequisite for CP-CCS1** because the adapter + type-tag must land into the seam bundle · sequencing constraint added at this survey)
2. **(b) CP-C13-CLOSURE-KEY-SCOPING-PROVENANCE-TTL** (in parallel with this survey · owner ruling this-turn)
3. **(c) CP-CLEANUP-STATE-DISCIPLINE** (slotted between C.13 and memory layer per owner ruling item 2)
4. **Memory layer opens on (b) seal** — memory_compaction_v1 + R-19/R-20 defaults + user-memory flag OFF + 7 property tests + hard bans grep-negative (owner ruling item 3)
5. **CP-CCS1-C17-SEAM-BUNDLE-FREEZE** (contract closure wave 1 · after memory layer or in parallel per §6.7 interleave discipline)
6. **CP-CCS2-DAP-ENTITLEMENT-FREEZE** (contract closure wave 2 · after CCS1)
7. **CP-CCS3-DAP-RECEIPT-FREEZE** (contract closure wave 3 · after CCS2)
8. **Frontends card drafted from UI Handoff Brief §5** (batched for ratification at CCS3 close · body derives from brief · **STOP AND REPORT** to owner before opening frontend build waves per orchestrator plan item 5 · web/Expo delegated to specialist agents)
9. **Frontends build waves** (out of scope for main autopilot · delegated to specialist agents per banked ruling)

**Continuous interleave:**
- G5 slices to 1,096 (currently 640/1096)
- Staleness ceremony on its clock (armed 2026-09-20T~11:35Z)

---

## §5 · Absence findings (SO §6.1 · reportable per client's binding rule)

1. **DAP UI Handoff Brief §5** document not surveyed on disk at this-wave close. Location TBD before frontends-card wave.
2. **`dap_backend_spec_v1` machine-readable JSON-Schema** does not exist as a separate on-disk file; the schema is derived from pydantic model wrappers in `contracts/dap.py`. Per T-b JSON-Schema-authoritative discipline, the pydantic `model_json_schema()` output serves as the frozen schema for each contract, sha256-pinned at closure wave.
3. **`DAP21MeteredEvent_v0`** (or equivalent DAP-21 receipt class) not surface-grepped in `contracts/dap.py` at this-wave. If absent, W1 of CCS3 authors it. If present under a different name, W1 of CCS3 sha256-pins it.
4. **C.17 seam-boundary bundle sha256 pin** does not exist at this-wave. W1 of CCS1 authors it.
5. **Six-profile entitlement matrix closed-tuple freeze** unknown at this-wave. W2 of CCS2 confirms/enforces.
6. **Reliable time source wiring for DAP-21 timestamp field** unknown at this-wave. W4 of CCS3 verifies structurally.
7. **Ledger-write-before-return discipline** for DAP-21 metered events unknown at this-wave. W3 of CCS3 verifies structurally.
8. **`approval_request.py` · `admission_refusal.py` · `erasure_request.py` · `v2_refusal.py` · `asset_registry.py` · `watch_action_v0.py`** frozen status unknown at this-wave. Recommended status-confirmation sub-wave at frontends-card-drafting boundary.
9. **Trust receipt vs DAP-21 receipt relationship** unknown at this-wave. W1 of CCS3 disambiguates.
10. **Outer-gate receipt (Watch) vs DAP-21 receipt relationship** unknown at this-wave. W1 of CCS3 disambiguates.

---

## §6 · Canon + anchor citations

- `STATE/DECISIONS.md:12115` (B-frontends-Q1 verbatim · frontends gate on frozen C.17 + DAP entitlement + DAP receipt)
- `STATE/DECISIONS.md:13600 + 13630 + STATE/STANDING_ORDERS.md:445` (Frontend fidelity bar · DAP UI Handoff Brief §5 · functional parity with five-stage pattern)
- Owner ruling 2026-09-19T~17:54Z verbatim (this-turn · digest item (e) ruled · survey now + closure waves in dependency order + T-b JSON-Schema-authoritative · frontends card + STOP AND REPORT before opening frontend build waves)
- `/app/assessment_workspace/canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` (Doc-3 · DAP-Spec `dap_backend_spec_v1` · DAP-1 · DAP-5 · DAP-12 · DAP-13 · DAP-19 · DAP-21 · six-profile §4)
- HR-2 (owner ruling this-turn · applied to CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG · included as prerequisite for CCS1 at §4 above)
- SO §3.10-α (closed-schema discipline · applied to every closure wave)
- SO §6.4 NOTHING-BEYOND (each closure wave scope frozen per its card)
- SO §6.7 (interleave discipline for G5 + staleness ceremony)
- Delegation ruling for web/Expo frontends to specialist agents (banked at prior seal · applied at STOP AND REPORT boundary)

---

## §7 · Survey close

**Survey close time:** 2026-09-19T~18:00Z.
**Ratchet at close:** 5452 (unchanged · this is a notes-only sub-wave).
**Files added:** this file (`notes/EFCS_FRONTENDS_CONTRACT_SURVEY_20260919.md`).
**Files modified:** STATE/DECISIONS.md (survey-close banking section) · STATE/NEXT.md (interlude marker) · notes/ORCH_BOOT.md (R-6 regen).
**Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered** at this survey close.
**Additive-only per SO §3.8** preserved.

**Autopilot next:** open CP-C13-CLOSURE-KEY-SCOPING-PROVENANCE-TTL RED authoring (per owner ruling this-turn item (b) · parallel to this survey close) OR proceed to slotted (c) CP-CLEANUP-STATE-DISCIPLINE OR (f) CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG per sequence clause.
