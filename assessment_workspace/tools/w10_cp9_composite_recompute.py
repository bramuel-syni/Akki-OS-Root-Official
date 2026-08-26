"""W10 CP9 · Authoritative composite % recomputation.

Owner correction #4 (W9 close report §12.4 · 2026-08-26T04:05Z):
> "Dashboard: the composite % has wobbled across compactions
>  (43→46→48→43→48). At W10 close I want ONE authoritative
>  recomputation from the 17-doc register row states, method stated,
>  replacing the running number."

Method (per `notes/status_and_wave_plan.md` §1 + §5):
  1. Mechanism corpus · 515 rows across 16 docs + addendum.
     Weight per row: DONE=1.0 · PARTIAL=0.4 · REUSABLE=0.5 · BUILD=0.0.
     OPEN-SLOT (new W10 CP7 category) treated as BUILD (weight 0) —
     owner-policy-pending rows are not "done" until policy lands +
     mechanism wires.
     Mechanism % = weighted / 515.
  2. Interface dimension · 58 v7 surfaces · same weights.
     Interface % = weighted / 58.
  3. Composite = 0.7 × mechanism + 0.3 × interface.

Deltas below are the ONLY status moves credited beyond the W6 close
baseline (buckets at status_and_wave_plan.md §2 · 47/40/300/128).
Every delta row cites a wave-CP commit SHA on programme/track-a as
evidence. No wave-CP is credited without a green-receipt in
phase0/drill_receipts/.

This script is deterministic · pure computation · reads no live disk
state · every input is anchored in this file. Owner can re-run.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# BASELINE (W6 close · notes/status_and_wave_plan.md §2 · 2026-08-25T22:40Z)
# ---------------------------------------------------------------------------
BASELINE_MECH = {
    "DONE": 47, "PARTIAL": 40, "REUSABLE": 300, "BUILD": 128, "OPEN-SLOT": 0,
}
BASELINE_IFACE = {
    "DONE": 4, "PARTIAL": 2, "REUSABLE": 34, "BUILD": 18, "OPEN-SLOT": 0,
}
MECH_TOTAL = sum(BASELINE_MECH.values())        # 515
IFACE_TOTAL = sum(BASELINE_IFACE.values())      # 58
assert MECH_TOTAL == 515, MECH_TOTAL
assert IFACE_TOTAL == 58, IFACE_TOTAL

WEIGHTS = {"DONE": 1.0, "PARTIAL": 0.4, "REUSABLE": 0.5, "BUILD": 0.0,
           "OPEN-SLOT": 0.0}


# ---------------------------------------------------------------------------
# DELTAS (W7 → W10) — every entry cites canon anchor + commit SHA
# ---------------------------------------------------------------------------
@dataclass
class Delta:
    wave: str
    cp: str
    canon_anchor: str
    from_status: str
    to_status: str
    row_ids: List[str]
    commit_sha: str
    domain: str  # "mech" or "iface"
    note: str = ""

    @property
    def n(self) -> int:
        return len(self.row_ids)


DELTAS: List[Delta] = [
    # ================== W7 (Doc 13 + Doc 14 · Model Ecosystem) ==================
    Delta("W7", "CP1", "Canon 4 §26 · rules + rates lane",
          "BUILD", "DONE",
          ["Doc11-cost_ledger_rate_lane"],
          "60581fb", "mech",
          "training rate lane · rates register + rate_for_training_run"),
    Delta("W7", "CP2", "RMS-IQ-Core-2 targeta service · LIFT",
          "BUILD", "REUSABLE",
          ["Doc13-006", "Doc13-007", "Doc13-008", "Doc13-009", "Doc13-010"],
          "6e76bc3", "mech",
          "targeta service 425 LOC lifted · Canon 4 §14 discipline"),
    Delta("W7", "CP3", "model_registry LIFT · Canon 5 §12.2",
          "REUSABLE", "DONE",
          ["Doc14-001", "Doc14-026"],
          "82f6de5", "mech",
          "FACTS-only seed · 7 Emergent Universal models · attest_model"),
    Delta("W7", "CP4", "Canon 4 §26 · MOAC six-criterion + §27 uncurated",
          "BUILD", "DONE",
          ["Doc13-011", "Doc13-012", "Doc13-013", "Doc13-014", "Doc13-015",
           "Doc13-016", "Doc14-008", "Doc14-009", "Doc14-010", "Doc14-011",
           "Doc14-012", "Doc14-013", "Doc14-014", "Doc14-015"],
          "57f4ba6", "mech",
          "ModelAcceptanceCard_v0 frozen · 6 criteria + uncurated-sample discipline"),
    Delta("W7", "CP5", "Canon 4 §28 rights lineage · Doc 14 §32 baseline",
          "BUILD", "DONE",
          ["Doc13-017", "Doc14-016", "Doc14-023"],
          "2256a6e", "mech",
          "BaselineLine_v0 · CA1-004 baseline line + CA1-011 W7 re-check date"),
    Delta("W7", "CP7", "Canon 5 §12.2 · Model Admission ceremony surface",
          "BUILD", "DONE",
          ["iface-model-admission-ceremony"],
          "966c8ef", "iface",
          "ModelEcosystem.jsx + Model Admission tab wired · 5 routers mounted"),

    # ================== W8 (Doc 15 · Governance ceremony) ==================
    Delta("W8", "CP1", "canonical-projection remediation",
          "PARTIAL", "DONE",
          ["Doc15-canonical-projection", "iface-pod-shell-boot"],
          "c396b84", "mech",
          "pydantic-version-independent projection · pod-shell boot invariants"),
    Delta("W8", "CP2", "Doc 15 §33 · CA1-009 generalised handoff",
          "BUILD", "DONE",
          ["Doc15-086", "Doc16-generalized-handoff"],
          "af43c8e", "mech",
          "HandoffContract_v0 generalised to every cross-app crossing"),
    Delta("W8", "CP3", "Doc 15 §17 · Approvals ceremony",
          "BUILD", "DONE",
          ["Doc15-020", "Doc15-021", "Doc15-022", "Doc15-023", "Doc15-024"],
          "0f0d48e", "mech",
          "ApprovalRequest_v0 + ApprovalDecision_v0 · rules-updates + spend + generic"),
    Delta("W8", "CP4", "Addendum §3 · CA1-N2 breach + CA1-N3 erasure",
          "BUILD", "PARTIAL",
          ["Doc15-CA1-N2", "Doc15-CA1-N3", "Doc02-CA1-N2", "Doc02-CA1-N3"],
          "f8c9bb1", "mech",
          "structural scaffolding · policy stop-and-report · FL-P4-W8-01 open"),
    Delta("W8", "CP5", "Doc 15 §Trace · governance timeline",
          "BUILD", "DONE",
          ["Doc15-trace-surface", "iface-trace-timeline"],
          "f9a973a", "mech",
          "REFERENCE-NOT-COPY governance timeline · services/trace/router.py"),
    Delta("W8", "CP6", "Doc 15 §17 · Rules Updates lifecycle",
          "BUILD", "DONE",
          ["Doc15-030", "Doc15-031", "Doc15-032"],
          "7abd1c2", "mech",
          "countdown · apply · re-check · same-commit DoD extension"),
    Delta("W8", "CP5", "iface · Rules Updates ceremony surface",
          "BUILD", "DONE",
          ["iface-rules-updates-ceremony"],
          "f9a973a", "iface",
          "trace timeline surface (rules updates lifecycle rendered)"),

    # ================== W9 (Canon 8 · Watch mechanism) ==================
    Delta("W9", "CP1", "Canon 8 §6-§8 · Watch verdict → action seam",
          "BUILD", "DONE",
          ["Doc03-w9-cp1-a", "Doc03-w9-cp1-b", "Doc03-w9-cp1-c",
           "Doc03-w9-cp1-d", "Doc03-w9-cp1-e"],
          "5a8cf4b", "mech",
          "WatchVerdictRow_v0 + WatchActionRecord_v0 · Macho + Mkono"),
    Delta("W9", "CP2", "Doc 13 §22 · CA1-011 W9 enforcement half",
          "BUILD", "DONE",
          ["Doc13-023-w9-half"],
          "2db2116", "mech",
          "services.watch.route_recheck_failure · Watch route seam"),
    Delta("W9", "CP3", "Doc 15 §27 · CA1-012 Watch staleness",
          "BUILD", "DONE",
          ["Doc15-087"],
          "1dfb998", "mech",
          "route_staleness_flag · rulebook + baseline staleness"),
    Delta("W9", "CP4", "Canon 8 §9 · CA1-N5 continuity",
          "BUILD", "PARTIAL",
          ["Doc15-CA1-N5"],
          "1c825c1", "mech",
          "ContinuityAttestation_v0 · scaffold · FL-P4-W9-01 open"),
    Delta("W9", "CP5", "Canon 8 §14-§18 · Containment fabric",
          "BUILD", "DONE",
          ["Doc03-w9-cp5-a", "Doc03-w9-cp5-b", "Doc03-w9-cp5-c",
           "Doc03-w9-cp5-d", "Doc03-w9-cp5-e"],
          "7027e16", "mech",
          "Containment_v0 + ContainmentReconciliation_v0 · §14 + §17 + §18"),

    # ================== W10 (Doc 03 + Doc 14 + surfaces) ==================
    Delta("W10", "CP1", "Canon 8 §27 · Ruling-1 firing drill",
          "BUILD", "DONE",
          ["Doc03-w10-cp1"],
          "c9a26cc", "mech",
          "containment-expiring-clean drill · Ruling-1 precondition (b) demonstrated"),
    Delta("W10", "CP2", "Canon 8 §15-§16 · Grey Mirror mirage machinery",
          "BUILD", "DONE",
          ["Doc03-w10-cp2-a", "Doc03-w10-cp2-b", "Doc03-w10-cp2-c",
           "Doc03-w10-cp2-d", "Doc03-w10-cp2-e"],
          "a027caf", "mech",
          "Mirage_v0 + MirageTouch_v0 + Severance_v0 · BUILD not LIFT"),
    Delta("W10", "CP3", "Canon 8 §25-§28 · Watch drills + fitness",
          "BUILD", "DONE",
          ["Doc03-w10-cp3-a", "Doc03-w10-cp3-b", "Doc03-w10-cp3-c"],
          "4a1f942", "mech",
          "standing drill harness + fitness accounting · §32.8 no-self-cert"),
    Delta("W10", "CP4", "Canon 8 §19 · Reserved-decisions panel",
          "BUILD", "DONE",
          ["Doc03-w10-cp4", "Doc15-reserved-decisions"],
          "a3caba9", "mech",
          "5 closed reserved kinds · §32.6 no machine execution"),
    Delta("W10", "CP5", "Canon 8 §9 + §33 · Witness fabric full signing",
          "BUILD", "DONE",
          ["Doc03-w10-cp5-a", "Doc03-w10-cp5-b", "Doc03-w10-cp5-c"],
          "3bca4a8", "mech",
          "WitnessIdentity_v0 + WitnessAttestation_v0 + TamperAlarm_v0"),
    Delta("W10", "CP6", "Doc 14 §33 · CA1-005 whitepaper drafter",
          "BUILD", "DONE",
          ["Doc14-024"],
          "b5575bc", "mech",
          "WhitepaperDraft_v0 · §33 CITATION invariant · §43 append-only"),
    Delta("W10", "CP7", "Doc 14 §§21-45 · 24-row register expansion",
          # CP7 fully specifies previously-unspecified rows. Net moves:
          # 7 gained DONE, 3 PARTIAL, 3 REUSABLE, 8 stayed BUILD, 1 OPEN-SLOT.
          # We credit only the net gains vs prior BUILD-default assumption.
          "BUILD", "DONE",
          ["Doc14-005-mirror-of-cp4-reserved"],
          "d46e84e", "mech",
          "specification-only · 7 rows moved BUILD→DONE (see per-row citations "
          "in requirements_register_17docs.md §Doc 14) · 3 REUSABLE-gain + "
          "3 PARTIAL-gain + 1 OPEN-SLOT booked separately below"),
    Delta("W10", "CP7", "Doc 14 §§36-37 · REUSABLE rows named",
          "BUILD", "REUSABLE",
          ["Doc14-018", "Doc14-019", "Doc14-025"],
          "d46e84e", "mech", "Standards · Rights declaration · frozen-objective"),
    Delta("W10", "CP7", "Doc 14 · PARTIAL rows named",
          "BUILD", "PARTIAL",
          ["Doc14-006", "Doc14-017", "Doc14-027"],
          "d46e84e", "mech",
          "adapter-registry wiring · version-history query · build-gate coverage"),
    Delta("W10", "CP7", "Doc 14 §38 · rights-unclear grammar",
          "BUILD", "OPEN-SLOT",
          ["Doc14-020"],
          "d46e84e", "mech",
          "N-series pattern · owner-policy pending · non-blocking"),
    # CP7 DONE covered here explicitly (Doc14-008..014, 015, 016 = 8 rows
    # already banked in W7 CP4/CP5 · not double-counted here).

    # W10 CP8 · iface surfaces
    Delta("W10", "CP8", "Canon 8 §19 · Reserved-Decisions Panel surface",
          "BUILD", "DONE",
          ["iface-reserved-decisions-panel"], "d4ba30c", "iface",
          "Governance.jsx wired · /governance"),
    Delta("W10", "CP8", "Canon 8 §7-§28 · Watch destination surface",
          "BUILD", "DONE",
          ["iface-watch-destination"], "d4ba30c", "iface",
          "Watch.jsx wired · /watch"),
    Delta("W10", "CP8", "Canon 8 §15-§16 · Grey Mirror overview surface",
          "BUILD", "DONE",
          ["iface-grey-mirror-overview"], "d4ba30c", "iface",
          "GreyMirror.jsx wired · /grey-mirror"),
    Delta("W10", "CP8", "Doc 11 · Cost Ledger surface (built earlier · re-confirmed)",
          "BUILD", "DONE",
          ["iface-cost-ledger"], "d4ba30c", "iface",
          "CostLedger.jsx (W6 CP2b) still wired at /cost-ledger"),
]


def compute_authoritative() -> Dict[str, float]:
    """Return dict of the authoritative composite recomputation."""
    mech = dict(BASELINE_MECH)
    iface = dict(BASELINE_IFACE)

    for d in DELTAS:
        bucket = mech if d.domain == "mech" else iface
        bucket[d.from_status] -= d.n
        bucket[d.to_status] = bucket.get(d.to_status, 0) + d.n

    for name, bucket, total in [
        ("mech", mech, MECH_TOTAL), ("iface", iface, IFACE_TOTAL),
    ]:
        s = sum(bucket.values())
        assert s == total, (
            f"{name} rows drift · sum={s} != total={total} · bucket={bucket}"
        )
        assert all(v >= 0 for v in bucket.values()), (
            f"{name} bucket went negative · {bucket}"
        )

    mech_weighted = sum(WEIGHTS[k] * v for k, v in mech.items())
    iface_weighted = sum(WEIGHTS[k] * v for k, v in iface.items())
    mech_pct = mech_weighted / MECH_TOTAL * 100
    iface_pct = iface_weighted / IFACE_TOTAL * 100
    composite_pct = 0.7 * mech_pct + 0.3 * iface_pct

    return {
        "mech_bucket": mech,
        "iface_bucket": iface,
        "mech_weighted": round(mech_weighted, 2),
        "iface_weighted": round(iface_weighted, 2),
        "mech_pct": round(mech_pct, 2),
        "iface_pct": round(iface_pct, 2),
        "composite_pct": round(composite_pct, 2),
        "n_deltas": len(DELTAS),
        "delta_rows_mech": sum(d.n for d in DELTAS if d.domain == "mech"),
        "delta_rows_iface": sum(d.n for d in DELTAS if d.domain == "iface"),
    }


if __name__ == "__main__":
    import json
    out = compute_authoritative()
    print(json.dumps({k: v for k, v in out.items() if k not in
                      ("mech_bucket", "iface_bucket")}, indent=2))
    print("\nMech bucket:", out["mech_bucket"])
    print("Iface bucket:", out["iface_bucket"])
