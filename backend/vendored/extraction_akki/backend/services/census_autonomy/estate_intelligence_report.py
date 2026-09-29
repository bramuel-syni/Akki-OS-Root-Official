"""Estate Intelligence report: turns the census worker's aggregates (never rows) into an estate-handling
brief — condition, duplication, storage economics, dimensional monetisation candidates, cost-reduction
strategies and per-database readiness grades — plus a Markdown brief and an optional governed LLM dossier
composed ONLY from these aggregates through the single chokepoint."""
import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from services.census_autonomy import estate_intelligence_dispatch as dispatch
from services.census_autonomy.estate_intelligence_worker import TIMESTAMP_TYPES, NUMERIC_TYPES, rollup

TERMINAL_WITH_RESULT = ("completed", "partial")
REPORT_VERSION = 2  # bump when build() gains sections so cached reports are rebuilt from the banked detail
BRIEF_DIR = Path(__file__).resolve().parents[6] / "frontend" / "public" / "briefs"
DEGRADATION_KINDS = ("mojibake_ratio", "placeholder_ratio", "truncation_ratio", "invalid_format_ratio", "whitespace_ratio")

DIMENSIONS = {
    "time": re.compile(r"(^|_)(date|time|created|updated|modified|timestamp|year|month|period|expires?|start|end)(_|$)|_at$|_on$"),
    "geo": re.compile(r"county|region|location|town|city|latitude|longitude|(^|_)lat(_|$)|(^|_)lng|(^|_)lon(_|$)|gps|ward|constituency|address|country|zone|district|area|branch"),
    "entity": re.compile(r"user|customer|member|subscriber|artist|agent|account|profile|client|voter|citizen|owner|merchant|vendor|staff|employee|person|fan|listener|viewer|reader"),
    "money": re.compile(r"amount|price|fee|cost|balance|payment|pay(?!load)|transaction|txn|currency|total|paid|revenue|commission|wallet|invoice|charge|deposit|withdraw|credit|debit|tariff|subscription|bill"),
    "content": re.compile(r"title|description|content|body|text|article|story|headline|caption|summary|media|image|photo|audio|video|file|track|song|album|episode|program|show|news|post|message|comment"),
    "channel": re.compile(r"msisdn|shortcode|short_code|channel|device|imei|network|operator|sms|ussd|platform|source|referr|campaign|utm|app_version|browser|os_"),
    "engagement": re.compile(r"view|click|like|share|rating|vote|response|event|session|visit|status|play|listen|download|stream|impression|open|read|reaction|poll|survey|answer|question"),
    "product": re.compile(r"product|item|sku|category|brand|inventory|stock|order|cart|catalog|package|plan|bundle|offer|service|ticket|form|report"),
    "identity": re.compile(r"(^|_)id$|_id_|uuid|(^|_)ref(erence)?$|code$|number$|passport|national|kra_pin|pin$|licen[cs]e"),
}

PRODUCTS = [
    ("transaction_analytics", "Transaction & revenue analytics", {"money", "time"}, {"entity"},
     "Revenue, fee and settlement analytics; cohort and churn views once the entity dimension is joined."),
    ("customer_360", "Customer / subscriber 360 and segmentation", {"entity", "engagement"}, {"geo", "channel"},
     "Segmentation, lifetime value and retention modelling across products; requires de-identification before any release."),
    ("geo_demand", "Geospatial demand and coverage mapping", {"geo", "time"}, {"money", "engagement"},
     "County / constituency level demand, penetration and service-coverage maps sold as aggregated indices."),
    ("content_corpus", "Content catalogue, recommendation and licensing corpus", {"content"}, {"engagement", "time"},
     "Catalogue metadata, engagement-weighted recommendation features and licensable archive indexes."),
    ("channel_engagement", "Channel / telco engagement analytics (USSD, SMS, app)", {"channel", "time"}, {"engagement", "entity"},
     "Channel performance, shortcode and campaign attribution, response-rate benchmarks."),
    ("forecasting", "Time-series forecasting datasets", {"time", "money"}, {"product", "geo"},
     "Daily/weekly demand and revenue series for forecasting products and planning benchmarks."),
    ("civic_insight", "Civic and audience insight panels", {"entity", "geo"}, {"engagement", "content"},
     "Aggregated audience and civic-participation indices by geography; strictly aggregate, never row-level."),
    ("reference_data", "Reference and master-data licensing", {"product"}, {"identity", "content"},
     "Clean product / catalogue / form reference tables licensable as master data where rights permit."),
]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _fmt_bytes(value):
    value = float(value or 0)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:,.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024


def _pct(value, digits=1):
    return None if value is None else round(100 * value, digits)


def _grade(score):
    return "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "E"


def latest_job():
    for job in dispatch.list_jobs():
        if job.get("status") in TERMINAL_WITH_RESULT and (job.get("receipt") or {}).get("digest_verified"):
            return job
    return None


def running_job():
    for job in dispatch.list_jobs():
        if job.get("status") == "running":
            return job
    return None


def detail_cached(job_id):
    return (dispatch._jobs_dir() / f"{job_id}.detail.json").exists()


def detail_for(job):
    if not job:
        return None
    try:
        return dispatch.fetch_detail(job["job_id"])
    except (OSError, ValueError, KeyError):
        return None


# ----------------------------------------------------------------------------- dimensional inference

def table_dimensions(metrics):
    found = {}
    for name, column in (metrics.get("columns") or {}).items():
        lowered = name.lower()
        for dimension, pattern in DIMENSIONS.items():
            if pattern.search(lowered) or (dimension == "time" and column.get("type") in TIMESTAMP_TYPES):
                found.setdefault(dimension, []).append(name)
    if any(c.get("type") in NUMERIC_TYPES and not n.lower().endswith("id") for n, c in (metrics.get("columns") or {}).items()):
        found.setdefault("measure", [])
    return found


def _freshness_factor(days):
    if days is None:
        return 0.6
    return 1.0 if days <= 30 else 0.9 if days <= 90 else 0.75 if days <= 365 else 0.45 if days <= 3 * 365 else 0.25


def _table_quality(m):
    completeness = 1 - (m.get("null_bearing_row_ratio") or 0)
    dup = m.get("exact_duplicate_ratio") or 0
    degraded = m.get("degraded_row_ratio") or 0
    pii = m.get("pii_row_ratio") or 0
    fresh = _freshness_factor((m.get("freshness") or {}).get("staleness_days"))
    score = 100 * (0.35 * completeness + 0.2 * (1 - dup) + 0.2 * (1 - degraded) + 0.15 * fresh + 0.1 * (1 - pii))
    return {"completeness": round(completeness, 4), "duplicate_ratio": dup, "degraded_ratio": degraded, "pii_ratio": pii,
            "freshness_factor": fresh, "score": round(score, 1), "grade": _grade(score)}


def flatten(detail):
    tables = []
    for entry in detail["databases"]:
        for name, m in entry["tables"].items():
            tables.append({"connection": entry["connection"], "database": entry["database"], "table": name, **m})
    return tables


