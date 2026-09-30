import json, os, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; PY = sys.executable; W = Path("/tmp/surface-studio-evals")
def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT); return r.returncode, r.stdout + r.stderr
def jl(p): return json.loads(Path(p).read_text())
def rev(fx, name, *changes):
    sh([PY, "scripts/revise.py", f"fixtures/{fx}", str(W / name / "fx"), str(W / "e1/a"), str(W / name / "b"), *changes]); return jl(W / name / "b/revision-report.json")
def e1():
    rc, out = sh([PY, "scripts/build.py", "fixtures/board360-rms", str(W / "e1"), "--prove"]); r = jl(W / "e1/a/out/content-record.json")
    return rc == 0 and "byte-identical" in out and [b["move"] for b in r["blocks"]] == ["interpret", "trigger", "report", "trigger", "silence"] and r["blocks"][1]["kind"] == "decision_pending"
def e2():
    r = rev("board360-rms", "e2", "page-state.facts.F002.value=10"); return r["built"] and r["cache_rekeyed"] and not r["strikes"] and r["release"] == "clear"
def e3():
    r = rev("board360-rms", "e3", "brief.audience.role=exco"); return r["release"] == "blocked pending re-verdict" and any(s["manifest"] == "M1" for s in r["strikes"])
def e4():
    fx = W / "e4/fx"; shutil.rmtree(fx, ignore_errors=True); shutil.copytree(ROOT / "fixtures/board360-rms", fx)
    s = jl(fx / "spec.json"); s["blocks"][1]["text"] += " The board should approve this."; (fx / "spec.json").write_text(json.dumps(s))
    rc, out = sh([PY, "scripts/build.py", str(fx), str(W / "e4/b")]); return rc != 0 and "directive" in out
def e5():
    fx = W / "e5/fx"; shutil.rmtree(fx, ignore_errors=True); shutil.copytree(ROOT / "fixtures/board360-rms", fx)
    ps = jl(fx / "page-state.json"); ps["receipts"]["R06"].pop("causal"); (fx / "page-state.json").write_text(json.dumps(ps))
    rc, out = sh([PY, "scripts/build.py", str(fx), str(W / "e5/b")]); return rc != 0 and "causal" in out
def e6():
    r = rev("board360-rms", "e6", "page-state.source=stub"); rec = jl(W / "e6/b/out/content-record.json")
    return r["built"] and r["release"].startswith("not servable") and rec["servable"] is False and "STUB PAGE STATE" in (W / "e6/b/out/preview.html").read_text()
def e7():
    r = rev("board360-rms", "e7", "page-state.unavailable_sources=[R02]"); rec = jl(W / "e7/b/out/content-record.json")
    b1 = rec["blocks"][0]; return r["built"] and b1["degraded"] and "[not available]" in b1["text"] and "62%" not in b1["text"] and "R02" in b1["text"]
def e8():
    r = rev("board360-rms", "e8", "page-state.aggregate_only_check.individual_fields_present=true"); return r["built"] is False
def e9():
    rc, out = sh([PY, "scripts/build.py", "fixtures/spend-requests-secops", str(W / "e9"), "--prove"]); r = jl(W / "e9/a/out/content-record.json")
    return rc == 0 and r["blocks"][0]["move"] == "trigger" and {b.get("kind") for b in r["blocks"][:3]} == {"decision_pending", "anomaly"} and r["voice"] == "operational"
def main():
    shutil.rmtree(W, ignore_errors=True); W.mkdir(parents=True)
    fns = {1: e1, 2: e2, 3: e3, 4: e4, 5: e5, 6: e6, 7: e7, 8: e8, 9: e9}; res = []
    for ev in jl(ROOT / "evals/evals.json")["evals"]:
        try: ok = bool(fns[ev["id"]]())
        except Exception as ex: ok = False; print("  ", repr(ex)[:160])
        res.append(ok); print(f"eval {ev['id']:>2} [{ev['mode'][:24]:<24}] {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if all(res) else 1)
if __name__ == "__main__": main()
