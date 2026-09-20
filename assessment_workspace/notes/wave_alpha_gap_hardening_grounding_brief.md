# Grounding Brief — CP-ALPHA-GAP-HARDENING · WAVE R-69 Step 7

**Wave chartered:** 2026-09-20T~08:56Z (owner disposition: *"α-GAP HARDENING WAVE APPROVED"* · banked verbatim at `STATE/DECISIONS.md 2026-09-20T~08:56Z · OWNER DISPOSITION`).

**Wave open authorized:** 2026-09-20T~09:48Z (owner subsequent ruling · banked verbatim at `STATE/DECISIONS.md 2026-09-20T~09:48Z`).

**Mutation-site discipline (owner ruling 2026-09-20T~09:48Z verbatim):**
> mutation-site regressions that surface when frozen=True lands must be fixed by building fresh instances at the CALL SITES (test fixtures included), never by weakening the freeze or adding model_copy escape hatches on the contracts themselves. If any production call site turns out to MUTATE a receipt after construction, that's not a test fix — that's a finding (receipts are immutable evidence by doctrine); bank it and adapt the call site.

## §A · Wave scope (SO §6.4 NOTHING-BEYOND)

**In-scope (exactly these two contracts):**
1. `backend/contracts/trust_receipt_v1.py::TrustReceiptV1` — currently `model_config = ConfigDict(extra="forbid", frozen=False)` (explicit unfrozen). Target: `frozen=True`.
2. `backend/contracts/outer_gate_receipt_v1.py::OuterGateReceiptV1` — currently `model_config = ConfigDict(extra="forbid")` (Pydantic default `frozen=False`). Target: explicit `frozen=True`.

**Out-of-scope (unchanged at this wave):**
- Any other Pydantic model in the codebase (only the two named above are α-gap targets per CCS3 W3.3/W3.4 banking).
- Contract field additions (no new fields; frozen=True is the sole delta).
- `MeteredEvent` (already frozen=True per CCS3 W1.3 · verified compliant).
- Any test file other than `test_ccs3_dap_receipt_freeze.py` (only the 2 banking-witness tests need transition update).

## §B · Canon anchors verbatim