def database_profiles(tables):
    profiles = {}
    for t in tables:
        key = f"{t['connection']}/{t['database']}"
        p = profiles.setdefault(key, {"connection": t["connection"], "database": t["database"], "tables": 0, "measured_tables": 0, "failed_tables": 0,
                                      "rows_estimate": 0, "bytes": 0, "dimensions": {}, "weighted": {"score": 0.0, "rows": 0}, "pii_tables": 0,
                                      "stale_tables": 0, "empty_tables": 0, "long_text_tables": 0})
        p["tables"] += 1
        p["rows_estimate"] += t.get("rows_estimate") or 0
        p["bytes"] += (t.get("data_bytes") or 0) + (t.get("index_bytes") or 0)
        if t.get("method") == "failed":
            p["failed_tables"] += 1
        if not t.get("rows_estimate"):
            p["empty_tables"] += 1
        if t.get("rows_measured"):
            p["measured_tables"] += 1
            q = _table_quality(t)
            weight = max(1, t.get("rows_estimate") or 0)
            p["weighted"]["score"] += q["score"] * weight
            p["weighted"]["rows"] += weight
            if q["pii_ratio"] > 0.05:
                p["pii_tables"] += 1
            if ((t.get("freshness") or {}).get("staleness_days") or 0) > 365:
                p["stale_tables"] += 1
            if t.get("long_text_signatures"):
                p["long_text_tables"] += 1
        for dimension, columns in table_dimensions(t).items():
            p["dimensions"][dimension] = p["dimensions"].get(dimension, 0) + 1
    out = []
    for p in profiles.values():
        score = round(p["weighted"]["score"] / p["weighted"]["rows"], 1) if p["weighted"]["rows"] else None
        p["readiness"] = {"score": score, "grade": _grade(score) if score is not None else "unmeasured"}
        p["dimensions"] = dict(sorted(p["dimensions"].items(), key=lambda kv: -kv[1]))
        del p["weighted"]
        out.append(p)
    return sorted(out, key=lambda p: -(p["rows_estimate"] or 0))


def _days_between(earliest, latest):
    try:
        return max(0, (datetime.fromisoformat(str(latest)[:19]) - datetime.fromisoformat(str(earliest)[:19])).days)
    except (TypeError, ValueError):
        return None


def table_grain(t, dims):
    """Finest measured grain per dimension: the column with the most distinct values (or the widest time span) on this table."""
    columns, rows, out = t.get("columns") or {}, t.get("rows_estimate") or 0, {}
    for dimension in dims:
        best = None
        for name in table_dimensions(t).get(dimension, []):
            c = columns.get(name) or {}
            if dimension == "time" and (c.get("earliest") or c.get("latest")):
                span = _days_between(c.get("earliest"), c.get("latest"))
                if best is None or (span or 0) > (best.get("span_days") or 0):
                    best = {"column": name, "earliest": c.get("earliest"), "latest": c.get("latest"), "span_days": span}
            elif dimension != "time" and c.get("distinct_ratio") is not None:
                distinct = int(round(c["distinct_ratio"] * rows))
                if best is None or distinct > best["estimated_distinct"]:
                    best = {"column": name, "estimated_distinct": distinct, "distinct_ratio": c["distinct_ratio"]}
        if best:
            out[dimension] = best
    return out


def product_grain(hits, sources, dims):
    """Product-level licensable grain: widest history and highest cardinality per product dimension across the supporting tables."""
    grain, units = {}, []
    for h in hits:
        for dimension, g in table_grain(sources[h["table"]], [d for d in h["dimensions"] if d in dims]).items():
            current = grain.get(dimension)
            if dimension == "time":
                if current is None:
                    grain[dimension] = {**g, "table": h["table"]}
                else:
                    earliest = min(x for x in (current.get("earliest"), g.get("earliest")) if x)
                    latest = max(x for x in (current.get("latest"), g.get("latest")) if x)
                    grain[dimension] = {"column": current["column"], "table": current["table"], "earliest": earliest, "latest": latest, "span_days": _days_between(earliest, latest)}
            elif current is None or g["estimated_distinct"] > current["estimated_distinct"]:
                grain[dimension] = {**g, "table": h["table"]}
    for dimension, g in grain.items():
        if dimension == "time" and g.get("span_days") is not None:
            units.append(f"history {str(g['earliest'])[:10]} → {str(g['latest'])[:10]} ({g['span_days']:,} days; {g['table']}.{g['column']})")
        elif dimension != "time":
            units.append(f"≈{g['estimated_distinct']:,} distinct {dimension} values ({g['table']}.{g['column']})")
    if grain.get("time") and str(grain["time"].get("latest") or "")[:10] > now()[:10]:
        grain["time"]["future_timestamps"] = True
        units.append("latest timestamp lies in the future: placeholder dates are present in the time dimension")
    return grain, units


def data_products(tables):
    candidates = []
    measured = [t for t in tables if t.get("rows_measured") and (t.get("rows_estimate") or 0) >= 500]
    sources = {f"{t['connection']}/{t['database']}.{t['table']}": t for t in measured}
    for key, title, required, supporting, use in PRODUCTS:
        hits = []
        for t in measured:
            dims = set(table_dimensions(t))
            if required <= dims:
                q = _table_quality(t)
                rows = t.get("rows_estimate") or 0
                support = len(supporting & dims)
                value = math.log10(max(10, rows)) * (q["score"] / 100) * (1 + 0.15 * support)
                hits.append({"table": f"{t['connection']}/{t['database']}.{t['table']}", "rows_estimate": rows, "grade": q["grade"],
                             "pii_ratio": q["pii_ratio"], "staleness_days": (t.get("freshness") or {}).get("staleness_days"),
                             "dimensions": sorted(dims), "value": round(value, 3)})
        if not hits:
            continue
        hits.sort(key=lambda h: -h["value"])
        rows = sum(h["rows_estimate"] for h in hits)
        avg_grade_score = sum({"A": 90, "B": 77, "C": 62, "D": 47, "E": 30}[h["grade"]] for h in hits) / len(hits)
        pii_share = sum(1 for h in hits if h["pii_ratio"] > 0.05) / len(hits)
        stale_share = sum(1 for h in hits if (h["staleness_days"] or 0) > 365) / len(hits)
        blockers = []
        if pii_share > 0:
            blockers.append(f"{_pct(pii_share, 0)}% of supporting tables carry PII markers: de-identify or aggregate before any release")
        if stale_share > 0.5:
            blockers.append("most supporting tables have not been written for over a year: value is historical, not live")
        if avg_grade_score < 55:
            blockers.append("supporting tables grade D/E on completeness, duplication or degradation: cleanse first")
        blockers.append("use rights are declared at Connect, not measured: a release needs its own grant and purpose")
        databases = sorted({h["table"].rsplit(".", 1)[0] for h in hits})
        grain, licensable_units = product_grain(hits[:12], sources, required | supporting | {"time"})
        candidates.append({"key": key, "title": title, "use": use, "required_dimensions": sorted(required), "supporting_dimensions": sorted(supporting),
                           "tables": len(hits), "rows_estimate": rows, "databases": databases, "readiness_grade": _grade(avg_grade_score),
                           "readiness_score": round(avg_grade_score, 1), "pii_table_share": round(pii_share, 3), "stale_table_share": round(stale_share, 3),
                           "score": round(sum(h["value"] for h in hits[:12]), 2), "top_tables": hits[:8], "blockers": blockers,
                           "grain": grain, "licensable_units": licensable_units})
    return sorted(candidates, key=lambda c: -c["score"])


