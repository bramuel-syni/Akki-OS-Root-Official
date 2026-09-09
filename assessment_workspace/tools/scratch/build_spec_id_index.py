#!/usr/bin/env python3
"""
build_spec_id_index.py — owner directive 2026-09-08T~06:15Z + 2026-09-09T~11:40Z extension.

Scans /app/assessment_workspace/canon/ (all drops, all extracted text) plus notes/
for spec-ID and design-ID tokens; for each discovered token, resolves it to a
banked file (via sha256 + filename mapping) or emits a zero-hit receipt entry.

Ground truth for filename ⇔ spec-ID mapping: the docx's own opening signature,
scraped as `<spec_id> — Draft for owner ratification` from word/document.xml.

Output:
  notes/spec_id_index.json  — machine-readable {id, filename, sha256, kind, status}
  notes/spec_id_index.md    — human-readable table + missing list

Tests-first invariant at backend/tests/invariants/test_spec_id_tracking_index.py
consumes the JSON.

Thin-kernel note: this is a workspace analysis tool under tools/scratch/, NOT
production code. It is not imported by any FastAPI/React runtime.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/app/assessment_workspace")
CANON = ROOT / "canon"
NOTES = ROOT / "notes"
FIXTURES = ROOT / "fixtures"

# ---------- Regex for spec-ID discovery in citing text ----------

# Spec-ID token regex — well-known IDs plus generic *_spec_v<n> / *_annex_v<n>
SPEC_ID_RE = re.compile(
    r"\b("
    r"rule_criteria_spec_v\d+"
    r"|business_continuity_v\d+"
    r"|agent_containment_spec_v\d+"
    r"|dap_backend_spec_v\d+"
    r"|rulebook_engine_spec_v\d+"
    r"|trust_domains_v\d+"
    r"|failure_posture_v\d+"
    r"|determinism_inventory_v\d+"
    r"|handoff_registry_v\d+"
    r"|pruning_unlearning_amendment_v\d+"
    r"|security_function_policies_v\d+"
    r"|security_architecture_v\d+"
    r"|tcb_enumeration_v\d+"
    r"|whitepaper_wizard_spec_v\d+"
    r"|akki_governance_architecture_v\d+"
    r"|ratification_record_v\d+"
    r"|cif_spec_v\d+"
    r"|extraction_derisking_spec_v\d+"
    r"|training_techniques_spec_v\d+"
    r"|transformation_quality_spec_v\d+"
    r"|eab_tier1_adoption_spec_v\d+"
    r"|audio_intelligence_plane_spec_v\d+"
    r"|security_promise_set_amendments"
    r"|security_amendments_trojan_whisper"
    r")\b"
)

# ---------- Filename ⇔ spec-ID authoritative signature scan ----------

# Ground truth: scrape the docx opening line `<spec_id> — Draft for owner ratification`
SIG_RE = re.compile(rb"([a-z][a-z0-9_]+_v\d+) \xe2\x80\x94 (?:Draft|Ratified|Ruled)")

# Fallback filename→spec-ID map for docs without opening signature
FILENAME_FALLBACK_MAP = {
    # Canon 1..9 aren't cited by spec-ID; excluded from the spec-ID index by design
    # (they're the base canon; their requirements are already extracted into notes/canon_N_requirements.md).
    "Security_Promise_Set_Amendments.docx": "security_promise_set_amendments",
    "Security_Amendments_Trojan_Whisper.docx": "security_amendments_trojan_whisper",
    "Akki_Governance_Architecture_v1.docx": "akki_governance_architecture_v1",
    "Ratification_Record_v1.docx": "ratification_record_v1",
    "Pruning_Unlearning_Amendment_v1.docx": "pruning_unlearning_amendment_v1",
    "doc0_governance_architecture.docx": "akki_governance_architecture_v0",
}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def scrape_opening_signature(docx_path: Path) -> str | None:
    """Return the spec-ID from the docx's opening signature, or None if absent."""
    try:
        out = subprocess.run(
            ["unzip", "-p", str(docx_path), "word/document.xml"],
            capture_output=True, check=True, timeout=10,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None
    m = SIG_RE.search(out.stdout)
    if m:
        return m.group(1).decode("ascii")
    return None


# ---------- Design-ID inventory (owner extension 2026-09-09T~11:40Z) ----------

DESIGN_ID_MAP = {
    "prototype_v3": "canon/drops/20260909/raw/RMS_AI_Prototype_standalone_v3.html",
    "prototype_v2_standalone": "canon/prototypes/20260907_v2_standalone/RMS_AI_Prototype_v2_Standalone.html",
    "prototype_v2_decoded": "canon/prototypes/20260907_v2_standalone/decoded_v2.html",
    "prototype_v8_decoded": "canon/prototypes/20260907_v2_standalone/decoded_v8.html",
    "prototype_v7_standalone": "fixtures/RMS_AI_Akki_Prototype_v7_Standalone.html",
    "prototype_v7_standalone_v2": "fixtures/RMS_AI_Akki_Prototype_v7_Standalone_v2.html",
    "prototype_v7_v2_embedded_app": "fixtures/RMS_AI_Akki_Prototype_v7_v2_EMBEDDED_APP.html",
    "prototype_v8_standalone": "fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html",
    "dap_frontend_standalone": "canon/drops/20260909/raw/RMS_Data_Access_Portal_standalone.html",
    "v8_template": "notes/wave_g_step0_v8/v8_template.html",
    "v8_template_decoded": "notes/wave_g_step0_v8/v8_template_decoded.html",
}


# ---------- Build filename→spec-ID mapping from opening signatures ----------

def build_docx_mapping() -> dict[str, dict]:
    """Return dict[spec_id → {filename, path, sha256, kind, signature_source}]."""
    mapping: dict[str, dict] = {}
    for base in [CANON, FIXTURES]:
        for path in base.rglob("*.docx"):
            spec_id = scrape_opening_signature(path)
            source = "opening_signature"
            if spec_id is None:
                spec_id = FILENAME_FALLBACK_MAP.get(path.name)
                source = "filename_fallback" if spec_id else None
            if spec_id is None:
                continue
            entry = {
                "filename": path.name,
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256_of(path),
                "kind": "docx",
                "signature_source": source,
            }
            # If already have an entry, prefer raw/ paths over extracted/
            if spec_id in mapping:
                if "raw" in path.parts and "raw" not in Path(mapping[spec_id]["path"]).parts:
                    mapping[spec_id]["_duplicate_paths"] = mapping[spec_id].get("_duplicate_paths", []) + [mapping[spec_id]["path"]]
                    mapping[spec_id].update(entry)
                else:
                    mapping[spec_id].setdefault("_duplicate_paths", []).append(str(path.relative_to(ROOT)))
            else:
                mapping[spec_id] = entry
    return mapping


# ---------- Discover spec-IDs referenced in canon + notes text ----------

def discover_referenced_ids() -> dict[str, list[str]]:
    citations: dict[str, list[str]] = {}
    for base in [CANON, NOTES]:
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".txt", ".md", ".json"}:
                continue
            # Skip self — the index itself must not count as a citation source
            if path.name.startswith("spec_id_index."):
                continue
            if path.stat().st_size > 5_000_000:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in SPEC_ID_RE.finditer(text):
                citations.setdefault(m.group(1), []).append(str(path.relative_to(ROOT)))
    known_ids = {
        "rule_criteria_spec_v1", "business_continuity_v1", "agent_containment_spec_v1",
        "dap_backend_spec_v1", "rulebook_engine_spec_v1", "trust_domains_v1",
        "failure_posture_v1", "determinism_inventory_v1", "handoff_registry_v1",
        "pruning_unlearning_amendment_v1", "security_function_policies_v1",
        "security_architecture_v1", "tcb_enumeration_v1",
        "whitepaper_wizard_spec_v1", "akki_governance_architecture_v1",
        "ratification_record_v1",
    }
    cleaned: dict[str, list[str]] = {}
    for k, v in citations.items():
        paths = sorted(set(v))
        if len(paths) >= 2 or k in known_ids:
            cleaned[k] = paths
    return cleaned


