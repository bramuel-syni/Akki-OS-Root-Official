"""Build a commission end to end.

  python scripts/build.py <fixture_dir> <build_dir> [--prove] [--repair N]

Steps: resolve → validate (blockers stop the build) → render each format →
recalc workbook → freeze (normalize + hash + manifest) → QA (blockers stop
release). --prove builds twice into build_dir/a and build_dir/b and fails if
any output hash differs: that is the determinism contract, tested, not assumed.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from studio import load, resolve  # noqa: E402
import freeze as fz  # noqa: E402
import qa  # noqa: E402
import validate as va  # noqa: E402

SKILLS = Path("/mnt/skills/public")


def build_once(fixture_dir, build_dir, log):
    fixture_dir, build_dir = Path(fixture_dir), Path(build_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    resolved, out = build_dir / "resolved", build_dir / "out"
    out.mkdir(parents=True)
    plans = {}
    for spec in sorted(fixture_dir.glob("*.json")):
        d = load(spec)
        if "spec_type" in d:
            _, plan = resolve(spec, fixture_dir, resolved)
            plans[d["spec_type"]] = plan
    log(f"resolved {sorted(plans)}; look {plans[next(iter(plans))]['look']['palette_id']}/{plans[next(iter(plans))]['look']['type_pair_id']}")
    if va.main(fixture_dir, resolved) != 0:
        raise SystemExit("validation blockers; build stopped")
    stamp = next(iter(plans.values()))["build_stamp"]
    base = next(iter(plans.values()))["content_ref"].split("@")[0]
    if "deck" in plans:
        from render_pptx import Deck
        from render_html import render as render_html
        Deck(plans["deck"]).render(out / f"{base}.pptx")
        render_html(plans["deck"], out / f"{base}-review.html")
    if "paper" in plans:
        from render_docx import Paper
        Paper(plans["paper"]).render(out / f"{base}.docx")
    recalc_json = None
    if "workbook" in plans:
        from render_xlsx import render as render_xlsx
        xp = out / f"{base}.xlsx"
        render_xlsx(plans["workbook"], xp, fixture_dir / "content.json")
        recalc_json = build_dir / "recalc.json"
        if shutil.which("soffice"):
            r = subprocess.run([sys.executable, str(SKILLS / "xlsx/scripts/recalc.py"), str(xp)], capture_output=True, text=True)
            recalc_json.write_text(r.stdout)
            log(f"recalc: {json.loads(r.stdout).get('status')} · backend real (libreoffice)")
        else:
            recalc_json.write_text(json.dumps({"status": "unavailable", "backend": "stub", "note": "no LibreOffice; formulas unevaluated; workbook not releasable"}))
            log("recalc: backend stub (LibreOffice unavailable) · workbook not releasable")
    manifest = fz.freeze(out, resolved, stamp)
    log("frozen: " + ", ".join(f"{k}={v[:12]}" for k, v in manifest["outputs_sha256"].items()))
    if qa.main(out, recalc_json) != 0:
        raise SystemExit("QA blockers; not releasable")
    return manifest


def main():
    args = sys.argv[1:]
    prove = "--prove" in args
    args = [a for a in args if not a.startswith("--")]
    fixture_dir, build_dir = Path(args[0]), Path(args[1])
    log = lambda m: print(f"[build] {m}")  # noqa: E731
    if not prove:
        build_once(fixture_dir, build_dir, log)
        return
    a = build_once(fixture_dir, build_dir / "a", log)
    b = build_once(fixture_dir, build_dir / "b", log)
    diff = {k: (a["outputs_sha256"][k][:12], b["outputs_sha256"].get(k, "")[:12]) for k in a["outputs_sha256"] if a["outputs_sha256"][k] != b["outputs_sha256"].get(k)}
    if diff:
        print("[prove] NOT REPRODUCIBLE:", json.dumps(diff, indent=2))
        raise SystemExit(2)
    print(f"[prove] byte-identical across two builds: {len(a['outputs_sha256'])} outputs")


if __name__ == "__main__":
    main()