def _dead_columns(t):
    return [n for n, c in (t.get("columns") or {}).items() if (c.get("null_ratio") or 0) >= 0.999 and n != t.get("primary_key")]


def degradation(tables, previous, headline):
    """How the estate is decaying: damage kinds, never-populated columns, write spans per database and the trend against the previous census."""
    measured = [t for t in tables if t.get("rows_measured")]
    rows_total = sum(max(1, t.get("rows_estimate") or 0) for t in measured) or 1
    kinds = {k: 0.0 for k in DEGRADATION_KINDS}
    per_db = {}
    for t in tables:
        key = f"{t['connection']}/{t['database']}"
        p = per_db.setdefault(key, {"connection": t["connection"], "database": t["database"], "tables": 0, "measured": 0, "rows": 0, "degraded_weighted": 0.0,
                                    "columns": 0, "dead_columns": 0, "dead_column_names": [], "stale_tables": 0, "earliest_write": None, "latest_write": None, "worst_table": None})
        p["tables"] += 1
        if not t.get("rows_measured"):
            continue
        weight = max(1, t.get("rows_estimate") or 0)
        p["measured"] += 1; p["rows"] += weight; p["degraded_weighted"] += (t.get("degraded_row_ratio") or 0) * weight
        for k in DEGRADATION_KINDS:
            kinds[k] += max((c.get(k) or 0) for c in (t.get("columns") or {}).values()) * weight if t.get("columns") else 0.0
        dead = _dead_columns(t)
        p["columns"] += t.get("column_count") or len(t.get("columns") or {}); p["dead_columns"] += len(dead)
        p["dead_column_names"].extend(f"{t['table']}.{n}" for n in dead[:3])
        fresh = t.get("freshness") or {}
        if (fresh.get("staleness_days") or 0) > 365:
            p["stale_tables"] += 1
        if fresh.get("earliest_write") and (p["earliest_write"] is None or fresh["earliest_write"] < p["earliest_write"]):
            p["earliest_write"] = fresh["earliest_write"]
        if fresh.get("latest_write") and (p["latest_write"] is None or fresh["latest_write"] > p["latest_write"]):
            p["latest_write"] = fresh["latest_write"]
        if (t.get("degraded_row_ratio") or 0) > 0 and (p["worst_table"] is None or t["degraded_row_ratio"] > p["worst_table"]["degraded_row_ratio"]):
            p["worst_table"] = {"table": t["table"], "degraded_row_ratio": t["degraded_row_ratio"], "rows_estimate": t.get("rows_estimate")}
    previous_dbs = {f"{d['connection']}/{d['database']}": d for d in (previous or {}).get("databases", [])}
    previous_fp = (previous or {}).get("schema_fingerprints") or {}
    databases = []
    for key, p in per_db.items():
        drift = sorted(k.rsplit(".", 1)[1] for k, fp in _fingerprints(tables).items() if k.startswith(key + ".") and k in previous_fp and previous_fp[k] != fp)
        prev = previous_dbs.get(key)
        p.update(degraded_ratio=round(p["degraded_weighted"] / p["rows"], 4) if p["rows"] else None,
                 dead_column_share=round(p["dead_columns"] / p["columns"], 4) if p["columns"] else None,
                 write_span_days=_days_between(p["earliest_write"], p["latest_write"]),
                 days_since_last_write=_days_between(p["latest_write"], now()) if p["latest_write"] else None,
                 growth={"rows_delta": (sum(t.get("rows_estimate") or 0 for t in tables if f"{t['connection']}/{t['database']}" == key) - (prev.get("rows_estimate") or 0)) if prev else None,
                         "bytes_delta": (sum((t.get("data_bytes") or 0) + (t.get("index_bytes") or 0) for t in tables if f"{t['connection']}/{t['database']}" == key) - (prev.get("bytes") or 0)) if prev else None,
                         "tables_delta": (p["tables"] - prev["tables"]) if prev else None},
                 schema_drift_tables=drift, dead_column_names=p["dead_column_names"][:6])
        del p["degraded_weighted"]
        databases.append(p)
    databases.sort(key=lambda p: -(p["degraded_ratio"] or 0))
    dead_total = sum(p["dead_columns"] for p in databases); columns_total = sum(p["columns"] for p in databases)
    trend = None
    if previous:
        ph = previous["headline"]
        trend = {"previous_job_id": previous["job_id"], "previous_measured_at": previous.get("measured_at"),
                 "deltas": {k: (round(headline[k] - ph[k], 2) if isinstance(headline.get(k), (int, float)) and isinstance(ph.get(k), (int, float)) else None)
                            for k in ("bytes_total", "rows_estimate", "tables", "tables_measured", "exact_duplicate_pct", "degraded_pct", "null_bearing_pct", "pii_pct",
                                      "stale_pct_of_bytes", "reclaimable_bytes", "empty_tables", "failed_tables", "duplicate_table_pairs")},
                 "schema_drift_tables": sum(len(p["schema_drift_tables"]) for p in databases),
                 "coverage_changed": (headline.get("tables_measured") != ph.get("tables_measured")) or (headline.get("connections") != ph.get("connections")),
                 "databases_grown": sum(1 for p in databases if (p["growth"]["rows_delta"] or 0) > 0),
                 "databases_shrunk": sum(1 for p in databases if (p["growth"]["rows_delta"] or 0) < 0)}
    return {"kinds": {k.replace("_ratio", ""): round(v / rows_total, 4) for k, v in kinds.items()},
            "kinds_note": "Row-weighted share of measured rows whose worst column shows the kind; a row can carry several kinds.",
            "dead_columns": dead_total, "columns_measured": columns_total, "dead_column_share": round(dead_total / columns_total, 4) if columns_total else None,
            "dead_columns_note": "Columns never populated (null on ≥99.9 % of measured rows, primary key excluded): schema carried without data.",
            "databases": databases, "trend": trend,
            "trend_note": ("Deltas against the previous verified estate intelligence census over the same connections." if previous else
                           "No previous verified census to compare against; trend starts with the next census.")}


def _fingerprints(tables):
    return {f"{t['connection']}/{t['database']}.{t['table']}": t.get("schema_fingerprint") for t in tables if t.get("schema_fingerprint")}


