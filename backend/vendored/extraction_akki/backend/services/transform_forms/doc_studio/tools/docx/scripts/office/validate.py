"""In-repo stand-in for the office skills' validate.py, reached through DOC_STUDIO_TOOLS_DIR (doc-studio v1.1, owner condition A).

Package-level checks only: the ZIP container is intact, [Content_Types].xml and the root relationships exist, every
relationship target inside the package resolves to a part, and the file reopens with python-pptx / python-docx.
This is not an OOXML schema validator; the build manifest's environment records that honestly. Prints PASSED (rc 0)
or the enumerated failures (rc 1)."""
import posixpath
import re
import sys
import zipfile
from pathlib import Path

REL_TARGET = re.compile(r'Target="([^"]+)"(?:[^>]*TargetMode="([^"]+)")?')


def check(path: str) -> list:
    p = Path(path)
    failures = []
    try:
        z = zipfile.ZipFile(p)
    except (zipfile.BadZipFile, OSError) as exc:
        return [f"not a readable OOXML package: {type(exc).__name__}"]
    bad = z.testzip()
    if bad:
        failures.append(f"corrupt entry {bad}")
    names = set(z.namelist())
    for required in ("[Content_Types].xml", "_rels/.rels"):
        if required not in names:
            failures.append(f"missing {required}")
    for rels in [n for n in names if n.endswith(".rels")]:
        base = posixpath.dirname(posixpath.dirname(rels))
        text = z.read(rels).decode("utf-8", "replace")
        for target, mode in REL_TARGET.findall(text):
            if mode == "External" or target.startswith("http"):
                continue
            resolved = posixpath.normpath(posixpath.join(base, target)) if not target.startswith("/") else target.lstrip("/")
            if resolved not in names:
                failures.append(f"{rels}: relationship target {target} is not in the package")
    try:
        if p.suffix == ".pptx":
            from pptx import Presentation
            prs = Presentation(str(p))
            if len(prs.slides) == 0:
                failures.append("pptx has no slides")
        elif p.suffix == ".docx":
            from docx import Document
            Document(str(p))
    except Exception as exc:  # noqa: BLE001 — every reopen failure is reported, never swallowed
        failures.append(f"reopen failed: {type(exc).__name__}: {str(exc)[:160]}")
    return failures


if __name__ == "__main__":
    problems = check(sys.argv[1])
    if problems:
        print("FAILED\n" + "\n".join(problems)); sys.exit(1)
    print(f"PASSED package checks for {Path(sys.argv[1]).name} (container, content types, relationships, reopen)")
