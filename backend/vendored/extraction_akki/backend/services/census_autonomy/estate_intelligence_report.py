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

from services.census_autonomy.language_register import LANGUAGES_KEPT
from services.census_autonomy import estate_intelligence_dispatch as dispatch
from services.census_autonomy.estate_intelligence_worker import TIMESTAMP_TYPES, NUMERIC_TYPES, rollup

TERMINAL_WITH_RESULT = ("completed", "partial")
REPORT_VERSION = 4  # bump when build() gains sections so cached reports are rebuilt from the banked detail
ARCHIVE_CLASSES = ("GLACIER", "COLD", "DEEP_ARCHIVE", "ARCHIVE")  # S3-API names Huawei OBS returns for its Archive / Cold tiers
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


def tariff():
    """Storage tariff [SLOT] from the environment; savings are priced at READ time so a tariff change never needs a re-census."""
    def num(key):
        value = os.environ.get(key)
        return float(value) if value else None
    return {"database_per_gb_month": num("ESTATE_STORAGE_COST_PER_GB_MONTH"), "object_per_gb_month": num("ESTATE_OBJECT_STORAGE_COST_PER_GB_MONTH"),
            "archive_per_gb_month": num("ESTATE_ARCHIVE_STORAGE_COST_PER_GB_MONTH"),
            "currency": os.environ.get("ESTATE_STORAGE_COST_CURRENCY") or "USD", "source": os.environ.get("ESTATE_STORAGE_COST_SOURCE") or None}


def price_strategies(report):
    """Attach monthly savings to each strategy (database tables at the database tariff, object stores at the object tariff;
    archive tiering is the Standard→Archive delta when an archive tariff is set, else an upper bound at the full tariff)."""
    t = tariff()
    items = report["cost_strategies"]["items"]
    for item in items:
        rate = t["object_per_gb_month"] if item.get("store") == "object" else t["database_per_gb_month"]
        item["saving_basis"] = None
        if item["key"] == "obs_cold_buckets" and rate:
            if t["archive_per_gb_month"] is not None:
                rate = max(0.0, rate - t["archive_per_gb_month"]); item["saving_basis"] = "Standard minus archive-class tariff; retrieval fees not included"
            else:
                item["saving_basis"] = "upper bound at the full Standard tariff (set ESTATE_ARCHIVE_STORAGE_COST_PER_GB_MONTH for the tiering delta)"
        item["monthly_saving"] = round(rate * item["bytes"] / 1024 ** 3, 2) if rate and item["bytes"] else None
        item["currency"] = t["currency"] if item["monthly_saving"] is not None else None
    priced = [i["monthly_saving"] for i in items if i["monthly_saving"] is not None]
    parts = []
    if t["database_per_gb_month"]:
        parts.append(f"database storage at {t['currency']} {t['database_per_gb_month']}/GB-month")
    if t["object_per_gb_month"]:
        parts.append(f"object storage at {t['currency']} {t['object_per_gb_month']}/GB-month")
    report["cost_strategies"].update(
        tariff=t, monthly_saving_total=round(sum(priced), 2) if priced else None, currency=t["currency"],
        currency_note=("Priced with " + " and ".join(parts) + (f" ({t['source']})" if t["source"] else "") + "; overlaps between strategies are possible, so the total is an upper bound.")
        if parts else "No storage tariff on record: savings are stated in bytes. Set ESTATE_STORAGE_COST_PER_GB_MONTH (databases) and ESTATE_OBJECT_STORAGE_COST_PER_GB_MONTH (object stores) to price them.")
    return report


def _latest_store_outcome(source_id, tenant_id):
    """Retained deep-census outcomes for an object/file source, merged per source label (newest observation of each
    bucket/share wins, so a re-check of blocked buckets does not hide the full inventory). Cached results only; never a remote read."""
    from services.census_autonomy import engine
    docs = []
    for path in (engine.CENSUS_STATE_DIR / engine.RESULTS_SUBDIR).glob("*_result.json"):
        try:
            doc = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if doc.get("tenant_id") != tenant_id:
            continue
        for outcome in (doc.get("payload") or {}).get("outcomes") or []:
            if outcome.get("source_id") == source_id and outcome.get("sources"):
                docs.append((doc.get("completed_at_utc", ""), path.name, outcome))
    if not docs:
        return None
    docs.sort(key=lambda d: d[0])
    merged, runs = {}, []
    inventory_keys = ("object_count", "file_count", "volume_bytes", "formats", "date_min", "date_max", "duplicate_candidates", "pages", "directories_complete", "directories_pending", "enumeration", "storage_classes")
    for _, name, outcome in docs:
        runs.append(outcome.get("census_run_id"))
        for s in outcome["sources"]:
            previous = merged.get(s.get("label"))
            # A content pass still listing a store must not shrink the retained full enumeration; it brings its content reading only.
            if previous and previous.get("enumeration") == "full" and s.get("content") and s.get("enumeration") != "full":
                s = {**s, **{k: previous[k] for k in inventory_keys if k in previous}, "status": previous.get("status", s.get("status"))}
            merged[s.get("label")] = s
    latest = docs[-1][2]
    fullest = max(docs, key=lambda d: len(d[2]["sources"]))[2]
    return {**fullest, "sources": list(merged.values()), "observed_at": latest.get("observed_at"), "census_run_id": fullest.get("census_run_id"),
            "census_run_ids": runs, "result_receipt": docs[-1][1]}


