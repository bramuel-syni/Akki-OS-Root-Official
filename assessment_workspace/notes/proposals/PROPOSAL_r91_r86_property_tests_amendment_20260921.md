READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PROPOSAL · Amend `test_baseline_drift_annotations_present.py` Properties 2, 3, 5 · Canon 3 §24 rule-change ceremony · ordinary tier

**Filed:** 2026-09-21T03:23:15Z
**Filer:** main-agent Autopilot (under owner ruling this-session 2026-09-21T~01:00Z · Path ε RATIFIED · rule-change ceremony ordinary tier · precedent shape = CP-STALENESS-CEREMONY 2026-09-18/2026-09-20)
**Ceremony type:** rule change per Canon 3 §24 (propose → counter-sign → wait → apply). This file is the **propose** step. **The owner ruling this-session is the batched counter-sign** per SO §4 line at STATE/STANDING_ORDERS.md:437 verbatim: "ordinary-tier re-scopes that tighten (never loosen) may be proposed and countdown-started without waiting, countersign requested in the batch."
**Countdown:** ordinary tier (48 hours per R-18 effect 12 · GPU-staleness precedent line 12358/12381). Starts at proposal filing timestamp. Horizon: **2026-09-23T03:23:15Z**. Apply step schedule: at horizon.

---

## §1 · Owner ruling verbatim (source of this proposal · banked in `STATE/DECISIONS.md` at this-turn ceremony-open commit)

> "R-91 — PATH ε RATIFIED, via the RULE-CHANGE CEREMONY at the ordinary tier (48 hours), the same path as the GPU-staleness re-scope. Owner verbatim: 'the ceremony is the authorised way a sealed test file changes — a ceremonied amendment is not a §3.8 refactor.' Conditions, binding exactly:
> 1. Properties 2, 3, and 5 tolerate an empty annotation set ONLY when the CP_APP_JS_UNIFY card status is SEALED — accidental emptiness before closure stays RED.
> 2. The early return is a NAMED success, never a silent pass: the test output must state 'annotation set empty by ruled closure R-91' so the reason is on record every run.
> 3. Property 4 stays untouched.
> 4. The ceremony receipt cites this ruling.
> 5. On apply: retire 5/5 baselines, re-run the full sweep, seal at the new floor.
> Execute the ceremony per the GPU-staleness precedent shape exactly — including whatever notice/window mechanics the ordinary tier carries. If the ordinary tier imposes a 48-hour window before apply, do NOT idle: open the G5-v5 second slice (below) during the window and apply+seal R-91 at expiry. If the banked ceremony rules permit apply-on-owner-ruling-on-record, apply now. Follow the banked ceremony mechanics; do not invent."

---

## §2 · What is being amended

**File:** `repos/Extraction-Akki/backend/tests/invariants/test_baseline_drift_annotations_present.py`

**Currently sealed at:** R-86 seal `2eca0e58d1d9773d1b781abe570c3e015e0c98f2` (schedules R-91 slot + establishes annotation pattern). File is 241 lines, contains 5 property tests (labelled Properties 1..5 by docstring convention).

**Amended by this proposal:** Properties 2, 3, 5 gain a NAMED-SUCCESS early return when BOTH:
1. `known_runtime_drift_annotations` is empty AND
2. The R-91 closure card (`STATE/OBJECTIVES/CP_APP_JS_UNIFY.md`) `milestone_status` line contains the token `SEALED`.

**Untouched by this proposal:**
- Property 1 (`test_every_mirror_drift_baseline_entry_has_an_annotation`) — vacuously passes at empty state (already correct semantics · no floor guard).
- Property 4 (`test_annotation_count_equals_mirror_drift_baseline_entry_count`) — **UNTOUCHED per owner condition 3.** Set-equality guard passes at 0 == 0 (already correct semantics).

## §3 · Root cause (why the amendment is needed)

**Discovered during R-91 Phase 2 landing adjudication** (main-agent stop-and-report 2026-09-21T~00:50Z, this-session). Empirical trace:

