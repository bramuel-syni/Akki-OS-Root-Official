"""Census → commission producer (DR-R10 through doc-studio): the banked, digest-verified estate-intelligence report becomes one
content model (facts, series, options, calculations, claims, receipts with platform_ref, coverage), a six-dimension brief, a
verdict under the standing frame with a manifest generated from that brief, and structure-only deck + paper specs.
Deterministic: zero authoring tokens; the seed is derived from content_id, purpose and commission date (owner ruling 4);
build_stamp is set once at commission creation and frozen. The workbook declares its option rows and checks in the spec
(doc-studio v1.2, owner ruling 3a) so strategy bytes, monthly saving and share checks are carried honestly."""
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
        "C008": {"text": "The estate owner has declared that all data in the estate is owned outright and every right to use it is established; the census measures condition, not rights", "supports": ["F010"]},
        "C009": {"text": "Dead columns are {F017} of measured columns", "supports": ["F017"]},
        "C010": {"text": "{F018} product candidates rank by rows, readiness and dimensions", "supports": ["F018"]},
        "C011": {"text": "{F013} rows are held; {F014} table pairs duplicate each other", "supports": ["F013", "F014"]},
    }
    if "F019" in facts:
        claims["C012"] = {"text": f"Priced strategies bound the monthly saving at {{F019}} {cs.get('currency', 'USD')} at reference list prices", "supports": ["F019"]}
    if "K004" in calculations:
        claims["C013"] = {"text": "Three strategies address {K004} of the {F021} GiB that all cost strategies reach", "supports": ["F020", "F021"]}
    for i, p in enumerate(products[:3], start=1):
        blockers = [b for b in p['blockers'] if 'rights' not in b.lower()][:2]
        claims[f"C02{i}"] = {"text": f"{p['title']}: grade {p['readiness_grade']}, {p['tables']} tables, {p['rows_estimate']:,} rows (est.); to prepare: {' · '.join(blockers) or 'nothing recorded'}", "supports": ["F018"]}
    cannot_say = [
        {"gap": "Duplicate, damage, empty-field and PII ratios on sampled tables", "reason": "complete passes where the table allowed it, stratified samples elsewhere", "closes_with": "a complete-pass census on the sampled tables"},
        {"gap": "Semantic similarity between candidate datasets and the market", "reason": "not measured; candidates are dimensional readiness only", "closes_with": "a buyer-side review of each candidate against its intended use"},
    ]
    for label in h.get("blocked_connections") or []:
        cannot_say.append({"gap": f"Connection {label}", "reason": "could not be read (MySQL GRANT pending)", "closes_with": "owner grants read access; re-census"})
    nas, obs = stores.get("nas") or {}, stores.get("obs") or {}
    if nas.get("measured") and nas.get("duplicate_candidates") is None:
        cannot_say.append({"gap": "NAS duplication", "reason": "the enumeration recorded sizes and dates, not content fingerprints", "closes_with": "a fingerprinting pass over the NAS shares"})
    if obs.get("sources_blocked"):
        cannot_say.append({"gap": f"{obs['sources_blocked']} of {obs['sources']} OBS buckets", "reason": "unreachable (NoSuchBucket / client errors)", "closes_with": "bucket inventory reconciled with the provider"})
    _estate_wide(report, facts, series, calculations, claims, receipts)
    story = _story(facts, series, options, claims)
    return {"content_id": f"estate-intelligence-{job}-estatewide", "version": 1, "title": f"Estate-wide intelligence — {job}", "organisation": tenant_id,
            "census_ref": job, "measured_on": (report.get("measured_at") or "")[:10] or "unmeasured",
            "receipts": receipts, "facts": facts, "series": series, "options": options, "calculations": calculations, "claims": claims, "story": story,
            "owner_declarations": OWNER_DECLARATIONS,
            "coverage": {"covers": f"The whole admitted estate as measured by census {job}: {h['databases']} databases and {h['tables']:,} tables ({h['bytes_label']}), the object store and the file shares enumerated by their own census runs. Ratios are complete-pass where the table allowed it and stratified samples elsewhere. No row value is present in this pack.", "cannot_say": cannot_say}}


