"""services.business_continuity.policy — the owner-RATIFIED dynamic tiered recovery policy (BC-CROSS-INV-01).

Owner ruling 2026-09-30 (5a), verbatim answer "5 - a" to: "BC recovery tiers — a. Ratify the 15 Sep dynamic-recovery packet
tiers as proposed." Source packet: assessment_workspace/notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md §B–§F. The packet's
proposed options are bound here exactly as proposed (Tier 3 COMPLIANCE object-lock mode; Tier 4 warm-standby; quarterly drills).

BC-CROSS-INV-02: the `BC_3_PENDING_OVERRIDE` / `BC_4_PENDING_OVERRIDE` sentinels in anchors.py stay in place as "static number
refused"; this structured record supersedes them. Nothing here is a claim that a tier has been DRILLED — drill evidence lives in
phase0/bc_drill_receipts and is reported separately (Tier 4 site restore and real notification delivery are explicitly deferred
by the same ruling: 4-c, 3-d).
"""
from __future__ import annotations

RATIFICATION_REF = ("owner ruling 2026-09-30 (5a): ratify BC_DYNAMIC_RECOVERY_PACKET_20260915 tiers as proposed · recorded in "
                    "assessment_workspace/notes/m8_m9_completion_20260930/OWNER_RULINGS_20260930.md")
PACKET_REF = "assessment_workspace/notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md"

TIERS = {
    "tier_1_gpu_training_runs": {
        "asset_class": "GPU training runs (LoRA fine-tunes · full runs · calibration stages)",
        "rpo": {"value_seconds": 900, "statement": "≤ 15 min of GPU compute (owner verbatim: never lose more than ~10–15 min)"},
        "rto": {"same_host_seconds": 300, "lost_host_seconds": 1800},
        "cost_tier": "LOW-MED",
        "mechanism": {"checkpoint_cadence": "Young/Daly τ ≈ √(2·C·MTBF), recomputed at every checkpoint boundary, capped by the RPO", "mtbf_bootstrap_seconds": 86400,
                      "storage": {"tier_1a": "local host volume, rolling", "tier_1b": "durable off-host copy (shared estate volume) when configured"},
                      "resume_completeness_carriers": ["weights", "optimizer", "scheduler", "data_offset", "rng"]},
        "invariants": {"BC-1-GPU-INV-01": "no run opens without the five carriers declared", "BC-1-GPU-INV-02": "a resume that cannot restore all five carriers refuses",
                       "BC-1-GPU-INV-03": "τ recomputed per boundary and receipted (checkpoint_cadence_receipt.jsonl)", "BC-1-GPU-INV-04": "durable replication is monotonic"},
        "ratification_ref": RATIFICATION_REF,
    },
    "tier_2_ledgers_registry": {
        "asset_class": "append-only truth: control-event Ledger, registries, decision ledgers, receipts",
        "rpo": {"value_seconds": 0, "statement": "~0 · transaction-boundary granularity"},
        "rto": {"same_host_seconds": 300, "lost_host_seconds": 900},
        "cost_tier": "LOW",
        "mechanism": {"archive": "continuous append archive of the hash-chained Ledger to the WORM tier within the bounded window", "archive_window_seconds": 900,
                      "recovery": "point-in-time restore to any committed row; chain integrity re-verified row by row; head countersigned by an independent witness"},
        "invariants": {"BC-2-LEDGER-INV-01": "every ledger write is durable before it returns", "BC-2-LEDGER-INV-02": "archive pushed to WORM within 15 min", "BC-2-LEDGER-INV-03": "quarterly PITR drill"},
        "existing_bounds_preserved": {"ledger_continuity_rto_seconds": 3600, "breach_notification_window_hours": 72},
        "ratification_ref": RATIFICATION_REF,
    },
    "tier_3_worm_artifacts": {
        "asset_class": "artefacts · receipts · seals · certificates · admission records · ledger archives",
        "rpo": {"value_seconds": 0, "statement": "~0 for committed objects"},
        "rto": {"seconds": 3600},
        "cost_tier": "MED",
        "mechanism": {"object_lock_mode": "COMPLIANCE", "versioning": True, "local_emulation": "write-once versioned store with sha-256 receipts until the owner provisions the cloud bucket",
                      "cloud_bucket_provisioning": "OWNER-PROVISIONED · not yet provisioned"},
        "invariants": {"BC-3-WORM-INV-01": "versioned key + immutability receipt per write", "BC-3-WORM-INV-02": "no estate write path can delete/modify a WORM object",
                       "BC-3-WORM-INV-03": "retention set at write time", "BC-3-WORM-INV-04": "quarterly restore drill"},
        "ratification_ref": RATIFICATION_REF,
    },
    "tier_4_site_loss": {
        "asset_class": "whole-site loss",
        "regime": "warm-standby",
        "rpo": {"value_seconds": 900},
        "rto": {"statement": "hours-not-days"},
        "cost_tier": "MED",
        "failover_trigger": {"operator_declaration": True, "liveness_absence_window_seconds": 1800},
        "standby_site": "OWNER-PROVISIONED · not yet provisioned (owner ruling 2026-09-30 4c: T4 site-restore drill deferred)",
        "invariants": {"BC-4-DRILL-INV-01": "quarterly (≤ 90 days between drills)", "BC-4-DRILL-INV-02": "3 artefact classes restored into an isolated environment",
                       "BC-4-DRILL-INV-03": "row counts · checksums · invariant runs", "BC-4-DRILL-INV-04": "receipt at phase0/bc_drill_receipts/", "BC-4-DRILL-INV-05": "failed drill ⇒ MARK write before next drill"},
        "ratification_ref": RATIFICATION_REF,
    },
}

DRILL_CADENCE = {"cadence": "quarterly", "max_days_between_drills": 90, "ratification_ref": RATIFICATION_REF}

DEFERRED_BY_OWNER = {
    "M8-T4 site restore on an isolated replacement environment": "owner ruling 2026-09-30 (4c): deferred",
    "M8-T5 real notification delivery to test recipients": "owner ruling 2026-09-30 (3d): deferred · file-drop alerts remain NOT delivered notices",
}

SENTINEL_SUPERSESSION = {
    "BC_3_PENDING_OVERRIDE": "superseded by TIERS['tier_3_worm_artifacts'] (structured record · not a static number)",
    "BC_4_PENDING_OVERRIDE": "superseded by TIERS['tier_4_site_loss'] (structured record · not a static number)",
}


def policy_view():
    from services.business_continuity import anchors
    anchors.assert_ca1_n5_rto_matches_s10()
    anchors.assert_ca1_n2_window_matches_s11()
    return {"ratification_ref": RATIFICATION_REF, "packet_ref": PACKET_REF, "tiers": TIERS, "drill_cadence": DRILL_CADENCE, "deferred_by_owner": DEFERRED_BY_OWNER,
            "sentinel_supersession": SENTINEL_SUPERSESSION, "canon_bounds": {"S-10 ledger continuity rto_seconds": anchors.S_10_RTO_SECONDS, "S-11 breach window_hours": anchors.S_11_WINDOW_HOURS}}


__all__ = ["RATIFICATION_REF", "PACKET_REF", "TIERS", "DRILL_CADENCE", "DEFERRED_BY_OWNER", "SENTINEL_SUPERSESSION", "policy_view"]
