"""Revise a commission without losing the design.

  python scripts/revise.py <fixture_dir> <new_fixture_dir> <prev_build_dir> <new_build_dir> --set path=value [...]

Paths address content.json or brief.json, e.g.  content.options.O2.capex=28.5
or  brief.setting.printed=false.  The script:
1. copies the fixture, applies the changes, bumps content.version and every
   spec's content_ref;
2. checks each change against the verdict manifest: a change to a field a
   manifest entry names as its source is a STRIKE and lists the flips that
   must be re-verdicted (CIF flip detection, scoped to direction level);
3. rebuilds and diffs output hashes against the previous build;
4. reports: look preserved or not, which outputs changed, and any strike.
A strike does not block the build; it blocks *release* until the verdict is
re-confirmed, which is the coach's decision, not the builder's.
"""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build import build_once  # noqa: E402
from studio import dump, load  # noqa: E402


def parse_value(v):
    if v in ("true", "false"):
        return v == "true"
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return v


def set_path(d, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        d = d[k]
    old = d.get(keys[-1])
    d[keys[-1]] = value
    return old


def main():
    args = sys.argv[1:]
    sets = [a.split("=", 1) for a in args if a.startswith("--set")]
    sets = [(a[0].replace("--set ", "").replace("--set", "").strip() or a[0], a[1]) for a in sets]
    pos = [a for a in args if not a.startswith("--")]
    src, dst, prev_build, new_build = map(Path, pos[:4])
    changes = [(k, parse_value(v)) for k, v in (s.split("=", 1) for s in pos[4:])] if len(pos) > 4 else []
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    content, brief, verdict = load(dst / "content.json"), load(dst / "brief.json"), load(dst / "verdict.json")
    applied, strikes = [], []
    for path, value in changes:
        root, rest = path.split(".", 1)
        target = {"content": content, "brief": brief}[root]
        old = set_path(target, rest, value)
        applied.append({"path": path, "old": old, "new": value})
        for m in verdict["manifest"]:
            if root == "brief" and any(rest.startswith(s.strip().replace("brief.", "")) for s in m["source"].split(",")):
                strikes.append({"manifest": m["id"], "assumption": m["assumption"], "flips": m["flips"], "cause": path})
    content["version"] += 1
    dump(content, dst / "content.json")
    dump(brief, dst / "brief.json")
    cref = f"{content['content_id']}@{content['version']}"
    for spec in dst.glob("*.json"):
        d = load(spec)
        if "spec_type" in d:
            d["content_ref"] = cref
            dump(d, spec)
    log = lambda m: print(f"[revise] {m}")  # noqa: E731
    new = build_once(dst, new_build, log)
    old_manifest = json.loads((prev_build / "out" / "build-manifest.json").read_text())
    changed = [k for k in new["outputs_sha256"] if new["outputs_sha256"][k] != old_manifest["outputs_sha256"].get(k)]
    prev_plan = json.loads((prev_build / "resolved" / "deck.resolved.json").read_text())
    new_plan = json.loads((new_build / "resolved" / "deck.resolved.json").read_text())
    look_same = {k: prev_plan["look"][k] for k in ("palette_id", "type_pair_id", "cover_composition", "divider_treatment")} == \
                {k: new_plan["look"][k] for k in ("palette_id", "type_pair_id", "cover_composition", "divider_treatment")}
    report = {
        "changes": applied, "content_ref": cref, "outputs_changed": changed,
        "look_preserved": look_same, "strikes": strikes,
        "release": "blocked pending re-verdict" if strikes else "clear",
    }
    (new_build / "revision-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