def _store_rows(outcome, kind, cold_after_days=365):
    observed = outcome.get("observed_at") or now()
    observed_dt = datetime.fromisoformat(observed.replace("Z", "+00:00"))
    rows = []
    for s in outcome["sources"]:
        units = s.get("object_count") if kind == "object" else s.get("file_count")
        units = units or 0
        mean = (s.get("volume_bytes") or 0) / units if units else 0
        candidates = s.get("duplicate_candidates")
        last = s.get("date_max")
        if isinstance(last, (int, float)):
            last_dt = datetime.fromtimestamp(last, tz=timezone.utc)
        elif isinstance(last, str):
            last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
        else:
            last_dt = None
        idle_days = (observed_dt - last_dt).days if last_dt else None
        formats = sorted((s.get("formats") or {}).items(), key=lambda kv: -kv[1])[:4]
        rows.append({"label": s.get("label"), "status": s.get("status"), "enumeration": s.get("enumeration"), "units": units, "bytes": s.get("volume_bytes") or 0,
                     "duplicate_candidates": candidates, "duplicate_bytes_estimate": int(candidates * mean) if candidates else 0,
                     "last_write": last_dt.isoformat().replace("+00:00", "Z") if last_dt else None, "idle_days": idle_days,
                     "cold": bool(idle_days is not None and idle_days > cold_after_days and (s.get("volume_bytes") or 0) > 0),
                     "reason_code": s.get("reason_code"), "top_formats": [f"{ext} {n:,}" for ext, n in formats], "pending": s.get("directories_pending"),
                     "storage_classes": s.get("storage_classes"), "archive_bytes": sum(v.get("bytes") or 0 for k, v in (s.get("storage_classes") or {}).items() if k in ARCHIVE_CLASSES),
                     "content_measurement": s.get("content_measurement"), "content": s.get("content")})
    rows.sort(key=lambda r: -r["bytes"])
    return rows


def _merge_classes(rows):
    out = {}
    for r in rows:
        for name, v in (r.get("storage_classes") or {}).items():
            slot = out.setdefault(name, {"objects": 0, "bytes": 0})
            slot["objects"] += v.get("objects") or 0; slot["bytes"] += v.get("bytes") or 0
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["bytes"]))