def cost_strategies(summary, tables, total_bytes):
    unit = os.environ.get("ESTATE_STORAGE_COST_PER_GB_MONTH")
    price = float(unit) if unit else None

    def money(bytes_):
        return round(price * bytes_ / 1024 ** 3, 2) if price else None

    storage, dup = summary["storage"], summary["duplication"]
    empty = [t for t in tables if not t.get("rows_estimate")]
    stale = storage.get("top_stale") or []
    within = [t for t in tables if (t.get("exact_duplicate_ratio") or 0) >= 0.01 and t.get("data_bytes")]
    within.sort(key=lambda t: -(t["exact_duplicate_ratio"] * t["data_bytes"]))
    redundant = [t for t in tables if t.get("redundant_indexes")]
    orphaned = summary["quality"].get("orphaned_references") or []
    groups = summary["duplication"].get("same_schema_groups") or 0
    items = [
        {"key": "cross_table_consolidation", "title": "Consolidate duplicate and staging copies of the same tables",
         "bytes": dup["cross_table_duplicate_bytes_estimate"], "action": "Retire or snapshot-then-drop the smaller copy of each same-schema pair with measured content overlap; keep one system of record.",
         "evidence": [f"{p['a']} ↔ {p['b']} · overlap {_pct(p['content_overlap_estimate'], 0)}% · {_fmt_bytes(p['bytes_smaller'])}" for p in dup["top_pairs"][:6]],
         "risk": "Copies may be deliberate (staging, backups). Confirm ownership before retirement; the sketch overlap is an estimate, not a row-level diff."},
        {"key": "within_table_dedup", "title": "De-duplicate exact repeated rows inside tables",
         "bytes": dup["within_table_duplicate_bytes_estimate"], "action": "Add uniqueness constraints or a merge step at ingestion; archive the historical duplicates.",
         "evidence": [f"{t['database']}.{t['table']} · {_pct(t['exact_duplicate_ratio'])}% repeated · {_fmt_bytes(t['data_bytes'])}" for t in within[:6]],
         "risk": "Duplicates measured on complete passes or stratified samples; the primary key was excluded from the comparison."},
        {"key": "archive_stale", "title": "Move tables not written for over a year to cold storage",
         "bytes": storage["stale_bytes"], "action": "Export to compressed object storage, keep a schema stub and a pointer; restore on demand.",
         "evidence": [f"{t['database']}.{t['table']} · {t['staleness_days']} days · {_fmt_bytes(t['data_bytes'])}" for t in stale[:6]],
         "risk": "Staleness is read from the latest timestamp column; tables without timestamps are not counted as stale."},
        {"key": "drop_empty", "title": "Drop or archive empty tables",
         "bytes": storage["empty_table_bytes"], "action": "Remove empty tables and their indexes after a 30-day observation window.",
         "evidence": [f"{t['database']}.{t['table']}" for t in empty[:8]] + ([f"… {len(empty) - 8} more"] if len(empty) > 8 else []),
         "risk": "Empty by TABLE_ROWS estimate; a freshly truncated live table looks the same."},
        {"key": "redundant_indexes", "title": "Remove redundant (prefix-covered) indexes",
         "bytes": storage["redundant_index_bytes_estimate"], "action": "Drop each non-unique index whose columns are a leading prefix of another index on the same table.",
         "evidence": [f"{t['database']}.{t['table']} · {r['index']} covered by {r['covered_by']}" for t in redundant[:6] for r in t["redundant_indexes"][:1]],
         "risk": "Write amplification falls immediately; verify no query hints name the dropped index."},
        {"key": "orphan_repair", "title": "Repair or purge orphaned references",
         "bytes": 0, "action": "Reconcile foreign-key candidates whose sampled values are missing in the target table; purge rows that reference nothing.",
         "evidence": [f"{o['table']}.{o['column']} → {o['target']} · {_pct(o['orphan_ratio'], 0)}% orphaned of {o['sampled']} sampled" for o in orphaned[:6]],
         "risk": "Targets were inferred from column names (x_id → x/xs); a missing target may be a naming convention, not a break."},
        {"key": "pii_minimisation", "title": "Minimise PII-dense tables that no product needs",
         "bytes": 0, "action": "Tokenise or drop personal columns in analytics copies; keep raw identifiers only in the system of record.",
         "evidence": [f"{t['database']}.{t['table']} · {_pct(t['pii_row_ratio'], 0)}% of sampled rows" for t in (summary["quality"].get("top_pii") or [])[:6]],
         "risk": "Detector is deterministic and sampled; absence of a marker is not absence of personal data."},
    ]
    for item in items:
        item["share_of_estate"] = round(item["bytes"] / total_bytes, 4) if total_bytes else None
        item["monthly_saving"] = money(item["bytes"])
        item["bytes_label"] = _fmt_bytes(item["bytes"]) if item["bytes"] else "not a storage saving"
    items.sort(key=lambda i: -i["bytes"])
    return {"currency_note": ("priced with ESTATE_STORAGE_COST_PER_GB_MONTH=" + unit) if price else
            "No storage tariff on record: savings are stated in bytes. Set ESTATE_STORAGE_COST_PER_GB_MONTH to price them.",
            "same_schema_groups": groups, "items": items}


def condition_bytes(tables):
    """Byte-weighted condition split for the 'Condition of what was read' bar (conditions can overlap; clean is the remainder)."""
    total = sum((t.get("data_bytes") or 0) + (t.get("index_bytes") or 0) for t in tables)
    not_read = sum((t.get("data_bytes") or 0) + (t.get("index_bytes") or 0) for t in tables if t.get("method") == "failed")
    measured = [t for t in tables if t.get("rows_measured")]
    dup = sum((t.get("exact_duplicate_ratio") or 0) * (t.get("data_bytes") or 0) for t in measured)
    degraded = sum((t.get("degraded_row_ratio") or 0) * (t.get("data_bytes") or 0) for t in measured)
    incomplete = sum((t.get("null_bearing_row_ratio") or 0) * (t.get("data_bytes") or 0) for t in measured)
    stale_90 = sum((t.get("data_bytes") or 0) + (t.get("index_bytes") or 0) for t in measured if ((t.get("freshness") or {}).get("staleness_days") or 0) > 90)
    measured_bytes = sum((t.get("data_bytes") or 0) + (t.get("index_bytes") or 0) for t in tables if t.get("rows_measured") or not t.get("rows_estimate"))
    clean = max(0, measured_bytes - dup - degraded - incomplete)
    return {"total": total, "not_read": int(not_read), "duplicate": int(dup), "degraded": int(degraded), "incomplete": int(incomplete),
            "stale_90_days": int(stale_90), "measured": int(measured_bytes), "clean": int(clean),
            "unmeasured": int(max(0, total - measured_bytes - not_read))}


def _reason(code):
    code = str(code or "")
    if "1045" in code:
        return "MYSQL_ACCESS_DENIED_1045 (GRANT pending, owner dependency)"
    if "rc=137" in code or "out of memory" in code.lower() or code.endswith("PULL_SEAM_WORKER_FAILED:"):
        return "JUMP_HOST_OUT_OF_MEMORY"
    return code[:80]


def _connection_detail(job, detail, tables):
    """Per-connection source rows in the Registry's source_details shape (label, status, tables, bytes, reason)."""
    errors = (job.get("receipt") or {}).get("result", {}).get("errors") or []
    declared = [c["label"] for c in job.get("connections") or []]
    out = []
    for index, label in enumerate(dict.fromkeys(declared)):
        mine = [t for t in tables if t["connection"] == label]
        db_errors = [e for e in errors if e.get("connection") == label]
        blocked = bool(db_errors) and not mine
        failed = sum(1 for t in mine if t.get("method") == "failed")
        status = "blocked" if blocked else "partial" if (db_errors or failed) else "complete"
        reason = (_reason(db_errors[0].get("code")) if db_errors else f"{failed} tables failed" if failed else None)
        out.append({"source_ref": f"{job['job_id']}:{index}", "label": label, "kind": "mysql", "status": status, "reason_code": reason,
                    "table_count": len(mine), "database_count": len({t["database"] for t in mine}),
                    "volume_bytes": sum((t.get("data_bytes") or 0) + (t.get("index_bytes") or 0) for t in mine),
                    "rows_estimate": sum(t.get("rows_estimate") or 0 for t in mine), "method": "estate intelligence census via the jump host; aggregates only",
                    "observed_at": job.get("finished_at"), "worker_id": job.get("host")})
    return out