- **Owner ruling 2026-09-20T~08:56Z (α-gap hardening wave approval)** — `STATE/DECISIONS.md 2026-09-20T~08:56Z · OWNER DISPOSITION` verbatim: *"α-GAP HARDENING WAVE APPROVED"*.
- **Owner ruling 2026-09-20T~09:48Z (mutation-site discipline · Step 7 opening authorization)** — `STATE/DECISIONS.md 2026-09-20T~09:48Z` verbatim (quoted above at header).
- **SO §3.10-α** — closed-schema discipline: `frozen=True` + `extra='forbid'` on all contract-boundary shapes.
- **SO §3.8** — thin-kernel additive-only. This wave adds tests + flips two contract config fields (frozen=False → frozen=True); no sealed contract shape is edited (field set preserved byte-identical); no external interface breaks. The 2 CCS3 banking-witness tests self-documented their transition procedure at authoring; flipping their assertions per their own docstring instructions is the sanctioned closure path (not a sealed-test edit; it's the pre-authorized transition).
- **SO §3.3** — 3-Commit Seal on dual branches. Commit-A code on `programme/track-a` + Commit-B state master banking + Commit-C fixup (banks Commit-B SHA + ORCH_BOOT R-6 boundary regen + POD audit mirror sync).
- **Canon 3 §9.3** — canonicalization discipline. Every owner ruling in this brief is quoted verbatim from `STATE/DECISIONS.md`.
- **Canon 8 §W8** — the-floor-never-learns. This wave adds 5 invariants → ratchet 5527 → 5532. Monotonic-up; never rebaselined silently.
- **Canon 8 §W11** — one-task-one-identity. Contract imports use sole allowed identity paths (`from contracts.trust_receipt_v1 import TrustReceiptV1` etc.).
- **CCS3 W3.3 + W3.4** (`backend/tests/invariants/test_ccs3_dap_receipt_freeze.py` module docstring · lines 32-35 + 104-107) — banked at CCS3 for **exactly this wave's** closure.

## §C · Empirical facts verified this-wave (pre-code)

1. **Pydantic v2 `model_json_schema()` is BYTE-IDENTICAL between frozen and non-frozen models** (given identical title/name). Verified via toy `class X(BaseModel): model_config = ConfigDict(extra='forbid', frozen=<bool>); x: str` — schema output identical for both.
   **Consequence:** no schema-drift will occur when frozen=True lands. The three CCS3 sha256 pins (`_TRUST_RECEIPT_V1_SCHEMA_SHA256` · `_OUTER_GATE_RECEIPT_V1_SCHEMA_SHA256` · `_CCS3_DAP_RECEIPT_BUNDLE_SHA256`) will remain valid without update. `contract_snapshot.json` files will not need regen. `test_frozen_contract_snapshot_parity.py` will remain GREEN.
2. **Mutation on a frozen Pydantic v2 model raises `pydantic.ValidationError`** (type=`frozen_instance`) when attempting `.attr = value` on a constructed instance. Verified empirically.
3. **Zero mutation sites in production code** on TrustReceiptV1 / OuterGateReceiptV1 instances. Grep verified: sole hit was `perception_router.py:59 body["signature"] = trust_receipt.sign(...)` where `body` is a plain dict and `trust_receipt` is the module (not a receipt instance) — NOT a mutation-site.
4. **Two CCS3 banking-witness tests will require transition update** (per their own docstring instructions):
   - `test_ccs3_trust_receipt_v1_frozen_status_banked_for_owner_ratification` (line 358-384) asserts `frozen is False` — will fail. Update: assert `frozen is True` + flip banking status to CLOSED.
   - `test_ccs3_outer_gate_receipt_v1_frozen_status_banked_for_owner_ratification` (line 387-403) asserts `frozen is None` — will fail. Same update.

**Consequence for owner mutation-site discipline:** since ZERO production mutation sites exist, no FINDING needs to be banked. Both α-gap targets can flip cleanly. If a mutation-site is discovered during regression sweep (unlikely per grep evidence), that will be banked as a FINDING per owner ruling verbatim.

## §D · Wave sequence (this-turn autonomous per owner Go)

1. **Grounding brief author** (this document · landing this-turn).
2. **RED-first test authoring** at `backend/tests/invariants/test_alpha_gap_hardening.py` — 5 new invariants:
   - `test_alpha_gap_hardening_trust_receipt_v1_is_frozen` — asserts `TrustReceiptV1.model_config.get('frozen') is True`.
   - `test_alpha_gap_hardening_outer_gate_receipt_v1_is_frozen` — asserts `OuterGateReceiptV1.model_config.get('frozen') is True`.
   - `test_alpha_gap_hardening_trust_receipt_v1_mutation_raises` — construct valid instance; attempt `.audit_id = 'x'`; expect `pydantic.ValidationError` with `type=='frozen_instance'`.
   - `test_alpha_gap_hardening_outer_gate_receipt_v1_mutation_raises` — same for OuterGateReceiptV1.
   - `test_alpha_gap_hardening_wave_closure_attestation` — attests that at α-gap hardening wave, both CCS3 W3.3/W3.4 banked α-gaps are CLOSED (structural attestation of scope frozen + closure disposition).
3. **RED verification** — run `pytest tests/invariants/test_alpha_gap_hardening.py -v` → expect all 5 tests FAIL right-reason. Bank RED receipt at `phase0/drill_receipts/YYYYMMDDTHHMMZ_alpha_gap_hardening_RED_pre.log`.
4. **Code change (Commit-A body):**
   - `backend/contracts/trust_receipt_v1.py`: `model_config = ConfigDict(extra="forbid", frozen=False)` → `model_config = ConfigDict(extra="forbid", frozen=True)`.
   - `backend/contracts/outer_gate_receipt_v1.py`: `model_config = ConfigDict(extra="forbid")` → `model_config = ConfigDict(extra="forbid", frozen=True)`.
5. **CCS3 transition update (Commit-A body · per docstring self-instruction):**
   - `test_ccs3_dap_receipt_freeze.py::test_ccs3_trust_receipt_v1_frozen_status_banked_for_owner_ratification`: flip assertion `is False` → `is True` + update docstring to name closure at α-gap hardening wave.
   - `test_ccs3_dap_receipt_freeze.py::test_ccs3_outer_gate_receipt_v1_frozen_status_banked_for_owner_ratification`: flip assertion `is None` → `is True` + update docstring.
   - `test_ccs3_dap_receipt_freeze.py` module docstring (lines 32-35 + 104-107): update SO §3.10-α banking status from "banked for owner ratification in a future ceremony" to "CLOSED at α-gap hardening wave 2026-09-20T~09:48Z".
6. **Targeted GREEN verification** — run `pytest tests/invariants/test_alpha_gap_hardening.py tests/invariants/test_ccs3_dap_receipt_freeze.py -v` → expect all pass. Bank GREEN receipt.
7. **Full-suite regression sweep** — run `pytest tests/invariants/ -v` → expect all pass (ratchet 5527 + 5 new = 5532). If any regression fires:
   - **Test fixture regressions** → adapt fixture to build fresh instance (per owner discipline).
   - **Production mutation regressions** → **bank as FINDING** per owner discipline verbatim, adapt call site to build fresh instance.
8. **Double-green BASELINE_GUARD=1 byte-identical sweep** — run twice, verify stripped-sha256 IDENTICAL, against unchanged `baseline_failures.json` sha256 `8a7d92289c06bbfaae75c08750575dd5e73a70745693f741fdf85215238562b1`.
9. **Ratchet bump** in `baseline_failures.json`:
   - `counts_at_baseline.passed`: 5527 → 5532
   - `invariants_enforced_when_baseline_guard_1.passed_floor`: 5527 → 5532
   - `ratchet_history` append entry.
   - Recompute new sha256 of the file.
10. **Commit-A on programme/track-a** — grounding brief + 2 contract edits + NEW test file + 2 CCS3 test transition updates + drill receipts + ratchet bump.
11. **Commit-B on master (state master banking)** — banks Commit-A SHA + Commit-A scope + mutation-site sweep verdict + closure of CCS3 W3.3/W3.4 α-gap bankings + Canon anchors + Stop-conditions + autopilot next.
12. **Commit-C fixup on master** — banks Commit-B SHA + `notes/ORCH_BOOT.md` R-6 boundary regen (advance state_head + code_head + ratchet.passed_floor to 5532 + baseline_failures_sha256 to new sha) + POD-repo audit mirror byte-identical sync.
13. **Post-Commit-C `test_orch_boot` verification** — confirm banking chain intact.

## §E · Interlude marker discipline (owner-authorized)

If context budget insufficient for full RED→GREEN→double-green→3-Commit cycle in one turn, land INTERLUDE marker at Commit-A boundary. Commits-B+C follow at next opportunity. **Better to interlude than truncate mid-wave.**

## §F · Discipline (still binding)

- Zero push · terminal pytest only · no testing_agent (STRICTLY BANNED · owner standing law).
- CWD constraint: `pytest` invocations run strictly from `/app/assessment_workspace/repos/Extraction-Akki/backend/`.
- Additive-only per SO §3.8. Test-body edits at CCS3 transition tests are the pre-authorized closure procedure (per those tests' own docstring self-instruction · not sealed-test in-place-mutation).
- Three-repo discipline (CODE `programme/track-a` + STATE `master` + POD `main`) preserved.
- Ratchet monotonic-up · never rebaselined silently (§Canon 8 §W8).
- Stop-conditions #1/#2/#3 discipline · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered.

## §G · Anti-slop note

Every empirical claim in §C traces to a shell command or file:line opened this-turn. The plan in §D lands as file-additions and file-edits only (no filename-only "will implement" — actual code produced this-turn). If any premise in §C proves wrong at RED (e.g., a mutation-site is discovered), the wave banks the FINDING and adapts per owner discipline.

**End of grounding brief.**
