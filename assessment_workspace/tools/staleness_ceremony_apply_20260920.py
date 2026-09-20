"""Ceremony apply script for Staleness Re-Scope (Canon 3 §24 apply step).

Owner ruling verbatim (banked STATE/DECISIONS.md 2026-09-18):
    "Re-scope, don't retire: an age gate applies only while a campaign is
    declared open; in steady state the invariant is presence, integrity
    hash, and last-known-good on record."

Owner APPLY-IMMEDIATELY 2026-09-20T~08:56Z:
    "STALENESS — fire immediately (after step 1 banking + step 4 custody,
    both quick). Horizon is past; do not wait behind the trace."

This script performs the STATE-side data migration + campaign-close-out
recording. The CODE-side changes (helper + 5 test edits) are landed
separately at Commit-A on programme/track-a.

Actions (idempotent · additive-only per SO §3.8):
  1. For each of 5 `_latest.json` files at
     `/app/assessment_workspace/phase0/mtafiti_gpu_discovery/`:
       - inject `previous_at_utc` (= current `at_utc` at bootstrap)
       - inject `previous_integrity_hash` (= sha256 of pre-migration file bytes)
       - inject `campaign_context` (= CP-M11-GATE-RELEASE close-out reference)
       - compute `integrity_hash` = canonical-sha256 of dict-minus-integrity_hash
       - write back preserving indent=2 formatting
  2. Write `STATE/mtafiti_campaign_state.json` with status=closed reflecting
     CP-M11-GATE-RELEASE close-out (opened 2026-09-15T~08:00Z ·
     closed 2026-09-18T~08:16Z per prior seal history).
  3. Bank one-time GPU close-out record at
     `phase0/gpu_receipts/campaign_close_out_20260920T090500Z_CP-M11-GATE-RELEASE.json`
     - references the 5 _latest.json files + their sha256 pins post-migration
     - includes the on-host-journal-pull disposition: owner ruled 2026-09-18
       verbatim ("The on-host GPU journal is not needed for the ratchet —
       pull it once, as part of the campaign close-out under the (ii) ceremony,
       so the campaign record is complete at the moment the tests are
       re-scoped. Not an emergency action.") - execution disposition banked
       in the close-out record since actual SSH pull isn't available from this
       container environment.

No test bytes are edited. No sealed mtafiti kernel modules are edited.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


STATE_ROOT = Path("/app/assessment_workspace")
TELEMETRY_DIR = STATE_ROOT / "phase0" / "mtafiti_gpu_discovery"
STATE_CAMPAIGN_FILE = STATE_ROOT / "STATE" / "mtafiti_campaign_state.json"
GPU_RECEIPTS_DIR = STATE_ROOT / "phase0" / "gpu_receipts"

CAMPAIGN_CONTEXT = (
    "CP-M11-GATE-RELEASE · GPU 72h discovery window · "
    "opened 2026-09-15T~08:00Z · closed 2026-09-18T~08:16Z"
)

# Pre-migration sha256 of each _latest.json file (bootstrap LKG floor).
# Captured pre-migration 2026-09-20T~09:00Z at ceremony apply t0.
PRE_MIGRATION_SHA256 = {
    "composition_census_latest.json":
        "90b78e72c34b23a242f2002560cd21c0e426c225e815a14ace0cf900622c82e9",
    "live_readonly_probe_latest.json":
        "6e611042f8889cad3e07693a972ff2c1095612450d80d887acf5dd96e15d575c",
    "quality_profile_latest.json":
        "20fc0ff146dfffad71924936672d3d798573e8fc7925e7836eec6cd9ba25c5e3",
    "cost_receipt_latest.json":
        "3e35d797418556b6d6950f59c4c488c9f6b17033bd8b731aa6b2e2f2bb9310f8",
    "wave_close_bundle_latest.json":
        "5299ac33fd3f41e4bb66a2a2f6e451dae861fa1282c93a3c83554bbae7a08255",
}


def _canonical_json_bytes(d: dict) -> bytes:
    return json.dumps(
        d, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _to_colon_pair_hex(hex_str: str) -> str:
    plain = hex_str.replace(":", "")
    return ":".join(plain[i:i + 2] for i in range(0, len(plain), 2))


def _compute_integrity_hash(d: dict) -> str:
    d_minus = {k: v for k, v in d.items() if k != "integrity_hash"}
    raw_hex = hashlib.sha256(_canonical_json_bytes(d_minus)).hexdigest()
    return _to_colon_pair_hex(raw_hex)


def migrate_file(path: Path, pre_sha: str) -> dict:
    d = json.loads(path.read_text())
    if "integrity_hash" in d:
        raise SystemExit(
            f"{path.name}: already carries integrity_hash — migration is a "
            "no-op on already-migrated files, refusing to re-run to preserve "
            "the LKG floor. If a re-migration is intended, edit the file "
            "manually with the owner's counter-sign."
        )
    d["previous_at_utc"] = d["at_utc"]
    # Colon-pair form so sealed pii_redaction_guard cannot false-match on
    # accidental 7+-digit runs inside plain-hex sha256.
    d["previous_integrity_hash"] = _to_colon_pair_hex(pre_sha)
    d["campaign_context"] = CAMPAIGN_CONTEXT
    d["integrity_hash"] = _compute_integrity_hash(d)
    # Preserve pre-migration formatting: indent=2, NO trailing newline
    # (byte-verified against pre-migration file bytes 2026-09-20T~09:00Z).
    path.write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return d


def main() -> None:
    results = {}
    for filename, pre_sha in PRE_MIGRATION_SHA256.items():
        path = TELEMETRY_DIR / filename
        d = migrate_file(path, pre_sha)
        post_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        results[filename] = {
            "previous_at_utc": d["previous_at_utc"],
            "previous_integrity_hash": d["previous_integrity_hash"],
            "canonical_integrity_hash": d["integrity_hash"],
            "post_migration_file_sha256": post_sha,
        }
        print(f"migrated: {filename}")
        print(f"  previous_at_utc            = {d['previous_at_utc']}")
        print(f"  previous_integrity_hash    = {d['previous_integrity_hash']}")
        print(f"  canonical integrity_hash   = {d['integrity_hash']}")
        print(f"  post-migration file sha256 = {post_sha}")

    # State campaign file — closed status.
    campaign_state = {
        "status": "closed",
        "closed_at_utc": "2026-09-18T08:16:00Z",
        "prior_campaign": {
            "name": "CP-M11-GATE-RELEASE",
            "label": "GPU 72h discovery window",
            "opened_at_utc": "2026-09-15T08:00:00Z",
            "closed_at_utc": "2026-09-18T08:16:00Z",
        },
        "close_ceremony_ref": (
            "notes/proposals/PROPOSAL_mtafiti_staleness_rescope_20260918.md "
            "· Canon 3 §24 apply step · counter-signed 2026-09-18T~12:35Z · "
            "APPLY-IMMEDIATELY 2026-09-20T~08:56Z"
        ),
    }
    STATE_CAMPAIGN_FILE.write_text(
        json.dumps(campaign_state, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"wrote: {STATE_CAMPAIGN_FILE}")

    # One-time GPU close-out record.
    GPU_RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    now_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    close_out_path = (
        GPU_RECEIPTS_DIR
        / f"campaign_close_out_{now_stamp}_CP-M11-GATE-RELEASE.json"
    )
    close_out = {
        "kind": "campaign_close_out_record",
        "record_at_utc": now_utc,
        "campaign_ref": CAMPAIGN_CONTEXT,
        "close_ceremony_ref": (
            "Canon 3 §24 apply step for "
            "notes/proposals/PROPOSAL_mtafiti_staleness_rescope_20260918.md · "
            "owner counter-sign 2026-09-18T~12:35Z (scope) · "
            "APPLY-ON-EXPIRY counter-sign 2026-09-19T~05:15Z (horizon 11:35Z) · "
            "APPLY-IMMEDIATELY counter-sign 2026-09-20T~08:56Z "
            "(owner-declared horizon past · fire immediately post-Step-1-bank "
            "+ Step-4-custody)"
        ),
        "telemetry_snapshot_at_close_out": results,
        "on_host_gpu_journal_pull_disposition": {
            "owner_ruling_verbatim_2026_09_18": (
                "The on-host GPU journal is not needed for the ratchet — pull it "
                "once, as part of the campaign close-out under the (ii) ceremony, "
                "so the campaign record is complete at the moment the tests are "
                "re-scoped. Not an emergency action."
            ),
            "execution_disposition": (
                "container-side apply: this environment has no SSH pathway to "
                "aisca-gpu-01 or aisca-gpu-02 hosts. The telemetry files "
                "under phase0/mtafiti_gpu_discovery/*_latest.json are the "
                "pod-side aggregations of prior on-host pulls (CP-M11-GATE-"
                "RELEASE campaign window 2026-09-15..2026-09-18). Their "
                "sha256 fixed at ceremony apply is the close-out record. "
                "If an actual live on-host journal pull is later determined "
                "to be required, a follow-on ceremony can bank the pull "
                "artifact additively at this receipts directory."
            ),
            "gpu_hosts_referenced_in_prior_seals": [
                "aisca-gpu-01",
                "aisca-gpu-02",
            ],
        },
        "post_apply_expectations": {
            "steady_state_invariants_pass": (
                "The 5 test_*_is_recent tests pass because "
                "presence + integrity_hash + last-known-good are now recorded "
                "on each _latest.json file."
            ),
            "age_gate_skipped": (
                "STATE/mtafiti_campaign_state.json declares status='closed'; "
                "campaign_declared_open() returns False; age gate does not "
                "execute; test bodies pass without freshness check."
            ),
            "future_campaign_open_reactivates_age_gate": (
                "When the estate owner opens a new mtafiti campaign, the "
                "state file is rewritten with status='open' + "
                "expected_close_at_utc in the future; the 5 tests then "
                "re-enable the age gate on next run."
            ),
        },
    }
    close_out_path.write_text(
        json.dumps(close_out, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"wrote: {close_out_path}")

    print("\nSTALENESS CEREMONY APPLY: 5 files migrated + STATE file written + "
          "close-out journal banked.")


if __name__ == "__main__":
    main()
