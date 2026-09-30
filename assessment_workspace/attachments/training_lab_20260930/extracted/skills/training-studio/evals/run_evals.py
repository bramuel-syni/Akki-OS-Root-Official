"""Execute the evals with assertions. Each eval is a shell-level scenario against the fixtures; pass/fail is mechanical."""
import json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
W = Path("/tmp/training-studio-evals")


def sh(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env={**os.environ, **(env or {})})
    return r.returncode, r.stdout + r.stderr


def jl(p):
    return json.loads(Path(p).read_text())


def e1():
    rc, out = sh([PY, "scripts/build.py", "fixtures/asr-register-adapter", str(W / "e1"), "--prove"])
    rep = (W / "e1/a/out/technical-report.md").read_text()
    return rc == 0 and "content-identical" in out and rep.startswith("# ") and "STUB RUN" in rep and "Verdict: pending" in rep


def e2():
    rc, _ = sh([PY, "scripts/revise.py", "fixtures/asr-register-adapter", str(W / "e2/fx"), str(W / "e1/a"), str(W / "e2/b"), "objective.cost.gpu_hour_gbp=2.9"])
    r = jl(W / "e2/b/revision-report.json")
    return r["built"] and r["release"] == "clear" and not r["strikes"] and "run-record.json" in r["outputs_changed"]


def e3():
    sh([PY, "scripts/revise.py", "fixtures/asr-register-adapter", str(W / "e3/fx"), str(W / "e1/a"), str(W / "e3/b"), "brief.constraints.budget_cap_gbp=900"])
    r = jl(W / "e3/b/revision-report.json")
    return r["release"] == "blocked pending re-verdict" and any(s["manifest"] == "M2" for s in r["strikes"])


def e4():
    rec = jl(W / "e1/a/out/run-record.json")
    blob = json.dumps(rec)
    return '"adopted": true' not in blob and "pending Owner ruling" in rec["stages"]["comparison"]["owner_verdict"] and rec["stages"]["comparison"]["compute_is_gating"] is False


def e5():
    sh([PY, "scripts/revise.py", "fixtures/asr-register-adapter", str(W / "e5/fx"), str(W / "e1/a"), str(W / "e5/b"), "objective.materials.M03.lawful_basis="])
    r = jl(W / "e5/b/revision-report.json")
    return r["built"] is False and not (W / "e5/b/out/run-record.json").exists()


def e6():
    fx = W / "e6/fx"
    if fx.exists():
        shutil.rmtree(fx)
    shutil.copytree(ROOT / "fixtures/asr-register-adapter", fx)
    p = jl(fx / "plan.json"); p["backend"] = "real"; (fx / "plan.json").write_text(json.dumps(p))
    rc1, out1 = sh([PY, "scripts/build.py", str(fx), str(W / "e6/b1")], env={"AKKI_EXECUTION_MODE": ""})
    rc2, out2 = sh([PY, "scripts/build.py", str(fx), str(W / "e6/b2")], env={"AKKI_EXECUTION_MODE": "cuda"})
    return rc1 != 0 and "A17.9" in out1 and rc2 != 0 and "A17.12" in out2 and not (W / "e6/b2/out/run-record.json").exists()


def e7():
    rc1, out1 = sh([PY, "scripts/build.py", "fixtures/asr-register-adapter", str(W / "e7/b1"), "--interrupt-after=ST2"])
    rc2, _ = sh([PY, "scripts/build.py", "fixtures/asr-register-adapter", str(W / "e7/b2"), "--interrupt-after=ST2", "--partial-ruling=OO-partial"])
    rep = (W / "e7/b2/out/technical-report.md").read_text()
    rec = jl(W / "e7/b2/out/run-record.json")
    return rc1 != 0 and "partial_ruling_ref" in out1 and rc2 == 0 and "INTERRUPTED" in rep and rep.count("not evaluated") >= 2 and rec["status"] == "interrupted"


def e8():
    sh([PY, "scripts/revise.py", "fixtures/asr-register-adapter", str(W / "e8/fx"), str(W / "e1/a"), str(W / "e8/b"), "objective.materials.M04.examples=9800"])
    r = jl(W / "e8/b/revision-report.json")
    return r["built"] is False  # datasheet count must match the per-example index