def build(job, detail, previous=None):
    """Full report from a job and its verified detail (per-table aggregates); `previous` is the prior verified report for trend."""
    tables = flatten(detail)
    summary = rollup([{**d, "connection_label": d["connection"]} for d in detail["databases"]])
    measured = [t for t in tables if t.get("rows_measured")]
    total_bytes = summary["bytes_total"]
    w = summary["weighted"]
    stale_bytes = summary["storage"]["stale_bytes"]
    grades = {}
    for t in measured:
        grades[_table_quality(t)["grade"]] = grades.get(_table_quality(t)["grade"], 0) + 1
    profiles = database_profiles(tables)
    products = data_products(tables)
    strategies = cost_strategies(summary, tables, total_bytes)
    errors = (job.get("receipt") or {}).get("result", {}).get("errors") or []
    headline = {
        "connections": len({t["connection"] for t in tables}), "databases": len(detail["databases"]), "tables": summary["tables_total"],
        "tables_measured": summary["tables_measured"], "rows_estimate": summary["rows_estimate_total"], "rows_measured": summary["rows_measured_total"],
        "bytes_total": total_bytes, "bytes_label": _fmt_bytes(total_bytes),
        "exact_duplicate_pct": _pct(w.get("exact_duplicate_ratio")), "normalised_duplicate_pct": _pct(w.get("normalised_duplicate_ratio")),
        "degraded_pct": _pct(w.get("degraded_row_ratio")), "null_bearing_pct": _pct(w.get("null_bearing_row_ratio")), "pii_pct": _pct(w.get("pii_row_ratio")),
        "near_duplicate_text_pct": _pct(w.get("near_duplicate_text_ratio")), "stale_pct_of_bytes": _pct(stale_bytes / total_bytes) if total_bytes else None,
        "reclaimable_bytes": summary["storage"]["reclaimable_bytes_estimate"], "reclaimable_label": _fmt_bytes(summary["storage"]["reclaimable_bytes_estimate"]),
        "reclaimable_pct": _pct(summary["storage"]["reclaimable_bytes_estimate"] / total_bytes) if total_bytes else None,
        "duplicate_table_pairs": summary["duplication"]["cross_table_pairs"], "failed_tables": summary["failed_tables"], "empty_tables": summary["storage"]["empty_tables"],
        "grades": dict(sorted(grades.items())), "blocked_connections": sorted({e["connection"] for e in errors if not e.get("database")}),
        "pii_rows_checked": sum(t.get("pii_rows_checked") or 0 for t in measured),
    }
    reading = (f"{headline['databases']} databases and {headline['tables']:,} tables ({headline['bytes_label']}, ≈{headline['rows_estimate']:,} rows) were measured; "
               f"{headline['exact_duplicate_pct']}% of rows repeat exactly, {headline['degraded_pct']}% carry damage, {headline['null_bearing_pct']}% have empty required-looking fields "
               f"and {headline['pii_pct']}% of sampled rows carry personal-data markers. About {headline['reclaimable_label']} ({headline['reclaimable_pct']}%) looks reclaimable.")
    within = sorted([t for t in measured if (t.get("exact_duplicate_ratio") or 0) >= 0.01], key=lambda t: -(t["exact_duplicate_ratio"] * (t.get("data_bytes") or 0)))
    return {"job_id": job["job_id"], "status": job["status"], "measured_at": job.get("finished_at"), "built_at": now(), "reading": reading, "report_version": REPORT_VERSION,
            "headline": headline, "summary": summary, "databases": profiles, "data_products": products, "cost_strategies": strategies,
            "degradation": degradation(tables, previous, headline),
            "within_table_duplicates": [{"connection": t["connection"], "database": t["database"], "table": t["table"], "exact_duplicate_ratio": t["exact_duplicate_ratio"],
                                         "normalised_duplicate_ratio": t.get("normalised_duplicate_ratio"), "rows_estimate": t.get("rows_estimate"), "data_bytes": t.get("data_bytes"),
                                         "method": t.get("method")} for t in within[:25]],
            "condition_bytes": condition_bytes(tables),
            "connections": _connection_detail(job, detail, tables),
            "schema_fingerprints": {f"{t['connection']}/{t['database']}.{t['table']}": t.get("schema_fingerprint") for t in tables if t.get("schema_fingerprint")},
            "errors": errors, "coverage_note": "RMS MySQL only (owner order 1-a). OBS object and NAS file duplication follow from the enumeration frontier; "
            "languages, rights and semantic (embedding) similarity were not measured. Text near-duplicates use MinHash on the jump host so row text never left the estate.",
            "method_note": summary["method_note"], "row_values_retained": False}


def compact(report):
    """Registry-sized projection for the overview envelope."""
    h = report["headline"]
    return {"job_id": report["job_id"], "status": report["status"], "measured_at": report["measured_at"], "reading": report["reading"], "headline": h,
            "condition": {k: report["summary"]["weighted"].get(k) for k in ("exact_duplicate_ratio", "degraded_row_ratio", "null_bearing_row_ratio", "pii_row_ratio")},
            "stale_bytes": report["summary"]["storage"]["stale_bytes"], "method_shares": {k: report["summary"][k] for k in ("complete_tables", "sampled_tables", "head_sampled_tables", "failed_tables")},
            "connections": _connection_bytes(report), "top_pairs": report["summary"]["duplication"]["top_pairs"][:5],
            "top_degraded": report["summary"]["quality"]["top_degraded"][:5], "top_pii": report["summary"]["quality"]["top_pii"][:5],
            "data_products": [{k: c[k] for k in ("key", "title", "use", "tables", "rows_estimate", "readiness_grade", "databases", "blockers")} for c in report["data_products"][:8]],
            "cost_strategies": [{k: s[k] for k in ("key", "title", "bytes", "bytes_label", "share_of_estate", "action", "monthly_saving")} for s in report["cost_strategies"]["items"]],
            "currency_note": report["cost_strategies"]["currency_note"], "databases": [{k: p[k] for k in ("connection", "database", "tables", "rows_estimate", "bytes", "readiness", "dimensions", "failed_tables")} for p in report["databases"]],
            "coverage_note": report["coverage_note"], "brief_path": report.get("brief_path"), "dossier": report.get("dossier")}


def _connection_bytes(report):
    out = {}
    for p in report["databases"]:
        out[p["connection"]] = out.get(p["connection"], 0) + p["bytes"]
    return [{"connection": k, "bytes": v} for k, v in sorted(out.items(), key=lambda kv: -kv[1])]


