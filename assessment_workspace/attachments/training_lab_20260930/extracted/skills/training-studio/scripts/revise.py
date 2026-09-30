"""training-studio revise: apply changes to objective or brief, bump the objective version, detect manifest strikes, rebuild, report.
  python scripts/revise.py <fixture> <new_fixture> <prev_build> <new_build> path=value [...]
A strike (a change to a brief or objective field a manifest entry names as its source) blocks release pending re-verdict."""
import json, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import build_once  # noqa: E402


def parse(v):
    if v in ("true", "false"):
        return v == "true"
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return v


def setp(d, path, value):
    ks = path.split(".")
    for k in ks[:-1]:
        d = d[k]
    old = d.get(ks[-1])
    d[ks[-1]] = value
    return old


def main():
    src, dst, prev, new = map(Path, sys.argv[1:5])
    changes = [(k, parse(v)) for k, v in (a.split("=", 1) for a in sys.argv[5:])]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    obj, brief, verdict = (json.loads((dst / f).read_text()) for f in ("objective.json", "brief.json", "verdict.json"))
    applied, strikes = [], []
    for path, value in changes:
        root, rest = path.split(".", 1)
        target = {"objective": obj, "brief": brief}[root]
        old = setp(target, rest, value)
        applied.append({"path": path, "old": old, "new": value})
        for m in verdict["manifest"]:
            for src_field in m["source"].split(","):
                sf = src_field.strip()
                if not sf.startswith(root + "."):
                    continue
                pat = re.escape(sf[len(root) + 1:]).replace(r"\[\*\]", r"\.[^.]+") + r"(\..*)?"
                if re.fullmatch(pat, rest):
                    strikes.append({"manifest": m["id"], "assumption": m["assumption"], "flips": m["flips"], "cause": path})
    obj["version"] += 1
    oref = f"{obj['objective_id']}@{obj['version']}"
    brief["objective_ref"] = oref
    plan = json.loads((dst / "plan.json").read_text())
    plan["objective_ref"] = oref
    for name, d in (("objective.json", obj), ("brief.json", brief), ("plan.json", plan)):
        (dst / name).write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    log = lambda m: print(f"[revise] {m}")  # noqa: E731
    try:
        manifest = build_once(dst, new, log)
        prev_m = json.loads((prev / "out" / "build-manifest.json").read_text())
        changed = [k for k in manifest["outputs_sha256"] if manifest["outputs_sha256"][k] != prev_m["outputs_sha256"].get(k)]
        built = True
    except SystemExit as e:
        changed, built = [], False
        log(f"build stopped: {e}")
    rep = {"changes": applied, "objective_ref": oref, "built": built, "outputs_changed": changed, "strikes": strikes,
           "release": "blocked pending re-verdict" if strikes else ("clear" if built else "blocked by validation")}
    new.mkdir(parents=True, exist_ok=True)
    (new / "revision-report.json").write_text(json.dumps(rep, indent=2) + "\n")
    print(json.dumps({k: rep[k] for k in ("objective_ref", "built", "outputs_changed", "strikes", "release")}, indent=2))


if __name__ == "__main__":
    main()
