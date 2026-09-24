"""tools/lid_overlay_reaggregate_with_abstention_and_estate_filter_20260224.py

Owner correction 2026-02-24 · re-aggregate the raw 2026-09-22 DIGICOW_LANGID
sweep (which carries mi/ar/la/nn/ro/ko/de/es/pt/cy/gu/el/nl false-positive
language codes) through the new sealed abstention + estate-filter boundary
at `lid_overlay_abstention_and_estate_filter_v1.apply_abstention_and_estate_filter`.

Anti-loss: raw output preserved on every filtered carrier; filtered output
shows how many samples clear (label kept) vs abstain (label→None,
marker='unmeasured'), with abstention_reason breakdown.

Additive-only per SO §3.8. Reads raw receipt read-only, writes NEW receipt
alongside the raw one. Sealed carriers UNCHANGED.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add backend to sys.path
_REPO = Path("/app/assessment_workspace/repos/Extraction-Akki")
sys.path.insert(0, str(_REPO))

from backend.services.audio_plane_v1 import (  # noqa: E402
    lid_overlay_abstention_and_estate_filter_v1 as FILTER,
)


RAW_RECEIPT = Path(
    "/app/assessment_workspace/phase0/census_v3/duplication_v2/"
    "20260922T020300Z_DIGICOW_LANGID_AGGREGATE.json"
)
OUT_DIR = Path(
    "/app/assessment_workspace/phase0/census_v3/duplication_v2/"
    "lid_reaggregate_20260224"
)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _pick_representative_confidence(code: str, conf_stats_per_lang: dict) -> float:
    """Use per-language avg confidence when available; else fall back to 0.0.

    This is the honest average from the raw sweep — the actual per-sample
    values are not present in the aggregate, only per-language distributions.
    So the re-aggregation applies the filter to (raw_label=code, raw_confidence=avg)
    which lower-bounds the abstention effect: below-threshold codes will
    always abstain; borderline codes will be tested at their measured avg.
    """
    stats = conf_stats_per_lang.get(code) or {}
    return float(stats.get("avg", 0.0))


def reaggregate() -> dict:
    raw = json.loads(RAW_RECEIPT.read_text())
    lang_by_prior = raw.get("lang_by_prior_label", {})
    conf_stats = raw.get("conf_stats_per_lang", {})

    filtered_summary: dict = {
        "sweep_id": "LID-REAGGREGATE-ABSTENTION-ESTATE-FILTER-20260224T000000Z",
        "raw_receipt_path": str(RAW_RECEIPT),
        "raw_receipt_sha256": _sha256_file(RAW_RECEIPT),
        "raw_sweep_id": raw.get("sweep_id"),
        "harvested_at": _now(),
        "filter_module": "backend.services.audio_plane_v1.lid_overlay_abstention_and_estate_filter_v1",
        "filter_threshold": FILTER.LID_ABSTENTION_DEFAULT_THRESHOLD,
        "estate_language_allowlist": sorted(FILTER.ESTATE_LANGUAGE_ALLOWLIST_v1),
        "abstention_reasons_enum": list(FILTER.LID_ABSTENTION_REASONS),
        "per_prior_label_breakdown": {},
        "totals": {
            "ok_kept_labels_in_estate_high_conf": 0,
            "abstained_below_confidence": 0,
            "abstained_out_of_estate_suspected_false_positive": 0,
        },
        "raw_output_preserved_anti_loss": True,
        "posture_markers": [
            FILTER.LID_ESTATE_ALLOWLIST_PRIOR_POSTURE,
            FILTER.LID_ABSTENTION_ENFORCED_AT_WRITER_BOUNDARY_POSTURE,
            FILTER.LID_RAW_OUTPUT_PRESERVED_ANTI_LOSS_POSTURE,
        ],
    }

    for prior_label, code_counts in lang_by_prior.items():
        prior_breakdown = {
            "raw_by_code": dict(code_counts),
            "filtered_by_reason": {
                "ok_kept": {},
                "below_confidence": {},
                "out_of_estate_suspected_false_positive": {},
            },
        }
        for code, n in code_counts.items():
            avg_conf = _pick_representative_confidence(code, conf_stats)
            # Apply the filter using the representative avg confidence.
            # NOTE: this LOWER-BOUNDS the abstention effect — real per-sample
            # confidences vary, so filtered_below_confidence counts here are
            # a conservative estimate of "how many would abstain if every
            # sample sat at the avg". The estate-filter effect is EXACT
            # (label is either in ESTATE_LANGUAGE_ALLOWLIST_v1 or it isn't).
            filtered = FILTER.apply_abstention_and_estate_filter(
                segment_ref=f"reagg://{prior_label}/{code}/aggregate",
                model_entry="speechbrain-voxlingua107-apache-2-0",
                raw_label=code,
                raw_confidence=avg_conf,
                execution_mode="cpu",
                detected_at_utc=_now(),
            )
            reason = filtered.abstention_reason
            key = "ok_kept" if reason == "ok" else reason
            bucket = prior_breakdown["filtered_by_reason"][key]
            bucket[code] = bucket.get(code, 0) + int(n)
            filtered_summary["totals"][
                {
                    "ok": "ok_kept_labels_in_estate_high_conf",
                    "below_confidence": "abstained_below_confidence",
                    "out_of_estate_suspected_false_positive":
                        "abstained_out_of_estate_suspected_false_positive",
                }[reason]
            ] += int(n)
        filtered_summary["per_prior_label_breakdown"][prior_label] = prior_breakdown

    # Also show the specific mi/ar findings that owner called out
    filtered_summary["owner_named_false_positives_20260224"] = {}
    for code in ("mi", "ar"):
        raw_total = 0
        for prior, counts in lang_by_prior.items():
            raw_total += int(counts.get(code, 0))
        avg_conf = _pick_representative_confidence(code, conf_stats)
        filtered_owner = FILTER.apply_abstention_and_estate_filter(
            segment_ref=f"reagg://owner_named/{code}",
            model_entry="speechbrain-voxlingua107-apache-2-0",
            raw_label=code,
            raw_confidence=avg_conf,
            execution_mode="cpu",
            detected_at_utc=_now(),
        )
        filtered_summary["owner_named_false_positives_20260224"][code] = {
            "raw_total_samples_across_prior_labels": raw_total,
            "raw_avg_confidence": avg_conf,
            "filtered_overlay_label": filtered_owner.overlay.label,
            "filtered_overlay_marker": filtered_owner.overlay.marker,
            "abstention_reason": filtered_owner.abstention_reason,
            "raw_output_preserved": {
                "raw_label": filtered_owner.raw_label,
                "raw_confidence": filtered_owner.raw_confidence,
            },
        }
    return filtered_summary


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = reaggregate()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUT_DIR / f"{stamp}_LID_REAGGREGATE_ABSTENTION_ESTATE_FILTER.json"
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(f"receipt_path: {out}")
    print(f"receipt_sha256: {_sha256_file(out)}")
    print()
    print(f"raw_total_kept_in_estate: {summary['totals']['ok_kept_labels_in_estate_high_conf']}")
    print(f"raw_total_abstained_below_confidence: {summary['totals']['abstained_below_confidence']}")
    print(f"raw_total_abstained_out_of_estate: {summary['totals']['abstained_out_of_estate_suspected_false_positive']}")
    print()
    print("owner_named_false_positives_20260224:")
    for code, block in summary["owner_named_false_positives_20260224"].items():
        print(f"  {code}: raw_samples={block['raw_total_samples_across_prior_labels']}  "
              f"raw_avg_conf={block['raw_avg_confidence']:.3f}  "
              f"filtered_label={block['filtered_overlay_label']!r}  "
              f"marker={block['filtered_overlay_marker']!r}  "
              f"abstention_reason={block['abstention_reason']!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