def render_markdown(report):
    h = report["headline"]
    lines = [f"# Akki Estate Intelligence — RMS MySQL estate", "",
             f"Job `{report['job_id']}` · status **{report['status']}** · measured {report['measured_at']} · built {report['built_at']}", "",
             "Census only: rows were measured on the jump host and discarded; this brief carries aggregates, sketches and hashes — no row, cell or identifier value.", "",
             "## What the census found", "", report["reading"], "",
             "| Figure | Value |", "|---|---|",
             f"| Connections / databases / tables | {h['connections']} / {h['databases']} / {h['tables']:,} |",
             f"| Rows (estimate) / rows measured | {h['rows_estimate']:,} / {h['rows_measured']:,} |",
             f"| Bytes held (data + index) | {h['bytes_label']} |",
             f"| Exact duplicate rows | {h['exact_duplicate_pct']}% (normalised {h['normalised_duplicate_pct']}%) |",
             f"| Degraded rows (placeholder, mojibake, truncation) | {h['degraded_pct']}% |",
             f"| Rows with empty fields | {h['null_bearing_pct']}% |",
             f"| Sampled rows with PII markers | {h['pii_pct']}% |",
             f"| Long-text near-duplicates (MinHash) | {h['near_duplicate_text_pct']}% |",
             f"| Bytes in tables not written for > 1 year | {h['stale_pct_of_bytes']}% |",
             f"| Reclaimable bytes (estimate) | {h['reclaimable_label']} ({h['reclaimable_pct']}%) |",
             f"| Same-schema duplicate table pairs with content overlap | {h['duplicate_table_pairs']} |",
             f"| Tables failed / empty | {h['failed_tables']} / {h['empty_tables']} |",
             f"| Table readiness grades | {', '.join(f'{k}: {v}' for k, v in h['grades'].items())} |", "",
             "## Databases — readiness grades and dimensional profile", "",
             "| Connection / database | Tables | Rows est. | Bytes | Grade | Dimensions (tables carrying) |", "|---|---|---|---|---|---|"]
    for p in report["databases"]:
        dims = ", ".join(f"{k} {v}" for k, v in list(p["dimensions"].items())[:6])
        lines.append(f"| {p['connection']} / {p['database']} | {p['tables']} | {p['rows_estimate']:,} | {_fmt_bytes(p['bytes'])} | {p['readiness']['grade']} ({p['readiness']['score']}) | {dims} |")
    lines += ["", "## Degradation and trend", "", report["degradation"]["kinds_note"], "",
              "| Damage kind | Share of measured rows |", "|---|---|"] + [f"| {k} | {_pct(v)}% |" for k, v in report["degradation"]["kinds"].items()]
    lines += ["", f"Never-populated columns: {report['degradation']['dead_columns']:,} of {report['degradation']['columns_measured']:,} measured "
              f"({_pct(report['degradation']['dead_column_share'])}%). {report['degradation']['dead_columns_note']}", "",
              "| Connection / database | Degraded rows | Dead columns | Stale tables | Writes span | Last write | Schema drift | Rows Δ |", "|---|---|---|---|---|---|---|---|"]
    for p in report["degradation"]["databases"]:
        span = f"{p['write_span_days']:,} days" if p.get("write_span_days") is not None else "no timestamps"
        last = f"{p['days_since_last_write']:,} days ago" if p.get("days_since_last_write") is not None else "—"
        delta = f"{p['growth']['rows_delta']:+,}" if p["growth"].get("rows_delta") is not None else "—"
        lines.append(f"| {p['connection']} / {p['database']} | {_pct(p['degraded_ratio']) if p['degraded_ratio'] is not None else '—'}% | {p['dead_columns']} / {p['columns']} | {p['stale_tables']} | {span} | {last} | {len(p['schema_drift_tables'])} | {delta} |")
    trend = report["degradation"]["trend"]
    lines += ["", report["degradation"]["trend_note"], ""]
    if trend:
        lines += [f"Against `{trend['previous_job_id']}` ({trend['previous_measured_at']}): " + "; ".join(f"{k} {v:+,}" for k, v in trend["deltas"].items() if v is not None)
                  + f"; {trend['schema_drift_tables']} tables changed schema; {trend['databases_grown']} databases grew, {trend['databases_shrunk']} shrank.", ""]
    lines += ["## What the data can do — dimensional monetisation candidates", "",
              "Ranked by rows × readiness × supporting dimensions. Every candidate is an aggregate or de-identified product; rights are declared at Connect, not measured here.", ""]
    for i, c in enumerate(report["data_products"], 1):
        lines += [f"### {i}. {c['title']} — grade {c['readiness_grade']}", "", c["use"], "",
                  f"- Dimensions required: {', '.join(c['required_dimensions'])}; supporting: {', '.join(c['supporting_dimensions'])}",
                  f"- {c['tables']} supporting tables, ≈{c['rows_estimate']:,} rows across {len(c['databases'])} databases",
                  f"- Licensable grain: " + ("; ".join(c.get("licensable_units") or []) or "not measurable from column statistics"),
                  f"- Top tables: " + "; ".join(f"{t['table']} ({t['rows_estimate']:,} rows, {t['grade']})" for t in c["top_tables"][:4]),
                  "- Blockers: " + " · ".join(c["blockers"]), ""]
    lines += ["## Strategies to reduce cost", "", report["cost_strategies"]["currency_note"], "",
              "| Strategy | Reclaimable | Share | Action |", "|---|---|---|---|"]
    for s in report["cost_strategies"]["items"]:
        share = f"{_pct(s['share_of_estate'])}%" if s["share_of_estate"] is not None and s["bytes"] else "—"
        lines.append(f"| {s['title']} | {s['bytes_label']} | {share} | {s['action']} |")
    lines += ["", "### Evidence per strategy", ""]
    for s in report["cost_strategies"]["items"]:
        if s["evidence"]:
            lines += [f"**{s['title']}** — risk: {s['risk']}", ""] + [f"- {e}" for e in s["evidence"]] + [""]
    q = report["summary"]["quality"]
    lines += ["## Where it falls short", ""]
    for e in report["errors"]:
        lines.append(f"- Connection `{e.get('connection')}`" + (f" database `{e['database']}`" if e.get("database") else "") + f": {e.get('code')}")
    for t in q["top_degraded"][:8]:
        lines.append(f"- Degraded: {t['database']}.{t['table']} · {_pct(t['degraded_row_ratio'])}% of {t['rows_estimate']:,} rows ({t['method']})")
    for t in q["top_pii"][:8]:
        lines.append(f"- PII-dense: {t['database']}.{t['table']} · {_pct(t['pii_row_ratio'])}% of sampled rows")
    lines += ["", "## Method and limits", "", report["method_note"], "", report["coverage_note"], ""]
    if report.get("dossier"):
        lines += ["## Governed dossier (LLM-composed from these aggregates only)", "",
                  f"Model {report['dossier']['model_id']} via the single chokepoint · receipt `{report['dossier']['receipt_id']}` · {report['dossier']['at']}", "",
                  report["dossier"]["text"], ""]
    return "\n".join(lines)


def publish(report):
    BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    text = render_markdown(report)
    path = BRIEF_DIR / f"Akki_Estate_Intelligence_{report['job_id']}.md"
    path.write_text(text)
    (BRIEF_DIR / "Akki_Estate_Intelligence_latest.md").write_text(text)
    return f"/briefs/{path.name}", hashlib.sha256(text.encode()).hexdigest()


def _report_path(job_id):
    return dispatch._jobs_dir() / f"{job_id}.report.json"


