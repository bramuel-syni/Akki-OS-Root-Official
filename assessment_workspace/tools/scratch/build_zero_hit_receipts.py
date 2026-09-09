#!/usr/bin/env python3
"""Generate zero-hit receipts for spec-IDs on the missing list.

Owner directive 2026-09-08T~06:15Z: "any doc cited by spec-ID anywhere in canon
must either resolve to a banked file or appear on the missing list with a
zero-hit grep receipt."

Emits one receipt per missing spec-ID under
phase0/tracking_defect_20260908/grep_<spec_id>.txt with:
  1. All citation paths (evidence the ID is genuinely cited)
  2. Docx-body opening-signature scan result (zero-hits for that ID)
  3. Explicit "not banked" statement
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/app/assessment_workspace")
INDEX_JSON = ROOT / "notes" / "spec_id_index.json"
RECEIPT_DIR = ROOT / "phase0" / "tracking_defect_20260908"
SIG_RE_TEMPLATE = "{spec_id} \xe2\x80\x94 (?:Draft|Ratified|Ruled)"


def scrape_opening_signature_scan(spec_id: str) -> list[str]:
    """Return list of docx paths whose opening body contains the signature."""
    hits = []
    for docx in list(ROOT.rglob("canon/**/*.docx")) + list(ROOT.rglob("fixtures/**/*.docx")):
        try:
            out = subprocess.run(
                ["unzip", "-p", str(docx), "word/document.xml"],
                capture_output=True, check=True, timeout=10,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            continue
        pattern = re.compile(
            rf"{spec_id} \xe2\x80\x94 (?:Draft|Ratified|Ruled)".encode()
        )
        if pattern.search(out.stdout):
            hits.append(str(docx.relative_to(ROOT)))
    return hits


def main() -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    index = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    for row in index["missing"]:
        spec_id = row["id"]
        sig_hits = scrape_opening_signature_scan(spec_id)
        receipt_path = RECEIPT_DIR / f"grep_{spec_id}.txt"
        lines = [
            f"# Zero-hit grep receipt for spec-ID: {spec_id}",
            "",
            f"Generated: {index['generated_at']}",
            "Owner directive: 2026-09-08T~06:15Z (STEP 1 pipeline fix)",
            "Scope: canon/**/*.docx + fixtures/**/*.docx word/document.xml body scan",
            "",
            f"## Opening-signature scan for `{spec_id} — Draft|Ratified|Ruled`",
            "",
        ]
        if sig_hits:
            lines.append(f"HITS: {len(sig_hits)}")
            for h in sig_hits:
                lines.append(f"  - {h}")
        else:
            lines.append("HITS: 0")
            lines.append("")
            lines.append("Verdict: no docx opens with this spec-ID signature.")
            lines.append("The spec-ID is CITED in canon/notes but no standalone spec document is banked.")
        lines += [
            "",
            f"## Citation paths ({row['citation_count']} total)",
            "",
        ]
        for c in row["citation_paths"]:
            lines.append(f"  - {c}")
        lines += [
            "",
            "## Status",
            "",
            "MISSING · not banked · listed in notes/spec_id_index.json under `missing[]`.",
            "Requires owner ruling: either (a) drop the standalone spec doc in a future artifact,",
            "or (b) rule the ID BANKED-DERIVED against a named derivation source (like ROC-1).",
            "",
        ]
        receipt_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {receipt_path} · {receipt_path.stat().st_size} bytes · sig_hits={len(sig_hits)}")


if __name__ == "__main__":
    main()
