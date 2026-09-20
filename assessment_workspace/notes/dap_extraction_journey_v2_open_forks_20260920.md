# DAP Extraction Request Approval Journey v2 · Open Forks Register

**Banked at**: 2026-09-20T~16:00Z under CP-CONTENT-REGISTRY-INGEST-DROP · state-master-notes-only banking commit (WAVE R-81+prelude · precedes CP-ENTITLEMENT-BUILD-WAVE R-82).

**Source (this ingest)**: `custody/owner_drops/20260920T1600Z/extraction_request_approval_journey_v2.md` sha256 `c52356af28e7bb1c99a1ffb335f548e14297b7196670f33b2e9e651ec1d813b2` (byte-verified).

**Source (this ingest, sibling)**: `custody/owner_drops/20260920T1600Z/extraction_test_cases.xlsx` sha256 `c0c8c519d57f6db9873967633de63e8658aa1352c10cf00e8692bcbe4a54b0c6` (byte-verified · carries TC-INA-06 and TC-EXP-02 with conflicting copy).

**Predecessor**: `custody/owner_drops/20260920T1140Z/extraction_request_approval_journey.md` sha256 `a7485f06…` (v1 · consumed at CP-DAP-LIFECYCLE-BACKEND-WAVE seal `86348320` / `b4850fd8` / `6bdb5183` · sealed backend at `services/dap_lifecycle/*.py` and unlocked at CP-Q-UNLOCK-SUB-WAVE seal `c0f5e6d5` / `6fc1a99b` / `d5b0522f`).

**Owner directive at this ingest verbatim** (2026-09-20T~16:00Z):

> "THREE CONFLICTS are with the owner for ruling — bank them as open forks, build NOTHING against them until ruled: (i) journey doc + TC-INA-06/TC-EXP-02 contain 'Waited [N] days' copy vs banked Q6 OMITTED; (ii) journey doc says 'no Retry ships' and lacks `Interrupted` — I read it as pre-dating Q1/Q7 rulings (rulings supersede), owner to confirm; (iii) `party_halted` block kind + 'What's run so far will still be billed' confirm may be net-new vs the sealed lifecycle backend — check whether it exists in the sealed state machine and report presence/absence at your next seal, but do NOT build it before the owner rules."

**Standing bounds** (in force at this-file authoring):
- Zero build against any of the 3 conflicts until owner rules.
- Sealed DAP lifecycle backend at `services/dap_lifecycle/*.py` (CP-Q-UNLOCK-SUB-WAVE seal `c0f5e6d5` on `programme/track-a`, `6fc1a99b` on `master`, `d5b0522f` Commit-C fixup) REMAINS binding.
- Q-unlock rulings (Q1 retry-for-check-only bounded DEFAULT 3 · Q7 `Interrupted` non-terminal state bounded auto-retry DEFAULT 3) supersede any pre-dated journey v1 or v2 clause per SO §6.7 sequence discipline.

---

## FORK-CON-INGEST-1 · "Waited [N] days" copy

### Conflict statement

- Journey v2 body carries "Waited [N] days" copy on at least one surface (owner-reported at ingest note verbatim).
- Test cases `TC-INA-06` and `TC-EXP-02` (in `extraction_test_cases.xlsx`) carry the same "Waited [N] days" copy in their acceptance rows.
- Banked Q6 owner-turnaround-line ruling (per CP-Q-UNLOCK-SUB-WAVE seal report R-78 verbatim): "Q6 owner-turnaround-line stay HARD HOLDs not built" → the sealed backend and prior journey v1 did NOT surface any owner-turnaround-derived "Waited [N] days" line.

### Disposition at this ingest

- **OPEN FORK** banked at this-file.
- Build NOTHING against "Waited [N] days" copy in any code path or test until owner rules.
- Q6 remains HARD HOLD per CP-Q-UNLOCK-SUB-WAVE seal (`c0f5e6d5` / `6fc1a99b` / `d5b0522f`).
- No pre-emptive removal of Q6-HOLD gate at any sealed surface.

### Owner action required