```
FAILED tests/invariants/test_baseline_drift_annotations_present.py::test_every_annotation_has_the_required_8_field_shape
E       AssertionError: known_runtime_drift_annotations is absent or empty; Ruling 1(a) requires at least one annotation covering the three pod_shell mirror-drift baseline entries.
E       assert {}

FAILED tests/invariants/test_baseline_drift_annotations_present.py::test_annotation_closure_card_paths_resolve_to_real_files
E       AssertionError: known_runtime_drift_annotations is absent or empty; nothing to resolve...

FAILED tests/invariants/test_baseline_drift_annotations_present.py::test_every_annotation_names_cp_app_js_unify_as_closure_wave
E       AssertionError: known_runtime_drift_annotations is absent or empty; nothing to check...
```

Properties 2, 3, 5 carry `assert annotations` floor guards baked into R-86 authoring (lines 133, 172, 226 of the test file). Those guards presume at least one mirror-drift annotation always exists — the presumption held at R-86 authoring time (3 mirror-drift entries + 3 annotations existed) but breaks at the R-91 wave designed to retire ALL 3 mirror-drift entries + their annotations atomically. The closure card MUST section item 4 cites the set-equality guard (Property 4) as the retirement contract; Properties 2/3/5's floor guards were not anticipated.

**Character of the amendment (per owner verbatim above · condition 1 verbatim):** *"Properties 2, 3, and 5 tolerate an empty annotation set ONLY when the CP_APP_JS_UNIFY card status is SEALED — accidental emptiness before closure stays RED."* This is a **TIGHTENING** re-scope (never loosen): pre-closure emptiness still fires RED (accidental drift caught); post-closure emptiness is a named success. The re-scope removes a false-positive floor that fires under legitimate wave-close, while preserving the anti-drift guard that fires under illegitimate emptiness. Per GPU-staleness precedent verbatim (banked at STATE/DECISIONS.md 2026-09-19T~10:13Z, line 15149): *"that's a tightening, not a loosening, so it resolves at tier 1/3 without an owner round-trip"* — HOWEVER, owner ruled explicitly this-session that this specific amendment goes through the ordinary-tier ceremony (48h), NOT tier 1/3, to bank the amendment as an audit-visible ceremony receipt (per condition 4).

## §4 · Proposed new shape (normative text · applied verbatim at horizon)

### §4.1 · Shared helper (added to top of file, below existing helpers `_load_baseline` and `_annotations`)

```python
# ---------- R-91 ceremony · empty-state tolerance predicate (Path ε · 2026-09-21) ----------

CP_APP_JS_UNIFY_CARD_PATH = STATE_REPO_ROOT / "STATE" / "OBJECTIVES" / "CP_APP_JS_UNIFY.md"
R91_SEALED_EMPTY_MESSAGE = "annotation set empty by ruled closure R-91"


def _r91_closure_sealed() -> bool:
    """True iff the R-91 CP-APP-JS-UNIFY closure card's ``milestone_status``
    line contains the token ``SEALED``. Reads the live card each call so a
    manual revert to SCHEDULED re-arms the floor guard immediately.

    Ceremony authority: Canon 3 §24 rule-change ceremony · ordinary tier ·
    Path ε RATIFIED by owner ruling 2026-09-21T~01:00Z (this-session ·
    verbatim in STATE/DECISIONS.md at ceremony-open commit + at
    apply-seal commit).
    """
    try:
        card = CP_APP_JS_UNIFY_CARD_PATH.read_text(encoding="utf-8")
    except OSError:
        return False
    # Only the first ``milestone_status:`` line is authoritative (the card
    # front-matter). Guard against the token appearing incidentally elsewhere.
    for line in card.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("milestone_status:"):
            return "SEALED" in stripped
    return False
```

### §4.2 · Property 2 amendment (lines 125-154)

Replace the `assert annotations, (...)` block at L133-137 with:

