"""services.registry_facts.facts — assemble Registry facts from disk.

Owner Order 2026-08-19 · FL-P2-25. Read-only. No invention: every figure
traces to a record on disk. No secrets: never reads the custody dir.

Design rules encoded here (Screen Mockups v7 §6 Content Rules):
  1. Sentences first, measures second — facts carry a plain-sentence
     `headliner` per section for the frontend to render.
  2. No figure without provenance — approximate row counts are flagged
     `is_approximate=True`; every source carries `last_verified`.
  3. Gaps are drawn — empty tabs return [] plus a `reason` sentence.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Record directories — env overridable, defaults to the assessment workspace.
# ---------------------------------------------------------------------------

_DEFAULT_DCR = "/app/assessment_workspace/phase0/data_connection_records"
_DEFAULT_CR = "/app/assessment_workspace/phase0/commissioning_records"


def _data_connection_records_dir() -> Path:
    return Path(os.environ.get("DATA_CONNECTION_RECORD_DIR", _DEFAULT_DCR))


def _commissioning_records_dir() -> Path:
    return Path(os.environ.get("COMMISSIONING_RECORD_DIR", _DEFAULT_CR))


# ---------------------------------------------------------------------------
# data_sources
# ---------------------------------------------------------------------------

def _shape_data_source(record: Dict[str, Any]) -> Dict[str, Any]:
    """Project a data_connection_record onto the facts wire shape.

    Never carries the secret_arn subject-line, aws_* creds, or any other
    material outside the whitelisted fields.
    """
    resource = record.get("resource", {}) or {}
    top_25 = record.get("top_25_tables") or []
    top_tables: List[Dict[str, Any]] = []
    for t in top_25:
        approx = t.get("approx_rows")
        top_tables.append({
            "schema": t.get("schema", ""),
            "table": t.get("table", ""),
            "approx_rows": approx if isinstance(approx, int) else None,
            "size_mb": t.get("size_mb", ""),
            "is_approximate": True,
        })
    return {
        "source_id": record.get("source_id", ""),
        "database": resource.get("database", ""),
        "engine": record.get("engine", "unknown"),
        "engine_version": record.get("engine_version") or "",
        "region": resource.get("region", ""),
        "cluster_arn": resource.get("cluster_arn", ""),
        # NOTE secret_arn is a Secrets-Manager ARN, not a secret itself, but
        # we leave it out of the wire shape to keep the surface tidy —
        # the Registry surface does not need to render it.
        "channel": record.get("channel", ""),
        "link_working": bool(record.get("link_working")),
        "table_count": int(record.get("table_count") or 0),
        "top_tables": top_tables[:10],  # top-10 for the visual band
        "last_verified": record.get("at", ""),
        "posture": "STRUCTURE-ONLY",
    }


def load_data_sources() -> List[Dict[str, Any]]:
    """Return one entry per *_FINAL.json data_connection_record."""
    records_dir = _data_connection_records_dir()
    if not records_dir.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(records_dir.glob("data_source_*_FINAL.json")):
        try:
            record = json.loads(p.read_text())
        except Exception as exc:  # pragma: no cover
            log.warning("skipping unreadable record %s: %s", p, type(exc).__name__)
            continue
        out.append(_shape_data_source(record))
    return out


# ---------------------------------------------------------------------------
# compute
# ---------------------------------------------------------------------------

def _shape_compute(record: Dict[str, Any]) -> Dict[str, Any]:
    capacity = record.get("capacity", {}) or {}
    gpu = capacity.get("gpu", {}) or {}
    ram = capacity.get("ram_gb", {}) or {}
    cpu = capacity.get("cpu", {}) or {}
    link = record.get("link", {}) or {}
    hardening = record.get("hardening_section", {}) or {}
    storage = capacity.get("storage", []) or []

    primary_vol: Dict[str, Any] = {}
    for s in storage:
        if s.get("note") == "primary working volume":
            primary_vol = {
                "mount": s.get("mount", ""),
                "size_tb": s.get("size_tb"),
                "free_tb": s.get("free_tb"),
                "write_speed_MBps": s.get("write_speed_MBps"),
            }
            break
    if not primary_vol and storage:
        # fall through: pick the largest volume by size_tb, then size_gb
        def _size_score(s: Dict[str, Any]) -> float:
            return (s.get("size_tb") or 0.0) * 1000 + (s.get("size_gb") or 0.0)
        biggest = max(storage, key=_size_score)
        primary_vol = {
            "mount": biggest.get("mount", ""),
            "size_tb": biggest.get("size_tb"),
            "free_tb": biggest.get("free_tb"),
            "size_gb": biggest.get("size_gb"),
            "free_gb": biggest.get("free_gb"),
            "write_speed_MBps": biggest.get("write_speed_MBps"),
        }

    throughput = link.get("throughput_pod_vm_MBps", {}) or {}
    # symmetric mean of pod↔vm — the "4.7 MB/s" figure
    p_to_v = throughput.get("pod_to_vm_100MB")
    v_to_p = throughput.get("vm_to_pod_100MB")
    if isinstance(p_to_v, (int, float)) and isinstance(v_to_p, (int, float)):
        avg = round((p_to_v + v_to_p) / 2.0, 2)
    else:
        avg = None

    nvlink = gpu.get("nvlink", {}) or {}
    return {
        "host_name": record.get("host_name", ""),
        "state_class": record.get("state_class", ""),
        "accepted_at": record.get("at", ""),
        "deploy_date": record.get("deploy_date", ""),
        "os": (capacity.get("os", {}) or {}).get("pretty_name", ""),
        "cpu_model": cpu.get("model", ""),
        "cpu_threads": int(cpu.get("threads") or 0),
        "ram_gb_total": int(ram.get("total") or 0),
        "ram_gb_free": ram.get("free"),
        "gpus": {
            "count": int(gpu.get("count") or 0),
            "model": gpu.get("model", ""),
            "vram_gb_per_gpu": gpu.get("vram_gb_per_gpu"),
            "vram_gb_total": gpu.get("vram_gb_total"),
            "nvlink_active": bool(nvlink.get("active")),
            "nvlink_aggregate_gbps_per_gpu": nvlink.get("aggregate_bandwidth_gbps_per_gpu"),
        },
        "primary_volume": primary_vol,
        "link": {
            "verdict": link.get("verdict", ""),
            "throughput_MBps": avg,
            "symmetric": bool(throughput.get("symmetric")),
        },
        "hardened": hardening.get("status") == "attested",
        "hardening_result": hardening.get("external_probe_result", ""),
        "usability_paragraph": record.get("usability_paragraph", ""),
        "four_questions": {
            "link_working": link.get("verdict") == "works",
            "found": bool(gpu.get("count")),
            "ready": hardening.get("status") == "attested",
            "failure": None if hardening.get("status") == "attested" else "hardening_not_attested",
        },
    }


def load_compute() -> List[Dict[str, Any]]:
    """Return one entry per *_ACCEPTED.json commissioning_record."""
    records_dir = _commissioning_records_dir()
    if not records_dir.is_dir():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(records_dir.glob("commissioning_*_ACCEPTED.json")):
        try:
            record = json.loads(p.read_text())
        except Exception as exc:  # pragma: no cover
            log.warning("skipping unreadable record %s: %s", p, type(exc).__name__)
            continue
        out.append(_shape_compute(record))
    return out


# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# models — bought-in LLMs + trained models (both land here per Owner Order §5).
# ---------------------------------------------------------------------------

# Emergent Universal LLM catalogue at W5 open (per Owner Order 2026-08-25 §2
# binding effect §2; subset of the emergentintegrations playbook catalog
# admissible today). This is a governed value — updating requires a ruling.
_EMERGENT_UNIVERSAL_MODELS = [
    "gpt-5.4",
    "gpt-5.2",
    "gpt-5-mini",
    "claude-sonnet-4-6",
    "claude-haiku-4-5-20251001",
    "gemini-3.1-pro-preview",
    "gemini-2.5-flash",
]
_EMERGENT_UNIVERSAL_CONNECTED_AT = "2026-08-25T00:00:00Z"


def _shape_llm_from_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Project a data_connection_record (BYO LLM path) onto the wire shape.

    NEVER carries the `key` field; only custody markers.
    """
    resource = record.get("resource") or {}
    return {
        "provider": record.get("provider", "unknown"),
        "name": record.get("name") or f"{record.get('provider', 'unknown')} (byo-key)",
        "connection_id": record.get("source_id", ""),
        "region": resource.get("region", ""),
        "connected_at": record.get("connected_at") or record.get("at", ""),
        "custody_kind": "estate_keys_file",
        "models_available": record.get("models_available") or [],
        "link_working": bool(record.get("link_working")),
    }