# ---------- Build index ----------

def build_index() -> dict:
    docx_map = build_docx_mapping()
    referenced = discover_referenced_ids()

    all_ids = sorted(set(list(docx_map.keys()) + list(referenced.keys())))

    spec_rows: list[dict] = []
    missing: list[dict] = []
    for spec_id in all_ids:
        cite_paths = referenced.get(spec_id, [])
        banked = docx_map.get(spec_id)
        if banked is None:
            if spec_id == "rule_criteria_spec_v1":
                spec_rows.append({
                    "id": spec_id,
                    "status": "BANKED-DERIVED",
                    "filename": None,
                    "sha256": None,
                    "derived_from": [
                        "canon/drops/20260907/extracted/text/System_Rules_Registry.md",
                        "canon/drops/20260907/extracted/text/System_Rules_Registry.json",
                        "canon/drops/20260910/extracted/text/Master_Requirements_Registry.md",
                    ],
                    "citation_count": len(cite_paths),
                    "citation_paths": cite_paths,
                    "owner_ruling": "2026-09-09T~11:40Z — DEFAULT-PENDING-OVERRIDE ROC-1 ratified",
                })
                continue
            missing.append({
                "id": spec_id,
                "status": "MISSING",
                "citation_count": len(cite_paths),
                "citation_paths": cite_paths,
                "zero_hit_receipt": f"phase0/tracking_defect_20260908/grep_{spec_id}.txt",
            })
            continue
        row = {
            "id": spec_id,
            "status": "BANKED",
            "filename": banked["filename"],
            "path": banked["path"],
            "sha256": banked["sha256"],
            "kind": banked["kind"],
            "signature_source": banked["signature_source"],
            "citation_count": len(cite_paths),
            "citation_paths": cite_paths,
        }
        if "_duplicate_paths" in banked:
            row["duplicate_paths"] = banked["_duplicate_paths"]
        spec_rows.append(row)

    design_rows: list[dict] = []
    for design_id, rel_path in DESIGN_ID_MAP.items():
        path = ROOT / rel_path
        if not path.is_file():
            design_rows.append({"id": design_id, "status": "MISSING", "expected_path": rel_path})
            continue
        design_rows.append({
            "id": design_id,
            "status": "BANKED",
            "filename": path.name,
            "path": rel_path,
            "sha256": sha256_of(path),
            "kind": path.suffix.lstrip("."),
            "size_bytes": path.stat().st_size,
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner_directives": [
            "2026-09-08T~06:15Z — spec-ID tracking defect fix",
            "2026-09-09T~11:40Z — index scope extended to prototypes + HTML design drops",
        ],
        "ratchet_floor": 3006,
        "counts": {
            "spec_ids_total": len(spec_rows) + len(missing),
            "spec_ids_banked": sum(1 for r in spec_rows if r["status"] == "BANKED"),
            "spec_ids_banked_derived": sum(1 for r in spec_rows if r["status"] == "BANKED-DERIVED"),
            "spec_ids_missing": len(missing),
            "design_ids_total": len(design_rows),
            "design_ids_banked": sum(1 for r in design_rows if r["status"] == "BANKED"),
            "design_ids_missing": sum(1 for r in design_rows if r["status"] == "MISSING"),
        },
        "spec_ids": spec_rows,
        "missing": missing,
        "design_ids": design_rows,
    }


