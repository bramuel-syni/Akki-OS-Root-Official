"""training-studio qa: mechanical gates on the produced outputs. Outcome: pass | finding-not-blocking | blocked."""
import json, sys
from pathlib import Path


def main(build_dir):
    b = Path(build_dir)
    rec = json.loads((b / "out" / "run-record.json").read_text())
    rep = (b / "out" / "technical-report.md").read_text()
    blockers, review = [], []
    if rec["backend"] == "stub" and "STUB RUN" not in rep:
        blockers.append("report does not declare the stub run")
    for s in list(rec["stages"]["calibration"]["per_stratum"]) + rec["stages"]["calibration"].get("strata_missing", []):
        if f"| {s} |" not in rep:
            blockers.append(f"report omits stratum {s}")
    if rec["status"] == "interrupted" and "INTERRUPTED" not in rep:
        blockers.append("report does not declare the interruption")
    for m in __import__("re").finditer(r"Verdict:\s*([^\n*]*)", rep):
        if not m.group(1).strip().lower().startswith("pending"):
            blockers.append(f"report states a verdict: '{m.group(1).strip()[:40]}'")
    if "arms" in rec["stages"]["comparison"] and "Verdict: pending" not in rep:
        blockers.append("comparison reported without the pending-Owner verdict line")
    for sec in ["Objective critique", "Diagnosis per stratum", "Operational plan", "Value case", "Limitations (four lenses)", "Problem and objective", "Data statement", "Baseline record", "Method", "Setup and reproducibility", "Results on held-out material", "Ablations", "Limitations", "Negative results"]:
        if sec not in rep:
            blockers.append(f"report skeleton missing '{sec}' (WPW-8)")
    if "Receipt R" not in rep:
        blockers.append("no receipt lines in report (WPW-9)")
    q = rec["stages"]["quote"]
    if q.get("recommended_examples") and q["recommended_examples"] > sum(x["available_examples"] for x in rec["stages"]["calibration"]["per_stratum"].values()):
        blockers.append("quote recommends more examples than exist")
    for f in ("training-manifest.jsonl", "notebook.jsonl", "review.html", "critique-table.json", "critique.md"):
        if rec["status"] != "refused" and not (b / "out" / f).exists():
            blockers.append(f"{f} missing from outputs")
    if "training-manifest.jsonl" in [p.name for p in (b / "out").iterdir()] and "training-manifest.jsonl" not in rep:
        blockers.append("report does not reference the per-example manifest")
    review.append("Does the milestone list name an owner for every done-condition the objective owner will be asked to agree?")
    out = {"outcome": "blocked" if blockers else "finding-not-blocking", "blockers": blockers, "review": review}
    (b / "out" / "qa-report.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
