"""DR-R10 producers: compile existing, receipted platform outputs into DeckSpec_v1 content. No LLM here — deterministic
producers spend zero authoring tokens; figures carry the measurement class the source already declares."""
from __future__ import annotations

from typing import Any, Dict, List

GIB = 1024 ** 3


def _gib(value) -> float:
    return round((value or 0) / GIB, 1)


def estate_intelligence_deck(report: Dict[str, Any], deck_id: str) -> Dict[str, Any]:
    """Estate intelligence census → R4 (commission close) deck. Ratios from sampled tables are `estimated`; counts and bytes `measured`."""
    h, job = report["headline"], report["job_id"]
    refs = [job]
    stores = report.get("stores") or {}
    for key in ("obs", "nas"):
        st = stores.get(key) or {}
        if st.get("measured") and st.get("census_run_id"):
            refs.append(st["census_run_id"])
    ratio_class = "measured" if h["tables_measured"] == h["tables"] else "estimated"
    dbs = sorted(report["databases"], key=lambda p: -p["bytes"])[:8]
    strategies = [s for s in report["cost_strategies"]["items"] if s["bytes"]]
    products = report["data_products"][:6]
    slides: List[Dict[str, Any]] = [
        {"type": "title", "kicker": "Estate intelligence · commission close", "title": report["reading"].split(";")[0].rstrip(".") + ".",
         "notes": "Composed deterministically from the banked, digest-verified census report; no row value is present."},
        {"type": "big_number", "kicker": "What is held", "title": f"{h['bytes_label']} of data and index sit in {h['databases']} databases and {h['tables']:,} tables.",
         "plate": "P11", "figures": [{"value": _gib(h["bytes_total"]), "unit": "GiB", "class": "measured", "receipt_refs": [job], "label": "data + index"}],
         "so_what": f"About {h['reclaimable_label']} ({h['reclaimable_pct']}%) looks reclaimable before pricing."},
        {"type": "table", "kicker": "Condition", "title": "Duplication, damage and personal data are measured on the estate, not assumed.", "plate": "P3",
         "data": {"columns": ["Condition", "Share", "Basis"], "rows": [
             ["Exact duplicate rows", f"{h['exact_duplicate_pct']}%", "complete passes or stratified samples, primary key excluded"],
             ["Degraded rows", f"{h['degraded_pct']}%", "placeholder · mojibake · truncation · invalid format"],
             ["Rows with empty required-looking fields", f"{h['null_bearing_pct']}%", "row-weighted across measured tables"],
             ["Sampled rows with PII markers", f"{h['pii_pct']}%", f"{h['pii_rows_checked']:,} sampled rows, deterministic detector"],
             ["Bytes not written for over a year", f"{h['stale_pct_of_bytes']}%", "latest timestamp column per table"]]},
         "figures": [{"value": h["exact_duplicate_pct"], "unit": "% exact duplicates", "class": ratio_class, "receipt_refs": [job]},
                     {"value": h["pii_pct"], "unit": "% rows with PII markers", "class": ratio_class, "receipt_refs": [job]}],
         "receipt_refs": [job]},
        {"type": "exhibit", "kicker": "Where the bytes are", "title": "Eight databases hold most of the estate.", "plate": "P4",
         "data": {"unit": "GiB", "series": [{"label": f"{p['database']} ({p['readiness']['grade']})", "value": _gib(p["bytes"]), "class": "measured"} for p in dbs]},
         "receipt_refs": [job]},
        {"type": "table", "kicker": "What the data can do", "title": "Aggregate and de-identified products rank by rows, readiness and dimensions.", "plate": "P3",
         "data": {"columns": ["Candidate", "Grade", "Tables", "Rows (est.)", "Blockers"],
                  "rows": [[c["title"], c["readiness_grade"], c["tables"], f"{c['rows_estimate']:,}", " · ".join(c["blockers"][:2]) or "none recorded"] for c in products]},
         "figures": [{"value": len(report["data_products"]), "unit": "candidates", "class": "measured", "receipt_refs": [job]}], "receipt_refs": [job],
         "so_what": "Rights are declared at Connect, not measured by the census; every candidate is aggregate or de-identified."},
    ]
    if strategies:
        slides.append({"type": "exhibit", "kicker": "Cost", "title": "Archive tiering and de-duplication carry most of the reclaimable bytes.", "plate": "P4",
                       "data": {"unit": "GiB", "series": [{"label": s["title"][:48], "value": _gib(s["bytes"]), "class": "estimated"} for s in strategies[:8]]},
                       "receipt_refs": refs, "so_what": report["cost_strategies"]["currency_note"]})
        total = report["cost_strategies"].get("monthly_saving_total")
        if total is not None:
            slides.append({"type": "big_number", "kicker": "Priced", "title": "Priced strategies bound the monthly saving from above.", "plate": "P11",
                           "figures": [{"value": total, "unit": f"{report['cost_strategies'].get('currency')} / month", "class": "estimated", "receipt_refs": refs}],
                           "so_what": "Upper bound at reference list prices; overlaps between strategies are possible."})
    obs, nas = stores.get("obs") or {}, stores.get("nas") or {}
    if obs.get("measured") or nas.get("measured"):
        def row(label, st, unit_name):
            if not st.get("measured"):
                return [label, {"value": None, "unmeasured": True, "caption": "no enumeration receipt"}, {"value": None, "unmeasured": True, "caption": "no enumeration receipt"}, {"value": None, "unmeasured": True, "caption": "no enumeration receipt"}]
            dup = f"{st['duplicate_candidates']:,} ({st['duplicate_pct_of_units']}%)" if st.get("duplicate_candidates") is not None else {"value": None, "unmeasured": True, "caption": "no fingerprints in this pass"}
            return [label, f"{st['units']:,} {unit_name}", st["bytes_label"], dup]
        slides.append({"type": "table", "kicker": "Object and file estate", "title": "Object storage dwarfs the databases; duplication is measured where fingerprints exist.", "plate": "P3",
                       "data": {"columns": ["Store", "Units", "Bytes", "Duplicate candidates"], "rows": [row("OBS buckets", obs, "objects"), row("NAS shares", nas, "files")]},
                       "figures": [{"value": _gib(obs.get("bytes")), "unit": "GiB in OBS", "class": "measured", "receipt_refs": [obs.get("census_run_id")] if obs.get("census_run_id") else refs}],
                       "receipt_refs": refs})
    limits = [{"reason": "sampled_only", "statement": "Duplicate, damage, empty-field and PII ratios come from complete passes where the table allowed it and stratified samples elsewhere.",
               "closing_condition": "A complete-pass census on the sampled tables."},
              {"reason": "rights_withheld", "statement": "Rights, licences and semantic similarity were not measured; candidates are dimensional readiness only.",
               "closing_condition": "Rights declared at Connect and bound to each candidate."}]
    for label in h.get("blocked_connections") or []:
        limits.append({"reason": "blocked_source", "statement": f"Connection {label} could not be read (MySQL GRANT pending).", "closing_condition": "Owner grants read access; re-census."})
    if nas.get("measured") and nas.get("duplicate_candidates") is None:
        limits.append({"reason": "unmeasured", "statement": "NAS duplication is unmeasured: the enumeration recorded sizes and dates, not content fingerprints.", "closing_condition": "A fingerprinting pass over the NAS shares."})
    if obs.get("sources_blocked"):
        limits.append({"reason": "blocked_source", "statement": f"{obs['sources_blocked']} of {obs['sources']} OBS buckets were unreachable (NoSuchBucket / client errors).", "closing_condition": "Bucket inventory reconciled with the provider."})
    return {"deck_id": deck_id, "spec_version": "v1", "register": "R4",
            "meta": {"title": f"Estate intelligence — {report['job_id']}", "audience_line": "Estate owner and operators · RMS", "date": (report.get("measured_at") or "")[:10] or "unmeasured",
                     "rights_posture_ref": "census-only; no extraction or release right is granted by this deck", "sample_deck": False},
            "selection_manifest": {"register_why": "DR-R10: a completed governed census is a commission close → R4", "overrides": []},
            "slides": slides, "coverage_and_limits": {"covered_basis_ref": job, "limits": limits}, "appendix": {"exhibit_index_auto": True, "extra_slides": []}}
