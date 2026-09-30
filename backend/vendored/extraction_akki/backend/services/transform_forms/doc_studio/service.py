"""Commission lifecycle around the installed doc-studio skill: create (producer) → build --prove → revise → export → read.
The skill's own scripts do the production in a subprocess (build.py --prove: resolve → validate → render → recalc → freeze → QA,
twice, asserting byte identity); this module only writes the commission directory, records what the skill reported, binds
platform receipts, and keeps the tenant-scoped record. Nothing here edits a commission version in place."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from services.transform_forms.doc_studio import store
from services.transform_forms.doc_studio.frames import FRAMES, frame_for, verdict_from_frame
from services.transform_forms.doc_studio.install import environment, read_manifest
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief
from services.transform_forms.doc_studio.producer_estate import commission_from_report
from services.transform_forms.doc_studio.receipts import bind_receipts
from services.transform_forms.doc_studio.skill_env import SCRIPTS_DIR, build_env, skill_module

MEDIA = {".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
         ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".html": "text/html; charset=utf-8", ".pdf": "application/pdf", ".json": "application/json"}
LOOK_KEYS = ("palette_id", "type_pair_id", "cover_composition", "divider_treatment")
BUILD_TIMEOUT = 280


def now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(dt: Optional[datetime] = None) -> str:
    return (dt or now()).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ----------------------------------------------------------------------------- create


def create_from_estate(job_id: str, tenant_id: str, principal_id: str) -> Tuple[Dict[str, Any], bool]:
    """Idempotent per (tenant, census, purpose, day): a repeat call returns the existing commission, never a duplicate."""
    from services.census_autonomy import estate_intelligence_report as eir
    report = eir.report_for(job_id, cached_only=True)
    if not report:
        raise LookupError("No verified estate intelligence report is banked for that census.")
    plan = commission_from_report(report, tenant_id, principal_id, now())
    existing = store.load_record(tenant_id, plan["commission_id"])
    if existing:
        return existing, False
    vdir = store.version_dir(tenant_id, plan["commission_id"], 1)
    for name, doc in plan["files"].items():
        store.write_json(vdir / name, doc)
    bound, blockers = bind_receipts(plan["files"]["content.json"])
    record = {"commission_id": plan["commission_id"], "tenant_id": tenant_id, "title": plan["title"], "organisation": tenant_id, "producer": plan["producer"], "source_ref": plan["source_ref"],
              "content_id": plan["content_id"], "purpose": plan["files"]["brief.json"]["purpose"]["kind"], "frame_ref": plan["frame_ref"], "voice": plan["voice"], "house": plan["files"]["brief.json"]["brand"]["house"],
              "seed": plan["seed"], "seed_rule": "content_id/purpose.kind/commission-date, derived by the producer", "build_stamp": plan["build_stamp"], "build_stamp_rule": "set once at commission creation; frozen",
              "brief_id": plan["files"]["brief.json"]["brief_id"], "verdict_id": plan["files"]["verdict.json"]["verdict_id"], "adopted_direction": plan["files"]["verdict.json"]["adopted"],
              "manifest": plan["files"]["verdict.json"]["manifest"], "outputs": [o["format"] for o in plan["files"]["brief.json"]["outputs"]], "specs": sorted(n for n in plan["files"] if n not in ("brief.json", "content.json", "verdict.json")),
              "created_at": stamp(), "created_by": principal_id, "updated_at": stamp(), "current_content_version": 1,
              "versions": [{"version": 1, "at": stamp(), "by": principal_id, "reason": "commissioned from the verified census report"}],
              "receipts": bound, "receipt_blockers": blockers, "builds": [], "revisions": [],
              "release": {"state": "unbuilt", "reason": "no build yet"}, "authoring": {"tokens": 0, "source": "deterministic producer estate_intelligence; no model authored the brief, content or specs"},
              "economics": {"builds_total": 0, "renders_total": 0, "authoring_tokens_total": 0, "rerender_authoring_tokens": 0,
                            "note": "every build renders twice (prove); re-renders and revisions invoke no authoring model by construction"}}
    return store.save_record(record), True


# ----------------------------------------------------------------------------- build


def _run_build(vdir: Path, bdir: Path) -> Dict[str, Any]:
    bdir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(SCRIPTS_DIR / "build.py"), str(vdir), str(bdir), "--prove"]
    try:
        run = subprocess.run(cmd, capture_output=True, text=True, timeout=BUILD_TIMEOUT, env=build_env(), cwd=str(SCRIPTS_DIR.parent))
        out, err, rc = run.stdout, run.stderr, run.returncode
    except subprocess.TimeoutExpired as exc:
        out, err, rc = exc.stdout or "", f"BUILD_TIMEOUT after {BUILD_TIMEOUT}s", 124
    (bdir / "log.txt").write_text(out + ("\n--- stderr ---\n" + err if err else ""))
    return {"rc": rc, "stdout": out, "stderr": err}


def _read(path: Path) -> Optional[Any]:
    return store.read_json(path)


def build(tenant_id: str, commission_id: str, principal_id: str, *, previous_outputs: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    record = store.load_record(tenant_id, commission_id)
    if not record:
        raise LookupError("No commission with that reference is available in your tenant.")
    version = record["current_content_version"]
    vdir = store.version_dir(tenant_id, commission_id, version)
    content = _read(vdir / "content.json")
    bound, blockers = bind_receipts(content)
    record["receipts"], record["receipt_blockers"] = bound, blockers
    build_id = "bld-" + _sha(f"{commission_id}|{version}|{stamp()}|{len(record['builds'])}".encode())[:12]
    entry: Dict[str, Any] = {"build_id": build_id, "content_version": version, "at": stamp(), "by": principal_id, "status": "blocked", "outputs": [], "prove": None, "validate": None, "qa": None, "look": None, "exports": {}}
    if blockers:
        entry["error"] = "receipt binding blocked the build; no artefact was produced"
        entry["blockers"] = blockers
    else:
        bdir = store.build_dir(tenant_id, commission_id, build_id)
        run = _run_build(vdir, bdir)
        entry.update(_summarise(bdir, run, previous_outputs))
    record["builds"].append(entry)
    record["economics"]["builds_total"] += 1
    record["economics"]["renders_total"] += (2 if entry["status"] in ("released", "not_reproducible") else 0)
    record["updated_at"] = stamp()
    record["release"] = _release_state(record)
    return store.save_record(record)


def _summarise(bdir: Path, run: Dict[str, Any], previous_outputs: Optional[Dict[str, str]]) -> Dict[str, Any]:
    a, b = bdir / "a", bdir / "b"
    validate = _read(a / "resolved" / "validate-report.json")
    qa = _read(a / "out" / "qa-report.json")
    ma, mb = _read(a / "out" / "build-manifest.json"), _read(b / "out" / "build-manifest.json")
    plan = _read(a / "resolved" / "deck.resolved.json") or _read(a / "resolved" / "paper.resolved.json")
    look = {k: (plan or {}).get("look", {}).get(k) for k in LOOK_KEYS} if plan else None
    outputs = []
    if ma:
        for name, sha in ma["outputs_sha256"].items():
            path = a / "out" / name
            outputs.append({"name": name, "sha256": sha, "size": path.stat().st_size if path.exists() else None, "format": Path(name).suffix.lstrip("."),
                            "changed_from_previous": (previous_outputs.get(name) != sha) if previous_outputs is not None else None})
    prove = None
    if ma and mb:
        diff = {k: {"a": ma["outputs_sha256"][k], "b": mb["outputs_sha256"].get(k)} for k in ma["outputs_sha256"] if ma["outputs_sha256"][k] != mb["outputs_sha256"].get(k)}
        prove = {"byte_identical": not diff and run["rc"] == 0, "diff": diff, "builds_compared": 2}
    if run["rc"] == 0 and prove and prove["byte_identical"] and (qa or {}).get("status") == "PASS":
        status = "released"
    elif prove and not prove["byte_identical"]:
        status = "not_reproducible"
    elif validate and validate.get("status") == "FAIL":
        status = "blocked"
    elif qa and qa.get("status") == "FAIL":
        status = "blocked"
    else:
        status = "failed"
    return {"status": status, "outputs": outputs, "prove": prove, "validate": validate, "qa": qa, "look": look, "manifest": ma, "environment": (ma or {}).get("environment") or environment(),
            "error": None if status == "released" else (run["stderr"].strip().splitlines() or ["build did not release"])[-1][:300], "log_path": str(bdir / "log.txt")}


def _release_state(record: Dict[str, Any]) -> Dict[str, Any]:
    last_build = record["builds"][-1] if record["builds"] else None
    last_rev = record["revisions"][-1] if record["revisions"] else None
    if last_rev and last_rev.get("strikes") and last_rev["to_version"] == record["current_content_version"]:
        return {"state": "blocked pending re-verdict", "reason": f"{len(last_rev['strikes'])} manifest strike(s): {', '.join(s['manifest'] for s in last_rev['strikes'])}"}
    if not last_build:
        return {"state": "unbuilt", "reason": "no build yet"}
    if last_build["status"] == "released":
        return {"state": "clear", "reason": f"build {last_build['build_id']} byte-identical across two builds; validate and QA PASS"}
    return {"state": "blocked", "reason": last_build.get("error") or last_build["status"]}


# ----------------------------------------------------------------------------- revise / re-verdict


def _new_version(tenant_id: str, commission_id: str, record: Dict[str, Any]) -> Tuple[int, Path, Path]:
    cur = record["current_content_version"]
    src, dst = store.version_dir(tenant_id, commission_id, cur), store.version_dir(tenant_id, commission_id, cur + 1)
    if dst.exists():
        raise FileExistsError(f"version {cur + 1} already exists")
    shutil.copytree(src, dst)
    return cur + 1, src, dst


def _bump_content_ref(dst: Path) -> str:
    content = _read(dst / "content.json")
    content["version"] += 1
    store.write_json(dst / "content.json", content)
    cref = f"{content['content_id']}@{content['version']}"
    for spec in dst.glob("*.json"):
        doc = _read(spec)
        if isinstance(doc, dict) and "spec_type" in doc:
            doc["content_ref"] = cref
            store.write_json(spec, doc)
    return cref


def _last_released_outputs(record: Dict[str, Any]) -> Optional[Dict[str, str]]:
    for b in reversed(record["builds"]):
        if b["status"] == "released":
            return {o["name"]: o["sha256"] for o in b["outputs"]}
    return None


def _look_of(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for b in reversed(record["builds"]):
        if b.get("look"):
            return b["look"]
    return None


def revise(tenant_id: str, commission_id: str, principal_id: str, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Mirror of scripts/revise.py: copy → apply → strike-check against the manifest → bump → rebuild → diff. A strike blocks release, not the build."""
    revise_mod = skill_module("revise")
    record = store.load_record(tenant_id, commission_id)
    if not record:
        raise LookupError("No commission with that reference is available in your tenant.")
    if not changes:
        raise ValueError("A revision needs at least one change (path=value).")
    prev_outputs, prev_look = _last_released_outputs(record), _look_of(record)
    new_version, _, dst = _new_version(tenant_id, commission_id, record)
    docs = {"content": _read(dst / "content.json"), "brief": _read(dst / "brief.json")}
    verdict = _read(dst / "verdict.json")
    applied, strikes = [], []
    for change in changes:
        path, value = str(change["path"]), change["value"]
        root, _, rest = path.partition(".")
        if root not in docs or not rest:
            shutil.rmtree(dst)
            raise ValueError(f"paths address content.* or brief.*; got {path}")
        value = revise_mod.parse_value(value) if isinstance(value, str) else value
        try:
            old = revise_mod.set_path(docs[root], rest, value)
        except (KeyError, TypeError):
            shutil.rmtree(dst)
            raise ValueError(f"{path} does not address an existing field") from None
        applied.append({"path": path, "old": old, "new": value})
        for m in verdict["manifest"]:
            if root == "brief" and any(rest.startswith(s.strip().replace("brief.", "")) for s in m["source"].split(",")):
                strikes.append({"manifest": m["id"], "assumption": m["assumption"], "flips": m["flips"], "cause": path})
    for name, doc in docs.items():
        store.write_json(dst / f"{name}.json", doc)
    cref = _bump_content_ref(dst)
    record["current_content_version"] = new_version
    record["versions"].append({"version": new_version, "at": stamp(), "by": principal_id, "reason": "revision: " + "; ".join(a["path"] for a in applied)})
    rev_id = f"rev-{new_version}"
    record["revisions"].append({"rev_id": rev_id, "at": stamp(), "by": principal_id, "from_version": new_version - 1, "to_version": new_version, "changes": applied, "content_ref": cref,
                                "strikes": strikes, "release": "blocked pending re-verdict" if strikes else "clear", "build_id": None, "look_preserved": None, "outputs_changed": None})
    store.save_record(record)
    record = build(tenant_id, commission_id, principal_id, previous_outputs=prev_outputs)
    last = record["builds"][-1]
    rev = record["revisions"][-1]
    rev["build_id"] = last["build_id"]
    rev["look_preserved"] = (prev_look == last["look"]) if prev_look and last.get("look") else None
    rev["outputs_changed"] = [o["name"] for o in last["outputs"] if o.get("changed_from_previous")] if prev_outputs is not None else None
    if last["status"] != "released":
        rev["release"] = "blocked"
    record["release"] = _release_state(record)
    record["updated_at"] = stamp()
    return store.save_record(record)


