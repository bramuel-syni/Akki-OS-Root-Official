#!/usr/bin/env python3
"""Extract sampled filenames from the audio_location_probe shape summary."""
import json, sys, pathlib
src = pathlib.Path("/app/assessment_workspace/phase0/audio_location_probe/20260906T093940Z/per_column_shape_summary.json")
data = json.loads(src.read_text())
out = []
for entry in data:
    for name in entry.get("first_path_seg_histogram", {}).keys():
        out.append((entry["database"], entry["table"], entry["column"], name))
print(f"# extracted {len(out)} filenames from sampled DB rows", file=sys.stderr)
for row in out:
    print("\t".join(row))
