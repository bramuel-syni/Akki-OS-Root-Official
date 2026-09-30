"""Training manifest: per-example provenance carried through to the trained artefact (A17.20, #24).

Built from the commission's materials index. Selection for each calibration
volume is deterministic (examples ordered by sha256(example_id); first N;
each volume a superset of the previous). An example without class, lawful
basis, basis_ref or content_hash is refused and counted; the run does not
start if any refusal occurs, because a partial manifest is not a manifest.
"""
import hashlib, json
from pathlib import Path

REQUIRED = ["example_id", "source", "stratum", "class", "lawful_basis", "basis_ref", "content_hash"]


def load_index(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def build(plan, index_rows):
    refused = []
    rows = []
    for r in index_rows:
        missing = [k for k in REQUIRED if not r.get(k)]
        if missing:
            refused.append({"example_id": r.get("example_id"), "missing": missing})
            continue
        rows.append(r)
    # deterministic order per stratum
    by_stratum = {}
    for r in rows:
        by_stratum.setdefault(r["stratum"], []).append(r)
    for s in by_stratum:
        by_stratum[s].sort(key=lambda r: hashlib.sha256(r["example_id"].encode()).hexdigest())
    vols = plan["calibration"]["volumes"]
    manifest_rows = []
    for s, lst in by_stratum.items():
        for i, r in enumerate(lst):
            sel = [f"calibration@{v}" for v in vols if i < v]
            manifest_rows.append({**{k: r[k] for k in REQUIRED}, "duration_s": r.get("duration_s"), "selected_for": sel})
    manifest_rows.sort(key=lambda r: (r["stratum"], r["example_id"]))
    canonical = "\n".join(json.dumps(r, sort_keys=True) for r in manifest_rows)
    counts = {}
    for r in manifest_rows:
        counts.setdefault(r["stratum"], {"total": 0, "by_class": {}, "by_basis": {}})
        c = counts[r["stratum"]]
        c["total"] += 1
        c["by_class"][r["class"]] = c["by_class"].get(r["class"], 0) + 1
        c["by_basis"][r["lawful_basis"]] = c["by_basis"].get(r["lawful_basis"], 0) + 1
    return {
        "manifest_hash": "sha256:" + hashlib.sha256(canonical.encode()).hexdigest(),
        "examples": len(manifest_rows), "refused": refused, "classed_pct": 100.0 if manifest_rows else 0.0,
        "lawful_basis_present": all(r["lawful_basis"] for r in manifest_rows),
        "per_stratum": counts, "selection_rule": plan["calibration"].get("selection", "deterministic by sha256(example_id)"),
        "volumes": vols,
    }, manifest_rows


def check_counts(objective_materials, index_rows):
    """Objective counts must equal the index counts per source; otherwise the datasheet lies about the manifest."""
    got = {}
    for r in index_rows:
        got[r["source"]] = got.get(r["source"], 0) + 1
    out = []
    for mid, m in objective_materials.items():
        if got.get(mid, 0) != m["examples"]:
            out.append(f"material {mid}: objective says {m['examples']} examples, index has {got.get(mid, 0)}")
    for src in got:
        if src not in objective_materials:
            out.append(f"index source {src} not declared in objective.materials")
    return out