def store_estate(tenant_id="RMS"):
    """Object (OBS) and file (NAS) estate from the retained enumeration receipts: inventory, ETag+size duplicate candidates, cold sources.
    Duplicate BYTES are candidates × the source's mean object size — an estimate disclosed as such; no object body was read."""
    stores, outcomes = {}, {}
    for key, source_id, kind, unit_name in (("obs", "rms_obs", "object", "objects"), ("nas", "rms_nas", "file", "files")):
        outcome = _latest_store_outcome(source_id, tenant_id)
        if not outcome:
            stores[key] = {"measured": False, "kind": kind, "unit_name": unit_name, "note": "No retained enumeration receipt for this store."}
            continue
        outcomes[key] = outcome
        rows = _store_rows(outcome, kind)
        complete = [r for r in rows if r["status"] == "complete"]
        blocked = [r for r in rows if r["status"] != "complete"]
        total = sum(r["bytes"] for r in rows)
        dup_bytes = sum(r["duplicate_bytes_estimate"] for r in rows)
        cold = [r for r in rows if r["cold"]]
        fingerprinted = any(r["duplicate_candidates"] is not None for r in rows)
        classed = [r for r in rows if r.get("storage_classes")]
        archive_bytes = sum(r["archive_bytes"] for r in rows)
        stores[key] = {"measured": True, "kind": kind, "unit_name": unit_name, "census_run_id": outcome.get("census_run_id"), "observed_at": outcome.get("observed_at"),
                       "status": outcome.get("status"), "reason_code": outcome.get("reason_code"), "result_receipt": outcome.get("result_receipt"), "census_run_ids": outcome.get("census_run_ids"),
                       "sources": len(rows), "sources_complete": len(complete), "sources_blocked": len(blocked), "units": sum(r["units"] for r in rows),
                       "bytes": total, "bytes_label": _fmt_bytes(total), "frontier_complete": all((r["pending"] or 0) == 0 for r in complete) and all(r["enumeration"] == "full" for r in complete),
                       "duplicate_candidates": sum(r["duplicate_candidates"] or 0 for r in rows) if fingerprinted else None,
                       "duplicate_bytes_estimate": dup_bytes if fingerprinted else None, "duplicate_pct_of_units": _pct(sum(r["duplicate_candidates"] or 0 for r in rows) / sum(r["units"] for r in rows)) if fingerprinted and sum(r["units"] for r in rows) else None,
                       "cold_sources": len(cold), "cold_bytes": sum(r["bytes"] for r in cold), "cold_bytes_label": _fmt_bytes(sum(r["bytes"] for r in cold)),
                       "cold_bytes_already_archive": sum(r["archive_bytes"] for r in cold), "cold_bytes_standard": sum(r["bytes"] - r["archive_bytes"] for r in cold if r.get("storage_classes")),
                       "storage_classes": {"measured_sources": len(classed), "archive_bytes": archive_bytes, "archive_bytes_label": _fmt_bytes(archive_bytes),
                                           "archive_pct_of_bytes": _pct(archive_bytes / sum(r["bytes"] for r in classed)) if classed and sum(r["bytes"] for r in classed) else None,
                                           "by_class": _merge_classes(classed)} if classed else None,
                       "blocked": [{"label": r["label"], "reason_code": r["reason_code"]} for r in blocked][:40],
                       "top_sources": rows[:12], "method": (outcome["sources"][0].get("method") if outcome["sources"] else None),
                       "content": content_rollup(rows, source_id, tenant_id),
                       "duplication_note": ("Duplicate candidates are objects whose ETag+size fingerprint was already seen in the same store; duplicate bytes = candidates × mean object size of the bucket (estimate). Not proven byte duplicates."
                                            if fingerprinted else "This enumeration recorded no content fingerprints (stat/listing only), so duplication is unmeasured; sizes and dates were read, bodies were not.")}
    total = content_estate_total(stores)
    if total:
        stores["content_total"] = total
        from services.census_autonomy import estate_forecast
        try:
            forecast = estate_forecast.forecast(outcomes)
        except (ValueError, KeyError, TypeError, ZeroDivisionError):  # a malformed receipt never hides the measured roll-up; the pack discloses the missing forecast
            forecast = None
        if forecast:
            stores["content_forecast"] = forecast
            from services.census_autonomy import language_register, text_estate_evidence
            try:
                aggregates = (text_estate_evidence.latest(tenant_id) or {}).get("summary")
                profiles = (text_estate_evidence.latest(tenant_id, "profiles") or {}).get("summary")
                register = language_register.build(forecast, aggregates, profiles)
            except (ValueError, KeyError, TypeError, ZeroDivisionError):
                register = None
            if register:
                stores["language_register"] = register
    return stores