```python
    if not annotations:
        if _r91_closure_sealed():
            # Owner ruling 2026-09-21T~01:00Z · condition 2: named success,
            # never silent pass. Message goes to pytest stdout every run.
            print(R91_SEALED_EMPTY_MESSAGE + " · Property 2 tolerance")
            return
        raise AssertionError(
            "known_runtime_drift_annotations is absent or empty; Ruling 1(a) "
            "requires at least one annotation covering the three pod_shell "
            "mirror-drift baseline entries. (R-91 closure card is not SEALED · "
            "accidental emptiness before closure stays RED · owner ruling "
            "2026-09-21T~01:00Z condition 1.)"
        )
```

The remainder of Property 2 (the `for nodeid, ann in annotations.items():` loop) is unchanged — it runs only when `annotations` is non-empty, unchanged semantics.

### §4.3 · Property 3 amendment (lines 159-189)

Replace the `assert annotations, (...)` block at L172-176 with:

```python
    if not annotations:
        if _r91_closure_sealed():
            print(R91_SEALED_EMPTY_MESSAGE + " · Property 3 tolerance")
            return
        raise AssertionError(
            "known_runtime_drift_annotations is absent or empty; nothing to "
            "resolve. Ruling 1(a) requires annotations for the three pod_shell "
            "mirror-drift baseline entries. (R-91 closure card is not SEALED · "
            "accidental emptiness before closure stays RED · owner ruling "
            "2026-09-21T~01:00Z condition 1.)"
        )
```

The remainder of Property 3 (the `for nodeid, ann in annotations.items():` loop) is unchanged.

### §4.4 · Property 5 amendment (lines 217-240)

Replace the `assert annotations, (...)` block at L226-230 with:

```python
    if not annotations:
        if _r91_closure_sealed():
            print(R91_SEALED_EMPTY_MESSAGE + " · Property 5 tolerance")
            return
        raise AssertionError(
            "known_runtime_drift_annotations is absent or empty; nothing to "
            "check. Ruling 1(a) requires annotations for the three pod_shell "
            "mirror-drift baseline entries. (R-91 closure card is not SEALED · "
            "accidental emptiness before closure stays RED · owner ruling "
            "2026-09-21T~01:00Z condition 1.)"
        )
```

The remainder of Property 5 (the `offenders = {...}` comprehension + assertion) is unchanged.

### §4.5 · Property 4 · UNTOUCHED (per owner condition 3)

Property 4 (`test_annotation_count_equals_mirror_drift_baseline_entry_count`) is NOT amended. Set-equality guard `assert set(annotations.keys()) == covered_mirror_drift` passes at 0 == 0 without modification. Explicit non-touch per owner condition 3 verbatim: "*Property 4 stays untouched.*"

### §4.6 · Property 1 · UNTOUCHED (no floor guard to amend)

Property 1 (`test_every_mirror_drift_baseline_entry_has_an_annotation`) already handles the empty case correctly via `covered_mirror_drift = MIRROR_DRIFT_NODEIDS & baseline` — when baseline is empty, `covered_mirror_drift` is empty, `missing` is empty, `assert not missing` passes vacuously. No amendment needed.

## §5 · Character of the change · TIGHTENING, not LOOSENING

Per GPU-staleness precedent verbatim (STATE/DECISIONS.md line 15149 · this-session applicable): tightening re-scopes clear at ordinary tier; loosening re-scopes require higher tier.

**Tightening evidence for this amendment:**
- Pre-amendment: `assert annotations` fires RED on ANY empty state (accidental drift + legitimate wave-close indistinguishable).
- Post-amendment: RED still fires on accidental drift (card not SEALED). Named success only on legitimate wave-close (card SEALED).
- Discriminator: the R-91 closure card `milestone_status` value. That value is only set to SEALED at the apply-step of the ceremony · a single-write event in the wave's Commit-A.
- Manual revert to SCHEDULED re-arms the floor guard immediately (predicate reads card each call).

**Owner condition 1 reads as tightening:** *"Properties 2, 3, and 5 tolerate an empty annotation set ONLY when the CP_APP_JS_UNIFY card status is SEALED — accidental emptiness before closure stays RED."* Explicit tightening posture.

