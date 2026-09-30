"""Freeze: make delivered bytes repeatable and record what produced them.

Promise 3 of the determinism contract (binary reproducibility) fails without
this step, whatever the renderer: zip entries carry mtimes, docProps carry
created/modified stamps, and LibreOffice (recalc) writes its own metadata.
Normalising after rendering makes the guarantee independent of the renderer.
"""
import hashlib
import importlib.metadata as im
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

OOXML = {".pptx", ".docx", ".xlsx"}
FIXED_DT = (1980, 1, 1, 0, 0, 0)


def _stamp_core(xml, stamp):
    xml = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rf"\g<1>{stamp}\g<2>", xml)
    xml = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rf"\g<1>{stamp}\g<2>", xml)
    xml = re.sub(r"<dc:date>[^<]*</dc:date>", "", xml)
    xml = re.sub(r"(<cp:lastPrinted>)[^<]*(</cp:lastPrinted>)", r"\g<1>\g<2>", xml)
    return xml


def _strip_app(xml):
    xml = re.sub(r"<TotalTime>[^<]*</TotalTime>", "<TotalTime>0</TotalTime>", xml)
    return xml


def normalize_bytes(blob, stamp):
    """Normalize one OOXML package held in memory; recurses into embedded packages
    (chart data workbooks inside a pptx carry their own docProps timestamps)."""
    import io
    src = zipfile.ZipFile(io.BytesIO(blob))
    entries = []
    for name in sorted(src.namelist()):
        data = src.read(name)
        if name == "docProps/core.xml":
            data = _stamp_core(data.decode("utf-8"), stamp).encode("utf-8")
        elif name == "docProps/app.xml":
            data = _strip_app(data.decode("utf-8")).encode("utf-8")
        elif name.rsplit(".", 1)[-1] in ("xlsx", "docx", "pptx") and data[:2] == b"PK":
            data = normalize_bytes(data, stamp)
        entries.append((name, data))
    src.close()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries:
            zi = zipfile.ZipInfo(name, date_time=FIXED_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED if name != "mimetype" else zipfile.ZIP_STORED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    return buf.getvalue()


def normalize_ooxml(path, stamp):
    path = Path(path)
    path.write_bytes(normalize_bytes(path.read_bytes(), stamp))


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def freeze(out_dir, resolved_dir, stamp):
    out_dir, resolved_dir = Path(out_dir), Path(resolved_dir)
    outputs = {}
    for p in sorted(out_dir.iterdir()):
        if p.suffix in OOXML:
            normalize_ooxml(p, stamp)
        if p.suffix in OOXML | {".html", ".md"}:
            outputs[p.name] = sha256(p)
    inputs = {}
    for r in sorted(resolved_dir.glob("*.resolved.json")):
        plan = json.loads(r.read_text())
        inputs[r.name] = sha256(r)
        inputs.update({f"{r.stem}/{k}": v for k, v in plan.get("inputs_sha256", {}).items()})
    try:
        soffice = subprocess.run(["soffice", "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        soffice = "unavailable"
    manifest = {
        "build_stamp": stamp,
        "outputs_sha256": outputs,
        "inputs_sha256": inputs,
        "environment": {
            "python": sys.version.split()[0],
            "python-pptx": im.version("python-pptx"), "python-docx": im.version("python-docx"),
            "openpyxl": im.version("openpyxl"), "matplotlib": im.version("matplotlib"),
            "libreoffice": soffice,
        },
        "contract": "Same inputs_sha256 + same environment => same outputs_sha256. Revisions create a new manifest; never edit outputs by hand.",
    }
    mp = out_dir / "build-manifest.json"
    mp.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    m = freeze(sys.argv[1], sys.argv[2], sys.argv[3])
    for k, v in m["outputs_sha256"].items():
        print(f"{v[:16]}  {k}")
