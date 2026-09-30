"""training-studio build: resolve → validate → run → report → freeze → qa. --prove builds twice and asserts the domain's contract."""
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import studio, validate as va, run as rn, report as rp, freeze as fz, qa, review as rvw, critique as cq  # noqa: E402


def build_once(fx, b, log, interrupt_after=None, partial_ruling_ref=None):
    fx, b = Path(fx), Path(b)
    if b.exists():
        shutil.rmtree(b)
    (b / "out").mkdir(parents=True)
    plan = studio.resolve(fx, b / "resolved")
    log(f"resolved · backend={plan['backend']} · comparison on {plan['comparison']['stratum']}")
    blk, rv = va.pre(fx)
    if blk:
        (b / "validate-report.json").write_text(json.dumps({"outcome": "blocked", "blockers": blk, "review": rv}, indent=2))
        raise SystemExit(f"blocked before run: {blk}")
    ct = cq.run(studio.load(fx / "objective.json"), studio.load(fx / "brief.json"))
    (b / "out" / "critique-table.json").write_text(json.dumps(ct, indent=2, sort_keys=True) + "\n")
    (b / "out" / "critique.md").write_text(cq.to_md(ct))
    if ct["blockers"]:
        (b / "validate-report.json").write_text(json.dumps({"outcome": "blocked", "blockers": ct["blockers"], "review": rv}, indent=2))
        raise SystemExit(f"blocked at objective critique: {ct['blockers']}")
    log(f"critique: {len(ct['rows'])} rows, {sum(1 for r in ct['rows'] if r['severity']=='escalate')} to escalate")
    rec = rn.run(plan, b / "out", interrupt_after=interrupt_after)
    rec["critique_ref"] = "critique-table.json"
    if rec["status"] == "interrupted" and partial_ruling_ref:
        rec["interruption"]["partial_ruling_ref"] = partial_ruling_ref
        rn.dump(rec, b / "out" / "run-record.json")
    blk2, rv2 = va.post(b / "out" / "run-record.json", b / "resolved" / "run_plan.resolved.json")
    (b / "validate-report.json").write_text(json.dumps({"outcome": "blocked" if blk2 else ("finding-not-blocking" if rv + rv2 else "pass"), "blockers": blk2, "review": rv + rv2}, indent=2) + "\n")
    if blk2:
        raise SystemExit(f"blocked after run: {blk2}")
    (b / "out" / "technical-report.md").write_text(rp.render(plan, rec))
    rvw.render(plan, rec, b / "out" / "review.html")
    (b / "out" / "moac-pack-request.json").write_text(json.dumps(rec["moac_pack_request"], indent=2, sort_keys=True) + "\n")
    m = fz.freeze(b)
    log("frozen: " + ", ".join(f"{k}={v[:10]}" for k, v in m["outputs_sha256"].items()))
    if qa.main(b) != 0:
        raise SystemExit("QA blockers")
    return m


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prove = "--prove" in sys.argv
    opt = {a.split("=")[0]: a.split("=", 1)[1] for a in sys.argv if a.startswith("--") and "=" in a}
    ia, pr = opt.get("--interrupt-after"), opt.get("--partial-ruling")
    fx, b = Path(args[0]), Path(args[1])
    log = lambda m: print(f"[build] {m}")  # noqa: E731
    if not prove:
        build_once(fx, b, log, interrupt_after=ia, partial_ruling_ref=pr)
        return
    a, c = build_once(fx, b / "a", log), build_once(fx, b / "b", log)
    plan = json.loads((b / "a" / "resolved" / "run_plan.resolved.json").read_text())
    if plan["backend"] == "stub":
        diff = {k for k in a["outputs_sha256"] if a["outputs_sha256"][k] != c["outputs_sha256"].get(k)}
        if diff:
            print("[prove] NOT REPRODUCIBLE:", sorted(diff))
            raise SystemExit(2)
        print(f"[prove] stub backend: content-identical across two builds, {len(a['outputs_sha256'])} outputs")
    else:
        ra = json.loads((b / "a" / "out" / "run-record.json").read_text())
        rb = json.loads((b / "b" / "out" / "run-record.json").read_text())
        tol = plan["reproducibility"]["tolerance_accuracy"]
        worst = max(abs(pa["accuracy"] - pb["accuracy"]) for s in ra["stages"]["calibration"]["per_stratum"] for pa, pb in zip(ra["stages"]["calibration"]["per_stratum"][s]["points"], rb["stages"]["calibration"]["per_stratum"][s]["points"]))
        print(f"[prove] real backend: worst accuracy delta {worst:.4f} vs tolerance {tol}: {'within' if worst <= tol else 'OUTSIDE'}")
        if worst > tol:
            raise SystemExit(2)


if __name__ == "__main__":
    main()