## §6 · Apply step (schedule)

**Schedule:** at countdown horizon `2026-09-23T03:23:15Z` (48h from filing this proposal).

**Apply-step operations (in order · single Commit-A on `programme/track-a` · dual-branch §3.3 seal follows):**

1. Apply the §4 amendment verbatim (helper + 3 Property replacements + Property 4/1 untouched).
2. Re-run terminal `pytest` on the amended test file — expect all 5 property tests GREEN under empty annotations + SEALED card state.
3. Apply the R-91 mirror per Phase 2 plan:
   - Copy `/app/frontend/src/App.js` (sha `90c8956d…` · 1108 lines merged App.js) → `pod_shell/frontend/src/App.js`.
   - Copy `/app/frontend/src/pages/*` (9 `.jsx` files) → `pod_shell/frontend/src/pages/`.
4. Update `baseline_failures.json` atomically:
   - `baseline_failures[] = []` (5 wrapped → 0).
   - `known_runtime_drift_annotations = {}` (3 mirror-drift → 0).
   - `known_r91_closure_scheduled_receipt_drift_annotations` reduced 3 → 1 (retain `test_cp10_harness_receipt_is_still_recent` per R-88+ Property 1 · retire 2 v8-cascade keys).
   - `counts_at_baseline.passed`: 5695 → 5700 (5 wrapped baselines flipped GREEN).
   - `counts_at_baseline.failed`: 5 → 0.
   - `invariants_enforced_when_baseline_guard_1.passed_floor`: 5695 → 5700.
   - Append `ratchet_history` entry.
5. Flip `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` `milestone_status`: SCHEDULED → SEALED. **This is the single write that activates the Property 2/3/5 tolerance predicate for the FIRST time in the pytest session.**
6. Regenerate `notes/ORCH_BOOT.md` ratchet block (pre-Commit-A per M16-W3 corrected order).
7. Sync POD audit mirror (`/app/frontend/public/audit/ORCH_BOOT.md`) byte-identical.
8. Regenerate CP10 harness ground-truth if freshness window drifts past 48h before apply (currently at 2026-09-21T00:38:25Z · non-vacuous · will still be within window at horizon).
9. Run BASELINE_GUARD=1 double-green byte-identical sweep against `tests/invariants/` — expect 5700+ passed / 0 failed / 1 skipped / stripped-sha256 identical run1 vs run2.
10. Execute §3.3 3-Commit Seal:
    - Commit-A on `programme/track-a`: apply-step amendment + mirror + baseline_failures.json atomic update + closure card SEALED flip + pre-Commit-A ORCH_BOOT ratchet regen + POD audit mirror sync.
    - Commit-B on `master`: state banking (DECISIONS append + NEXT R-91 SEALED marker flip + PINS R-91-PHASE-2-PINS block + this-proposal-referenced ceremony-apply receipt + all drill receipts + harness receipt).
    - Commit-C fixup on `master`: R-6 boundary regen advancing `heads_last_sealed.state_repo.head` to this-CP Commit-B + code_repo history entry for this-CP Commit-A + FE-DISPATCH-READY LOWERED note bank.

## §7 · Discipline reconciliation

- **SO §3.8 (additive-only)** — this ceremony is the AUTHORIZED EXCEPTION per owner ruling this-session verbatim: *"the ceremony is the authorised way a sealed test file changes — a ceremonied amendment is not a §3.8 refactor."*
- **SO §2.5 (verbatim docstring)** — the amendment ADDS documentation lines citing owner ruling + condition 2 message · does not remove or modify the original SO §2.5 docstring of the test module.
- **SO §3 (tests-first)** — the apply-step is not a NEW test authored under RED-first; it's a rule-change ceremony to a sealed test. Pre-apply verification runs the amended tests + full BASELINE_GUARD=1 sweep verifying the ceremony contract holds.
- **SO §3.3 (3-Commit Seal)** — apply-step follows the full 3-Commit Seal precedent (R-92 shape · this-session inheritable).
- **CCS2 (both counters bump together)** — `counts_at_baseline.passed` + `passed_floor` bump together `5695 → 5700`.
- **M16-W3 (pre-Commit-A ORCH_BOOT regen)** — ratchet block regen precedes Commit-A · POD audit mirror sync in same operation.
- **R-86 Property 4 (set-equality)** — untouched by amendment · continues verifying 0 == 0 post-retirement.
- **R-88+ Property 6 (SEALED-vs-vacuous guard)** — activates at the moment card `milestone_status` flips SEALED · harness receipt already non-vacuous 2026-09-21T00:38:25Z · passes at flip moment.

