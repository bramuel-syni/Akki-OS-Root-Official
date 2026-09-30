import hashlib, importlib.metadata as im, json, sys
from pathlib import Path


def freeze(build_dir):
    b = Path(build_dir)
    plan = json.loads((b / "resolved" / "content_plan.resolved.json").read_text())
    outputs = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((b / "out").iterdir()) if p.name not in ("build-manifest.json", "qa-report.json")}
    m = {"build_stamp": plan["build_stamp"], "cache_key": plan["cache_key"], "page_state_hash": plan["page_state_hash"], "outputs_sha256": outputs, "inputs_sha256": plan["inputs_sha256"],
         "environment": {"python": sys.version.split()[0], "jsonschema": im.version("jsonschema")},
         "contract": "byte-identical content record and preview for the same cache key (page state, role, voice, spec, policy version)"}
    (b / "out" / "build-manifest.json").write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")
    return m


if __name__ == "__main__":
    for k, v in freeze(sys.argv[1])["outputs_sha256"].items():
        print(v[:16], k)