def content_rollup(rows, source_id, tenant_id):
    """Tiered content census roll-up for one store (owner ruling 2026-10-02): tier-1 facts (listed, header-measured hours with their
    extrapolation error, read, verified, denied, archived), the sample's progress, tier-2 interval estimates (speech, music, silence and
    speech hours by language; strata combined in quadrature), the folder table across stores, egress so far and the live cadence."""
    from services.census_autonomy import operational_store as store
    from services.census_autonomy.deep_sample import combine
    measured = [r for r in rows if r.get("content")]
    cadence = [run for run in store.runs(tenant_id) if run.get("measurement") in ("content_full", "content_sample") and source_id in (run.get("source_ids") or [])
               and (run.get("status") == "PENDING" or run.get("continuation_run_id"))]
    live = [{"census_run_id": run["census_run_id"], "worker_id": run.get("worker_id"), "status": run["status"], "stage": run.get("stage"), "reason_code": run.get("reason_code"),
             "measurement": run.get("measurement"), "scope_sources": len(run.get("source_refs") or []), "not_before": run.get("not_before"), "started_at": run.get("started_at"), "updated_at": run.get("updated_at")}
            for run in cadence if run.get("status") == "PENDING"]
    if not measured and not live:
        return {"measured": False, "note": "No content pass has been commissioned for this store."}
    contents = [r["content"] for r in measured]
    total = lambda key: sum((c.get(key) or 0) for c in contents)  # noqa: E731
    # Hours are stated only where at least one header was read; a store or folder with no probe has unknown hours, not a guess.
    for c in contents:
        if not (c.get("headers") or {}).get("probed_files"):
            c["headers"] = {**(c.get("headers") or {}), "hours_est": None, "hours_se": None, "hours_lo": None, "hours_hi": None}
        for f in c.get("folders") or []:
            if not (f.get("hours") or {}).get("probed_files"):
                f["hours"] = {**(f.get("hours") or {}), "est": None, "se": None}
    headers = [c.get("headers") or {} for c in contents]
    hours_est = sum(h.get("hours_est") or 0 for h in headers)
    hours_se = math.sqrt(sum((h.get("hours_se") or 0) ** 2 for h in headers))
    basis = {}
    for h in headers:
        for k, v in (h.get("basis") or {}).items():
            basis[k] = basis.get(k, 0) + v
    estimates = {k: combine([(c.get("estimates") or {}).get(k) for c in contents]) for k in ("speech", "music", "silence", "decoded")}
    languages = {}
    for c in contents:
        for code, e in ((c.get("estimates") or {}).get("languages") or {}).items():
            languages.setdefault(code, []).append(e)
    languages = dict(sorted(((code, combine(parts)) for code, parts in languages.items()), key=lambda kv: -(kv[1]["est"] or 0))[:LANGUAGES_KEPT])
    folders = [f for c in contents for f in (c.get("folders") or [])]
    folders.sort(key=lambda f: -((f["estimates"]["speech"].get("est") or 0) if f["sample"].get("read") else (f["hours"].get("est") or 0)))
    samples = [c.get("sample") or {} for c in contents]
    latest = [c.get("this_run") or {} for c in contents]
    run_seconds = max((t.get("run_seconds") or 0) for t in latest) if latest else 0
    files_this_run = sum(t.get("objects_read") or 0 for t in latest)
    pending_files = total("objects_pending")
    egress = [c.get("egress") or {} for c in contents]
    windows = [c.get("read_window") for c in contents if c.get("read_window")]
    source_rows = sorted([{"label": r["label"], "access": r["content"].get("access"), "measurement": r["content"].get("measurement"), "inventory_complete": r["content"].get("inventory_complete"),
                           "media_objects": r["content"].get("media_objects"), "media_bytes": r["content"].get("media_bytes"), "audio_objects": r["content"].get("media_audio_objects"), "video_objects": r["content"].get("media_video_objects"),
                           "hours": {"est": (r["content"].get("headers") or {}).get("hours_est"), "lo": (r["content"].get("headers") or {}).get("hours_lo"), "hi": (r["content"].get("headers") or {}).get("hours_hi"),
                                     "probed_files": (r["content"].get("headers") or {}).get("probed_files")},
                           "speech": (r["content"].get("estimates") or {}).get("speech"), "music": (r["content"].get("estimates") or {}).get("music"),
                           "languages": dict(list(((r["content"].get("estimates") or {}).get("languages") or {}).items())[:4]),
                           "sample": {k: (r["content"].get("sample") or {}).get(k) for k in ("planned_files", "read_files", "strata", "census_strata", "sampled_strata", "complete")},
                           "objects_read": r["content"].get("objects_read"), "bytes_read": r["content"].get("bytes_read"), "objects_failed": r["content"].get("objects_failed"), "failures": r["content"].get("failures"),
                           "objects_denied": r["content"].get("objects_denied"), "bytes_denied": r["content"].get("bytes_denied"), "objects_archived": r["content"].get("objects_archived"), "bytes_archived": r["content"].get("bytes_archived"),
                           "egress_usd": (r["content"].get("egress") or {}).get("usd_estimate"), "strata_mode": r["content"].get("strata_mode"),
                           "storage_classes": r.get("storage_classes"), "archive_bytes": r.get("archive_bytes"), "bucket_bytes": r.get("bytes"), "access_since": r["content"].get("access_since")} for r in measured],
                         key=lambda s: -(s["media_bytes"] or 0))
    blocked = [s for s in source_rows if s["access"] in ("denied", "archived")]
    media_all = sum(s["media_objects"] or 0 for s in source_rows) or 1
    access_blocked = {
        "sources": [{"label": s["label"], "access": s["access"], "media_objects": s["media_objects"], "media_bytes": s["media_bytes"], "audio_objects": s["audio_objects"], "video_objects": s["video_objects"],
                     "archive_bytes": s["archive_bytes"], "since": s["access_since"]} for s in blocked],
        "denied_sources": sum(1 for s in blocked if s["access"] == "denied"), "archived_sources": sum(1 for s in blocked if s["access"] == "archived"),
        "media_objects": sum(s["media_objects"] or 0 for s in blocked), "media_bytes": sum(s["media_bytes"] or 0 for s in blocked),
        "share_of_media_objects": round(sum(s["media_objects"] or 0 for s in blocked) / media_all, 4),
        "denied_grant": ("The census key can list these buckets but every HEAD and GET returns 403 AccessDenied (verified from the control plane with a one-byte ranged read; the same account owns the objects). "
                         "The Huawei account administrator must grant the census IAM user object read — obs:object:GetObject (HeadObject is covered by it) — on each bucket, by IAM policy or bucket policy. "
                         "Every run re-probes these buckets with six one-byte reads; the census resumes by itself once the grant lands." if any(s["access"] == "denied" for s in blocked) else None),
        "archived_note": ("Objects in Archive class without direct read answer InvalidObjectState; they can be read only after a restore (restore fee, then egress). Counted, not estimated, "
                          "until the owner orders a restore." if any(s["access"] == "archived" for s in blocked) else None),
    } if blocked else None
    archive_bytes_total = sum(s["archive_bytes"] or 0 for s in source_rows if s.get("storage_classes"))
    classed_bytes = sum(s["bucket_bytes"] or 0 for s in source_rows if s.get("storage_classes"))
    return {"measured": bool(measured), "sources": len(measured), "sources_readable": sum(1 for s in source_rows if s["access"] == "readable"), "sources_denied": sum(1 for s in source_rows if s["access"] == "denied"),
            "sources_archived": sum(1 for s in source_rows if s["access"] == "archived"), "sources_complete": sum(1 for s in source_rows if s["measurement"] in ("estimated", "census", "denied", "archived", "no_media")),
            "sources_listing": sum(1 for s in source_rows if not s["inventory_complete"]),
            "media_objects": total("media_objects"), "media_bytes": total("media_bytes"), "audio_objects": total("media_audio_objects"), "video_objects": total("media_video_objects"),
            "objects_read": total("objects_read"), "bytes_read": total("bytes_read"), "bytes_verified": total("bytes_verified"),
            "objects_denied": total("objects_denied"), "bytes_denied": total("bytes_denied"), "objects_archived": total("objects_archived"), "bytes_archived": total("bytes_archived"),
            "objects_pending": pending_files, "objects_failed": total("objects_failed"), "hours_decoded": round(total("hours_decoded"), 2),
            "headers": {"probed_files": sum(h.get("probed_files") or 0 for h in headers), "probed_hours": round(sum(h.get("probed_hours") or 0 for h in headers), 1), "basis": basis,
                        "hours_est": round(hours_est, 1), "hours_se": round(hours_se, 1), "hours_lo": round(max(0.0, hours_est - 1.96 * hours_se), 1), "hours_hi": round(hours_est + 1.96 * hours_se, 1),
                        "complete": all(h.get("complete") for h in headers) if headers else False},
            "sample": {"planned_files": sum(s.get("planned_files") or 0 for s in samples), "read_files": sum(s.get("read_files") or 0 for s in samples), "strata": sum(s.get("strata") or 0 for s in samples),
                       "census_strata": sum(s.get("census_strata") or 0 for s in samples), "sampled_strata": sum(s.get("sampled_strata") or 0 for s in samples),
                       "hours_decoded": round(sum(s.get("hours_decoded") or 0 for s in samples), 1), "complete": all(s.get("complete") for s in samples) if samples else False,
                       "plan": next((c.get("plan") for c in contents if c.get("plan")), None)},
            "estimates": {**estimates, "languages": languages},
            "folders": folders[:60], "folders_total": len(folders),
            "egress": {"bytes": sum(e.get("bytes") or 0 for e in egress), "usd_estimate": round(sum(e.get("usd_estimate") or 0 for e in egress), 2) if any(e.get("usd_estimate") is not None for e in egress) else None,
                       "usd_per_gb_assumed": next((e.get("usd_per_gb_assumed") for e in egress if e.get("usd_per_gb_assumed")), None), "billed_to": next((e.get("billed_to") for e in egress if e.get("billed_to")), None)},
            "read_window": windows[0] if windows else None,
            "throughput_files_per_hour": round(files_this_run / run_seconds * 3600) if run_seconds else None,
            "eta_hours": round(pending_files / (files_this_run / run_seconds) / 3600, 1) if run_seconds and files_this_run and pending_files else None,
            "live_runs": live, "source_rows": source_rows,
            "access_blocked": access_blocked,
            "readable": {"sources": sum(1 for s in source_rows if s["access"] == "readable"), "media_objects": sum(s["media_objects"] or 0 for s in source_rows if s["access"] == "readable"),
                         "media_bytes": sum(s["media_bytes"] or 0 for s in source_rows if s["access"] == "readable")},
            "storage_classes": {"archive_bytes": archive_bytes_total, "bucket_bytes": classed_bytes, "archive_pct_of_bytes": _pct(archive_bytes_total / classed_bytes) if classed_bytes else None,
                                "sources_measured": sum(1 for s in source_rows if s.get("storage_classes"))} if classed_bytes else None,
            "evidence_class": {"bytes": "fact (listed sizes; sampled objects read in full and checked against the listing by sha256/size/ETag)",
                               "hours_held": "measured on the file header for every audio file and a per-folder sample of video files; the rest extrapolated by the folder's seconds-per-byte with a standard error",
                               "estimates": "detected (admitted music detector and current audio language model on every two-second window of a deterministic stratified sample; ratio estimators with finite-population correction; 95 % intervals); not human labels"}}


