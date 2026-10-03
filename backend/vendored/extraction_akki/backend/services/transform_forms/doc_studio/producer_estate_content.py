"""Content census chapter of the estate pack (owner direction 3 Oct 2026: "note the part you cannot access, focus on the part you can access …
get us closer to the truth and revise these reports"). Reads the live store roll-up (tier 1 header-measured hours for every readable object,
tier 2 stratified sample read in full with 95 % intervals) and adds receipt R10, facts F100–F129, series S020–S022, tables T040–T044, claims
C050–C059, two decisions and the gaps. Readable stores are measured; refused and archived stores are counted, never estimated."""
from __future__ import annotations

from typing import Any, Dict, List

from services.transform_forms.doc_studio.producer_estate_language import name_of

TIB = 2 ** 40


def _tib(value) -> float:
    return round((value or 0) / TIB, 2)


def _h(value) -> float | None:
    return round(value, 1) if isinstance(value, (int, float)) else None


def _iv(e: Dict[str, Any] | None) -> str:
    if not e or e.get("est") is None:
        return "—"
    if e.get("lo") is not None and e.get("hi") is not None and e["hi"] != e["lo"]:
        return f"{e['est']:,.1f} ({e['lo']:,.1f}–{e['hi']:,.1f})"
    return f"{e['est']:,.1f}"


def _langs(m: Dict[str, Any] | None, n: int = 3) -> str:
    ranked = sorted(((code, e) for code, e in (m or {}).items() if e and e.get("est") is not None), key=lambda kv: -kv[1]["est"])
    return "; ".join(f"{name_of(code)} {e['est']:,.0f} h" for code, e in ranked[:n]) or "—"


