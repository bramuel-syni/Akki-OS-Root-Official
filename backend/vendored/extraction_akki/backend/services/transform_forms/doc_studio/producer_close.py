"""Commission-close producer: the accepted census result (job record + digest-verified report) becomes a decide pack —
"accept the delivery and close the commission, or hold it open" — for the estate owner. Deterministic, receipted, no model.
Facts come from the job receipt (what ran, where, how long, what the Ledger recorded) and the report's connection table."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from services.transform_forms.doc_studio.frames import frame_for, verdict_from_frame
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief
from services.transform_forms.doc_studio.producer_estate import CONFIDENTIALITY, HOUSE, _gib, commission_id_for

GOVERNING = "CP-CENSUS-ESTATE-INTELLIGENCE"


def load_job(job_id: str) -> Dict[str, Any]:
    from services.census_autonomy import estate_intelligence_dispatch as dispatch
    path = dispatch._jobs_dir() / f"{job_id}.json"
    if not path.exists():
        raise LookupError("No estate intelligence job record is banked for that census.")
    return json.loads(path.read_text())


def _minutes(a: str, b: str) -> float:
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    return round((datetime.strptime(b, fmt) - datetime.strptime(a, fmt)).total_seconds() / 60, 1)


def build_content(job: Dict[str, Any], report: Dict[str, Any], tenant_id: str) -> Dict[str, Any]:
    receipt, job_id = job["receipt"], job["job_id"]
    summary, conns = receipt["result"]["summary"], report["connections"]
    status = receipt["status"]
    blocked = [c for c in conns if c["status"] == "blocked"]
    partial = [c for c in conns if c["status"] == "partial"]
    complete = [c for c in conns if c["status"] == "complete"]
    dossier = report.get("dossier") or {}
    receipts: Dict[str, Any] = {
        "R01": {"resolves_to": f"Estate intelligence job record {job_id}: submitted {job['submitted_at'][:19]}Z by principal {job['principal_id']}, runtime {receipt['runtime_id']}, code {receipt['code_sha256'][:12]}, result receipt digest-verified ({receipt['receipt_sha256'][:12]})", "platform_ref": job_id},
        "R02": {"resolves_to": f"Estate intelligence report v{report['report_version']} for {job_id}, built {report['built_at'][:19]}Z; connection table and coverage notes", "platform_ref": job_id},
        "R03": {"resolves_to": f"Lawful basis admit {Path(job['lawful_basis_ref']).name} (sha256 {job['lawful_basis_sha256'][:12]}); governing artifact {GOVERNING} version {job_id}"},
        "R04": {"resolves_to": f"Ledger rows {', '.join(r['row_id'] for r in job['ledger_rows'])}: {' → '.join(r['stage'] + ':' + r['decision'] for r in job['ledger_rows'])}"},
    }
    if dossier.get("receipt_id"):
        receipts["R05"] = {"resolves_to": f"Executive dossier receipt {dossier['receipt_id']}: {dossier.get('model_id')} via {dossier.get('provider')}, {dossier.get('tokens_in')} tokens in / {dossier.get('tokens_out')} out, prompt {str(dossier.get('prompt_sha256'))[:12]}"}
    stores = report.get("stores") or {}
    for rid, key, label in (("R06", "obs", "OBS bucket enumeration"), ("R07", "nas", "NAS share enumeration")):
        st = stores.get(key) or {}
        if st.get("measured") and st.get("census_run_id"):
            receipts[rid] = {"resolves_to": f"{label} census run {st['census_run_id']} ({st.get('units', 0):,} {st.get('unit_name', 'units')}, {st.get('bytes_label')})", "platform_ref": st["census_run_id"]}
    facts = {
        "F001": {"label": "Tables in scope", "value": summary["tables_total"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F002": {"label": "Tables measured", "value": summary["tables_measured"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F003": {"label": "Tables measured by complete pass", "value": summary["complete_tables"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F004": {"label": "Tables measured by stratified sample", "value": summary["sampled_tables"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F005": {"label": "Tables measured by head sample", "value": summary["head_sampled_tables"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F006": {"label": "Tables that failed", "value": summary["failed_tables"], "unit": "tables", "class": "measured", "receipt": "R01"},
        "F007": {"label": "Rows measured", "value": round(summary["rows_measured_total"] / 1e6, 1), "unit": "m", "class": "measured", "receipt": "R01"},
        "F008": {"label": "Wall clock on the runtime", "value": _minutes(receipt["started_at"], receipt["finished_at"]), "unit": "minutes", "class": "measured", "receipt": "R01"},
        "F009": {"label": "Connections in scope", "value": len(conns), "unit": "connections", "class": "measured", "receipt": "R02"},
        "F010": {"label": "Connections complete", "value": len(complete), "unit": "connections", "class": "measured", "receipt": "R02"},
        "F011": {"label": "Connections partial", "value": len(partial), "unit": "connections", "class": "measured", "receipt": "R02"},
        "F012": {"label": "Connections blocked", "value": len(blocked), "unit": "connections", "class": "measured", "receipt": "R02"},
        "F013": {"label": "Data and index measured", "value": _gib(summary["bytes_total"]), "unit": "GiB", "class": "measured", "receipt": "R01"},
        "F014": {"label": "Databases measured", "value": report["headline"]["databases"], "unit": "databases", "class": "measured", "receipt": "R02"},
        "F015": {"label": "Ledger rows for the run", "value": len(job["ledger_rows"]), "unit": "rows", "class": "measured", "receipt": "R04"},
        "F016": {"label": "Rows held (estimate)", "value": round(summary["rows_estimate_total"] / 1e6, 1), "unit": "m", "class": "estimated", "receipt": "R01"},
    }
    if "R05" in receipts:
        facts["F017"] = {"label": "Dossier tokens in", "value": int(dossier.get("tokens_in") or 0), "unit": "tokens", "class": "measured", "receipt": "R05"}
        facts["F018"] = {"label": "Dossier tokens out", "value": int(dossier.get("tokens_out") or 0), "unit": "tokens", "class": "measured", "receipt": "R05"}
    obs = stores.get("obs") or {}
    if "R06" in receipts:
        facts["F019"] = {"label": "OBS buckets enumerated", "value": int(obs.get("sources") or 0), "unit": "buckets", "class": "measured", "receipt": "R06"}
        facts["F020"] = {"label": "OBS buckets unreachable", "value": int(obs.get("sources_blocked") or 0), "unit": "buckets", "class": "measured", "receipt": "R06"}
    series = {
        "S001": {"label": "Tables measured by connection", "categories": [f"{c['label'][:28]} ({c['status']})" for c in conns], "values": {"Tables": [c["table_count"] for c in conns]}, "unit": "tables", "class": "measured", "receipt": "R02"},
        "S002": {"label": "How tables were measured", "categories": ["Complete pass", "Stratified sample", "Head sample", "Failed", "Not reached"],
                 "values": {"Tables": [summary["complete_tables"], summary["sampled_tables"], summary["head_sampled_tables"], summary["failed_tables"], max(0, summary["tables_total"] - summary["tables_measured"] - summary["failed_tables"])]}, "unit": "tables", "class": "measured", "receipt": "R01"},
        "S003": {"label": "Data and index by connection, GiB", "categories": [c["label"][:28] for c in conns], "values": {"GiB": [_gib(c["volume_bytes"]) for c in conns]}, "unit": "GiB", "class": "measured", "receipt": "R02"},
    }
    calculations = {
        "K001": {"label": "Share of tables measured", "formula": "F002 / F001", "inputs": ["F001", "F002"], "unit": "pct"},
        "K002": {"label": "Share of tables by complete pass", "formula": "F003 / F001", "inputs": ["F001", "F003"], "unit": "pct"},
        "K003": {"label": "Share of connections complete", "formula": "F010 / F009", "inputs": ["F009", "F010"], "unit": "pct"},
        "K004": {"label": "Share of tables that failed", "formula": "F006 / F001", "inputs": ["F001", "F006"], "unit": "pct"},
    }
    blocked_text = "; ".join(f"{c['label']} blocked ({(c.get('reason_code') or 'no reason recorded').split(' (')[0]})" for c in blocked) or "no connection blocked"
    claims: Dict[str, Any] = {
        "C001": {"text": f"The census ran under {GOVERNING} on runtime {receipt['runtime_id']} for {{F008}} minutes and closed {status}", "supports": ["F008"]},
        "C002": {"text": "{F002} of {F001} tables were measured ({K001}): {F003} by complete pass, {F004} by stratified sample, {F005} by head sample; {F006} failed", "supports": ["F001", "F002", "F003", "F004", "F005", "F006"]},
        "C003": {"text": "{F010} of {F009} connections completed, {F011} were partial and {F012} blocked", "supports": ["F009", "F010", "F011", "F012"]},
        "C004": {"text": "The result receipt is digest-verified; the Ledger records admit, gate and converge", "supports": ["F015"]},
        "C005": {"text": "The report holds aggregates, sketches and hashes only; no row value was retained or returned", "supports": ["F007"]},
        "C006": {"text": f"The delivered result is {status}: {blocked_text}", "supports": ["F012"]},
        "C009": {"text": "Complete passes cover {K002} of tables; {K004} of tables failed", "supports": ["F001", "F003", "F006"]},
        "C010": {"text": f"Lawful basis: {Path(job['lawful_basis_ref']).name.split('_LAWFUL')[0]} census admit; scope: {job['scope']}", "supports": ["F015"]},
        "C011": {"text": "{F013} GiB across {F014} databases were measured in {F008} minutes", "supports": ["F008", "F013", "F014"]},
        "C012": {"text": f"Measured usage: {{F008}} minutes wall clock and {{F007}} rows read on {receipt['runtime_id']}; {receipt['result'].get('execution', 'execution note not recorded')}", "supports": ["F007", "F008"]},
        "C013": {"text": "{F002} of {F001} tables were measured ({K001}); {F006} failed", "supports": ["F001", "F002", "F006"]},
        "C014": {"text": f"The result closed {status} with {{F012}} blocked and {{F011}} partial connections", "supports": ["F011", "F012"]},
    }
    if "F017" in facts:
        claims["C007"] = {"text": f"The executive dossier was composed by {dossier.get('model_id')} from {{F017}} tokens in and {{F018}} tokens out, receipt {dossier.get('receipt_id')}", "supports": ["F017", "F018"]}
    if "F019" in facts:
        claims["C008"] = {"text": "Object storage enumeration reached {F019} buckets; {F020} were unreachable", "supports": ["F019", "F020"]}
    open_items: List[str] = []
    for i, c in enumerate(blocked + partial, start=1):
        claims[f"C02{i}"] = {"text": f"{c['label']}: {c['status']}{' — ' + c['reason_code'] if c.get('reason_code') else ''}; {c['table_count']} tables reached", "supports": ["F012" if c["status"] == "blocked" else "F011"]}
        open_items.append(f"C02{i}")
        if i >= 4:
            break
    cannot_say = [{"gap": f"Connection {c['label']}", "reason": c.get("reason_code") or "not read", "closes_with": "owner grants access; re-census"} for c in blocked]
    cannot_say.append({"gap": "Ratios on sampled tables", "reason": "stratified or head samples where complete passes were not possible", "closes_with": "a complete-pass census on those tables"})
    if summary["failed_tables"]:
        cannot_say.append({"gap": f"{summary['failed_tables']} failed tables", "reason": "the worker could not measure them in this run", "closes_with": "re-census with the recorded errors addressed"})
    cannot_say.append({"gap": "Languages, rights and semantic similarity", "reason": "not measured by this census", "closes_with": "rights declared at Connect; a language and similarity pass"})
    return {"content_id": f"commission-close-{job_id}", "version": 1, "title": f"Commission close — estate intelligence {job_id}", "organisation": tenant_id,
            "census_ref": job_id, "delivered_on": receipt["finished_at"][:10], "status": status,
            "receipts": receipts, "facts": facts, "series": series, "options": {}, "calculations": calculations, "claims": claims,
            "coverage": {"covers": f"Delivery of census {job_id}: {summary['tables_measured']} of {summary['tables_total']} tables, {len(conns)} connections, wall clock, Ledger rows, receipts and the dossier composition. Everything here is read from the job record and the digest-verified report.", "cannot_say": cannot_say},
            "_open_items": open_items}


def build_brief(content: Dict[str, Any], tenant_id: str, day: str) -> Dict[str, Any]:
    return {"brief_id": f"BR-{day}-close-{content['census_ref']}", "content_ref": f"{content['content_id']}@{content['version']}",
            "purpose": {"kind": "decide", "statement": f"Accept the delivered estate-intelligence census {content['census_ref']} and close the commission, or hold it open until the blocked connections are read."},
            "audience": {"who": f"Estate owner · {tenant_id}", "knowledge": "high on the business, mixed on the data estate", "priorities": ["what was delivered", "what remains open", "evidence and usage"], "detail": "summary with an evidence appendix"},
            "setting": {"mode": "read-ahead then presented", "presentation_minutes": 10, "read_unattended": True, "printed": True, "ongoing_use": False},
            "content": {"evidence": True, "narrative": True, "financial": False, "diagrams": False, "imagery": False, "appendix": True},
            "brand": {"house": HOUSE, "formality": "formal", "expressiveness": "restrained", "variation_allowed": "within-family"},
            "outputs": [{"format": "pptx", "role": "presented deck", "editable_charts": True}, {"format": "docx", "role": "paper for read-ahead", "editable_charts": False},
                        {"format": "xlsx", "role": "delivery measures and cross-checks", "editable_charts": False}, {"format": "html", "role": "review surface", "editable_charts": False}],
            "constraints": {"max_deck_slides": 12, "page_size": "A4", "confidentiality": CONFIDENTIALITY}}


def _spec_base(kind: str, prefix: str, content, brief, verdict, seed, stamp, voice) -> Dict[str, Any]:
    return {"spec_type": kind, "spec_id": f"{prefix}-close-{content['census_ref']}", "content_ref": brief["content_ref"], "brief_ref": brief["brief_id"], "verdict_ref": verdict["verdict_id"],
            "objective": "decide", "family": "strategy", "voice": voice, "seed": seed, "build_stamp": stamp}


def build_deck(content, brief, verdict, seed, stamp, voice) -> Dict[str, Any]:
    partial = content["status"] != "complete"
    evidence_points = ["{C005}", "{C010}"] + (["{C007}"] if "C007" in content["claims"] else [])
    slides: List[Dict[str, Any]] = [
        {"type": "cover", "title": "{content.title}", "subtitle": "Commission close · delivered {content.delivered_on}", "org": "{content.organisation}"},
        {"type": "exec_summary", "kicker": "Executive summary",
         "title": "The census delivered a partial, digest-verified result; blocked connections remain open" if partial else "The census delivered a complete, digest-verified result",
         "situation": "{C001}. {C002}.", "complication": "{C003}. {C006}.",
         "question": "Should the estate owner accept the delivery and close the commission, or hold it open until the blocked connections are read?",
         "answer": "{C004}. {C005}. The decision is the estate owner's; this pack sets out what was delivered and what was not."},
        {"type": "section", "number": 1, "title": "What was commissioned and what was delivered"},
        {"type": "assertion_exhibit", "kicker": "Coverage", "title": "{C013}", "exhibit": {"plate": "bar", "series_ref": "S002", "y_format": "num", "so_what": "{C009}"}},
        {"type": "assertion_exhibit", "kicker": "Connections", "title": "{C003}", "exhibit": {"plate": "bar", "series_ref": "S001", "y_format": "num", "so_what": "{C006}"}},
        {"type": "assertion_points", "kicker": "Evidence", "title": "{C004}", "points": evidence_points},
        {"type": "section", "number": 2, "title": "Usage, volume and what remains open"},
        {"type": "assertion_exhibit", "kicker": "Volume", "title": "{C011}", "exhibit": {"plate": "bar", "series_ref": "S003", "y_format": "num", "so_what": "{C012}"}},
    ]
    if content["_open_items"]:
        slides.append({"type": "assertion_points", "kicker": "Open items", "title": "{C014}", "points": [f"{{{c}}}" for c in content["_open_items"]]})
    slides += [{"type": "coverage_limits"}, {"type": "appendix"}]
    return {**_spec_base("deck", "DK", content, brief, verdict, seed, stamp, voice), "furniture": {"deck_id": f"CC-{content['census_ref']}", "confidentiality": CONFIDENTIALITY}, "slides": slides}


def build_paper(content, brief, verdict, seed, stamp, voice) -> Dict[str, Any]:
    open_paras = [{"para": f"{{{c}}}."} for c in content["_open_items"]]
    return {**_spec_base("paper", "PP", content, brief, verdict, seed, stamp, voice), "furniture": {"paper_id": f"CC-{content['census_ref']} (paper)", "confidentiality": CONFIDENTIALITY},
            "title": "{content.title}", "subtitle": "Commission-close paper for the estate owner",
            "sections": [
                {"heading": "Summary", "blocks": [{"para": "{C001}. {C002}."}, {"para": "{C003}. {C006}."}, {"para": "{C004}. {C005}. The decision to accept and close, or to hold, is the estate owner's."}]},
                {"heading": "1. What was delivered", "blocks": [{"figure": {"plate": "bar", "series_ref": "S002", "y_format": "num", "caption": "{C009}"}}, {"table": {"series_ref": "S001", "caption": "Tables measured by connection"}}, {"para": "{C011}. {C012}."}]},
                {"heading": "2. Evidence", "blocks": [{"para": "{C004}. {C010}."}] + ([{"para": "{C007}."}] if "C007" in content["claims"] else []) + ([{"para": "{C008}."}] if "C008" in content["claims"] else [])},
                {"heading": "3. What remains open", "blocks": [{"para": "{C006}."}] + open_paras},
                {"heading": "4. Coverage and limits", "blocks": [{"coverage_limits": True}]},
                {"heading": "Appendix: receipts", "blocks": [{"receipts": True}]}]}


def build_workbook(content, brief, verdict, seed, stamp, voice) -> Dict[str, Any]:
    checks = [{"label": "K001 share of tables measured", "calc": "K001", "formula": "Inputs.F002/Inputs.F001"},
              {"label": "K002 share of tables by complete pass", "calc": "K002", "formula": "Inputs.F003/Inputs.F001"},
              {"label": "K003 share of connections complete", "calc": "K003", "formula": "Inputs.F010/Inputs.F009"},
              {"label": "K004 share of tables that failed", "calc": "K004", "formula": "Inputs.F006/Inputs.F001"}]
    return {**_spec_base("workbook", "WB", content, brief, verdict, seed, stamp, voice),
            "sheets": [{"name": "Cover", "kind": "cover"}, {"name": "Inputs", "kind": "inputs", "facts": sorted(content["facts"])},
                       {"name": "Series", "kind": "series", "series": sorted(content["series"])}, {"name": "Checks", "kind": "checks", "checks": checks}]}


def commission_from_job(job_id: str, tenant_id: str, principal_id: str, now: datetime) -> Dict[str, Any]:
    from services.census_autonomy import estate_intelligence_report as eir
    job = load_job(job_id)
    report = eir.report_for(job_id, cached_only=True)
    if not report:
        raise LookupError("No verified estate intelligence report is banked for that census.")
    day, stamp = now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%dT%H:%M:%SZ")
    content = build_content(job, report, tenant_id)
    open_items = content.pop("_open_items")
    brief = build_brief(content, tenant_id, day)
    frame = frame_for(brief)
    if frame is None:
        raise LookupError("non-routine commission: no standing frame covers this brief and CIF's ideas endpoint is not mounted in this runtime")
    verdict = verdict_from_frame(frame, brief, f"V-{day}-close-{job_id}", manifest_from_brief(brief, has_options=False), confirmed_by=principal_id, confirmed_at=stamp)
    seed = f"{content['content_id']}/{brief['purpose']['kind']}/{day}"
    spec_content = {**content, "_open_items": open_items}
    return {"commission_id": commission_id_for(tenant_id, content["content_id"], brief["purpose"]["kind"], day), "content_id": content["content_id"], "seed": seed, "build_stamp": stamp,
            "frame_ref": frame["frame_id"], "voice": frame["voice"], "producer": "commission_close", "source_ref": job_id, "title": content["title"],
            "files": {"brief.json": brief, "content.json": content, "verdict.json": verdict,
                      "deck.json": build_deck(spec_content, brief, verdict, seed, stamp, frame["voice"]), "paper.json": build_paper(spec_content, brief, verdict, seed, stamp, frame["voice"]),
                      "workbook.json": build_workbook(content, brief, verdict, seed, stamp, frame["voice"])}}