def _previous_report(job):
    """The latest verified report banked BEFORE this job (cached only; never a remote read)."""
    for other in dispatch.list_jobs():
        if other["job_id"] != job["job_id"] and other.get("submitted_at", "") < job.get("submitted_at", "") and other.get("status") in TERMINAL_WITH_RESULT:
            path = _report_path(other["job_id"])
            if path.exists():
                return json.loads(path.read_text())
    return None


def report_for(job_id, rebuild=False, cached_only=False):
    """Cached report for a terminal job; built once from the digest-verified detail, then banked beside the job."""
    job = dispatch.load_job(job_id)
    if not job or job.get("status") not in TERMINAL_WITH_RESULT or not (job.get("receipt") or {}).get("digest_verified"):
        return None
    path = _report_path(job_id)
    if path.exists() and not rebuild:
        cached = json.loads(path.read_text())
        if cached.get("report_version") == REPORT_VERSION:
            return cached
    if cached_only and not detail_cached(job_id):
        return None
    detail = detail_for(job)
    if not detail:
        return None
    report = build(job, detail, _previous_report(job))
    dossier_path = dispatch._jobs_dir() / f"{job_id}.dossier.json"
    if dossier_path.exists():
        report["dossier"] = json.loads(dossier_path.read_text())
    report["brief_path"], report["brief_sha256"] = publish(report)
    path.write_text(json.dumps(report, indent=1, default=str))
    return report


def latest_report(cached_only=False):
    job = latest_job()
    return report_for(job["job_id"], cached_only=cached_only) if job else None


def overview_projection():
    """What the Registry needs: the latest verified report (compact, cached only — no remote read on a poll) and any running census."""
    running = running_job()
    report = latest_report(cached_only=True)
    return {"latest": compact(report) if report else None, "awaiting_report": bool(latest_job() and not report),
            "running": {"job_id": running["job_id"], "started_at": running.get("started_at"),
                        "progress": (running.get("remote_state") or {}).get("progress"),
                        "databases_done": len((running.get("remote_state") or {}).get("databases_done") or [])} if running else None}


DOSSIER_SYSTEM = ("You are Akki's estate intelligence analyst. You receive ONLY aggregate census measurements of a relational data estate "
                  "(ratios, byte counts, table and column names, readiness grades). Write a decisive, numerate estate-handling dossier for the "
                  "estate owner in British English Markdown with these sections: Executive summary; Condition of the estate; Duplication and "
                  "storage economics; What the data can do (dimensional monetisation, one paragraph per candidate, aggregate or de-identified "
                  "products only); Risks and obligations (PII, staleness, rights); 90-day plan (numbered). Cite the figures you use. Never invent "
                  "figures, prices or rights; where a figure is missing say it is unmeasured.")