def content_estate_total(stores):
    """OBS + NAS combined interval estimates for the headline (independent stores add in quadrature)."""
    from services.census_autonomy.deep_sample import combine
    parts = [s.get("content") for s in stores.values() if isinstance(s, dict) and (s.get("content") or {}).get("measured")]
    if not parts:
        return None
    languages = {}
    for c in parts:
        for code, e in (c["estimates"].get("languages") or {}).items():
            languages.setdefault(code, []).append(e)
    hours_est = sum((c["headers"].get("hours_est") or 0) for c in parts)
    hours_se = math.sqrt(sum((c["headers"].get("hours_se") or 0) ** 2 for c in parts))
    return {"hours_held": {"est": round(hours_est, 1), "lo": round(max(0.0, hours_est - 1.96 * hours_se), 1), "hi": round(hours_est + 1.96 * hours_se, 1)},
            "speech": combine([c["estimates"]["speech"] for c in parts]), "music": combine([c["estimates"]["music"] for c in parts]),
            "languages": dict(sorted(((code, combine(v)) for code, v in languages.items()), key=lambda kv: -(kv[1]["est"] or 0))[:LANGUAGES_KEPT]),
            "media_objects": sum(c.get("media_objects") or 0 for c in parts), "media_bytes": sum(c.get("media_bytes") or 0 for c in parts),
            "sample_read_files": sum((c.get("sample") or {}).get("read_files") or 0 for c in parts), "sample_planned_files": sum((c.get("sample") or {}).get("planned_files") or 0 for c in parts),
            "egress_usd": round(sum((c.get("egress") or {}).get("usd_estimate") or 0 for c in parts), 2)}