OWNER_DECLARATIONS = [
    "The estate owner owns all data in the estate and has declared every right to use it established (owner statement, 2 October 2026). Rights are therefore settled facts, not open questions, and no recommendation is conditional on them.",
    "Personal-data markers remain a measured condition of the rows: de-identification or aggregation is a preparation step for a product, not a rights question.",
]


def _tib(value) -> float:
    return round((value or 0) / 2 ** 40, 2)


def _estate_wide(report, facts, series, calculations, claims, receipts) -> None:
    """Facts and exhibits for the object store and the file shares, and the estate total, so the pack reads estate-wide rather than database-first."""
    stores = report.get("stores") or {}
    obs, nas = stores.get("obs") or {}, stores.get("nas") or {}
    db_bytes = report["headline"]["bytes_total"]
    facts["F052"] = {"label": "Database data and index", "value": _tib(db_bytes), "unit": "TiB", "class": "measured", "receipt": "R01"}
    by_store, store_cats = [_tib(db_bytes)], ["Databases"]
    if obs.get("measured"):
        rid = "R04" if "R04" in receipts else "R01"
        facts.update({
            "F030": {"label": "Object store (OBS) held", "value": _tib(obs["bytes"]), "unit": "TiB", "class": "measured", "receipt": rid},
            "F031": {"label": "Objects enumerated", "value": round(obs["units"] / 1e6, 1), "unit": "m", "class": "measured", "receipt": rid},
            "F032": {"label": "OBS buckets", "value": obs["sources"], "unit": "buckets", "class": "measured", "receipt": rid},
            "F033": {"label": "OBS buckets unreadable", "value": obs.get("sources_blocked") or 0, "unit": "buckets", "class": "measured", "receipt": rid},
            "F034": {"label": "OBS duplicate-candidate bytes", "value": _tib(obs.get("duplicate_bytes_estimate")), "unit": "TiB", "class": "estimated", "receipt": rid, "measurement_scope": "size-and-name candidates, not content-hash confirmed"},
            "F035": {"label": "OBS objects that are duplicate candidates", "value": _ratio(obs.get("duplicate_pct_of_units")), "unit": "pct", "class": "estimated", "receipt": rid},
            "F036": {"label": "OBS bytes not written for over a year", "value": _tib(obs.get("cold_bytes")), "unit": "TiB", "class": "measured", "receipt": rid},
            "F037": {"label": "OBS buckets cold for over a year", "value": obs.get("cold_sources") or 0, "unit": "buckets", "class": "measured", "receipt": rid},
        })
        top = sorted(obs.get("top_sources") or [], key=lambda t: -t["bytes"])[:8]
        if top:
            series["S005"] = {"label": "Largest OBS buckets, TiB", "categories": [f"{t['label']}{' (cold)' if t.get('cold') else ''}" for t in top], "values": {"TiB": [_tib(t["bytes"]) for t in top]}, "unit": "TiB", "class": "measured", "receipt": rid}
            facts["F038"] = {"label": "Bytes in the largest OBS bucket", "value": _tib(top[0]["bytes"]), "unit": "TiB", "class": "measured", "receipt": rid}
            calculations["K008"] = {"label": "Largest bucket's share of the object store", "formula": "F038 / F030", "inputs": ["F030", "F038"], "unit": "pct"}
        calculations["K009"] = {"label": "Cold share of the object store", "formula": "F036 / F030", "inputs": ["F030", "F036"], "unit": "pct"}
        by_store.append(_tib(obs["bytes"])); store_cats.append("Object store (OBS)")
        claims["C030"] = {"text": "The object store holds {F030} TiB in {F032} buckets; {F036} TiB ({K009}) has not been written for over a year and {F034} TiB are duplicate candidates", "supports": ["F030", "F032", "F034", "F036"]}
    if nas.get("measured"):
        rid = "R05" if "R05" in receipts else "R01"
        facts.update({
            "F040": {"label": "File shares (NAS) held", "value": _tib(nas["bytes"]), "unit": "TiB", "class": "measured", "receipt": rid},
            "F041": {"label": "Files enumerated", "value": round(nas["units"] / 1e6, 1), "unit": "m", "class": "measured", "receipt": rid},
            "F042": {"label": "NAS shares", "value": nas["sources"], "unit": "shares", "class": "measured", "receipt": rid},
        })
        top = sorted(nas.get("top_sources") or [], key=lambda t: -t["bytes"])[:8]
        if top:
            series["S006"] = {"label": "Largest NAS shares, TiB", "categories": [t["label"] for t in top], "values": {"TiB": [_tib(t["bytes"]) for t in top]}, "unit": "TiB", "class": "measured", "receipt": rid}
        by_store.append(_tib(nas["bytes"])); store_cats.append("File shares (NAS)")
        claims["C031"] = {"text": "The file shares hold {F040} TiB in {F042} shares and {F041} million files; their duplication is not yet measured", "supports": ["F040", "F041", "F042"]}
    facts["F050"] = {"label": "Whole estate held (databases, object store, file shares)", "value": round(sum(by_store), 2), "unit": "TiB", "class": "measured", "receipt": "R01"}
    series["S004"] = {"label": "Estate bytes by store, TiB", "categories": store_cats, "values": {"TiB": by_store}, "unit": "TiB", "class": "measured", "receipt": "R01"}
    if "F030" in facts: calculations["K005"] = {"label": "Object store share of the estate", "formula": "F030 / F050", "inputs": ["F030", "F050"], "unit": "pct"}
    if "F040" in facts: calculations["K006"] = {"label": "File-share share of the estate", "formula": "F040 / F050", "inputs": ["F040", "F050"], "unit": "pct"}
    calculations["K007"] = {"label": "Database share of the estate", "formula": "F052 / F050", "inputs": ["F050", "F052"], "unit": "pct"}
    claims["C032"] = {"text": "The whole estate holds {F050} TiB; the databases are {K007} of it", "supports": ["F050", "F052"]}


