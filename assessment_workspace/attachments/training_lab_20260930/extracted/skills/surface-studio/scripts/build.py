"""surface-studio build: resolve → validate → assemble → freeze → qa; --prove builds twice and asserts byte-identical outputs."""
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import studio, validate as va, assemble as asm, freeze as fz, qa  # noqa: E402


def build_once(fx, b, log):
    fx, b = Path(fx), Path(b)
    if b.exists():
        shutil.rmtree(b)
    (b / "out").mkdir(parents=True)
    plan = studio.resolve(fx, b / "resolved")
    log(f"resolved {plan['page']} for {plan['role']} · {len(plan['blocks'])} blocks")
    blk, rv = va.pre(fx)
    b2, r2 = va.post(b / "resolved" / "content_plan.resolved.json")
    blk, rv = blk + b2, rv + r2
    (b / "validate-report.json").write_text(json.dumps({"outcome": "blocked" if blk else ("finding-not-blocking" if rv else "pass"), "blockers": blk, "review": rv}, indent=2) + "\n")
    if blk:
        raise SystemExit(f"blocked: {blk}")
    rec = asm.content_record(plan)
    (b / "out" / "content-record.json").write_text(json.dumps(rec, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    (b / "out" / "preview.html").write_text(asm.preview(plan, rec), encoding="utf-8")
    m = fz.freeze(b)
    log("frozen: " + ", ".join(f"{k}={v[:10]}" for k, v in m["outputs_sha256"].items()))
    if qa.main(b) != 0:
        raise SystemExit("QA blockers")
    return m


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fx, b = Path(args[0]), Path(args[1])
    log = lambda m: print(f"[build] {m}")  # noqa: E731
    if "--prove" not in sys.argv:
        build_once(fx, b, log)
        return
    a, c = build_once(fx, b / "a", log), build_once(fx, b / "b", log)
    diff = {k for k in a["outputs_sha256"] if a["outputs_sha256"][k] != c["outputs_sha256"].get(k)}
    if diff:
        print("[prove] NOT REPRODUCIBLE:", sorted(diff)); raise SystemExit(2)
    print(f"[prove] byte-identical across two builds: {len(a['outputs_sha256'])} outputs · cache {a['cache_key'][:20]}")


if __name__ == "__main__":
    main()