def write_markdown(index: dict) -> str:
    lines = [
        "# spec_id_index.md — canonical {id, filename, sha256} tracking",
        "",
        f"**Generated:** {index['generated_at']}",
        "",
        "**Owner directives banked:**",
    ]
    for d in index["owner_directives"]:
        lines.append(f"- {d}")
    lines += [
        "",
        f"**Ratchet floor:** {index['ratchet_floor']}",
        "",
        "## Counts",
        "",
        "| Class | Total | Banked | Banked-derived | Missing |",
        "|---|--:|--:|--:|--:|",
        f"| Spec IDs | {index['counts']['spec_ids_total']} | {index['counts']['spec_ids_banked']} | {index['counts']['spec_ids_banked_derived']} | {index['counts']['spec_ids_missing']} |",
        f"| Design IDs | {index['counts']['design_ids_total']} | {index['counts']['design_ids_banked']} | 0 | {index['counts']['design_ids_missing']} |",
        "",
        "## Spec-ID index (canon-cited requirement sources)",
        "",
        "Ground truth for filename ⇔ spec-ID: docx opening signature scraped from `word/document.xml`.",
        "",
        "| ID | Status | Filename | sha256 (12) | Sig source | Citations |",
        "|---|---|---|---|---|--:|",
    ]
    for row in sorted(index["spec_ids"], key=lambda r: r["id"]):
        fn = row.get("filename") or "—"
        sha = row.get("sha256")
        sha_short = (sha[:12] + "…") if sha else "—"
        sig_src = row.get("signature_source", "—")
        lines.append(f"| `{row['id']}` | {row['status']} | `{fn}` | `{sha_short}` | {sig_src} | {row['citation_count']} |")
    lines += ["", "## Missing spec IDs (zero-hit or unresolved)"]
    if index["missing"]:
        lines += ["", "| ID | Citations | Zero-hit receipt |", "|---|--:|---|"]
        for row in sorted(index["missing"], key=lambda r: r["id"]):
            lines.append(f"| `{row['id']}` | {row['citation_count']} | `{row['zero_hit_receipt']}` |")
    else:
        lines += ["", "_No genuinely-missing spec IDs (all cited IDs resolve to banked or banked-derived rows)._"]
    lines += ["", "## Design-ID index (prototypes + HTML design drops)",
              "",
              "| ID | Status | Filename | sha256 (12) | Kind | Size |",
              "|---|---|---|---|---|--:|"]
    for row in index["design_ids"]:
        fn = row.get("filename") or "—"
        sha = row.get("sha256")
        sha_short = (sha[:12] + "…") if sha else "—"
        kind = row.get("kind") or "—"
        size = row.get("size_bytes") or 0
        lines.append(f"| `{row['id']}` | {row['status']} | `{fn}` | `{sha_short}` | {kind} | {size:,} |")
    lines += ["", "---", "", "**Read STANDING_ORDERS.md first — permanent standing law.**", ""]
    return "\n".join(lines)


def main() -> None:
    index = build_index()
    out_json = NOTES / "spec_id_index.json"
    out_md = NOTES / "spec_id_index.md"
    out_json.write_text(json.dumps(index, indent=2), encoding="utf-8")
    out_md.write_text(write_markdown(index), encoding="utf-8")
    print(f"wrote {out_json} · {out_json.stat().st_size} bytes")
    print(f"wrote {out_md} · {out_md.stat().st_size} bytes")
    c = index["counts"]
    print(f"spec_ids: total={c['spec_ids_total']} banked={c['spec_ids_banked']} derived={c['spec_ids_banked_derived']} missing={c['spec_ids_missing']}")
    print(f"design_ids: total={c['design_ids_total']} banked={c['design_ids_banked']} missing={c['design_ids_missing']}")


if __name__ == "__main__":
    main()