def _story(facts, series, options, claims):
    """The chapters the pack must tell, in order; each names the question it answers, the evidence that answers it and the exhibit that shows it."""
    chapters = [
        {"question": "How big is the whole estate and where do the bytes sit — databases, object store or file shares?",
         "answers_with": [t for t in ("F050", "F030", "F040", "F052", "K005", "K006", "K007", "F038", "K008") if t in facts or t in ("K005", "K006", "K007", "K008")], "exhibits": [s for s in ("S004", "S005") if s in series]},
        {"question": "Where is money being spent on bytes nobody touches, and how much could each move save?",
         "answers_with": [t for t in ("F036", "K009", "F034", "F035", "F037", "F019", "F020", "F021", "K004") if t in facts or t.startswith("K")], "exhibits": [s for s in ("S003",) if s in series], "kind": "comparison" if len(options) == 3 else "points"},
        {"question": "What condition are the database rows in — duplication, damage, completeness and personal-data markers?",
         "answers_with": ["F007", "F008", "F009", "F010", "F011", "F012", "F013", "F014", "F015", "F017"], "exhibits": [s for s in ("S002", "S001") if s in series]},
        {"question": "Which data products could the estate stand up first, and what preparation does each need?",
         "answers_with": [t for t in ("F018", "C021", "C022", "C023") if t in facts or t in claims]},
        {"question": "What is still unmeasured across the estate, and what would it take to measure it?",
         "answers_with": [t for t in ("F003", "F002", "F033", "F040", "F041") if t in facts]},
    ]
    return [c for c in chapters if c["answers_with"]]


