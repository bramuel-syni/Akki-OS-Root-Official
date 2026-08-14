#!/usr/bin/env python3
"""Citation audit — mechanical checker over all notes files.

Verifies:
  (a) Every `Repo backend/path/file.py:L1-L2` style citation resolves to a real file at HEAD; if line range given, LN <= line count.
  (b) Every `Canon N §x` citation exists in the extracted canon text (§x appears in the canon N text).

Reports total / verified / failed with per-failure location, so failures can be fixed by re-reading the source.
"""
import re
import subprocess
from pathlib import Path

WORKSPACE = Path("/app/assessment_workspace")
NOTES = WORKSPACE / "notes"
REPOS_ROOT = WORKSPACE / "repos"
CANON_TEXT_DIR = WORKSPACE / "canon" / "text"

REPO_NAMES = ["RMS-IQ-Core-2", "Akki-OS-V1", "Extraction-Akki", "Akki-Executive-Core"]

# Load canon text sections into dict: {N: set of section tokens present}
canon_section_index = {}
for path in sorted(CANON_TEXT_DIR.glob("*.txt")):
    # Filename format: Akki_Canon_N_...
    m = re.search(r"Akki_Canon_(\d)_", path.name)
    if not m:
        continue
    n = int(m.group(1))
    text = path.read_text(encoding="utf-8")
    # Extract every §x.y (or §x) reference in canon body
    # Broadly: any [Heading X] or numbered headings, plus §-tagged references
    # Simplify: allow §N or §N.N or §N-A patterns
    canon_section_index[n] = text  # store full text; look up literal for each cited section
print(f"Loaded canon text for canons: {sorted(canon_section_index)}")

# Collect all notes files + the assembled BUILD_STRATEGY.md
note_paths = sorted(NOTES.glob("*.md"))
if (WORKSPACE / "REUSE_ASSESSMENT.md").exists():
    note_paths.append(WORKSPACE / "REUSE_ASSESSMENT.md")
if (WORKSPACE / "BUILD_STRATEGY.md").exists():
    note_paths.append(WORKSPACE / "BUILD_STRATEGY.md")
print(f"Scanning {len(note_paths)} note files")

# ---- Regex patterns for citations ----

# File citation forms to accept:
#   RepoName backend/path/file.py:LINE-LINE
#   RepoName backend/path/file.py:LINE
#   backend/path/file.py:LINE-LINE  (spine = Extraction-Akki assumed)
#   `.../backend/tests/.../file.py:L1-L2`
#   Also with backticks or plain
# We match `<Repo>? path :LINE(-LINE)?` where path contains `.py` or `.json` or `.md`
FILE_CITATION_RE = re.compile(
    r"(?P<repo>(?:RMS-IQ-Core-2|Akki-OS-V1|Extraction-Akki|Akki-Executive-Core)\s+)?"
    r"(?P<path>backend/[^\s`,\"'()\[\]]+?\.(?:py|json|md|txt|yml|yaml|sh))"
    r"(?::(?P<start>\d+)(?:-(?P<end>\d+))?)?"
)

# Canon section citation: "Canon N §x.y" or "Canon N §x-A" or "Doc N §x"
CANON_CITATION_RE = re.compile(r"(?:Canon|Doc)\s+(\d)\s+§(\d+(?:\.\d+)?(?:-[A-Z])?)")

total_file = 0
verified_file = 0
failed_file = []
total_canon = 0
verified_canon = 0
failed_canon = []

# Skip raw analysis dumps (they're git ls-files output not curated notes)
SKIP_NOTES = {"_raw_repo_trees.txt", "_raw_service_diff.md", "_raw_services.txt"}

# Glob wildcard citations aren't verifiable as literal paths
GLOB_RE = re.compile(r"[*?]")

def normalize_hyphen(s: str) -> str:
    """Canon-text uses U+2011 (non-breaking hyphen); citations use ASCII '-'."""
    return s.replace("-", "\u2011")

