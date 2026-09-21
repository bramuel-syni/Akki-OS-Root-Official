"""Trainer runner orchestration · Doc 17 lines 15, 55, 88-101.

Owner directive verbatim (waveB_grounding_brief.md line 66):
    'trainer runner: LoRA/PEFT + Muon two-arm + Critic Seam gating
     every output + MOAC emission + cost-ledger metering + whitepaper
     on close.'

Orchestration steps (mock seam · CP8 landing):
  1. admit_material()    · TrainingMaterialAdmitV0 refuses if any
                           qualification bit is False (Doc 17 line 15).
  2. open_run()          · TrainingRunV0 shell, status='admitted'.
                           Refuses if recipe_version is not on the
                           adopted recipe seat (A17.4 UnevidencedRecipe).
  3. execute_run()       · ssh_seam.execute_lora_train (mock or real).
                           Status flips to running_mock or running_real.
  4. emit_moac()         · moac_emitter.emit_six_check_card. Status
                           flips to moac_emitted. Critic Seam routes
                           the emitted card (Doc19A-005 Callers-Cover-
                           the-Rule).
  5. close_run()         · Cost-ledger metering row + whitepaper draft +
                           status flips to closed_adopted or
                           closed_rejected based on MOAC accept_for_service.

Every persisted mutation is a fresh upsert to runs.jsonl (see persistence).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from contracts.training_material_admit_v0 import TrainingMaterialAdmitV0
from contracts.training_run_v0 import TrainingRunV0
from services.training_runner import moac_emitter, persistence, ssh_seam


class RecipeSeatEmpty(RuntimeError):
    """A17.4 · run open refused because recipe seat is empty."""


class RecipeNotAdopted(RuntimeError):
    """A17.4 · recipe_version cited but not on the adopted seat."""


class MaterialAdmitNotFound(KeyError):
    """Run open refused because material_admit_ref is unknown."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def admit_material(
    admit_id: str, training_run_id: str, unit_manifest_ref: str, unit_count: int,
    deduped: bool, vad_cleaned: bool, qualified: bool,
    extraction_pipeline_ref: str, rights_state: str = "declared",
    quarantine_reason: str = "",
) -> TrainingMaterialAdmitV0:
    """Doc 17 line 15 · admit material. Contract enforces the three
    qualification bits; missing any -> ValueError with verbatim spec.

    Wave E · CP-E4 · Doc14-020 quarantine-pending-review wiring:
    if rights_state=='unclear', REFUSE to admit and quarantine with
    receipt per owner ruling verbatim: 'admit refuses to pass rights-
    unclear material through; it quarantines with receipt.'"""
    if rights_state == "unclear":
        from services.rights_quarantine import quarantine_admit
        quarantine_admit(
            admit_id=admit_id,
            training_run_id=training_run_id,
            unit_manifest_ref=unit_manifest_ref,
            unit_count=unit_count,
            extraction_pipeline_ref=extraction_pipeline_ref,
            quarantine_reason=quarantine_reason or (
                "rights_state='unclear' — caller did not name a specific "
                "reason; rights posture must be resolved via "
                "/api/rights_quarantine/{admit_id}/{release|refuse}."
            ),
        )
        raise ValueError(
            f"Doc14-020 · rights-unclear material REFUSED at training "
            f"admit (per owner ruling verbatim: 'admit refuses to pass "
            f"rights-unclear material through; it quarantines with "
            f"receipt'). Record quarantined at "
            f"phase0/rights_quarantine/{admit_id}.json awaiting review."
        )
    admit = TrainingMaterialAdmitV0(
        admit_id=admit_id,
        training_run_id=training_run_id,
        unit_manifest_ref=unit_manifest_ref,
        unit_count=unit_count,
        deduped=deduped,
        vad_cleaned=vad_cleaned,
        qualified=qualified,
        extraction_pipeline_ref=extraction_pipeline_ref,
        admitted_at=_now_iso(),
    )
    persistence.append_admit(admit)
    return admit