def _llms() -> List[Dict[str, Any]]:
    """Enumerate connected LLMs from two sources:
      (a) env-var EMERGENT_LLM_KEY present → emergent-universal entry.
      (b) data_connection_records/llm_<provider>_*_FINAL.json on disk → BYO entries.

    Custody discipline: the response NEVER carries a `key`, `api_key`,
    `secret`, `token`, or `credential` field. Owner Order 2026-08-25 §4:
    'no raw credential/secret material'.
    """
    out: List[Dict[str, Any]] = []

    # (a) Emergent-universal via env var — a real connection at W5 open.
    if (os.environ.get("EMERGENT_LLM_KEY") or "").strip():
        out.append({
            "provider": "emergent",
            "name": "Emergent Universal — testing stack, all available models",
            "connection_id": "emergent-universal",
            "region": "platform-managed",
            "connected_at": _EMERGENT_UNIVERSAL_CONNECTED_AT,
            "custody_kind": "env_var",
            "models_available": list(_EMERGENT_UNIVERSAL_MODELS),
            "link_working": True,
        })

    # (b) BYO provider keys from data_connection_records/.
    records_dir = _data_connection_records_dir()
    if records_dir.is_dir():
        for p in sorted(records_dir.glob("data_source_llm_*_FINAL.json")):
            try:
                record = json.loads(p.read_text())
            except Exception as exc:  # pragma: no cover
                log.warning("skipping unreadable llm record %s: %s", p, type(exc).__name__)
                continue
            out.append(_shape_llm_from_record(record))

    return out


def load_models() -> Dict[str, Any]:
    """Bought-in LLMs (via _llms()) + locally-trained models (empty today).

    Owner Order 2026-08-25 §2 binding effect §2: Emergent Universal LLM is
    a real connected LLM. It renders under records.
    """
    llms = _llms()
    return {
        "records": llms,
        "reason": (
            "" if llms else
            "No models connected yet. Bought-in and locally-trained models "
            "both land here, on one record."
        ),
    }


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def assemble_facts() -> Dict[str, Any]:
    """Assemble the Registry facts dict.

    Shape (stable wire contract):
      {
        "data_sources": [ ...shape_data_source ],
        "compute":      [ ...shape_compute ],
        "models":       { "records": [], "reason": "..." },
        "provenance":   { "data_connection_record_dir": "...",
                          "commissioning_record_dir": "..." }
      }
    """
    data_sources = load_data_sources()
    compute = load_compute()
    models = load_models()
    return {
        "data_sources": data_sources,
        "compute": compute,
        "models": models,
        "provenance": {
            "data_connection_record_dir": str(_data_connection_records_dir()),
            "commissioning_record_dir": str(_commissioning_records_dir()),
        },
    }
