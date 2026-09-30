"""Deck rendering service (DR-R1): validate → render → write-once artefact → production record keyed by deck_id (DR-R2/R12).
Tenant-scoped store under AKKI_DECK_STORE_DIR; every render is a metered event on the record (renders-per-deck, authoring tokens)."""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.transform_forms.deck_engine import render as R
from services.transform_forms.deck_engine.validate import DeckValidationError, Resolver, default_resolver, lint, validate

SAFE = re.compile(r"[^A-Za-z0-9_.-]")


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _store(tenant_id: str) -> Path:
    root = Path(os.environ["AKKI_DECK_STORE_DIR"]) / SAFE.sub("_", tenant_id)
    root.mkdir(parents=True, exist_ok=True)
    return root


def _record_path(tenant_id: str, deck_id: str) -> Path:
    return _store(tenant_id) / f"{SAFE.sub('_', deck_id)}.json"


def _put_once(path: Path, data: bytes) -> Dict[str, Any]:
    """Write-once: an existing artefact is never overwritten; identical bytes prove determinism, different bytes are a breach."""
    if path.exists():
        existing = path.read_bytes()
        return {"existed": True, "byte_identical": existing == data, "sha256": hashlib.sha256(existing).hexdigest(), "size": len(existing)}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data); os.replace(tmp, path)
    return {"existed": False, "byte_identical": None, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def render_deck(spec: Dict[str, Any], tenant_id: str, principal_id: str, *, resolver: Resolver = default_resolver,
                want_pdf: bool = False, authoring: Optional[Dict[str, Any]] = None, producer: Optional[str] = None) -> Dict[str, Any]:
    """Raises DeckValidationError (full enumerated set) or returns the production record. All-or-nothing: no partial artefact."""
    checked = validate(spec, resolver)
    deck = checked["spec"]
    html = R.render_html(deck, checked["plate_models"])
    sh = R.spec_hash(deck)
    store = _store(tenant_id)
    deck_dir = store / SAFE.sub("_", deck.deck_id)
    stem = f"{sh[:16]}-{R.TOKEN_VERSION}-{R.ENGINE_VERSION}"
    html_put = _put_once(deck_dir / f"{stem}.html", html)
    if html_put["existed"] and not html_put["byte_identical"]:
        raise DeckValidationError([{"slide_index": None, "rule": "determinism_breach",
                                    "message": f"artifact for spec {sh} / tokens {R.TOKEN_VERSION} / engine {R.ENGINE_VERSION} already exists with different bytes"}])
    (deck_dir / f"{stem}.spec.json").write_text(json.dumps(spec, indent=1, sort_keys=True, default=str)) if not (deck_dir / f"{stem}.spec.json").exists() else None
    path = _record_path(tenant_id, deck.deck_id)
    previous = json.loads(path.read_text()) if path.exists() else {}
    versions = {v["spec_hash"]: v for v in previous.get("versions", [])}
    version = versions.get(sh) or {"spec_hash": sh, "token_version": R.TOKEN_VERSION, "engine_version": R.ENGINE_VERSION, "first_rendered_at": now(), "render_count": 0,
                                    "artifact": {"html": {"path": str(deck_dir / f"{stem}.html"), "sha256": html_put["sha256"], "size": html_put["size"]}},
                                    "authoring": authoring or {"tokens": 0, "source": producer or "submitted spec; no model authored it through this service"}}
    version["render_count"] += 1
    version["last_rendered_at"] = now()
    version["byte_identical_rerender"] = html_put["byte_identical"] if html_put["existed"] else None
    if want_pdf:
        version["artifact"]["pdf"] = _export_pdf(deck_dir / f"{stem}.pdf", html)
    versions[sh] = version
    exhibits = [s for s in list(deck.slides) + list(deck.appendix.extra_slides) if s.figures or s.plate in ("P3", "P4", "P5", "P11")]
    record = {"deck_id": deck.deck_id, "tenant_id": tenant_id, "spec_version": deck.spec_version, "register": deck.register_, "title": deck.meta.title,
              "sample_deck": deck.meta.sample_deck, "slides": len(deck.slides), "exhibits": len(exhibits), "current_spec_hash": sh,
              "token_version": R.TOKEN_VERSION, "engine_version": R.ENGINE_VERSION, "producer": producer or previous.get("producer"),
              "rendered_by": principal_id, "created_at": previous.get("created_at") or now(), "updated_at": now(),
              "receipts_resolved": {ref: {k: rec.get(k) for k in ("kind", "status", "verified")} for ref, rec in checked["receipts"].items()},
              "lint": lint(deck), "errors": [], "live_motion": False, "pdf_capability": R.pdf_capability(),
              "versions": sorted(versions.values(), key=lambda v: v["first_rendered_at"]),
              "economics": {"authoring_tokens_total": sum(int((v.get("authoring") or {}).get("tokens") or 0) for v in versions.values()),
                            "renders_total": sum(v["render_count"] for v in versions.values()),
                            "rerender_authoring_tokens": 0, "note": "re-renders and register switches invoke no authoring model by construction (DR-R12); tokens are read from the producer's chokepoint receipt, never estimated"}}
    path.write_text(json.dumps(record, indent=1, default=str))
    return record


def _export_pdf(path: Path, html: bytes) -> Dict[str, Any]:
    try:
        pdf = R.render_pdf(html)
    except (RuntimeError, OSError, Exception) as exc:  # noqa: BLE001 — every export failure is an enumerated refusal, never a silent HTML-only success
        return {"exported": False, "refusal": f"{type(exc).__name__}: {str(exc)[:200]}"}
    check = R.furniture_survives(pdf, list(R.FURNITURE_MARKERS[:0]) + ["Receipts:", "Covered basis"])
    if check.get("checked") and not check.get("survives"):
        return {"exported": False, "refusal": "EXPORT_FURNITURE_LOST: " + ", ".join(check["missing"]), "check": check}
    put = _put_once(path, pdf)
    return {"exported": True, "path": str(path), "sha256": put["sha256"], "size": put["size"], "check": check,
            "determinism_note": "PDF bytes carry producer metadata; determinism is asserted on the HTML artifact of record"}


def load(tenant_id: str, deck_id: str) -> Optional[Dict[str, Any]]:
    path = _record_path(tenant_id, deck_id)
    return json.loads(path.read_text()) if path.exists() else None


def list_decks(tenant_id: str) -> List[Dict[str, Any]]:
    out = []
    for path in sorted(_store(tenant_id).glob("*.json")):
        try:
            rec = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        out.append({k: rec.get(k) for k in ("deck_id", "title", "register", "slides", "exhibits", "current_spec_hash", "engine_version", "token_version", "producer", "updated_at", "sample_deck")}
                   | {"renders_total": (rec.get("economics") or {}).get("renders_total")})
    return sorted(out, key=lambda r: r.get("updated_at") or "", reverse=True)


def artifact_bytes(tenant_id: str, deck_id: str, spec_hash: Optional[str], ext: str) -> Optional[bytes]:
    rec = load(tenant_id, deck_id)
    if not rec:
        return None
    target = spec_hash or rec["current_spec_hash"]
    for v in rec["versions"]:
        if v["spec_hash"] == target and (v["artifact"].get(ext) or {}).get("path"):
            p = Path(v["artifact"][ext]["path"])
            return p.read_bytes() if p.exists() else None
    return None