Choose one:
- **(a)** Ratify "Waited [N] days" copy as super-supersede of Q6 HARD HOLD. Requires: R-N ruling opening a new sub-wave to build the owner-turnaround-line as a derived (never-a-stored-counter) view over the sealed submission-timestamp + decision-timestamp, without disclosing anything about the owner's identity (per identity-discipline seal test in W1 cluster).
- **(b)** Drop "Waited [N] days" copy from journey v2 + TC-INA-06 + TC-EXP-02 at next drop revision. This-desk to receive revised journey v2 + revised test cases at that drop boundary.
- **(c)** Other ruling.

---

## FORK-CON-INGEST-2 · "no Retry ships" clause + missing `Interrupted` state

### Conflict statement

- Journey v2 body reads "no Retry ships" and lacks the `Interrupted` state (owner-reported at ingest note verbatim).
- Sealed backend at `services/dap_lifecycle/state_machine.py` (CP-Q-UNLOCK-SUB-WAVE Commit-A `c0f5e6d5`) DOES ship Q1 retry-for-check-only bounded DEFAULT 3 and DOES have `Interrupted` as a new non-terminal state with 3 edges + `retry_service.py` + `interrupted_service.py`.
- Sealed test surface at `backend/tests/invariants/test_dap_lifecycle_wave.py` W9-W15 clusters (23 invariants) enforces Q1/Q7 rulings structurally against the sealed state machine.
- Q1/Q7 owner rulings (banked at CP-Q-UNLOCK-SUB-WAVE seal report R-78 verbatim 2026-09-20T~13:00Z) POST-DATE journey v2 (which owner reads as pre-dating).

### Owner ingest note verbatim

> "I read it as pre-dating Q1/Q7 rulings (rulings supersede), owner to confirm"

### Disposition at this ingest

- **OPEN FORK** banked at this-file · this-desk interpretation flagged: **Q1/Q7 rulings supersede journey v2 pre-dated clause per SO §6.7 sequence discipline and per owner ingest note verbatim** — awaiting explicit owner confirmation.
- Sealed backend REMAINS binding (state machine keeps `Interrupted` + retry service ships).
- Build NOTHING against journey v2 "no Retry ships" clause.

### Owner action required

Choose one:
- **(a)** Confirm Q1/Q7 rulings supersede · journey v2 "no Retry ships" clause is banked-void · journey v2 to be revised at next drop with the ruled `Interrupted` state + retry ceremony reflected.
- **(b)** Reverse Q1/Q7 rulings and remove `Interrupted` + retry service from sealed backend. Requires: R-N ruling opening rollback ceremony under Canon 3 §24 rule-change discipline (rollback of a sealed additive contract requires owner counter-sign + 4-step ceremony · this would be net-negative to the ratchet · not autopilot-authorised).
- **(c)** Other ruling.

---

## FORK-CON-INGEST-3 · 5 Blocked kinds vs sealed 3-kind enum + net-new "billed" copy

### Conflict statement

- Journey v2 body uses **5 Blocked kinds**: `request` · `check` · `estate` · `suspended` · `party_halted`.
- Sealed backend `BlockedKind(enum.Enum)` at `services/dap_lifecycle/blocked_kinds.py` has **3 kinds only**: `request` · `check` · `estate`. Module docstring line verbatim: "The 3 kinds of Blocked · request / check / estate."
- Journey v2 also introduces net-new release-attribution copy "What's run so far will still be billed" on the party_halted kind.

### Presence-check evidence (this-desk grep at ingest boundary)

Executed at 2026-09-20T~15:35Z via `grep -rniE "party_halted|party_halt|halt_party" services/ tests/` from `/app/assessment_workspace/repos/Extraction-Akki/backend/`:

