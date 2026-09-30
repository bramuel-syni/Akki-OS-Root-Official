"""surface-studio revise: apply page-state or brief changes, bump the page-state version, detect manifest strikes, rebuild.
  python scripts/revise.py <fixture> <new_fixture> <prev_build> <new_build> path=value [...]
A page-state change re-keys the cache and rebuilds; a brief change that a manifest entry names is a strike."""
import json, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import build_once  # noqa: E402


def parse(v):
    if v in ("true", "false"):
        return v == "true"
    if v.startswith("[") and v.endswith("]"):
        return [x.strip() for x in v[1:-1].split(",") if x.strip()]
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return v


def setp(d, path, value):
    ks = path.split(".")
    for k in ks[:-1]:
        d = d[k]
    old = d.get(ks[-1]); d[ks[-1]] = value
    return old


def main():
    src, dst, prev, new = map(Path, sys.argv[1:5])
    changes = [(k, parse(v)) for k, v in (a.split("=", 1) for a in sys.argv[5:])]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    ps, brief, verdict, spec = (json.loads((dst / f).read_text()) for f in ("page-state.json", "brief.json", "verdict.json", "spec.json"))
    applied, strikes = [], []
    for path, value in changes:
        root, rest = path.split(".", 1)
        target = {"page-state": ps, "brief": brief}[root]
        applied.append({"path": path, "old": setp(target, rest, value), "new": value})
        for m in verdict["manifest"]:
            for sf in (x.strip() for x in m["source"].split(",")):
                if not sf.startswith(root + "."):
                    continue
                pat = re.escape(sf[len(root) + 1:]).replace(r"\[\*\]", r"\.[^.]+") + r"(\..*)?"
                if re.fullmatch(pat, rest):
                    strikes.append({"manifest": m["id"], "assumption": m["assumption"], "flips": m["flips"], "cause": path})
    ps["version"] += 1
    pref = f"{ps['page_state_id']}@{ps['version']}"
    brief["page_state_ref"] = spec["page_state_ref"] = pref
    for name, d in (("page-state.json", ps), ("brief.json", brief), ("spec.json", spec)):
        (dst / name).write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    log = lambda m: print(f"[revise] {m}")  # noqa: E731
    try:
        m = build_once(dst, new, log)
        pm = json.loads((prev / "out" / "build-manifest.json").read_text())
        changed = [k for k in m["outputs_sha256"] if m["outputs_sha256"][k] != pm["outputs_sha256"].get(k)]
        built, rekeyed = True, m["cache_key"] != pm["cache_key"]
        stub = json.loads((new / "out" / "content-record.json").read_text()).get("stub", False)
    except SystemExit as e:
        changed, built, rekeyed, stub = [], False, None, False
        log(f"build stopped: {e}")
    rep = {"changes": applied, "page_state_ref": pref, "built": built, "cache_rekeyed": rekeyed, "outputs_changed": changed, "strikes": strikes,
           "release": "blocked pending re-verdict" if strikes else ("not servable (stub page state)" if built and stub else "clear" if built else "blocked by validation")}
    new.mkdir(parents=True, exist_ok=True)
    (new / "revision-report.json").write_text(json.dumps(rep, indent=2) + "\n")
    print(json.dumps({k: rep[k] for k in ("page_state_ref", "built", "cache_rekeyed", "strikes", "release")}, indent=2))


if __name__ == "__main__":
    main()
