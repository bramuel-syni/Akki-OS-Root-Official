# CP-AIP-10-TRAINING-RUNS · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §11.6 · Build Sequence #10.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-9 completes · LAST BY CONSTRUCTION).

## Rationale for position (spec §15 verbatim)

> *"Last by construction — the planner refuses to run earlier."*

## Scope

**§11.6 Run governance:**

- Training runs are commissioned jobs under the existing contract:
  - **Quoted before start** (from CP-AIP-8 confidence-interval quote).
  - **Metered during** (existing metering ledger).
  - **Certificated on completion** (new completion certificate).
- Completion certificate records:
  - Compute consumed.
  - Data touched.
  - Manifest hash.
  - Per-stratum results against the Outcome.
  - **Failed strata reported as plainly as passed ones** (§11.6 verbatim).

**§11.5 Provenance through training** (must be enforced by CP-AIP-10):

- Every training example carries its provenance into the training manifest.
- Consequences:
  - Rights are enforceable per example.
  - An example whose rights lapse is identifiable and the affected models enumerable.
  - "The trained model is the customer's property" is a statement backed by a manifest, not an assertion.

## Acceptance criteria (become RED-first pytest invariants)

1. Run without a passed §11.2 calibration → refused by planner (already sealed at CP-AIP-8; this-CP verifies the runner honours the refusal).
2. Completion certificate MUST carry `compute_consumed`, `data_touched`, `manifest_hash`, `per_stratum_results` (§11.6 verbatim).
3. Failed-stratum reporting invariant: `per_stratum_results` for failed strata carries `status="failed"` explicitly (§11.6 verbatim `"as plainly as passed ones"`).
4. Manifest per-example provenance invariant: every training example row has non-empty `provenance_ref` (§11.5 verbatim).
5. Rights-lapse detectability invariant: given a lapsed rights_id, the run manifest yields the enumerable set of affected model_ids.

## New additive modules (proposed shape)

- `services/training_runner/quoted_run.py` — quote-before-start.
- `services/training_runner/metered_run.py` — metering ledger wrapper.
- `services/training_runner/completion_certificate.py` — 4-field certificate (compute · data · manifest · per-stratum).
- `services/training_runner/per_example_provenance.py` — §11.5 per-example manifest.
- `services/training_runner/rights_lapse_detector.py` — §11.5 rights-lapse → model_ids enumerator.
- `contracts/completion_certificate_v0.py` — frozen contract.
- `contracts/training_manifest_v0.py` — frozen contract with per-example provenance shape.
- Test file: `tests/invariants/test_cp_aip_10_training_runs_aip_v1_0_section_11_6.py` (≥5 RED-first pins).

## Sealed carriers to NOT edit

- CP-AIP-7 planner + CP-AIP-8 S&R (upstream consumers · read-only).
- Existing metering + certificate patterns (`services/campaign_infra/`).

## HF-HOLD LIFT (this-session)

Per owner directive 2026-02-23T03:15Z verbatim (LIFT), online HF fetches for base models are permitted during CP-AIP-10 training runs. `local_files_only=True` fallback remains as offline path per SO §3.8.

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-10-TRAINING-RUNS and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD.**
