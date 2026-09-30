"""training-studio freeze: hash the content of every output with volatile fields removed; write the build manifest."""
import hashlib, importlib.metadata as im, json, sys
from pathlib import Path


def content_hash(obj):
    o = json.loads(json.dumps(obj))
    o.pop("volatile", None)
    return hashlib.sha256(json.dumps(o, sort_keys=True).encode()).hexdigest()


def freeze(build_dir):
    b = Path(build_dir)
    plan = json.loads((b / "resolved" / "run_plan.resolved.json").read_text())
    outputs = {}
    for p in sorted((b / "out").iterdir()):
        if p.name in ("build-manifest.json", "qa-report.json"):
            continue
        if p.suffix == ".json":
            outputs[p.name] = content_hash(json.loads(p.read_text()))
        else:
            outputs[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    m = {
        "build_stamp": plan["build_stamp"], "backend": plan["backend"],
        "outputs_sha256": outputs, "inputs_sha256": plan["inputs_sha256"],
        "environment": {"python": sys.version.split()[0], "jsonschema": im.version("jsonschema")},
        "reproducibility": plan["reproducibility"],
        "contract": "stub: content-identical across builds (volatile fields excluded). real: within tolerance per reproducibility.canon; hashes of real runs are recorded, not asserted equal.",
    }
    (b / "out" / "build-manifest.json").write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")
    return m


if __name__ == "__main__":
    for k, v in freeze(sys.argv[1])["outputs_sha256"].items():
        print(v[:16], k)