def reverdict(tenant_id: str, commission_id: str, principal_id: str) -> Dict[str, Any]:
    """The coach seat's re-verdict after a strike: a new version whose verdict is re-instantiated from the standing frame with a
    manifest regenerated from the current brief (condition B), confirmed by the operator; then a rebuild. Nothing is edited in place."""
    record = store.load_record(tenant_id, commission_id)
    if not record:
        raise LookupError("No commission with that reference is available in your tenant.")
    if record["release"]["state"] != "blocked pending re-verdict":
        raise ValueError("No strike is pending on this commission.")
    prev_outputs, prev_look = _last_released_outputs(record), _look_of(record)
    new_version, _, dst = _new_version(tenant_id, commission_id, record)
    brief, content, old_verdict = _read(dst / "brief.json"), _read(dst / "content.json"), _read(dst / "verdict.json")
    frame = frame_for(brief)
    if frame is None:
        shutil.rmtree(dst)
        raise LookupError("the revised brief is non-routine: no standing frame covers it and CIF's ideas endpoint is not mounted in this runtime")
    manifest = manifest_from_brief(brief, has_options=len(content.get("options") or {}) == 3)
    verdict = verdict_from_frame(frame, brief, f"{old_verdict['verdict_id'].split('-r')[0]}-r{new_version}", manifest, confirmed_by=principal_id, confirmed_at=stamp())
    verdict["re_verdict_of"] = old_verdict["verdict_id"]
    store.write_json(dst / "verdict.json", verdict)
    for spec in dst.glob("*.json"):
        doc = _read(spec)
        if isinstance(doc, dict) and "spec_type" in doc:
            doc["verdict_ref"] = verdict["verdict_id"]
            store.write_json(spec, doc)
    cref = _bump_content_ref(dst)
    record.update(current_content_version=new_version, verdict_id=verdict["verdict_id"], manifest=manifest, adopted_direction=verdict["adopted"])
    record["versions"].append({"version": new_version, "at": stamp(), "by": principal_id, "reason": f"re-verdict under {frame['frame_id']} after strike"})
    record["revisions"].append({"rev_id": f"rev-{new_version}", "at": stamp(), "by": principal_id, "from_version": new_version - 1, "to_version": new_version, "changes": [], "content_ref": cref,
                                "strikes": [], "release": "clear", "re_verdict": verdict["verdict_id"], "build_id": None, "look_preserved": None, "outputs_changed": None})
    store.save_record(record)
    record = build(tenant_id, commission_id, principal_id, previous_outputs=prev_outputs)
    last, rev = record["builds"][-1], record["revisions"][-1]
    rev.update(build_id=last["build_id"], look_preserved=(prev_look == last["look"]) if prev_look and last.get("look") else None,
               outputs_changed=[o["name"] for o in last["outputs"] if o.get("changed_from_previous")] if prev_outputs is not None else None, release="clear" if last["status"] == "released" else "blocked")
    record["release"] = _release_state(record)
    return store.save_record(record)