def build_brief(content: Dict[str, Any], tenant_id: str, day: str) -> Dict[str, Any]:
    return {"brief_id": f"BR-{day}-{content['census_ref']}", "content_ref": f"{content['content_id']}@{content['version']}",
            "purpose": {"kind": "decide", "statement": f"Give the estate owner one estate-wide account from census {content['census_ref']} — databases, object store and file shares — of what is held, what it costs to keep, what condition it is in and which data products to stand up first, so the owner can decide what to do first."},
            "audience": {"who": f"Estate owner and operators · {tenant_id}", "knowledge": "high on the business, mixed on the data estate", "priorities": ["the whole estate, not one store", "cost reduction with its certainty stated", "data condition and personal-data exposure as preparation work", "monetisable products and what each needs first"], "detail": "summary with an evidence appendix"},
            "setting": {"mode": "read-ahead then presented", "presentation_minutes": 15, "read_unattended": True, "printed": True, "ongoing_use": False},
            "content": {"evidence": True, "narrative": True, "financial": True, "diagrams": False, "imagery": False, "appendix": True},
            "brand": {"house": HOUSE, "formality": "formal", "expressiveness": "restrained", "variation_allowed": "within-family"},
            "outputs": [{"format": "pptx", "role": "presented deck", "editable_charts": True}, {"format": "docx", "role": "paper for read-ahead", "editable_charts": False},
                        {"format": "xlsx", "role": "model workbook: inputs, options, series and cross-checks", "editable_charts": False}, {"format": "html", "role": "review surface", "editable_charts": False}],
            "constraints": {"max_deck_slides": 24, "page_size": "A4", "confidentiality": CONFIDENTIALITY, "owner_declarations": content.get("owner_declarations") or []}}


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


def build_workbook(content: Dict[str, Any], brief: Dict[str, Any], verdict: Dict[str, Any], seed: str, stamp: str, voice: str) -> Dict[str, Any]:
    has_options = len(content["options"]) == 3
    checks: List[Dict[str, Any]] = [
        {"label": "K001 share of tables measured", "calc": "K001", "formula": "Inputs.F003/Inputs.F002"},
        {"label": "K002 share of bytes in the largest databases", "calc": "K002", "formula": "Inputs.F016/Inputs.F004"},
    ]
    sheets: List[Dict[str, Any]] = [{"name": "Cover", "kind": "cover"}, {"name": "Inputs", "kind": "inputs", "facts": sorted(content["facts"])}]
    if has_options:
        sheets.append({"name": "Options", "kind": "options_model", "options": ["O1", "O2", "O3"],
                       "rows": [{"label": "Bytes addressed", "unit": "GiB", "field": "reclaimable_gib", "format": "#,##0.0"},
                                {"label": "Monthly saving", "unit": "USD", "field": "monthly_saving_usd", "format": "#,##0.0"}],
                       "derived": [{"label": "Share of bytes addressed by all strategies", "formula": "reclaimable_gib / Inputs.F021", "calc": "K003", "format": "0.0%"},
                                   {"label": "Annual saving (USD)", "formula": "12 * monthly_saving_usd", "format": "#,##0.0"}]})
        checks.append({"label": "K004 three largest strategies' share of bytes addressed", "calc": "K004", "formula": "Inputs.F020/Inputs.F021"})
        checks += [{"label": f"K003 share of bytes addressed {oid}", "calc": "K003", "option": oid, "derived": 0} for oid in ("O1", "O2", "O3")]
    sheets += [{"name": "Series", "kind": "series", "series": sorted(content["series"])}, {"name": "Checks", "kind": "checks", "checks": checks}]
    return {"spec_type": "workbook", "spec_id": f"WB-{content['census_ref']}", "content_ref": brief["content_ref"], "brief_ref": brief["brief_id"], "verdict_ref": verdict["verdict_id"],
            "objective": "decide", "family": "strategy", "voice": voice, "seed": seed, "build_stamp": stamp, "sheets": sheets}


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
                      "deck.json": build_deck(content, brief, verdict, seed, stamp, frame["voice"]), "paper.json": build_paper(content, brief, verdict, seed, stamp, frame["voice"]),
                      "workbook.json": build_workbook(content, brief, verdict, seed, stamp, frame["voice"])}}
