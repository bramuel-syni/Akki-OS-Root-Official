"""Census → commission producer (DR-R10 through doc-studio): the banked, digest-verified estate-intelligence report becomes one
content model (facts, series, options, calculations, claims, receipts with platform_ref, coverage), a six-dimension brief, a
verdict under the standing frame with a manifest generated from that brief, and structure-only deck + paper specs.
Deterministic: zero authoring tokens; the seed is derived from content_id, purpose and commission date (owner ruling 4);
build_stamp is set once at commission creation and frozen. No workbook: the studio's Options/Checks sheets are bound to the
option-model shape (recorded limit)."""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Dict, List

from services.transform_forms.doc_studio.frames import frame_for, verdict_from_frame
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief

GIB = 1024 ** 3
CONFIDENTIALITY = "Tenant confidential"
HOUSE = "house-neutral"


def _gib(value) -> float:
    return round((value or 0) / GIB, 1)


def _ratio(pct) -> float:
    return round((pct or 0) / 100.0, 4)


def commission_id_for(tenant_id: str, content_id: str, purpose: str, day: str) -> str:
    return "com-" + hashlib.sha256(f"{tenant_id}|{content_id}|{purpose}|{day}".encode()).hexdigest()[:12]


def build_content(report: Dict[str, Any], tenant_id: str) -> Dict[str, Any]:
    h, job = report["headline"], report["job_id"]
    ratio_class = "measured" if h["tables_measured"] == h["tables"] else "estimated"
    receipts: Dict[str, Any] = {
        "R01": {"resolves_to": f"Estate intelligence census {job}, digest-verified report (measured {(report.get('measured_at') or '')[:10]}), headline aggregates and per-database measures", "platform_ref": job},
        "R02": {"resolves_to": f"Estate intelligence census {job}, cost_strategies priced at {(report.get('cost_strategies') or {}).get('tariff', {}).get('source') or 'the recorded tariff'}", "platform_ref": job},
        "R03": {"resolves_to": f"Estate intelligence census {job}, data_products readiness scoring (dimensions, grades, blockers)", "platform_ref": job},
    }
    stores = report.get("stores") or {}
    for rid, key, label in (("R04", "obs", "OBS bucket enumeration"), ("R05", "nas", "NAS share enumeration")):
        st = stores.get(key) or {}
        if st.get("measured") and st.get("census_run_id"):
            receipts[rid] = {"resolves_to": f"{label} census run {st['census_run_id']} ({st.get('units', 0):,} {st.get('unit_name', 'units')}, {st.get('bytes_label')})", "platform_ref": st["census_run_id"]}
    dbs = sorted(report["databases"], key=lambda p: -p["bytes"])[:8]
    top_bytes = sum(p["bytes"] for p in dbs)
    strategies = [s for s in (report.get("cost_strategies") or {}).get("items", []) if s.get("bytes")][:8]
    products = report.get("data_products") or []
    facts = {
        "F001": {"label": "Databases", "value": h["databases"], "unit": "databases", "class": "measured", "receipt": "R01"},
        "F002": {"label": "Tables", "value": h["tables"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F003": {"label": "Tables measured", "value": h["tables_measured"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F004": {"label": "Data and index held", "value": _gib(h["bytes_total"]), "unit": "GiB", "class": "measured", "receipt": "R01"},
        "F005": {"label": "Reclaimable before pricing", "value": _gib(h["reclaimable_bytes"]), "unit": "GiB", "class": "estimated", "receipt": "R01"},
        "F006": {"label": "Reclaimable share of bytes", "value": _ratio(h["reclaimable_pct"]), "unit": "pct", "class": "estimated", "receipt": "R01"},
        "F007": {"label": "Exact duplicate rows", "value": _ratio(h["exact_duplicate_pct"]), "unit": "pct", "class": ratio_class, "receipt": "R01"},
        "F008": {"label": "Degraded rows", "value": _ratio(h["degraded_pct"]), "unit": "pct", "class": ratio_class, "receipt": "R01"},
        "F009": {"label": "Rows with empty required-looking fields", "value": _ratio(h["null_bearing_pct"]), "unit": "pct", "class": ratio_class, "receipt": "R01"},
        "F010": {"label": "Sampled rows with PII markers", "value": _ratio(h["pii_pct"]), "unit": "pct", "class": ratio_class, "receipt": "R01"},
        "F011": {"label": "Rows sampled for PII", "value": round(h["pii_rows_checked"] / 1e6, 1), "unit": "m", "class": "measured", "receipt": "R01"},
        "F012": {"label": "Bytes not written for over a year", "value": _ratio(h["stale_pct_of_bytes"]), "unit": "pct", "class": "measured", "receipt": "R01"},
        "F013": {"label": "Rows held", "value": round(h["rows_estimate"] / 1e6, 1), "unit": "m", "class": "estimated", "receipt": "R01"},
        "F014": {"label": "Duplicate table pairs", "value": h["duplicate_table_pairs"], "unit": "pairs", "class": "measured", "receipt": "R01"},
        "F015": {"label": "Empty tables", "value": h["empty_tables"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F016": {"label": "Bytes in the largest databases", "value": _gib(top_bytes), "unit": "GiB", "class": "measured", "receipt": "R01"},
        "F017": {"label": "Dead columns share", "value": round((report.get("degradation") or {}).get("dead_column_share") or 0, 4), "unit": "pct", "class": "measured", "receipt": "R01"},
        "F018": {"label": "Product candidates", "value": len(products), "unit": "candidates", "class": "measured", "receipt": "R03"},
    }
    cs = report.get("cost_strategies") or {}
    if cs.get("monthly_saving_total") is not None:
        facts["F019"] = {"label": f"Priced monthly saving ({cs.get('currency', 'USD')})", "value": round(cs["monthly_saving_total"], 1), "unit": cs.get("currency", "USD"), "class": "estimated", "receipt": "R02"}
    if strategies:
        facts["F020"] = {"label": "Bytes addressed by the three largest strategies", "value": _gib(sum(s["bytes"] for s in strategies[:3])), "unit": "GiB", "class": "estimated", "receipt": "R02"}
        facts["F021"] = {"label": "Bytes addressed by all cost strategies (databases, object and file stores)", "value": _gib(sum(s["bytes"] for s in strategies)), "unit": "GiB", "class": "estimated", "receipt": "R02"}
    series = {
        "S001": {"label": "Data and index by database, GiB", "categories": [f"{p['database']} ({p['readiness']['grade']})" for p in dbs], "values": {"GiB": [_gib(p["bytes"]) for p in dbs]}, "unit": "GiB", "class": "measured", "receipt": "R01"},
        "S002": {"label": "Condition of measured rows", "categories": ["Exact duplicates", "Degraded", "Empty required fields", "PII markers (sampled)", "Stale bytes"],
                 "values": {"Share": [facts["F007"]["value"], facts["F008"]["value"], facts["F009"]["value"], facts["F010"]["value"], facts["F012"]["value"]]}, "unit": "pct", "class": ratio_class, "receipt": "R01"},
    }
    if strategies:
        series["S003"] = {"label": "Reclaimable GiB by cost strategy", "categories": [s["title"][:40] for s in strategies], "values": {"GiB": [_gib(s["bytes"]) for s in strategies]}, "unit": "GiB", "class": "estimated", "receipt": "R02"}
    options = {f"O{i}": {"name": s["title"][:60], "reclaimable_gib": _gib(s["bytes"]), "monthly_saving_usd": round(s.get("monthly_saving") or 0, 1), "class": "estimated", "receipt": "R02"} for i, s in enumerate(strategies[:3], start=1)}
    calculations = {
        "K001": {"label": "Share of tables measured", "formula": "F003 / F002", "inputs": ["F002", "F003"], "unit": "pct"},
        "K002": {"label": "Share of bytes in the largest databases", "formula": "F016 / F004", "inputs": ["F004", "F016"], "unit": "pct"},
    }
    if len(options) == 3:
        calculations["K003"] = {"label": "Share of bytes addressed by all strategies", "formula": "option.reclaimable_gib / F021", "inputs": ["O1", "O2", "O3"], "unit": "pct"}
        calculations["K004"] = {"label": "Three largest strategies' share of bytes addressed", "formula": "F020 / F021", "inputs": ["F020", "F021"], "unit": "pct"}
    claims = {
        "C001": {"text": "{F004} GiB sit in {F001} databases and {F002} tables", "supports": ["F001", "F002", "F004"]},
        "C002": {"text": "Exact duplicates are {F007} of rows; degraded rows {F008}; empty required fields {F009}", "supports": ["F007", "F008", "F009"]},
        "C003": {"text": "{F010} of {F011} sampled rows carry PII markers", "supports": ["F010", "F011"]},
        "C004": {"text": "{F012} of bytes have not been written for over a year; {F015} tables are empty", "supports": ["F012", "F015"]},
        "C005": {"text": "The largest databases hold {K002} of the estate's bytes", "supports": ["F004", "F016"]},
        "C006": {"text": "About {F005} GiB ({F006} of database bytes) looks reclaimable in the databases before pricing", "supports": ["F005", "F006"]},
        "C007": {"text": "Measures cover {K001} of tables; the remaining ratios are estimated from stratified samples", "supports": ["F002", "F003"]},
        "C008": {"text": "Rights are declared at Connect, not measured by the census; every candidate is aggregate or de-identified", "supports": ["F010"]},
        "C009": {"text": "Dead columns are {F017} of measured columns", "supports": ["F017"]},
        "C010": {"text": "{F018} product candidates rank by rows, readiness and dimensions", "supports": ["F018"]},
        "C011": {"text": "{F013} rows are held; {F014} table pairs duplicate each other", "supports": ["F013", "F014"]},
    }
    if "F019" in facts:
        claims["C012"] = {"text": f"Priced strategies bound the monthly saving at {{F019}} {cs.get('currency', 'USD')} at reference list prices", "supports": ["F019"]}
    if "K004" in calculations:
        claims["C013"] = {"text": "Three strategies address {K004} of the {F021} GiB that all cost strategies reach", "supports": ["F020", "F021"]}
    for i, p in enumerate(products[:3], start=1):
        claims[f"C02{i}"] = {"text": f"{p['title']}: grade {p['readiness_grade']}, {p['tables']} tables, {p['rows_estimate']:,} rows (est.); blockers: {' · '.join(p['blockers'][:2]) or 'none recorded'}", "supports": ["F018"]}
    cannot_say = [
        {"gap": "Duplicate, damage, empty-field and PII ratios on sampled tables", "reason": "complete passes where the table allowed it, stratified samples elsewhere", "closes_with": "a complete-pass census on the sampled tables"},
        {"gap": "Rights, licences and semantic similarity", "reason": "not measured; candidates are dimensional readiness only", "closes_with": "rights declared at Connect and bound to each candidate"},
    ]
    for label in h.get("blocked_connections") or []:
        cannot_say.append({"gap": f"Connection {label}", "reason": "could not be read (MySQL GRANT pending)", "closes_with": "owner grants read access; re-census"})
    nas, obs = stores.get("nas") or {}, stores.get("obs") or {}
    if nas.get("measured") and nas.get("duplicate_candidates") is None:
        cannot_say.append({"gap": "NAS duplication", "reason": "the enumeration recorded sizes and dates, not content fingerprints", "closes_with": "a fingerprinting pass over the NAS shares"})
    if obs.get("sources_blocked"):
        cannot_say.append({"gap": f"{obs['sources_blocked']} of {obs['sources']} OBS buckets", "reason": "unreachable (NoSuchBucket / client errors)", "closes_with": "bucket inventory reconciled with the provider"})
    return {"content_id": f"estate-intelligence-{job}", "version": 1, "title": f"Estate intelligence — {job}", "organisation": tenant_id,
            "census_ref": job, "measured_on": (report.get("measured_at") or "")[:10] or "unmeasured",
            "receipts": receipts, "facts": facts, "series": series, "options": options, "calculations": calculations, "claims": claims,
            "coverage": {"covers": f"{h['databases']} databases, {h['tables']:,} tables and {h['bytes_label']} measured by census {job}; ratios are complete-pass where the table allowed it and stratified samples elsewhere. No row value is present in this pack.", "cannot_say": cannot_say}}


def build_brief(content: Dict[str, Any], tenant_id: str, day: str) -> Dict[str, Any]:
    return {"brief_id": f"BR-{day}-{content['census_ref']}", "content_ref": f"{content['content_id']}@{content['version']}",
            "purpose": {"kind": "decide", "statement": f"Enable the estate owner to choose which cost-reduction strategies and data-product candidates to take forward from census {content['census_ref']}, or to defer."},
            "audience": {"who": f"Estate owner and operators · {tenant_id}", "knowledge": "high on the business, mixed on the data estate", "priorities": ["cost reduction", "personal-data exposure and quality", "monetisable products"], "detail": "summary with an evidence appendix"},
            "setting": {"mode": "read-ahead then presented", "presentation_minutes": 15, "read_unattended": True, "printed": True, "ongoing_use": False},
            "content": {"evidence": True, "narrative": True, "financial": True, "diagrams": False, "imagery": False, "appendix": True},
            "brand": {"house": HOUSE, "formality": "formal", "expressiveness": "restrained", "variation_allowed": "within-family"},
            "outputs": [{"format": "pptx", "role": "presented deck", "editable_charts": True}, {"format": "docx", "role": "paper for read-ahead", "editable_charts": False}, {"format": "html", "role": "review surface", "editable_charts": False}],
            "constraints": {"max_deck_slides": 14, "page_size": "A4", "confidentiality": CONFIDENTIALITY}}


def build_deck(content: Dict[str, Any], brief: Dict[str, Any], verdict: Dict[str, Any], seed: str, stamp: str, voice: str) -> Dict[str, Any]:
    has_options = len(content["options"]) == 3
    slides: List[Dict[str, Any]] = [
        {"type": "cover", "title": "{content.title}", "subtitle": "Commission close · measured {content.measured_on}", "org": "{content.organisation}"},
        {"type": "exec_summary", "kicker": "Executive summary", "title": "The estate is large, repetitive in places and mostly personal; reclaimable bytes are known",
         "situation": "{C001}. {C011}.", "complication": "{C002}. {C003}.", "question": "Which cost-reduction strategies and product candidates should the estate owner take forward?",
         "answer": ("{C006}. {C012}. " if "C012" in content["claims"] else "{C006}. ") + "{C008}. The decision is the estate owner's; this pack sets out the measured evidence."},
        {"type": "section", "number": 1, "title": "What the estate holds and how it is conditioned"},
        {"type": "assertion_exhibit", "kicker": "Where the bytes are", "title": "{C005}", "exhibit": {"plate": "bar", "series_ref": "S001", "y_format": "num", "so_what": "{C001}"}},
        {"type": "assertion_exhibit", "kicker": "Condition", "title": "{C002}", "exhibit": {"plate": "bar", "series_ref": "S002", "y_format": "pct", "so_what": "{C007}"}},
        {"type": "assertion_points", "kicker": "Personal data and staleness", "title": "{C003}", "points": ["{C004}", "{C009}", "{C008}"]},
        {"type": "section", "number": 2, "title": "What it costs to keep, and what it could become"},
    ]
    if "S003" in content["series"]:
        slides.append({"type": "assertion_exhibit", "kicker": "Cost", "title": "{C013}" if "C013" in content["claims"] else "{C006}", "exhibit": {"plate": "bar", "series_ref": "S003", "y_format": "num", "so_what": "{C012}" if "C012" in content["claims"] else "{C006}"}})
    if has_options:
        slides.append({"type": "comparison", "kicker": "Strategies", "title": "Three costed strategies sit side by side; the estate owner chooses the order", "columns": ["O1", "O2", "O3"],
                       "rows": [{"label": "Bytes addressed (GiB)", "field": "reclaimable_gib", "format": "num1"}, {"label": "Monthly saving (USD)", "field": "monthly_saving_usd", "format": "num1"}, {"label": "Share of bytes addressed", "calc": "K003", "format": "pct"}],
                       "so_what": "{C006}"})
    product_points = [f"{{C02{i}}}" for i in range(1, 4) if f"C02{i}" in content["claims"]]
    if product_points:
        slides.append({"type": "assertion_points", "kicker": "Products", "title": "{C010}", "points": product_points})
    slides += [{"type": "coverage_limits"}, {"type": "appendix"}]
    return {"spec_type": "deck", "spec_id": f"DK-{content['census_ref']}", "content_ref": brief["content_ref"], "brief_ref": brief["brief_id"], "verdict_ref": verdict["verdict_id"],
            "objective": "decide", "family": "strategy", "voice": voice, "seed": seed, "build_stamp": stamp,
            "furniture": {"deck_id": f"EI-{content['census_ref']}", "confidentiality": CONFIDENTIALITY}, "slides": slides}


def build_paper(content: Dict[str, Any], brief: Dict[str, Any], verdict: Dict[str, Any], seed: str, stamp: str, voice: str) -> Dict[str, Any]:
    has_options = len(content["options"]) == 3
    cost_blocks: List[Dict[str, Any]] = [{"para": ("{C006}. {C012}." if "C012" in content["claims"] else "{C006}.")}]
    if "S003" in content["series"]:
        cost_blocks.append({"figure": {"plate": "bar", "series_ref": "S003", "y_format": "num", "caption": "{C013}" if "C013" in content["claims"] else "{C006}"}})
    if has_options:
        cost_blocks.append({"options_table": {"columns": ["O1", "O2", "O3"], "rows": [{"label": "Bytes addressed (GiB)", "field": "reclaimable_gib", "format": "num1"}, {"label": "Monthly saving (USD)", "field": "monthly_saving_usd", "format": "num1"}, {"label": "Share of bytes addressed", "calc": "K003", "format": "pct"}],
                                              "caption": "Costed strategies; all figures estimated at reference list prices, receipts in appendix"}})
    product_paras = [{"para": f"{{C02{i}}}."} for i in range(1, 4) if f"C02{i}" in content["claims"]]
    return {"spec_type": "paper", "spec_id": f"PP-{content['census_ref']}", "content_ref": brief["content_ref"], "brief_ref": brief["brief_id"], "verdict_ref": verdict["verdict_id"],
            "objective": "decide", "family": "strategy", "voice": voice, "seed": seed, "build_stamp": stamp,
            "furniture": {"paper_id": f"EI-{content['census_ref']} (paper)", "confidentiality": CONFIDENTIALITY},
            "title": "{content.title}", "subtitle": "Commission-close paper for the estate owner",
            "sections": [
                {"heading": "Summary", "blocks": [{"para": "{C001}. {C011}."}, {"para": "{C006}. {C008}. This paper sets out the measured evidence; the decision is the estate owner's."}]},
                {"heading": "1. What the estate holds and how it is conditioned", "blocks": [{"para": "{C005}. {C002}."}, {"figure": {"plate": "bar", "series_ref": "S002", "y_format": "pct", "caption": "{C007}"}}, {"table": {"series_ref": "S001", "caption": "Data and index by database"}}, {"para": "{C003}. {C004}. {C009}."}]},
                {"heading": "2. What it costs to keep", "blocks": cost_blocks},
                {"heading": "3. What the data can do", "blocks": [{"para": "{C010}. {C008}."}] + product_paras},
                {"heading": "4. Coverage and limits", "blocks": [{"coverage_limits": True}]},
                {"heading": "Appendix: receipts", "blocks": [{"receipts": True}]}]}


def commission_from_report(report: Dict[str, Any], tenant_id: str, principal_id: str, now: datetime) -> Dict[str, Any]:
    """All commission files plus the identifiers the store needs. Raises LookupError when no standing frame covers the brief."""
    day = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    content = build_content(report, tenant_id)
    brief = build_brief(content, tenant_id, day)
    frame = frame_for(brief)
    if frame is None:
        raise LookupError("non-routine commission: no standing frame covers this brief and CIF's ideas endpoint is not mounted in this runtime")
    manifest = manifest_from_brief(brief, has_options=len(content["options"]) == 3)
    verdict = verdict_from_frame(frame, brief, f"V-{day}-{content['census_ref']}", manifest, confirmed_by=principal_id, confirmed_at=stamp)
    seed = f"{content['content_id']}/{brief['purpose']['kind']}/{day}"
    return {"commission_id": commission_id_for(tenant_id, content["content_id"], brief["purpose"]["kind"], day), "content_id": content["content_id"], "seed": seed, "build_stamp": stamp,
            "frame_ref": frame["frame_id"], "voice": frame["voice"], "producer": "estate_intelligence", "source_ref": report["job_id"], "title": content["title"],
            "files": {"brief.json": brief, "content.json": content, "verdict.json": verdict,
                      "deck.json": build_deck(content, brief, verdict, seed, stamp, frame["voice"]), "paper.json": build_paper(content, brief, verdict, seed, stamp, frame["voice"])}}