# ----------------------------------------------------------------------------- artefacts and exports


def _build_entry(record: Dict[str, Any], build_id: str) -> Optional[Dict[str, Any]]:
    return next((b for b in record["builds"] if b["build_id"] == build_id), None)


def artifact(tenant_id: str, commission_id: str, build_id: str, name: str) -> Optional[Tuple[bytes, str, str]]:
    record = store.load_record(tenant_id, commission_id)
    entry = _build_entry(record, build_id) if record else None
    if not entry:
        return None
    bdir = store.build_dir(tenant_id, commission_id, build_id)
    if name == "review.pdf" and entry.get("exports", {}).get("pdf"):
        path = bdir / "exports" / "review.pdf"
    elif name == "build-manifest.json" or any(o["name"] == name for o in entry["outputs"]):
        path = bdir / "a" / "out" / name
    else:
        return None
    if not path.exists():
        return None
    return path.read_bytes(), MEDIA.get(path.suffix, "application/octet-stream"), path.name


def export_pdf(tenant_id: str, commission_id: str, build_id: str, principal_id: str) -> Dict[str, Any]:
    """PDF of the review page through the Deck Rendering Engine's headless-browser pipeline; an export, outside the byte-identity contract."""
    from services.transform_forms.deck_engine import render as R
    record = store.load_record(tenant_id, commission_id)
    entry = _build_entry(record, build_id) if record else None
    if not entry or entry["status"] not in ("released",):
        raise LookupError("Only a released build can be exported.")
    html = next((o for o in entry["outputs"] if o["format"] == "html"), None)
    if not html:
        raise LookupError("This build has no review page to export.")
    bdir = store.build_dir(tenant_id, commission_id, build_id)
    try:
        pdf = R.render_pdf((bdir / "a" / "out" / html["name"]).read_bytes())
    except Exception as exc:  # noqa: BLE001 — every export failure is an enumerated refusal
        entry["exports"]["pdf"] = {"exported": False, "refusal": f"{type(exc).__name__}: {str(exc)[:200]}", "at": stamp(), "by": principal_id}
        return store.save_record(record)
    check = R.furniture_survives(pdf, ["Receipt", "CANNOT SAY"])
    out = bdir / "exports" / "review.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(pdf)
    entry["exports"]["pdf"] = {"exported": True, "name": "review.pdf", "sha256": _sha(pdf), "size": len(pdf), "check": check, "at": stamp(), "by": principal_id,
                               "note": "browser PDF carries producer metadata; determinism is proven on the pptx/docx/xlsx/html bytes"}
    record["updated_at"] = stamp()
    return store.save_record(record)


# ----------------------------------------------------------------------------- reads


def list_commissions(tenant_id: str) -> List[Dict[str, Any]]:
    keys = ("commission_id", "title", "producer", "source_ref", "purpose", "frame_ref", "voice", "outputs", "created_at", "updated_at", "current_content_version", "release", "adopted_direction")
    out = []
    for r in store.list_records(tenant_id):
        last = r["builds"][-1] if r["builds"] else None
        out.append({k: r.get(k) for k in keys} | {"builds": len(r["builds"]), "revisions": len(r["revisions"]), "last_build": {k: last.get(k) for k in ("build_id", "status", "at")} if last else None})
    return out


def get_commission(tenant_id: str, commission_id: str) -> Optional[Dict[str, Any]]:
    record = store.load_record(tenant_id, commission_id)
    if not record:
        return None
    vdir = store.version_dir(tenant_id, commission_id, record["current_content_version"])
    record["files"] = {p.name: _read(p) for p in sorted(vdir.glob("*.json"))}
    return record


def frames() -> Dict[str, Any]:
    return {"frames": list(FRAMES.values()), "manifest_template": "services/transform_forms/doc_studio/manifest_template.py", "install": {k: read_manifest()[k] for k in ("version", "installed_at", "changed_from_v1_0")}}