## §8 · Failure modes at apply

- **If pre-apply BASELINE_GUARD=1 sweep is not GREEN**: STOP-AND-REPORT, do NOT seal. Same-turn revert to pre-apply state.
- **If pre-apply harness receipt drifts past 48h freshness window**: regen harness at apply-step operation 8 · precedent shape line 18038.
- **If any invariant regresses (excluding the 5 wrapped baselines flipping GREEN)**: STOP-AND-REPORT, do NOT seal.
- **If `_r91_closure_sealed()` returns False under card SEALED state**: predicate bug · STOP-AND-REPORT.
- **If a wave lands between now and horizon that adds a NEW pod_shell mirror-drift baseline entry**: annotations non-empty · Properties 2/3/5 iterate over the new annotation normally · amendment predicate does not fire · unchanged semantics.
- **If owner manually flips card back to SCHEDULED**: predicate returns False on next test run · floor guard re-arms · matches design intent.

## §9 · Canon anchors verbatim

- **Owner ruling this-session** (2026-09-21T~01:00Z) — banked at ceremony-open commit STATE/DECISIONS.md OWNER RULINGS anchor.
- **Owner GPU-staleness precedent ruling** (2026-09-19T~10:13Z) — line 15149 verbatim: *"a test that measures ritual isn't a floor · dynamic now-anchored fixture dates restore the test to measuring the live property — that's a tightening, not a loosening, so it resolves at tier 1/3 without an owner round-trip."*
- **Owner ceremony-mechanics ruling** (STATE/STANDING_ORDERS.md:437 verbatim): *"ordinary-tier re-scopes that tighten (never loosen) may be proposed and countdown-started without waiting, countersign requested in the batch."*
- **CP-STALENESS-CEREMONY seal chain** (2026-09-20T09:28Z Commit-A `31d414b` + Commit-B `9c0dd840` + Commit-C `23ff5808`) — banked precedent shape.
- **Canon 3 §24** rule-change ceremony 4-step (propose → counter-sign → wait → apply).
- **R-18 effect 12** — 48-hour ordinary-tier countdown.
- **R-86 seal** `2eca0e58d1d9773d1b781abe570c3e015e0c98f2` (schedules R-91 slot + establishes 5-property test pattern under `test_baseline_drift_annotations_present.py`).
- **R-88+ seal chain** `db90089d/79d5d38d/0cbfc23b` (extends annotation umbrella + owner A-extension covering v8-cascade artifacts · Property 6 SEALED-vs-vacuous guard).
- **R-91 closure card** `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` (ratified 2026-09-20T21:55:00Z · milestone_status: SCHEDULED until apply-step).
- **R-91 Phase 1 opening seal** `282ba19e` (this-session · banks FE-DISPATCH-READY flag + HUNT receipt + landing spec).
- **R-92 seal chain** `ceaa24f/19030610/e8f9f168` (immediately-precedes · this-Phase-2-apply opens directly against R-92 Commit-C head or later on master).
- **Standing bounds** (unchanged from R-92): zero push · zero remote configured on `programme/track-a` · terminal `pytest` only · no `testing_agent` (STRICTLY BANNED per SO §6 Long Autonomous Run Protocol) · additive-only §3.8 (with this-ceremonied amendment as the SINGLE authorized exception per owner ruling this-session verbatim) · three-repo discipline · ratchet monotonic-up.

## §10 · Cross-refs