def store_strategies(stores):
    obs = stores.get("obs") or {}
    if not obs.get("measured"):
        return []
    dup_rows = sorted([r for r in obs["top_sources"] if r["duplicate_bytes_estimate"]], key=lambda r: -r["duplicate_bytes_estimate"])
    cold_rows = sorted([r for r in obs["top_sources"] if r["cold"]], key=lambda r: -r["bytes"])
    classed = obs.get("storage_classes") is not None
    # Bytes already in Archive class have no Standard → Archive saving left; only cold bytes still in Standard class are addressable.
    cold_addressable = (obs.get("cold_bytes_standard") or 0) if classed else (obs["cold_bytes"] or 0)
    return [
        {"key": "obs_duplicate_objects", "store": "object", "title": "Reconcile duplicate objects across OBS buckets", "bytes": obs["duplicate_bytes_estimate"] or 0,
         "action": "Confirm ETag+size candidates by object hash, keep one copy per bucket and replace the rest with references or lifecycle-delete them.",
         "evidence": [f"{r['label']} · {r['duplicate_candidates']:,} candidates · ≈{_fmt_bytes(r['duplicate_bytes_estimate'])}" for r in dup_rows[:6]],
         "risk": "Candidates share ETag and size, which for multipart uploads is not a content hash; bytes are candidates × mean object size, an estimate. Confirm before deleting."},
        {"key": "obs_cold_buckets", "store": "object", "title": "Move buckets not written for over a year to archive-class storage", "bytes": cold_addressable,
         "action": "Apply a lifecycle rule (Standard → Archive/Cold) on buckets whose last object write is older than a year; keep listing metadata hot.",
         "evidence": [f"{r['label']} · last write {r['idle_days']:,} days before the census · {_fmt_bytes(r['bytes'])}" + (f" · already Archive class {_fmt_bytes(r['archive_bytes'])}" if r.get("storage_classes") else "") for r in cold_rows[:6]],
         "already_archive_bytes": obs.get("cold_bytes_already_archive") if classed else None,
         "risk": ("The listing now records each object's storage class: " + _fmt_bytes(obs.get("cold_bytes_already_archive") or 0) + " of the cold bytes are already in Archive class and carry no further tiering saving; "
                  "only the Standard-class remainder is counted here. Read frequency was not measured, and archive-class retrieval carries its own fee.") if classed else
                 "Last write is the newest object timestamp in the listing; read frequency was not measured, and archive-class retrieval carries its own fee."},
    ]