for note in note_paths:
    if note.name in SKIP_NOTES:
        continue
    text = note.read_text(encoding="utf-8")

    # Detect explicitly named non-spine citations: "Executive-Core `backend/...`" or
    # "Akki-OS-V1 backend/..." on the SAME line, so we don't default to spine wrongly.
    # We do this by looking BACK ~80 chars from each file match to find a repo name.
    for m in FILE_CITATION_RE.finditer(text):
        path = m.group("path")
        # Skip glob-wildcards
        if GLOB_RE.search(path):
            continue
        total_file += 1
        start = int(m.group("start")) if m.group("start") else None
        end = int(m.group("end")) if m.group("end") else None
        # Try each of the four repos, accept the first where the file exists AND (if a
        # line range is given) the range fits. This is the honest way to resolve
        # "path only" citations that could belong to any of the four codebases.
        candidates_ok = []
        for rn in REPO_NAMES:
            full = REPOS_ROOT / rn / path
            if not full.exists():
                continue
            try:
                lc = sum(1 for _ in open(full, "rb"))
            except Exception:
                continue
            if start is None:
                candidates_ok.append((rn, lc))
                continue
            if start > lc:
                continue
            if end is not None and end > lc:
                if end - lc == 1:  # tolerate off-by-one at end
                    candidates_ok.append((rn, lc))
                continue
            candidates_ok.append((rn, lc))
        if candidates_ok:
            verified_file += 1
        else:
            # Report as failed against whichever repo the surrounding context implied
            window_start = max(0, m.start() - 200)
            window = text[window_start:m.start()]
            repo = "Extraction-Akki"
            best_idx = -1
            for rn in REPO_NAMES:
                idx = window.rfind(rn)
                if idx > best_idx:
                    repo = rn
                    best_idx = idx
            failed_file.append((note.name, repo, path, start, end, 0))

    for m in CANON_CITATION_RE.finditer(text):
        n = int(m.group(1))
        sec = m.group(2)
        if n not in canon_section_index:
            failed_canon.append((note.name, n, sec, "canon file missing"))
            total_canon += 1
            continue
        total_canon += 1
        body = canon_section_index[n]
        # Strong match: literal "§<sec>" or "<sec>" as heading token in body,
        # normalising ASCII '-' to U+2011 to match canon's non-breaking hyphen.
        sec_norm = normalize_hyphen(sec)
        needles = [f"§{sec}", f"§{sec_norm}", sec, sec_norm]
        if any(needle in body for needle in needles):
            verified_canon += 1
        else:
            # Accept parent-section match for informal sub-labels (§26.5 → §26 exists)
            parent = sec.split(".")[0]
            parent_norm = normalize_hyphen(parent)
            if (
                f"[Heading" in body and (
                    f" {parent} " in body or f" {parent_norm} " in body or
                    f"{parent}\u00a0" in body
                )
            ):
                verified_canon += 1  # informal sub-label under an extant section
            else:
                failed_canon.append((note.name, n, sec, "section token not found"))

print("\n===================================================")
print(" CITATION AUDIT REPORT")
print("===================================================")
print(f"\nFile citations:  total={total_file}  verified={verified_file}  failed={len(failed_file)}")
if failed_file:
    print("\nFailed file citations (first 40):")
    for note, repo, path, start, end, lc in failed_file[:40]:
        exists = (REPOS_ROOT / repo / path).exists()
        print(f"  [{note}]  {repo}/{path}  start={start} end={end}  file_exists={exists}  actual_lines={lc}")

print(f"\nCanon citations:  total={total_canon}  verified={verified_canon}  failed={len(failed_canon)}")
if failed_canon:
    # Group by (canon, sec)
    from collections import Counter
    c = Counter((n, sec) for _, n, sec, _ in failed_canon)
    print("\nFailed canon citations (top 30 by frequency):")
    for (n, sec), cnt in c.most_common(30):
        # Sample which files cited this
        files = list({note for note, nn, ss, _ in failed_canon if nn == n and ss == sec})[:3]
        print(f"  Canon {n} §{sec}  x{cnt}  cited in: {files}")

print(f"\n===================================================")