- HUNT receipt (R-91 Phase 1) at `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md`.
- Landing spec (R-91 Phase 1) at `phase0/specs/r91_cp_app_js_unify_spec.md`.
- Shadow-mirror adjudication receipt at `phase0/drill_receipts/20260921T003800Z_r91_phase2_adjudication_shadow_mirror_probe.log` (66 fail under prior deviation).
- Post-followup shadow probe (this-session) at `/tmp/r91_shadow_probe_v2.log` — 2 fail 380 pass; to be banked at apply-step Commit-B.
- Harness ground-truth receipt (non-vacuous · this-session) at `phase0/harness_ground_truth/latest.json` (2026-09-21T00:38:25Z · dummies_declared=37 · marked_slots_count=29 · per_rule=37 · orphan_count=0).

## §11 · Autopilot posture during countdown window (2026-09-21T03:23:15Z → 2026-09-23T03:23:15Z)

Per owner ruling this-session verbatim: *"do NOT idle: open the G5-v5 second slice (below) during the window and apply+seal R-91 at expiry."*

**Second-slice sequencing (owner verbatim in same ruling):** *"Map the rows whose components are already built and sealed, so canon_ref bites on live code: Document 1 (chokepoint, M12) and Document 5 (the Ledger, M10) first; then DAP-1 through DAP-38 (lifecycle and principal model landing); then RBM and ROC (Rules Service). Tier B rows in each family trail their Tier A. Sequence rows 1–565 accordingly."*

Slicing plan sketch (crystallizes as second-slice HUNTs progress · reported in the next seal report per owner directive):
- **Family A — Doc 1 M12 chokepoint** (canon_ref binds to `services/canon/chokepoint/*` + `services/canon/interpretation/*` per M12 seal chain).
- **Family B — Doc 5 M10 Ledger** (canon_ref binds to `services/ledger/*` + `contracts/ledger_v*.py` per M10 seal chain).
- **Family C — DAP-1..DAP-38** (canon_ref binds to `services/dap_lifecycle/*` + `contracts/principal_v1.py` per DAP wave seal chain).
- **Family D — RBM (Rules-By-Machine) + ROC (Rules-Of-Change) — Rules Service** (canon_ref binds to `services/rules_service/*` per Rules Service seal chain).
- **Tier B trails Tier A within each family** — Tier B rows enforce ratifications/exceptions/variants that DEPEND on the Tier A property being live. Tier B slice fires AFTER Tier A slice seals in the same family.
- **Sequence rows 1–565**: mapped by SRR row number range per family. Row numbers pre-authored in the v5 SRR sheet (sha256 `00072c58…` · Ruling 5 authority).

Slice sizes at autopilot discretion for clean seals · each slice fires its own §3.3 3-Commit Seal · owner receives slicing plan (families → slice boundaries → estimated invariant counts) in next seal report.

## §12 · What this proposal is NOT

- NOT a change to Property 1 or Property 4.
- NOT a deletion of any test.
- NOT a modification of the SO §2.5 docstring at module level.
- NOT a change to any other invariant test file.
- NOT a change to `baseline_failures.json` (the manifest edit is a separate apply-step operation covered by R-86 Property 4 discipline).
- NOT a change to any sealed contract, writer, or non-test source file.
- NOT a permit to grow the baseline set (5/5 baselines retire atomically at apply-step per owner condition 5).
- NOT a permit to silently rebaseline · both `counts_at_baseline.passed` and `passed_floor` bump together per CCS2.

## §13 · Ratification path

- **Filer:** main-agent Autopilot (this proposal).
- **Counter-sign:** owner ruling this-session (2026-09-21T~01:00Z) verbatim above · IS the batched counter-sign per STATE/STANDING_ORDERS.md:437.
- **Countdown:** starts at proposal filing (2026-09-21T03:23:15Z) · ends at horizon (2026-09-23T03:23:15Z) · ordinary tier 48h.
- **Apply:** at horizon (or later if a bridging reconcile is needed) · per §6 schedule.

**END OF PROPOSAL.**
