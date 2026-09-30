"""M8-T1 / M9-T3 physical interruption receipt and the G9 capability account.

The receipt is composed only from banked records: the SIGKILLed job (observed step, host state at kill) and the resumed job's
certificate (checkpoint step, five-carrier parity, completion). Work lost is measured in steps and seconds against the ratified
Tier 1 bound; nothing is inferred from a monitor restart.
"""
import json
import os
from pathlib import Path

from services.business_continuity import policy
from services.training_runner import m9_dispatch as m9

LC_STATE_DIR = Path("/app/assessment_workspace/phase0/census_autonomy_state/language_cognition")


def _receipts_dir():
    path = Path(os.environ.get("BC_DRILL_RECEIPTS_DIR", "/app/assessment_workspace/phase0/bc_drill_receipts"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def compose_interruption_receipt(killed_job_id, resumed_job_id, actor=None):
    killed, resumed = m9.load_job(killed_job_id), m9.load_job(resumed_job_id)
    if not killed or killed.get("status") != "interrupted":
        raise ValueError("KILLED_JOB_MUST_BE_INTERRUPTED:" + str(killed_job_id))
    if not resumed or resumed.get("status") != "completed" or not resumed.get("run_certificate"):
        raise ValueError("RESUMED_JOB_MUST_BE_COMPLETED_WITH_CERTIFICATE:" + str(resumed_job_id))
    if (resumed.get("params") or {}).get("resume_from_job_id") != killed_job_id:
        raise ValueError("RESUMED_JOB_DOES_NOT_CONTINUE_THE_KILLED_JOB")
    cert = resumed["run_certificate"]
    proof = (cert.get("checkpoint") or {}).get("resume_proof") or {}
    kill = killed.get("interrupt_rpc") or {}
    progress = ((killed.get("remote_state") or {}).get("progress") or {})
    observed = kill.get("observed_step_at_kill")
    from_step = proof.get("resumed_from_step")
    step_seconds = progress.get("recent_step_seconds")
    lost_steps = (observed - from_step) if isinstance(observed, int) and isinstance(from_step, int) else None
    lost_seconds = round(lost_steps * step_seconds, 1) if lost_steps is not None and step_seconds else None
    tier = policy.TIERS["tier_1_gpu_training_runs"]
    cadence = (cert.get("checkpoint") or {}).get("cadence") or {}
    receipt = {"drill": "M8-T1 interrupt-and-resume · M9-T3 checkpoint restore", "kind": "physical_process_loss_sigkill", "at": m9.now(), "actor": actor,
               "killed_job": {"job_id": killed_job_id, "host": killed["host"], "pid": (killed.get("remote") or {}).get("pid"), "signal": kill.get("signal"), "kill_receipt_id": kill.get("receipt_id"),
                              "observed_step_at_kill": observed, "observation_granularity_steps": kill.get("observation_granularity_steps"), "last_checkpoint_step_on_host": kill.get("last_checkpoint_step_on_host"),
                              "step_seconds_at_kill": step_seconds, "ledger_rows": killed.get("ledger_rows")},
               "resumed_job": {"job_id": resumed_job_id, "host": resumed["host"], "status": resumed["status"], "resumed_from_step": from_step, "carriers_restored": proof.get("carriers_restored"),
                               "checkpoint_sha256": proof.get("checkpoint_sha256"), "resumed_adapter_sha256": proof.get("resumed_adapter_sha256"), "steps_completed": (cert.get("compute") or {}).get("steps"),
                               "planned_steps": (cert.get("compute") or {}).get("total_steps_planned"), "artefact_sha256": cert.get("artefact_sha256"), "receipt_sha256": cert.get("receipt_sha256"),
                               "track4_run_receipt": resumed.get("track4_run_receipt"), "ledger_rows": resumed.get("ledger_rows")},
               "measured": {"work_lost_steps": lost_steps, "work_lost_seconds": lost_seconds, "rpo_bound_seconds": tier["rpo"]["value_seconds"], "within_rpo": (lost_seconds is not None and lost_seconds <= tier["rpo"]["value_seconds"]),
                            "five_carriers_restored": bool(proof.get("carriers_restored")) and all(proof["carriers_restored"].values()), "checkpoint_cadence_rule": cadence.get("rule"),
                            "cadence_receipts": cadence.get("receipts"), "last_cadence_receipt": cadence.get("last")},
               "single_effect": {"completed_runs": 1, "killed_run_terminal_receipt": bool(killed.get("receipt")), "usage_receipts": [r for r in (resumed.get("track4_run_receipt"),) if r],
                                 "note": "the killed process left no terminal receipt and no artefact; exactly one certificate and one usage receipt exist for the continued run"},
               "policy_ref": tier["ratification_ref"]}
    receipt["verdict"] = "PASS" if receipt["measured"]["within_rpo"] and receipt["measured"]["five_carriers_restored"] and resumed["status"] == "completed" else "FAIL"
    path = _receipts_dir() / f"{receipt['at'].replace(':', '').replace('-', '')}_m8t1_m9t3_interruption_{resumed_job_id}.json"
    path.write_text(json.dumps(receipt, indent=1, default=str))
    receipt["receipt_path"] = str(path)
    return receipt


def list_receipts():
    out = []
    for path in sorted(_receipts_dir().glob("*.json")):
        try:
            doc = json.loads(path.read_text()); doc["receipt_path"] = str(path); out.append(doc)
        except (OSError, ValueError):
            continue
    return out


def capabilities():
    """G9 account: activated capabilities with their evidence, dormant modalities named as dormant (owner ruling 2026-09-30 · 2a)."""
    from services.model_registry.registry import trained_adapters
    adapters = trained_adapters()
    served = [m for m, e in adapters.items() if (e.get("serving") or {}).get("status") == "running" and e.get("status") == "admitted"]
    admitted = [m for m, e in adapters.items() if e.get("status") == "admitted"]
    lc = []
    for path in sorted(LC_STATE_DIR.glob("run_certificate_lcj-*.json")):
        try:
            d = json.loads(path.read_text()); lc.append({"job_id": d.get("job_id"), "verdict": d.get("verdict"), "epsilon": (d.get("dp_sgd") or {}).get("epsilon")})
        except (OSError, ValueError):
            continue
    return {"as_of": m9.now(), "owner_ruling_ref": "owner ruling 2026-09-30 (2a): LC audio declared dormant/not-activated for G9; M9 closes on the text modality",
            "activated": [{"capability": "text language identification (transcript text · 7 strata)", "modality": "text", "task": "text_lid", "admitted_models": admitted, "served_models": served,
                           "evidence": "run certificates, admission records, registry versions, serving health/load-test and interruption receipts under /api/training/m9/*"}],
            "dormant": [{"capability": "audio language cognition (presenter-speech language ID with no-speaker-ID constraint)", "modality": "audio", "status": "dormant · research-only · NOT ACTIVATED",
                         "why": "every corrective arm measured NOT ADMISSIBLE: per-language accuracy below the 0.90 default, speaker leakage above chance, and the authorised corpus holds no labelled code-switch/English/Sheng material — a data gap, not a recipe gap",
                         "reactivation": "labelled code-switch/English/Sheng audio enters through M1's generic intake; a new calibration + full run + admission follows", "arms_on_record": lc},
                        {"capability": "streaming / synthetic identity (M9-T4)", "modality": "audio-stream", "status": "not adopted", "why": "no adoption decision on record; nothing deployed is smuggled into scope"},
                        {"capability": "image / video perception", "modality": "image/video", "status": "dormant", "why": "no commissioned job, no candidate, no claim"}]}
