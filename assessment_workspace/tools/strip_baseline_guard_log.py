"""Strip BASELINE_GUARD=1 sweep log of expected drift sources so byte-identity
can be computed across runs.

Drift sources stripped:
  1. Test duration float in the pytest summary line (e.g., "in 179.84s" → "in TIMING")
  2. Specialist-drift .jsx file name lines inside the pod_shell mirror-drift
     test output (filesystem enumeration order varies per run)
  3. Any absolute timing on collection lines

Per R-81 seal reconciliation pattern verbatim (CP-ENTITLEMENT-WAVE-SETUP commit
fc8b5c0 banking section): "byte-identity achieved after redacting specialist-
drift .jsx file names per identical CCS1/Q-unlock reconciliation pattern".

Usage:
    python3 tools/strip_baseline_guard_log.py <log_path>
Prints stripped-sha256 and (with -o OUT) writes stripped bytes to OUT.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys


_TIMING_LINE = re.compile(r"in \d+\.\d+s \(\d+:\d+:\d+\)")
_JSX_FILE_LINE = re.compile(r"^E\s+'[a-zA-Z0-9_/\-]+\.jsx'(\.\.\.)?\s*$")
_JS_FILE_LINE = re.compile(r"^E\s+'[a-zA-Z0-9_/\-]+\.js'(\.\.\.)?\s*$")


def strip(source_bytes: bytes) -> bytes:
    text = source_bytes.decode("utf-8", errors="strict")
    lines = text.splitlines(keepends=True)
    out = []
    for line in lines:
        # Drop specialist-drift .jsx / .js file name lines
        if _JSX_FILE_LINE.match(line.rstrip("\n\r")):
            continue
        if _JS_FILE_LINE.match(line.rstrip("\n\r")):
            continue
        # Normalise pytest summary timing
        line = _TIMING_LINE.sub("in TIMING", line)
        out.append(line)
    return "".join(out).encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log_path")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()
    with open(args.log_path, "rb") as fh:
        raw = fh.read()
    stripped = strip(raw)
    sha = hashlib.sha256(stripped).hexdigest()
    print(f"stripped_sha256={sha}  stripped_bytes={len(stripped)}  raw_bytes={len(raw)}  path={args.log_path}")
    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(stripped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