def open_run(
    run_id: str, recipe_version: str, base_model_id: str,
    adapter_kind: str, material_admit_ref: str,
) -> TrainingRunV0:
    """Doc 17 line 15 · open a run. LoRA/PEFT-only (grammar enforced)
    + recipe seat citation + material admit reference."""
    from services.training import recipe_seat
    if recipe_seat.is_empty_seat():
        raise RecipeSeatEmpty(
            "Doc 17 A17.4 · recipe seat is empty; a run cannot open. Fill "
            "the seat via CP5 optimizer harness (Owner ruling adopted)."
        )
    if recipe_seat.get_by_version(recipe_version) is None:
        raise RecipeNotAdopted(
            f"recipe_version {recipe_version!r} is not on the adopted seat. "
            "A17.4 refuses unevidenced runs."
        )
    if persistence.get_admit(material_admit_ref) is None:
        raise MaterialAdmitNotFound(
            f"material_admit_ref {material_admit_ref!r} not on record; "
            "call admit_material() first."
        )
    run = TrainingRunV0(
        run_id=run_id,
        recipe_version=recipe_version,
        base_model_id=base_model_id,
        adapter_kind=adapter_kind,
        material_admit_ref=material_admit_ref,
        ssh_mode=ssh_seam.current_mode(),
        status="admitted",
        started_at=_now_iso(),
    )
    persistence.upsert_run(run)

    # W11 C CP-C5 warn-followup · Doc 14 §33 citation preparation.
    # Persist a BaselineLine_v0 record so the whitepaper drafted at
    # close time cites an on-disk record (the drafter enforces
    # cites_baseline_line_id resolves to a file in BASELINE_LINES_DIR).
    try:
        import json
        import os
        from pathlib import Path
        from contracts.baseline_line import BaselineLine_v0

        safe_run = run_id.replace("/", "_").replace(":", "_")
        baseline_line_id = f"bl_{safe_run}"
        baseline = BaselineLine_v0(
            baseline_line_id=baseline_line_id,
            training_run_id=run_id,
            starting_model_id=base_model_id,
            starting_model_license_note=(
                "Baseline line auto-minted at run open for whitepaper "
                "citation. Doc 14 §33: whitepaper must cite the "
                "baseline this training extends from."
            ),
            authored_at=_now_iso(),
            authored_by="training_runner.open_run",
        )
        baseline_dir = Path(os.environ.get(
            "BASELINE_LINES_DIR",
            "/app/assessment_workspace/phase0/baseline_lines",
        ))
        baseline_dir.mkdir(parents=True, exist_ok=True)
        target = baseline_dir / f"{baseline_line_id}.json"
        if not target.exists():
            target.write_text(
                json.dumps(baseline.model_dump(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
    except Exception:
        # Non-blocking: the run still opens; the close-time citation
        # check will surface the missing baseline explicitly.
        pass

    # WPW-1 · attach WPW Tier 1 notebook at commissioning:
    #   'The wizard MUST attach to every training run at commissioning.
    #    There is no per-run opt-in and no manual activation.'
    # Zero-influence (WPW-2 · A2): attach_to_run() swallows all
    # exceptions internally; a wizard-side failure MUST NOT bubble
    # into open_run() and alter the run's outcome.
    try:
        from services.wpw import tier1_notebook as _wpw_nb
        _wpw_nb.attach_to_run(run_id)
        _wpw_nb.record_event(
            run_id=run_id,
            event_kind="commissioning_reflection",
            evidence_class="observed",
            run_artefact_ref=f"training_runner.open_run:{run_id}",
            payload={
                "recipe_version": recipe_version,
                "base_model_id": base_model_id,
                "adapter_kind": adapter_kind,
                "material_admit_ref": material_admit_ref,
                "ssh_mode": ssh_seam.current_mode(),
                "opened_at_utc": _now_iso(),
                "note": (
                    "Commissioning reflection auto-emitted by "
                    "training_runner.open_run at run commissioning. "
                    "WPW-3 minimum event set entry #1."
                ),
            },
        )
    except Exception:
        # Non-blocking (WPW-2): wizard is a stenographer, never a
        # participant. Failures in the notebook path stay in the
        # notebook's own error log; the run continues.
        pass

    return run


def execute_run(run_id: str) -> TrainingRunV0:
    """Fire the trainer through the SSH seam (mock or real). Status
    flips to running_mock or running_real depending on env mode."""
    run = persistence.get_run(run_id)
    if run is None:
        raise KeyError(run_id)
    seam_result = ssh_seam.execute_lora_train(
        run.recipe_version, run.base_model_id, run.material_admit_ref,
    )
    running_status = "running_mock" if seam_result.mocked else "running_real"
    payload = run.model_dump()
    payload["status"] = running_status
    updated = TrainingRunV0.model_validate(payload)
    persistence.upsert_run(updated)
    return updated


def emit_moac_for_run(run_id: str) -> Dict[str, Any]:
    """Doc 17 line 90 · six-check MOAC card. Fires seam again to get
    canned measurement inputs, then produces the card. Status flips
    to moac_emitted; moac_card_ref set on the run.
    """
    run = persistence.get_run(run_id)
    if run is None:
        raise KeyError(run_id)
    seam_result = ssh_seam.execute_lora_train(
        run.recipe_version, run.base_model_id, run.material_admit_ref,
    )
    card = moac_emitter.emit_six_check_card(
        run_id=run.run_id,
        seam_result=seam_result,
        lineage_recipe_version=run.recipe_version,
        lineage_base_model_id=run.base_model_id,
    )
    payload = run.model_dump()
    payload["status"] = "moac_emitted"
    payload["moac_card_ref"] = card["moac_card_id"]
    # Doc19A-005 Callers-Cover-the-Rule · route emitted card through
    # the Critic Seam producer-side attestation.
    try:
        from services.critic_pass import producer_seam as _seam
        verdict = _seam.route_through_seam(
            artifact_ref=f"moac_card:{card['moac_card_id']}",
            artifact_content=card["verdict_summary"],
            producing_instance_id="training_runner.emit_moac",
        )
        summary = _seam.verdict_summary(verdict)
        payload["critic_seam_verdict"] = (
            f"critic_pass:{summary.get('findings_count', 0)}_findings"
            f":{summary.get('critic_instance_id', '?')}"
        )
    except Exception as e:
        # Honesty grammar: if the seam refuses / errors, the run notes
        # the refusal rather than pretending the seam ran.
        payload["critic_seam_verdict"] = f"critic_seam_error: {e}"
    updated = TrainingRunV0.model_validate(payload)
    persistence.upsert_run(updated)

    # W11 C · Wave C completion · owner directive 2026-08-26T~12:25Z.
    # Route the MOAC card through the EXISTING registry admission
    # chokepoint (services.model_admission.ceremony.run_admission).
    # The ceremony writes an on-record admission the whitepaper
    # drafter can cite (§33). Mock/floor-failing cards land as
    # outcome='refused', so citation resolves while acceptance
    # stays impossible (Doc 17 line 101 verbatim).
    _fire_admission_ceremony_for_run(
        run_id=run_id, card=card, run=run,
    )

    return {"run": updated.model_dump(), "moac_card": card}


def _fire_admission_ceremony_for_run(
    *, run_id: str, card: Dict[str, Any], run,
) -> str:
    """Build a Doc 14 §33 ModelAcceptanceCard_v0 from the trainer's
    six-check MOAC card and fire the model_admission ceremony
    (services.model_admission.ceremony.run_admission). Returns the
    candidate_model_id that will appear as the substring the
    whitepaper drafter cites.

    Mock/floor-failing cards get REFUSED admission (record written,
    outcome='refused') so §33 citation resolves while acceptance
    stays impossible."""
    from contracts.model_acceptance_card import ModelAcceptanceCard_v0
    from services.model_admission import ceremony as _ma

    safe = run_id.replace("/", "_").replace(":", "_")
    candidate_model_id = f"adapter_{safe}"
    computed_at = _now_iso()

    # Doc 4 §26.1-§26.6 six criteria · derived from the trainer's
    # six-check card. Mock values keep every measured_value at 0.0
    # against unreachable floors (0.99) so ceremony refuses on the
    # first below-floor check while still writing the record.
    def _c(measured_value: float, floor_value: float, unit: str, method: str,
           anchor: str):
        return {
            "measured_value": measured_value,
            "unit": unit,
            "method_of_measurement": method,
            "floor_value": floor_value,
            "canon_anchor": anchor,
        }

    card_payload = {
        "candidate_model_id": candidate_model_id,
        "evidence_source_kind": "uncurated_registry_sample",
        "accuracy_uncurated": _c(
            0.0, 0.99, "kwer_delta",
            (
                "Trainer six-check M-a · mock harness · derived from "
                f"MOAC card {card['moac_card_id']!r} verdict_summary "
                f"'{card.get('verdict_summary', '')}'"
            ),
            "Canon 4 §26.1",
        ),
        "coverage_strata": _c(0.0, 0.99, "coverage_ratio",
                              "Trainer six-check M-b · mock",
                              "Canon 4 §26.2"),
        "refusal_behaviour": _c(0.0, 0.99, "refusal_score",
                                "Trainer six-check M-f · mock (awaits CP8 real flip)",
                                "Canon 4 §26.3"),
        "provenance_integrity": _c(0.0, 0.99, "integrity_score",
                                   "Trainer six-check · mock",
                                   "Canon 4 §26.4"),
        "cost_per_operation": _c(999.0, 0.5, "cost_units",
                                 "Trainer six-check · mock",
                                 "Canon 4 §26.5"),
        "time_to_answer_p95": _c(999.0, 5.0, "seconds",
                                 "Trainer six-check · mock",
                                 "Canon 4 §26.6"),
        "training_lineage_resolved": True,
        "training_lineage_note": (
            f"Trainer run {run_id} · base_model_id={run.base_model_id!r} · "
            f"recipe_version={run.recipe_version!r} · "
            f"material_admit_ref={run.material_admit_ref!r} · "
            f"MOAC card {card['moac_card_id']!r}."
        ),
        "computed_at": computed_at,
    }

    try:
        outcome = _ma.run_admission(card_payload)
        return outcome.model_id
    except Exception as e:
        # Ceremony refused at contract construction (curated benchmark
        # rejection, etc.). Log and fall back to the candidate id so
        # the whitepaper's downstream citation surfaces the honest gap
        # rather than a placeholder. The admission record still gets
        # written by ceremony for the refusal paths that reach step 2+.
        return candidate_model_id


def close_run(run_id: str, moac_card: Dict[str, Any]) -> TrainingRunV0:
    """Owner directive · 'cost-ledger metering + whitepaper on close'.

    Cost-ledger receipt is written into the CROSSING_RECEIPT_DIR that
    services.cost_ledger.ledger already reads on build_entries. Kind
    is 'ssh_seam' (GPU-hour lane); rate resolution happens on the
    ledger's next build. Whitepaper is drafted via
    services.whitepapers.draft; the citation set includes the MOAC
    card + baseline row. Verdict on the run flips to closed_adopted
    iff accept_for_service else closed_rejected.
    """
    import json
    import os
    from pathlib import Path
    run = persistence.get_run(run_id)
    if run is None:
        raise KeyError(run_id)
    # ---- Cost-ledger receipt · ssh_seam lane · rate resolved on ledger read.
    receipts_dir = Path(os.environ.get(
        "CROSSING_RECEIPT_DIR",
        "/app/assessment_workspace/phase0/crossing_receipts",
    ))
    receipts_dir.mkdir(parents=True, exist_ok=True)
    safe_id = run_id.replace("/", "_")
    receipt_id = f"rcp-training-{safe_id}"
    node_id = os.environ.get("AKKI_GPU_HOST", "mock")
    # Pull the seam result again for gpu_hours (deterministic in mock).
    seam_result = ssh_seam.execute_lora_train(
        run.recipe_version, run.base_model_id, run.material_admit_ref,
    )
    receipt = {
        "receipt_id": receipt_id,
        "kind": "ssh_seam",
        "at_iso": _now_iso(),
        "actor": "training_runner",
        "endpoint_host": node_id,
        "residency_region": "estate",
        "masking_tier": "n/a",
        "payload_shape": {
            "training_id": run_id,
            "node_id": node_id,
            "gpu_hours": seam_result.gpu_hours,
            "metering_source": "mock" if seam_result.mocked else "live",
        },
    }
    (receipts_dir / f"{receipt_id}.json").write_text(json.dumps(receipt))
    cost_ref = f"cost_ledger:crossing_receipt:{receipt_id}"

    # ---- Whitepaper on close · CA1-005 · every close draws a whitepaper.
    #      Doc 14 §33 citation invariant: whitepaper MUST resolve to
    #      an on-disk WhitepaperDraft_v0. CP-C5 warn-followup: prior
    #      call site used contract-mismatched field names and lost
    #      required fields (run_ref / drafted_at / drafted_by /
    #      retention_class); the drafter then Pydantic-refused and the
    #      run surfaced a 'whitepaper_draft_error' placeholder.
    whitepaper_ref = ""
    try:
        from services.whitepapers import draft as _wp
        # whitepaper_id pattern: ^wp_[a-z0-9_-]+$
        wp_id = f"wp_{safe_id.lower()}"
        # cites_model_admission_id / cites_baseline_line_id must resolve
        # to on-disk records (drafter enforces §33). emit_moac_for_run
        # routes the MOAC card through the model_admission ceremony
        # (chokepoint) which writes an admission record with
        # candidate_model_id in the filename. Close cites the
        # deterministic admission id here.
        admission_model_id = f"adapter_{safe_id}"
        wp = _wp.draft_whitepaper({
            "whitepaper_id": wp_id,
            "run_ref": run_id,
            "drafted_at": _now_iso(),
            "drafted_by": "training_runner.close_run",
            "cites_model_admission_id": admission_model_id,
            "cites_baseline_line_id": f"bl_{safe_id}",
            "summary_note": (
                f"Trainer run {run_id} closed with MOAC verdict "
                f"'{moac_card['verdict_summary']}'. Uncurated held-out "
                f"acceptance path per Doc 17 line 101."
            ),
            "retention_class": "standard",
        })
        # WhitepaperDraft_v0 exposes .whitepaper_id (attr) or [key].
        wp_id_out = getattr(wp, "whitepaper_id", None) or getattr(wp, "id", None) \
            or (wp.get("whitepaper_id") if isinstance(wp, dict) else None) \
            or wp_id
        whitepaper_ref = f"whitepaper:{wp_id_out}"
    except Exception as e:
        whitepaper_ref = f"whitepaper_draft_error:{e}"

    payload = run.model_dump()
    if moac_card["accept_for_service"]:
        payload["status"] = "closed_adopted"
    else:
        payload["status"] = "closed_rejected"
    payload["moac_card_ref"] = moac_card["moac_card_id"]
    payload["whitepaper_ref"] = whitepaper_ref
    payload["cost_ledger_ref"] = cost_ref
    payload["finished_at"] = _now_iso()
    updated = TrainingRunV0.model_validate(payload)
    persistence.upsert_run(updated)
    return updated


def state_rollup() -> Dict[str, Any]:
    """Rollup for /api/training-runs GET · empty at ship."""
    runs = persistence.read_runs()
    admits = persistence.read_admits()
    return {
        "ship_state": "empty" if not runs and not admits else "populated",
        "runs_count": len(runs),
        "admits_count": len(admits),
        "ssh_seam": ssh_seam.env_report(),
        "runs": [r.model_dump() for r in runs],
        "admits": [a.model_dump() for a in admits],
    }