def content(report: Dict[str, Any], receipts: Dict[str, Any], facts: Dict[str, Any], series: Dict[str, Any], calculations: Dict[str, Any], claims: Dict[str, Any],
            tables: Dict[str, Any], cannot_say: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    stores = report.get("stores") or {}
    obs, nas = (stores.get("obs") or {}).get("content") or {}, (stores.get("nas") or {}).get("content") or {}
    if not obs.get("measured") and not nas.get("measured"):
        cannot_say.append({"gap": "Hours, speech, music and languages held in the object store and the file shares", "reason": "no content census receipt is banked yet", "closes_with": "the tiered content census (content_sample) on the GPU hosts"})
        return []
    runs = sorted({r for s in (stores.get("obs"), stores.get("nas")) if s for r in (s.get("census_run_ids") or [])})
    observations = "; ".join(f"{key.upper()} {(stores.get(key) or {}).get('observed_at') or 'timestamp unavailable'}" for key in ("obs", "nas"))
    receipts["R10"] = {"resolves_to": (f"Interim tiered content census (content_sample); snapshots {observations}; receipts {', '.join(runs[-6:])} on akki-vm and akki-vm-ii. Resumable listing, "
                                       f"header probes of accessible audio and a per-folder video sample (ranged reads → ffprobe), with unprobed durations extrapolated where possible; a seeded stratified sample of files per folder read byte for byte, verified against the listing and judged on every two-second "
                                       f"window by the admitted music detector and the current audio language model; ratio estimators with finite-population correction give the 95 % intervals. "
                                       f"Listing, probing and sampling are incomplete. Model readings, not human labels; intervals exclude model error and inaccessible or unsampled content."), "platform_ref": runs[-1] if runs else None}
    total = stores.get("content_total") or {}
    blocked = obs.get("access_blocked") or {}
    readable = obs.get("readable") or {}
    listed_media = (obs.get("media_objects") or 0) + (nas.get("media_objects") or 0)
    f: Dict[str, Any] = {
        "F100": {"label": "Media files listed across the object store and the file shares", "value": round(listed_media / 1e6, 3), "unit": "m", "class": "measured", "receipt": "R10"},
        "F101": {"label": "Object-store media files the census key can read", "value": round((readable.get("media_objects") or 0) / 1e6, 3), "unit": "m", "class": "measured", "receipt": "R10"},
        "F102": {"label": "Object-store media files in buckets the key cannot read", "value": round((blocked.get("media_objects") or 0) / 1e6, 3), "unit": "m", "class": "measured", "receipt": "R10"},
        "F103": {"label": "Bytes in buckets the key cannot read", "value": _tib(blocked.get("media_bytes")), "unit": "TiB", "class": "measured", "receipt": "R10"},
        "F104": {"label": "Buckets refusing object reads (403 AccessDenied)", "value": blocked.get("denied_sources") or 0, "unit": "buckets", "class": "measured", "receipt": "R10"},
        "F105": {"label": "Buckets whose objects need a restore (Archive class, no direct read)", "value": blocked.get("archived_sources") or 0, "unit": "buckets", "class": "measured", "receipt": "R10"},
        "F106": {"label": "Hours held in the readable object-store buckets (header-measured)", "value": _h((obs.get("headers") or {}).get("hours_est")) or 0, "unit": "hours", "class": "estimated", "receipt": "R10",
                 "measurement_scope": f"95 % interval {_h((obs.get('headers') or {}).get('hours_lo'))}–{_h((obs.get('headers') or {}).get('hours_hi'))} h; {(obs.get('headers') or {}).get('probed_files') or 0:,} files probed on their headers, the rest extrapolated by each folder's seconds-per-byte"},
        "F107": {"label": "Speech hours in the readable object-store buckets (estimate)", "value": _h(((obs.get("estimates") or {}).get("speech") or {}).get("est")) or 0, "unit": "hours", "class": "estimated", "receipt": "R10",
                 "measurement_scope": f"95 % interval {_iv((obs.get('estimates') or {}).get('speech'))}"},
        "F108": {"label": "Music hours in the readable object-store buckets (estimate)", "value": _h(((obs.get("estimates") or {}).get("music") or {}).get("est")) or 0, "unit": "hours", "class": "estimated", "receipt": "R10",
                 "measurement_scope": f"95 % interval {_iv((obs.get('estimates') or {}).get('music'))}"},
        "F109": {"label": "Object-store files read in full for the sample", "value": (obs.get("sample") or {}).get("read_files") or 0, "unit": "files", "class": "measured", "receipt": "R10"},
        "F110": {"label": "Object-store files header-probed", "value": (obs.get("headers") or {}).get("probed_files") or 0, "unit": "files", "class": "measured", "receipt": "R10"},
        "F111": {"label": "OBS egress spent on the content census so far (assumed tariff)", "value": round((obs.get("egress") or {}).get("usd_estimate") or 0, 2), "unit": "USD", "class": "estimated", "receipt": "R10",
                 "measurement_scope": f"{_tib((obs.get('egress') or {}).get('bytes'))} TiB read at an assumed {(obs.get('egress') or {}).get('usd_per_gb_assumed') or '—'} USD per GB; Archive-class direct reads carry a retrieval fee on top that is not priced here"},
        "F112": {"label": "Readable object-store buckets", "value": readable.get("sources") or 0, "unit": "buckets", "class": "measured", "receipt": "R10"},
    }
    if blocked.get("share_of_media_objects") is not None:
        f["F113"] = {"label": "Share of listed object-store media files the key cannot read", "value": round(blocked["share_of_media_objects"], 4), "unit": "pct", "class": "measured", "receipt": "R10"}
    classes = obs.get("storage_classes") or {}
    if classes.get("archive_pct_of_bytes") is not None:
        f["F114"] = {"label": "Archive share of bytes in the subset with recorded storage classes (not the whole object store)", "value": round(classes["archive_pct_of_bytes"] / 100.0, 4), "unit": "pct", "class": "measured", "receipt": "R10",
                     "measurement_scope": f"Only {classes.get('sources_measured') or 0} buckets, {_tib(classes.get('bucket_bytes'))} TiB with class metadata; unknown classes excluded, not assumed Standard or Archive"}
    if nas.get("measured"):
        nh, ns = nas.get("headers") or {}, (nas.get("estimates") or {}).get("speech") or {}
        f.update({
            "F120": {"label": "File-share media files listed", "value": round((nas.get("media_objects") or 0) / 1e6, 3), "unit": "m", "class": "measured", "receipt": "R10"},
            "F121": {"label": "Hours held in the file shares measured so far (header-measured)", "value": _h(nh.get("hours_est")) or 0, "unit": "hours", "class": "estimated", "receipt": "R10",
                     "measurement_scope": f"95 % interval {_h(nh.get('hours_lo'))}–{_h(nh.get('hours_hi'))} h; {nh.get('probed_files') or 0:,} files probed; shares not yet probed are not counted"},
            "F122": {"label": "Speech hours in the file shares measured so far (estimate)", "value": _h(ns.get("est")) or 0, "unit": "hours", "class": "estimated", "receipt": "R10", "measurement_scope": f"95 % interval {_iv(ns)}"},
            "F123": {"label": "File-share files read in full for the sample", "value": (nas.get("sample") or {}).get("read_files") or 0, "unit": "files", "class": "measured", "receipt": "R10"},
            "F124": {"label": "File-share shares still listing or probing", "value": (nas.get("sources") or 0) - (nas.get("sources_complete") or 0), "unit": "shares", "class": "measured", "receipt": "R10"},
        })
    facts.update(f)
    calculations["K020"] = {"label": "Share of readable object-store hours that is speech", "formula": "F107 / F106", "inputs": ["F106", "F107"], "unit": "pct"}
    if "F101" in facts and "F102" in facts:
        calculations["K021"] = {"label": "Readable share of listed object-store media files", "formula": "F101 / (F101 + F102)", "inputs": ["F101", "F102"], "unit": "pct"}
    rows_obs = [s for s in (obs.get("source_rows") or []) if s.get("access") == "readable" and (s.get("hours") or {}).get("est")]
    rows_obs.sort(key=lambda s: -(s["hours"]["est"] or 0))
    if rows_obs:
        series["S020"] = {"label": "Hours held by readable object-store bucket (header-measured)", "categories": [s["label"] for s in rows_obs[:8]], "values": {"Hours": [_h(s["hours"]["est"]) for s in rows_obs[:8]]}, "unit": "hours", "class": "estimated", "receipt": "R10"}
    langs = (total.get("languages") or (obs.get("estimates") or {}).get("languages") or {})
    if langs:
        series["S021"] = {"label": "Speech hours by language across the readable stores (estimate)", "categories": [name_of(c) for c in langs], "values": {"Hours": [_h(e.get("est")) or 0 for e in langs.values()]}, "unit": "hours", "class": "estimated", "receipt": "R10"}
    if blocked.get("media_objects"):
        series["S022"] = {"label": "Object-store media files: readable versus not readable", "categories": ["Readable", "Key refused (403)", "Archive class, restore needed"],
                          "values": {"Files": [readable.get("media_objects") or 0, sum(s["media_objects"] or 0 for s in blocked["sources"] if s["access"] == "denied"), sum(s["media_objects"] or 0 for s in blocked["sources"] if s["access"] == "archived")]},
                          "unit": "files", "class": "measured", "receipt": "R10"}
    _tables(obs, nas, blocked, tables)
    claims.update({
        "C050": {"text": "The census has listed {F100} media files so far; {F101} object-store files are in readable buckets and {F102} ({F103} TiB) in buckets requiring access or restoration; {F104} buckets refuse reads and {F105} require restoration", "supports": ["F100", "F101", "F102", "F103", "F104", "F105"]},
        "C051": {"text": "The currently covered readable object-store scope has a header-derived estimate of {F106} hours; separate sample estimators give {F107} speech hours and {F108} music hours. These are provisional estimates, not a complete measured total or an exact additive partition", "supports": ["F106", "F107", "F108"]},
        "C052": {"text": "{F109} files were read byte for byte and {F110} header-probed to reach these intervals, at {F111} USD of egress so far", "supports": ["F109", "F110", "F111"]},
        "C053": {"text": "Listed buckets the key cannot read are counted, never assigned content estimates: their hours, speech and languages stay unknown until access is granted or Archive objects are restored", "supports": ["F104", "F102", "F105"]},
    })
    if "F114" in facts:
        claims["C054"] = {"text": "{F114} of bytes in the subset with recorded storage classes are already Archive-class; this subset does not establish the archive share or remaining tiering savings of the whole estate", "supports": ["F114"]}
    cannot_say.extend([
        {"gap": "A completed content census of every readable folder", "reason": "header probing and the planned samples are not finished; unsampled folders are forecast, not measured", "closes_with": "finish the per-folder samples, largest and widest-interval strata first"},
        {"gap": "Human-verified speech, music, silence and language hours", "reason": "every composition figure is a model reading; intervals cover sampling, not model error", "closes_with": "stratified human checks, abstentions included, and a reconciliation of header against decoded durations"},
        {"gap": "Estate-wide archive share and invoice-backed tiering savings", "reason": "storage-class metadata covers a subset; legacy full-Standard-price scenarios omit retrieval and restore costs", "closes_with": "class metadata and read demand per bucket, then repricing at actual tariffs"},
    ])
    if "F121" in facts:
        claims["C055"] = {"text": "The file shares measured so far hold {F121} hours, of which {F122} are speech; {F124} shares are still being listed or probed and are not yet counted", "supports": ["F121", "F122", "F124"]}
    if blocked.get("denied_sources"):
        denied = [source for source in blocked.get("sources", []) if source.get("access") == "denied"]
        cannot_say.append({"gap": f"Measured hours and languages for the {blocked['denied_sources']} buckets that refuse object reads ({sum(s.get('media_objects') or 0 for s in denied):,} media files, {_tib(sum(s.get('media_bytes') or 0 for s in denied))} TiB)",
                           "reason": "every HEAD and GET returns 403 AccessDenied; these rows are forecast from readable donors", "closes_with": "an object-read grant (obs:object:GetObject) to the census key; the census then measures them by itself"})
    if blocked.get("archived_sources"):
        cannot_say.append({"gap": f"Content of the {blocked['archived_sources']} buckets whose objects answer InvalidObjectState", "reason": "Archive class without direct read; a restore (with its fee) must precede any read", "closes_with": "an owner decision to restore, or to leave them counted only"})
    if nas.get("measured") and ((nas.get("sources") or 0) - (nas.get("sources_complete") or 0)):
        cannot_say.append({"gap": "File-share hours and speech for the shares still listing or probing", "reason": "listing and header probes run through the jump host's SFTP; reads only in the off-peak window", "closes_with": "the running NAS chain (listing any hour; reads 20:00–06:00 EAT)"})
    chapters = [{"question": "What do the readable media stores actually hold — hours on the files themselves, speech, music and languages — and which stores cannot be read at all?",
                 "answers_with": [t for t in ("F106", "F107", "F108", "K020", "F101", "F102", "F103", "F104", "F113", "F109", "F111") if t in facts or t == "K020"],
                 "exhibits": [s for s in ("S020", "S021", "S022") if s in series], "tables": [t for t in ("T040", "T042", "T041", "T045", "T046") if t in tables]}]
    if "F114" in facts or "F121" in facts:
        chapters.append({"question": "Where do the bytes sit by storage class, what has the census cost to read so far, and how far has the file-share census come?",
                         "answers_with": [t for t in ("F114", "F111", "F121", "F122", "F123", "F124") if t in facts], "tables": [t for t in ("T044", "T043") if t in tables]})
    return chapters


def _tables(obs: Dict[str, Any], nas: Dict[str, Any], blocked: Dict[str, Any], tables: Dict[str, Any]) -> None:
    rows = []
    for store_name, c in (("OBS", obs), ("NAS", nas)):
        for s in c.get("source_rows") or []:
            h = s.get("hours") or {}
            rows.append([store_name, s["label"], {"readable": "readable", "denied": "key refused (403)", "archived": "archive · restore needed", "no_media": "no media"}.get(s.get("access"), s.get("access")),
                         {"estimated": "sample complete", "census": "every file read", "partial": "sampling", "listing": "listing", "denied": "not measurable", "archived": "not measurable", "no_media": "—"}.get(s.get("measurement"), s.get("measurement")),
                         f"{s.get('media_objects') or 0:,}", _tib(s.get("media_bytes")),
                         (f"{h['est']:,.1f}" + (f" ({h['lo']:,.1f}–{h['hi']:,.1f})" if h.get("lo") is not None and h.get("hi") != h.get("lo") else "")) if s.get("access") == "readable" and h.get("est") is not None else "not measurable" if s.get("access") in ("denied", "archived") else "—",
                         _iv(s.get("speech")) if s.get("access") == "readable" else "—", _iv(s.get("music")) if s.get("access") == "readable" else "—", _langs(s.get("languages")) if s.get("access") == "readable" else "—",
                         f"{(s.get('sample') or {}).get('read_files') or 0:,} / {(s.get('sample') or {}).get('planned_files') or 0:,}", f"{s['egress_usd']:,.2f}" if s.get("egress_usd") is not None else "—"])
    rows.sort(key=lambda r: (r[0] != "OBS", -float(r[5])))
    tables["T040"] = {"label": "Media stores — what was listed, what could be read, hours held and what the sample says (largest first)", "class": "estimated", "receipt": "R10", "right_align_from": 4,
                      "note": "Interim accessible-scope baseline, not a completed census. Hours held combine available header probes with per-folder extrapolation; speech, music and language quantities are model-derived sample estimates. Parentheses show 95 % sampling intervals where available; these exclude model error, unmeasured folders and inaccessible content. Missing or zero-width intervals do not establish certainty.",
                      "columns": ["Store", "Bucket / share", "Access", "State", "Media files", "Media bytes (TiB)", "Hours held (95 %)", "Speech hours (95 %)", "Music hours (95 %)", "Top languages (speech hours)", "Sample read / planned", "Egress (USD)"],
                      "deck_columns": ["Bucket / share", "Access", "Media files", "Hours held (95 %)", "Speech hours (95 %)", "Top languages (speech hours)", "Sample read / planned"], "rows": rows}
    folders = [fo for c in (obs, nas) for fo in (c.get("folders") or []) if (fo.get("sample") or {}).get("read")]
    folders.sort(key=lambda fo: -(((fo.get("estimates") or {}).get("speech") or {}).get("est") or 0))
    if folders:
        tables["T041"] = {"label": "Folders sampled — hours held, speech, music and languages with 95 % intervals (ranked by estimated speech hours)", "class": "estimated", "receipt": "R10", "right_align_from": 2,
                          "note": "One row per folder stratum with reads, ranked by estimated speech hours. Whole-folder reads remove sampling error only, not model or decode error. All currently supplied folder rows appear in Word and Excel; the deck is an excerpt. Unread strata have no estimate.",
                          "columns": ["Bucket / share", "Folder", "Files", "Hours held", "Speech hours (95 %)", "Music hours (95 %)", "Languages (speech hours)", "Files read / planned", "Status"],
                          "deck_columns": ["Folder", "Files", "Hours held", "Speech hours (95 %)", "Languages (speech hours)", "Files read / planned"],
                          "rows": [[fo.get("label"), fo.get("folder"), f"{fo.get('files') or 0:,}", f"{(fo.get('hours') or {}).get('est'):,.1f}" if (fo.get("hours") or {}).get("est") is not None else "—",
                                    _iv((fo.get("estimates") or {}).get("speech")), _iv((fo.get("estimates") or {}).get("music")), _langs((fo.get("estimates") or {}).get("languages")),
                                    f"{(fo.get('sample') or {}).get('read') or 0:,} / {(fo.get('sample') or {}).get('target') or 0:,}",
                                    {"census": "read whole", "sampled": "sample complete", "reading": "reading", "planned": "planned"}.get((fo.get("sample") or {}).get("status"), (fo.get("sample") or {}).get("status"))] for fo in folders]}
    tables["T045"] = {"label": "Sampling coverage and what would improve this baseline", "class": "measured", "receipt": "R10", "right_align_from": 99,
                      "note": "Listed media, files with header probes and files read in full are different populations. A completed source listing is not a completed sample. These counters are the banked snapshot, not a live progress indicator.",
                      "columns": ["Store", "Media files listed", "Headers probed", "Sample read / planned", "Header / sample completion", "Next evidence step"],
                      "rows": [[name, f"{c.get('media_objects') or 0:,}", f"{(c.get('headers') or {}).get('probed_files') or 0:,}",
                                f"{(c.get('sample') or {}).get('read_files') or 0:,} / {(c.get('sample') or {}).get('planned_files') or 0:,}",
                                f"{'complete' if (c.get('headers') or {}).get('complete') else 'incomplete'} / {'complete' if (c.get('sample') or {}).get('complete') else 'incomplete'}",
                                "Finish accessible-folder samples; target wide intervals; independently check model labels and duration estimates"] for name, c in (("OBS", obs), ("NAS", nas))]}
    language_rows = [[name, name_of(code), _iv(value)] for name, c in (("OBS", obs), ("NAS", nas))
                     for code, value in sorted(((c.get("estimates") or {}).get("languages") or {}).items(), key=lambda item: -(item[1].get("est") or 0))]
    if language_rows:
        tables["T046"] = {"label": "Estimated speech hours by language in the currently covered readable scope", "class": "estimated", "receipt": "R10", "right_align_from": 2,
                          "note": "All model-reported languages, separately by store; 95 % sampling intervals do not include classification error. These are not certified non-English assets. Abstentions and unsupported languages are not redistributed; inaccessible and unsampled content is excluded.",
                          "columns": ["Store", "Model language", "Speech hours (95 %)"], "rows": language_rows}
    if blocked.get("sources"):
        tables["T042"] = {"label": "Object-store buckets the census key cannot read — counted, never estimated", "class": "measured", "receipt": "R10", "right_align_from": 2,
                          "note": "Denied and restore-required buckets are listed separately. Denied buckets require an object-read grant; Archive objects that return InvalidObjectState require a restore decision and its retrieval cost. Listed files and bytes do not establish their hours or languages.", "columns": ["Bucket", "State", "Media files", "Audio files", "Video files", "Media bytes (TiB)", "Bytes already in Archive class (TiB)", "Refused since", "Action required"],
                          "deck_columns": ["Bucket", "State", "Media files", "Media bytes (TiB)", "Action required"],
                          "rows": [[s["label"], "key refused (403 AccessDenied)" if s["access"] == "denied" else "Archive class · InvalidObjectState", f"{s.get('media_objects') or 0:,}", f"{s.get('audio_objects') or 0:,}", f"{s.get('video_objects') or 0:,}",
                                    _tib(s.get("media_bytes")), _tib(s.get("archive_bytes")) if s.get("archive_bytes") else "—", (s.get("since") or "")[:16].replace("T", " ") or "first probe",
                                    "grant obs:object:GetObject to the census key (IAM or bucket policy)" if s["access"] == "denied" else "decide: restore (fee) or leave counted only"] for s in blocked["sources"]]}
    egress_rows = [[s["label"], f"{(s.get('bytes_read') or 0) / 1e9:,.1f}", f"{s['egress_usd']:,.2f}" if s.get("egress_usd") is not None else "—", f"{(s.get('objects_read') or 0):,}", f"{(s.get('objects_failed') or 0):,}"]
                   for s in (obs.get("source_rows") or []) if s.get("bytes_read")]
    if egress_rows:
        egress_rows.sort(key=lambda r: -float(r[1].replace(",", "")))
        tables["T043"] = {"label": "What the content census has cost to read so far, by bucket", "class": "estimated", "receipt": "R10", "right_align_from": 1,
                          "note": f"Egress at an assumed {(obs.get('egress') or {}).get('usd_per_gb_assumed') or '—'} USD per GB billed to the RMS Huawei account; Archive-class direct reads carry a retrieval fee on top that is not priced here. File-share reads travel the estate uplink through the jump host and are not OBS egress.",
                          "columns": ["Bucket", "Bytes read (GB)", "Egress (USD, assumed)", "Files read", "Read failures"], "rows": egress_rows}
    classed = [s for s in (obs.get("source_rows") or []) if s.get("storage_classes")]
    if classed:
        classed.sort(key=lambda s: -(s.get("bucket_bytes") or 0))
        tables["T044"] = {"label": "Storage class by bucket — what is already in Archive class", "class": "measured", "receipt": "R10", "right_align_from": 1,
                          "note": "Read from the object listing. Objects in Archive class are cheap to keep and slow or costly to read; a bucket already in Archive class has no Standard → Archive saving left.",
                          "columns": ["Bucket", "Bytes listed (TiB)", "Archive class (TiB)", "Archive share", "Classes seen"],
                          "rows": [[s["label"], _tib(s.get("bucket_bytes")), _tib(s.get("archive_bytes")), f"{(s.get('archive_bytes') or 0) / (s.get('bucket_bytes') or 1) * 100:.1f}%",
                                    ", ".join(f"{k} {v.get('objects', 0):,}" for k, v in sorted((s.get("storage_classes") or {}).items(), key=lambda kv: -(kv[1].get('bytes') or 0))[:4])] for s in classed[:60]]}


def decisions(report: Dict[str, Any], tables: Dict[str, Any]) -> None:
    """Appends the content-census decisions to T013 and corrects D1 when the listing shows the cold buckets are already Archive class."""
    stores = report.get("stores") or {}
    obs_store = stores.get("obs") or {}
    obs = obs_store.get("content") or {}
    blocked = obs.get("access_blocked") or {}
    t013 = tables.get("T013")
    if not t013:
        return
    rows = t013["rows"]
    if obs_store.get("storage_classes") and obs_store.get("cold_bytes_already_archive"):
        standard = _tib(obs_store.get("cold_bytes_standard"))
        for row in rows:
            if row[0] == "D1":
                row[1] = "Verify cold-bucket storage classes before approving tiering"
                row[3] = f"class metadata confirms {_tib(obs_store['cold_bytes_already_archive'])} TiB of cold bytes already Archive and {standard} TiB Standard in the measured subset; remaining classes are unknown, not zero"
                row[6] = "net tiering saving unverified; historic full-Standard-price scenarios must be repriced, excluding already Archive bytes"
                row[8] = "class coverage for all cold bytes, actual prices, read demand and direct-read versus restore fees"
    if blocked.get("denied_sources"):
        rows.append(["D11", "Grant the census key object read on the buckets that refuse it", f"{blocked['denied_sources']} buckets, e.g. {', '.join(s['label'] for s in blocked['sources'] if s['access'] == 'denied')[:120]} ({blocked.get('media_objects') or 0:,} media files, {_tib(blocked.get('media_bytes'))} TiB)",
                     "the Huawei account administrator grants obs:object:GetObject to the census IAM user on each bucket (IAM policy or bucket policy); the census re-probes every run and resumes by itself",
                     "no data moves; access only (proposed)", "Cloud account owner", "hours, speech and languages for the larger part of the media estate, measured instead of unknown", "R10 · T042", "that the grant has landed (the next census run shows the buckets readable)"])
    if blocked.get("archived_sources"):
        rows.append(["D12", "Decide whether to restore the Archive-class buckets that cannot be read directly", f"{blocked['archived_sources']} buckets, e.g. {', '.join(s['label'] for s in blocked['sources'] if s['access'] == 'archived')[:120]}",
                     "order a restore (restore fee, then egress) for the sample files, or leave these buckets counted only", "same buckets; restored copies temporary (proposed)", "Head of Technology (storage owner)",
                     "a measured reading of otherwise dark buckets, at a known retrieval cost", "R10 · T042", "the restore tariff and the sample size wanted"])


GLOSSARY = [
    {"term": "Header-measured hours", "meaning": "A duration estimate based on available file headers and per-folder extrapolation for unprobed files. Probing is incomplete; some durations themselves use bitrate estimates. This is not an exact count of decoded estate hours."},
    {"term": "95 % interval", "meaning": "A sampling-uncertainty range produced by a method intended to cover its target in 95 % of repeated samples under its assumptions. It does not cover model error, failed reads, unmeasured folders or inaccessible content. Whole-folder reads remove sampling error, not measurement or classification error."},
    {"term": "Key refused (403)", "meaning": "The census key can list the bucket but is refused when it tries to read any object. Those files are counted but nothing about their content is estimated. The fix is an access grant on the owner's cloud account, not a change to the census."},
    {"term": "Archive class", "meaning": "The cheapest storage tier. Some buckets allow direct reads of Archive objects for a retrieval fee; others answer 'restore required', and a restore must be ordered and paid for before anything can be read."},
]