- **`party_halted` grep result**: ABSENT anywhere in `backend/services/**` or `backend/tests/**`. Zero hits. The four grep-hits (`services/cif/halt.py::is_halted`, `services/checker/consequence_classes.py`, `services/platform_control_plane/tenant_lifecycle.py`, `services/solva_v2/engines/reflection.py`) are unrelated surfaces (Targeta halt simulation, checker consequence class narrative, tenant-lifecycle §4.7 effects on suspended, and Solva reflection HALTED skeleton respectively). None is a DAP-lifecycle Blocked kind.
- **`suspended` as a DAP Blocked kind**: ABSENT. `suspended` exists as (i) a licence status per ENT-6 (`ENT-6 ... status ∈ {active, suspended, expired}`), and (ii) a request-level platform lifecycle state at `services/platform_control_plane/tenant_lifecycle.py:16` verbatim comment "§4.7 effects on entry to suspended: sessions_revoked, jobs_halted". Neither is a member of `BlockedKind(enum.Enum)` in the sealed DAP lifecycle backend.
- **`BlockedKind` enum in sealed backend**: exactly 3 members `request` / `check` / `estate` at `services/dap_lifecycle/blocked_kinds.py` (post-CP-Q-UNLOCK-SUB-WAVE seal · unchanged from CP-DAP-LIFECYCLE-BACKEND-WAVE seal · Q7 ruling verbatim per CP-Q-UNLOCK-SUB-WAVE seal report "Blocked stays 3-kind · non-gate fault = Interrupted new non-terminal state · not a 4th Blocked kind").
- **"What's run so far will still be billed" grep result**: ABSENT in `backend/services/**` and `backend/tests/**`. Zero hits.

### Disposition at this ingest

- **OPEN FORK** banked at this-file.
- Sealed 3-kind `BlockedKind` enum REMAINS binding.
- Build NOTHING against journey v2 5-kind model.
- **HARD prohibition** during any downstream wave until owner rules: do NOT author any `party_halted` or `suspended` enum member in `BlockedKind`; do NOT author "What's run so far will still be billed" copy at any release-attribution surface (which would touch DAP-35 release-budget-non-disclosure discipline — see below).
- **Cross-canon dependency**: adding `party_halted` and its "will still be billed" copy touches DAP-35 (release-budget non-disclosure per Canon 3 §9.3 and per CP-Q-UNLOCK-SUB-WAVE Q5 escrow ruling banked). Owner ruling on FORK-CON-INGEST-3 must reconcile with DAP-35 non-disclosure discipline: a "billed" copy that discloses release-budget consumption on suspension would violate DAP-35 verbatim.

### Owner action required

Choose one:
- **(a)** Authorise additive extension to sealed `BlockedKind` enum for `suspended` and `party_halted`. Requires: R-N ruling opening a new sub-wave under Canon 3 §24 rule-change discipline (adding members to a sealed closed-tuple enum ANY closed-schema-α discipline surface is a rule-change · 4-step ceremony required · propose → counter-sign → wait → apply). Also requires: cross-canon reconciliation with DAP-35 (release-budget non-disclosure) covering the "What's run so far will still be billed" copy · owner to specify whether this copy is a permitted disclosure OR whether it must be replaced by fixed-uninformative copy per DAP-35 discipline.
- **(b)** Confirm sealed 3-kind enum is binding · journey v2 "5 Blocked kinds" model is banked-void · journey v2 to be revised at next drop with only `request` / `check` / `estate`.
- **(c)** Other ruling.

---

## Standing bounds preserved by this-file

- Zero code change · zero test change · zero ratchet change.
- Zero write to `/app/frontend/*` (FE DISPATCH COORDINATION active · specialist owns `/app/frontend/*` write scope · this-desk read-only cross-check).
- Sealed contracts NOT edited.
- Sealed writers NOT edited.
- SO §3.8 thin-kernel additive-only (this-file adds a NEW state-side note · zero edit of sealed anchors).
- SO §6.4 NOTHING-BEYOND (scope frozen at 3 open-fork bankings + party_halted presence-check evidence + owner-directive verbatim citations).
- SO §4.1 §E custody discipline (source docx + journey md immutable in `custody/owner_drops/20260920T1600Z/`).
- SO §4.1 §F sha-pinning discipline (source sha256s pinned at head + at drop manifest).

END OF OPEN-FORKS REGISTER.