async def compose_dossier(job_id, actor, tenant_id, model="gpt-5-mini", provider="emergent"):
    """One governed crossing: compact aggregates in, Markdown dossier out; banked and folded into the report."""
    from services.chokepoint import llm as chokepoint
    report = report_for(job_id)
    if not report:
        return None
    prompt = json.dumps({k: report[k] for k in ("reading", "headline", "databases", "coverage_note")} |
                        {"data_products": [{k: c[k] for k in ("title", "use", "tables", "rows_estimate", "readiness_grade", "databases", "blockers", "licensable_units")} for c in report["data_products"]],
                         "cost_strategies": [{k: s[k] for k in ("title", "bytes_label", "share_of_estate", "action", "risk")} for s in report["cost_strategies"]["items"]],
                         "degradation": {k: report["degradation"][k] for k in ("kinds", "kinds_note", "dead_columns", "columns_measured", "dead_column_share", "trend", "trend_note")},
                         "top_duplicate_pairs": report["summary"]["duplication"]["top_pairs"][:8],
                         "top_degraded": report["summary"]["quality"]["top_degraded"][:8], "top_pii": report["summary"]["quality"]["top_pii"][:8],
                         "orphaned_references": report["summary"]["quality"]["orphaned_references"][:8]}, default=str)
    response = await chokepoint.invoke(purpose="census.estate_intelligence_dossier", prompt=prompt, masking_tier="llm_prompt_governed_text",
                                       actor=actor, model=model, provider=provider, tenant_id=tenant_id, custody_class="tenant_estate",
                                       system_message=DOSSIER_SYSTEM, session_id=f"eid-{job_id}")
    dossier = {"text": response.text, "receipt_id": response.receipt_id, "model_id": response.model_id, "provider": response.provider,
               "tokens_in": response.tokens_in, "tokens_out": response.tokens_out, "latency_ms": response.latency_ms, "at": now(),
               "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "composed_from": "aggregates only; no row values"}
    (dispatch._jobs_dir() / f"{job_id}.dossier.json").write_text(json.dumps(dossier, indent=1))
    report["dossier"] = dossier
    report["brief_path"], report["brief_sha256"] = publish(report)
    _report_path(job_id).write_text(json.dumps(report, indent=1, default=str))
    return report


# ----------------------------------------------------------------------------- census records (owner's census report design)

CONDITION_COLOURS = {"Clean": "var(--sage)", "Duplicate": "var(--brass)", "Degraded": "#b04a3a", "Incomplete": "#c9a24a", "Not read": "#b8b0a0"}


def _duration(job):
    try:
        return (datetime.fromisoformat(job["finished_at"].replace("Z", "+00:00")) - datetime.fromisoformat(job["started_at"].replace("Z", "+00:00"))).total_seconds()
    except (KeyError, TypeError, ValueError, AttributeError):
        return None


def _metrics(report, previous):
    """The Registry's coverage / condition / readiness rows, measured from the estate intelligence aggregates."""
    from services.census_autonomy.registry_report import ROWS
    h, cb, w = report["headline"], report["condition_bytes"], report["summary"]["weighted"]
    total = cb["total"] or 1
    connections = report["connections"]
    full = sum(1 for c in connections if c["status"] == "complete")
    blocked = sum(1 for c in connections if c["status"] == "blocked")
    drift = None
    if previous and previous.get("schema_fingerprints") and set(c["label"] for c in connections) == set(c["label"] for c in previous.get("connections", [])):
        old = previous["schema_fingerprints"]
        changed = {key.rsplit(".", 1)[0] for key, fp in report["schema_fingerprints"].items() if key in old and old[key] != fp}
        drift = len(changed)
    dup, degraded, incomplete = w.get("exact_duplicate_ratio"), w.get("degraded_row_ratio"), w.get("null_bearing_row_ratio")
    clean = max(0.0, 1 - (dup or 0) - (degraded or 0) - (incomplete or 0)) if None not in (dup, degraded, incomplete) else None
    values = {"data_held": cb["total"], "sources_full": full, "share_measured": _pct(cb["measured"] / total), "not_read": blocked,
              "duplicates": _pct(dup), "degraded": _pct(degraded), "incomplete": _pct(incomplete), "stale": _pct(cb["stale_90_days"] / total),
              "schema_drift": drift, "verified": None, "pii": _pct(w.get("pii_row_ratio")), "usable": _pct(clean), "opportunities": len(report["data_products"])}
    notes = {
        "data_held": f"Data + index bytes of every table reached across {len(connections)} connections; blocked connections contribute nothing.",
        "sources_full": f"{full} of {len(connections)} connections measured every table; {blocked} blocked, the rest had failed tables.",
        "share_measured": f"Bytes in tables read this census (complete pass, stratified or head sample; empty tables count as read): {_fmt_bytes(cb['measured'])} of {_fmt_bytes(cb['total'])}.",
        "not_read": f"{h['failed_tables']} tables refused or ran out of budget ({_fmt_bytes(cb['not_read'])}); blocked connections: {', '.join(h['blocked_connections']) or 'none'}.",
        "duplicates": f"Exact repeated rows (primary key excluded), weighted by estimated rows; ≈{_fmt_bytes(cb['duplicate'])} within tables plus {h['duplicate_table_pairs']} same-schema table pairs with content overlap.",
        "degraded": f"Rows with placeholder values, mojibake or truncation at the column limit; ≈{_fmt_bytes(cb['degraded'])}.",
        "incomplete": f"Rows with at least one empty field; ≈{_fmt_bytes(cb['incomplete'])}. Orphaned references are listed in the brief.",
        "stale": f"Bytes in tables whose latest timestamp is older than 90 days: {_fmt_bytes(cb['stale_90_days'])}; tables without timestamps are not counted.",
        "schema_drift": ("Databases with at least one table whose column set or types changed against the previous estate intelligence census." if drift is not None
                         else "No comparable previous estate intelligence census over the same connections."),
        "verified": "No second-source or human verification was performed by this census.",
        "pii": f"Deterministic PII detector on {h['pii_rows_checked']:,} sampled rows (every row for the first 2,000 of a table, then one in ten); URL markers excluded; kinds: "
               + ", ".join(f"{k.split('.')[-1]} {v:,}" for k, v in sorted(report["summary"]["quality"]["pii_kinds"].items(), key=lambda kv: -kv[1])) + ".",
        "usable": "Rows with no flagged condition (not duplicated, not degraded, no empty field). Use rights are declared at Connect, not established here.",
        "opportunities": f"Dimensional monetisation candidates inferred from measured columns; the top candidate is {report['data_products'][0]['title'] if report['data_products'] else 'none'}.",
    }
    metrics = {}
    for group, key, label, description, unit in ROWS:
        value = values.get(key)
        status = "sampled" if key == "pii" and value is not None else "measured" if value is not None else "unmeasured"
        prior = ((previous or {}).get("census_record") or {}).get("report", {}).get("metrics", {}).get(key, {})
        delta = round(value - prior["value"], 2) if value is not None and prior.get("value") is not None and prior.get("status") == status and isinstance(value, (int, float)) else None
        population = h["pii_rows_checked"] if key == "pii" else report["summary"]["rows_measured_total"]
        metrics[key] = {"key": key, "group": group, "label": label, "description": description, "unit": unit, "value": value, "status": status,
                        "method": notes[key], "measured_at": report["measured_at"], "population": population, "record_id": report["job_id"],
                        "previous_record_id": previous["job_id"] if previous else None, "delta": delta}
    shares = {"Clean": cb["clean"], "Duplicate": cb["duplicate"], "Degraded": cb["degraded"], "Incomplete": cb["incomplete"], "Not read": cb["not_read"] + cb["unmeasured"]}
    distribution = [{"label": k, "share": round(v / total, 4), "bytes": v, "color": CONDITION_COLOURS[k]} for k, v in shares.items()]
    return {"metrics": metrics, "groups": [{"key": g, "label": g.title(), "rows": [metrics[k] for grp, k, *_ in ROWS if grp == g]} for g in ("coverage", "condition", "readiness")],
            "condition_distribution": distribution,
            "condition_note": f"of {_fmt_bytes(cb['total'])} held · byte-weighted; a row can carry more than one condition, so clean is the remainder",
            "previous_record_id": previous["job_id"] if previous else None}


def census_record(job, report=None, previous=None):
    """Project an estate intelligence job as a census record for the Registry's census history."""
    status = {"completed": "COMPLETE", "partial": "PARTIAL", "running": "PENDING", "submitting": "PENDING", "failed": "REFUSED",
              "refused": "REFUSED", "cancelled": "CANCELLED"}.get(job.get("status"), "REFUSED")
    record = {"record_id": job["job_id"], "census_number": job.get("census_number"), "tenant_id": "RMS", "kind": "estate_intelligence",
              "status": status, "scope": "Estate intelligence census: duplication, quality, degradation, freshness, PII density, storage economics (aggregates only)",
              "execution_verified": bool((job.get("receipt") or {}).get("digest_verified")), "created_at": job.get("submitted_at"),
              "started_at": job.get("started_at"), "finished_at": job.get("finished_at"), "initiated_by": job.get("principal_id"),
              "worker_id": job.get("host"), "workers": [{"runtime_id": job.get("host"), "gpu_compute_hours": 0, "execution": "CPU census on the census worker; rows measured on the jump host"}],
              "proof_ref": f"census_autonomy_state/estate_intelligence/{job['job_id']}.json", "proof_sha256": (job.get("receipt") or {}).get("receipt_sha256"),
              "reason_code": job.get("reason"), "duration_seconds": _duration(job), "source_ids": ["rms_mysql"],
              "limitations": ["Ratios are measured on complete passes (tables ≤100k rows) or stratified keyset samples and weighted by estimated rows.",
                              "Content-quality and PII measures describe their assessed rows; rights, languages and semantic similarity were not measured.",
                              "No row, cell or identifier value was retained or returned; the brief carries aggregates, sketches and hashes only."],
              "progress": (job.get("remote_state") or {}).get("progress") if status == "PENDING" else None}
    if report:
        h = report["headline"]
        record.update(source_details=report["connections"], database_count=h["databases"], table_count=h["tables"], row_count_estimate=h["rows_estimate"],
                      row_count_measured=h["rows_measured"], volume_bytes=h["bytes_total"], brief_path=report.get("brief_path"),
                      coverage={"declared": len(report["connections"]), "completed": sum(1 for c in report["connections"] if c["status"] == "complete"),
                                "partial": sum(1 for c in report["connections"] if c["status"] == "partial"), "blocked": sum(1 for c in report["connections"] if c["status"] == "blocked")},
                      report=_metrics(report, previous), reading=report["reading"], data_products=[{k: c[k] for k in ("key", "title", "readiness_grade", "tables", "rows_estimate")} for c in report["data_products"]])
    else:
        declared = [c["label"] for c in job.get("connections") or []]
        record.update(source_details=[], coverage={"declared": len(declared), "completed": 0, "partial": 0, "blocked": 0}, database_count=None, table_count=None,
                      row_count_estimate=None, report={"metrics": {}, "groups": [], "condition_distribution": None,
                                                        "condition_note": "Condition is classified only from a digest-verified receipt."})
    return record


def census_records():
    """Every estate intelligence job as a census record, newest first; census numbers EI1… in submission order."""
    jobs = sorted(dispatch.list_jobs(), key=lambda j: j.get("submitted_at", ""))
    out, previous = [], None
    for index, job in enumerate(jobs, 1):
        job["census_number"] = f"EI{index}"
        report = report_for(job["job_id"], cached_only=True) if job.get("status") in TERMINAL_WITH_RESULT else None
        record = census_record(job, report, previous)
        if report:
            previous = {**report, "census_record": record}
        out.append(record)
    return sorted(out, key=lambda r: r.get("finished_at") or r.get("created_at") or "", reverse=True)