def cost_strategies(summary, tables, total_bytes, stores=None):
    def money(bytes_):
        return None  # priced at read time by price_strategies()

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
    items += store_strategies(stores or {})
    for item in items:
        item.setdefault("store", "database")
        item["share_of_estate"] = round(item["bytes"] / total_bytes, 4) if total_bytes and item["store"] == "database" else None
        item["monthly_saving"] = money(item["bytes"])
        item["bytes_label"] = _fmt_bytes(item["bytes"]) if item["bytes"] else "not a storage saving"
    items.sort(key=lambda i: -i["bytes"])
    return {"currency_note": "unpriced until read", "same_schema_groups": groups, "items": items}


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
    stores = store_estate(job.get("tenant_id") or "RMS")
    strategies = cost_strategies(summary, tables, total_bytes, stores)
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
            "stores": stores,
            "degradation": degradation(tables, previous, headline),
            "within_table_duplicates": [{"connection": t["connection"], "database": t["database"], "table": t["table"], "exact_duplicate_ratio": t["exact_duplicate_ratio"],
                                         "normalised_duplicate_ratio": t.get("normalised_duplicate_ratio"), "rows_estimate": t.get("rows_estimate"), "data_bytes": t.get("data_bytes"),
                                         "method": t.get("method")} for t in within[:25]],
            "condition_bytes": condition_bytes(tables),
            "connections": _connection_detail(job, detail, tables),
            "schema_fingerprints": {f"{t['connection']}/{t['database']}.{t['table']}": t.get("schema_fingerprint") for t in tables if t.get("schema_fingerprint")},
            "errors": errors, "coverage_note": "RMS MySQL measured in depth (owner order 1-a). OBS object and NAS file estates are read from their retained enumeration receipts "
            "(listing and stat only: sizes, dates, ETag+size duplicate candidates; no object or file body); "
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
            "cost_strategies": [{k: s.get(k) for k in ("key", "title", "bytes", "bytes_label", "share_of_estate", "action", "monthly_saving", "currency", "store")} for s in report["cost_strategies"]["items"]],
            "currency_note": report["cost_strategies"]["currency_note"], "monthly_saving_total": report["cost_strategies"].get("monthly_saving_total"),
            "stores": {k: {kk: v.get(kk) for kk in ("measured", "kind", "unit_name", "sources", "sources_complete", "units", "bytes", "bytes_label", "duplicate_candidates", "duplicate_bytes_estimate", "cold_bytes", "census_run_id")}
                       for k, v in (report.get("stores") or {}).items()},
            "databases": [{k: p[k] for k in ("connection", "database", "tables", "rows_estimate", "bytes", "readiness", "dimensions", "failed_tables")} for p in report["databases"]],
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
              "| Strategy | Reclaimable | Share | Saving / month | Action |", "|---|---|---|---|---|"]
    for s in report["cost_strategies"]["items"]:
        share = f"{_pct(s['share_of_estate'])}%" if s["share_of_estate"] is not None and s["bytes"] else "—"
        saving = f"{s.get('currency')} {s['monthly_saving']:,.2f}" if s.get("monthly_saving") is not None else "unpriced"
        lines.append(f"| {s['title']} | {s['bytes_label']} | {share} | {saving} | {s['action']} |")
    if report["cost_strategies"].get("monthly_saving_total") is not None:
        lines += ["", f"Priced strategies total ≈ {report['cost_strategies']['currency']} {report['cost_strategies']['monthly_saving_total']:,.2f} per month (upper bound; overlaps possible)."]
    lines += ["", "### Evidence per strategy", ""]
    for s in report["cost_strategies"]["items"]:
        if s["evidence"]:
            lines += [f"**{s['title']}** — risk: {s['risk']}", ""] + [f"- {e}" for e in s["evidence"]] + [""]
    lines += ["## Object and file estate (OBS buckets, NAS shares)", ""]
    for key, label in (("obs", "OBS object store"), ("nas", "NAS file shares")):
        st = (report.get("stores") or {}).get(key) or {}
        if not st.get("measured"):
            lines += [f"**{label}:** {st.get('note', 'not measured')}", ""]
            continue
        dup = (f"{st['duplicate_candidates']:,} duplicate candidates ({st['duplicate_pct_of_units']}% of {st['unit_name']}), ≈{_fmt_bytes(st['duplicate_bytes_estimate'])} estimated"
               if st.get("duplicate_candidates") is not None else "duplication unmeasured (no fingerprints in this pass)")
        lines += [f"**{label}** — census `{st['census_run_id']}` ({st['status']}, {st['observed_at']}): {st['sources_complete']} of {st['sources']} sources complete, "
                  f"{st['units']:,} {st['unit_name']}, {st['bytes_label']}; {dup}; {st['cold_sources']} sources not written for over a year ({st['cold_bytes_label']}). "
                  f"Frontier complete: {'yes' if st['frontier_complete'] else 'no'}.", "", st["duplication_note"], "",
                  "| Source | Status | Units | Bytes | Duplicate candidates | Last write | Formats |", "|---|---|---|---|---|---|---|"]
        for r in st["top_sources"]:
            lines.append(f"| {r['label']} | {r['status']}{(' · ' + r['reason_code']) if r['reason_code'] else ''} | {r['units']:,} | {_fmt_bytes(r['bytes'])} | "
                         f"{r['duplicate_candidates'] if r['duplicate_candidates'] is not None else '—'} | {r['last_write'] or '—'} | {', '.join(r['top_formats'])} |")
        if st["blocked"]:
            lines += ["", f"Blocked sources ({len(st['blocked'])}): " + "; ".join(f"{b['label']} ({b['reason_code']})" for b in st["blocked"][:12]) + (" …" if len(st["blocked"]) > 12 else "")]
        lines.append("")
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
            # The object/file store state is a live read of retained receipts (the full-content census grows run by run); the rest is banked.
            try:
                cached["stores"] = store_estate(job.get("tenant_id") or "RMS")
            except (OSError, ValueError, KeyError):
                pass
            return price_strategies(cached)
    if cached_only and not detail_cached(job_id):
        return None
    detail = detail_for(job)
    if not detail:
        return None
    report = build(job, detail, _previous_report(job))
    dossier_path = dispatch._jobs_dir() / f"{job_id}.dossier.json"
    if dossier_path.exists():
        report["dossier"] = json.loads(dossier_path.read_text())
    price_strategies(report)
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