def e9():
    rc, out = sh([PY, "scripts/build.py", "fixtures/dairy-record-classifier", str(W / "e9"), "--prove"])
    rec = jl(W / "e9/a/out/run-record.json")
    return rc == 0 and rec["stages"]["comparison"]["stratum"] == "ST3" and "ST4" in rec["stages"]["calibration"]["per_stratum"]


def _fx(name, mutate):
    fx = W / name / "fx"
    if fx.exists():
        shutil.rmtree(fx)
    shutil.copytree(ROOT / "fixtures/asr-register-adapter", fx)
    o = jl(fx / "objective.json"); b = jl(fx / "brief.json"); mutate(o, b)
    (fx / "objective.json").write_text(json.dumps(o)); (fx / "brief.json").write_text(json.dumps(b)); return fx


def e10():
    def m(o, b): o["population"]["strata"]["ST1"]["test_n"] = 100
    fx = _fx("e10", m); rc, out = sh([PY, "scripts/build.py", str(fx), str(W / "e10/b")])
    return rc != 0 and "unverifiable" in out and "ST1" in out and not (W / "e10/b/out/run-record.json").exists()


def e11():
    rec = jl(W / "e1/a/out/run-record.json"); d = rec["stages"]["diagnosis"]
    return d["comparison_design"]["lever_id"].startswith("aug.") and d["per_stratum"]["ST3"]["cause"] == "label-noise-limited" and "confident" in d["per_stratum"]["ST3"]["first_lever"].lower()


def e12():
    def m(o, b): o["production"]["owner_seat"] = ""
    fx = _fx("e12", m); rc, out = sh([PY, "scripts/build.py", str(fx), str(W / "e12/b")]); ct = jl(W / "e12/b/out/critique-table.json")
    return rc == 0 and any(r["lens"] == "industry" and r["severity"] == "escalate" and "owner" in r["objection"] for r in ct["rows"])


def e13():
    def m(o, b): b["constraints"]["budget_cap_gbp"] = 50
    fx = _fx("e13", m); rc, out = sh([PY, "scripts/build.py", str(fx), str(W / "e13/b")]); ct = jl(W / "e13/b/out/critique-table.json")
    rec = jl(W / "e13/b/out/run-record.json") if (W / "e13/b/out/run-record.json").exists() else {}
    return any(r["lens"] == "entrepreneur" and r["severity"] == "escalate" and "OVER" in r["objection"] for r in ct["rows"]) and rec.get("stages", {}).get("quote", {}).get("within_budget") is False and rec["stages"]["quote"]["over_cap_action"]


def e14():
    rc, out = sh([PY, "scripts/postmortem.py", str(W / "e1/a/out/run-record.json"), "evals/data/actuals.asr.json", str(W / "e14.json")]); r = jl(W / "e14.json")
    return rc == 0 and all(k in r["hit_rate"] for k in ("professor", "researcher", "industry", "entrepreneur")) and r["per_lens"]["researcher"][0]["was_detectable"] is False


def main():
    if W.exists():
        shutil.rmtree(W)
    W.mkdir(parents=True)
    evals = jl(ROOT / "evals/evals.json")["evals"]
    fns = {1: e1, 2: e2, 3: e3, 4: e4, 5: e5, 6: e6, 7: e7, 8: e8, 9: e9, 10: e10, 11: e11, 12: e12, 13: e13, 14: e14}
    results = []
    for ev in evals:
        fn = fns.get(ev["id"])
        try:
            ok = bool(fn()) if fn else None
        except Exception as ex:  # noqa: BLE001
            ok, ev["error"] = False, repr(ex)[:200]
        results.append({"id": ev["id"], "mode": ev.get("mode", ""), "pass": ok})
        print(f"eval {ev['id']:>2} [{ev.get('mode','')[:22]:<22}] {'PASS' if ok else 'FAIL' if ok is False else 'n/a'}")
    (ROOT / "evals/last-run.json").write_text(json.dumps(results, indent=2) + "\n")
    sys.exit(0 if all(r["pass"] for r in results if r["pass"] is not None) else 1)


if __name__ == "__main__":
    main()
