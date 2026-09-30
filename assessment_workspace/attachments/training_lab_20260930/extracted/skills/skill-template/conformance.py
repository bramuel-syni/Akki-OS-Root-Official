"""Conformance check for an Akki skill package against template contract v1.0. Read-only; reports."""
import json, re, sys
from pathlib import Path

VERBS = ["resolve", "validate", "freeze", "qa", "build", "revise"]
PRODUCE = ["render", "run", "assemble", "produce"]
FAILURE_MODES = ["missing evidence", "stub", "interrupted", "stale", "authority"]


def check(pkg):
    pkg = Path(pkg)
    f = []
    ok = lambda c, m: (None if c else f.append(m))  # noqa: E731
    ok((pkg / "SKILL.md").exists(), "SKILL.md missing")
    t = pkg / "template.json"
    ok(t.exists(), "template.json missing")
    if t.exists():
        d = json.loads(t.read_text())
        ok(d.get("template") == "akki-skill" and d.get("version") == "1.0", "template.json must declare akki-skill 1.0")
        ok(bool(d.get("skill")) and bool(d.get("domain")), "template.json needs skill and domain")
    decl = json.loads(t.read_text()) if t.exists() else {}
    for dname in ["references", "schemas", "scripts", "fixtures", "evals"]:
        ok((pkg / dname).is_dir(), f"{dname}/ missing")
    pdirs = decl.get("policy_dirs", ["policies"])
    ok(all((pkg / d).is_dir() for d in pdirs), f"policy dirs missing: {pdirs}")
    scripts = " ".join(p.name for p in (pkg / "scripts").glob("*.py")) if (pkg / "scripts").is_dir() else ""
    aliases = decl.get("scripts", {})
    for v in VERBS:
        ok(v in scripts or aliases.get(v, "") in scripts, f"scripts/: no {v} script")
    ok(any(pv in scripts for pv in PRODUCE), "scripts/: no produce-class script (render|run|assemble)")
    for r in ["discretion.md", "reproducibility.md"]:
        ok((pkg / "references" / r).exists(), f"references/{r} missing")
    vs = pkg / "schemas" / "verdict.schema.json"
    ok(vs.exists(), "schemas/verdict.schema.json missing")
    if vs.exists():
        s = vs.read_text()
        for k in ["candidates", "manifest", "confirmed_by", "adopt", "defer"]:
            ok(k in s, f"verdict schema lacks {k}")
    for s in (pkg / "schemas").glob("*.json") if (pkg / "schemas").is_dir() else []:
        ok('"decision"' not in s.read_text(), f"{s.name}: schemas must not define a decision output")
    ev = pkg / "evals" / "evals.json"
    ok(ev.exists(), "evals/evals.json missing")
    if ev.exists():
        e = json.loads(ev.read_text()).get("evals", [])
        ok(len(e) >= 4, f"evals: {len(e)} < 4")
        blob = json.dumps(e).lower()
        for fm in FAILURE_MODES:
            ok(fm in blob, f"evals: no failure-mode eval for '{fm}'")
    fx = list((pkg / "fixtures").iterdir()) if (pkg / "fixtures").is_dir() else []
    ok(len(fx) >= 1, "fixtures/: no commission")
    for c in fx:
        for need in ["brief.json", "verdict.json"]:
            ok((c / need).exists(), f"fixtures/{c.name}: {need} missing")
    src = "\n".join(p.read_text() for p in (pkg / "scripts").glob("*.py")) if (pkg / "scripts").is_dir() else ""
    ok('"stub"' in src and ("backend" in src or "source" in src), "scripts never record a stub-honesty field (backend real|stub for run-class skills, source live|snapshot|stub for read-class skills)")
    ev_runner = pkg / "evals" / "run_evals.py"
    ok(ev_runner.exists() or decl.get("evals_runner") == "manual", "evals/run_evals.py missing (mechanical assertions) — or declare evals_runner: manual in template.json")
    ok(not re.search(r"from (doc_studio|doc-studio|training_studio|skill_template)", src), "cross-skill import detected")
    return f


if __name__ == "__main__":
    findings = check(sys.argv[1])
    status = "CONFORMS" if not findings else "NONCONFORMING"
    print(json.dumps({"package": sys.argv[1], "template": "akki-skill 1.0", "status": status, "findings": findings}, indent=2))
    sys.exit(1 if findings else 0)