async def compose_dossier(job_id, actor, tenant_id, model=None, provider=None):
    """One governed crossing: compact aggregates in, Markdown dossier out; banked and folded into the report. The frontier writer model is
    configured once (REPORT_AUTHOR_MODEL); callers do not pick a weaker model."""
    from services.chokepoint import llm as chokepoint
    model = os.environ['REPORT_AUTHOR_MODEL']; provider = os.environ['REPORT_AUTHOR_CONNECTION']
    report = report_for(job_id)
    if not report:
        return None
    prompt = json.dumps({k: report[k] for k in ("reading", "headline", "databases", "coverage_note")} |
                        {"data_products": [{k: c[k] for k in ("title", "use", "tables", "rows_estimate", "readiness_grade", "databases", "blockers", "licensable_units")} for c in report["data_products"]],
                         "cost_strategies": [{k: s.get(k) for k in ("title", "bytes_label", "share_of_estate", "action", "risk", "monthly_saving", "currency")} for s in report["cost_strategies"]["items"]],
                         "tariff_note": report["cost_strategies"]["currency_note"],
                         "object_and_file_estate": {k: {kk: v.get(kk) for kk in ("kind", "sources", "sources_complete", "sources_blocked", "units", "bytes_label", "duplicate_candidates", "duplicate_pct_of_units", "duplicate_bytes_estimate", "cold_sources", "cold_bytes_label", "frontier_complete", "duplication_note")}
                                                    for k, v in (report.get("stores") or {}).items() if v.get("measured")},
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
