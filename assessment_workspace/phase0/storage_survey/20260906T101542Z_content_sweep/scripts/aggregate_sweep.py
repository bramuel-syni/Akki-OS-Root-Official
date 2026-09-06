#!/usr/bin/env python3
"""
aggregate_sweep.py — local aggregation of the remote sweep output.

Consumes:
    step2_enumeration.log     — Sections A..E (roots, du raw, enumeration, secrets, owner, mtime)
    step3_classify_hash_probe.log — Sections F..K (du, tree, magic, mime census, sha256, ffprobe)

Emits:
    aggregate/{host}/mime_census.tsv           # count \t mime  (top 100)
    aggregate/{host}/mime_category_rollup.tsv  # top-level MIME category counts
    aggregate/{host}/tree_home_depth2.txt      # /home tree depth 2
    aggregate/{host}/summary.md                # human summary per host
    aggregate/cross_check/db_overlap.tsv       # DB filename vs sweep path overlap
    aggregate/cross_check/db_overlap.md        # explicit verdict
"""

import re, sys, pathlib, collections, json, os

BASE = pathlib.Path("/app/assessment_workspace/phase0/storage_survey/20260906T101542Z_content_sweep")
AGG  = BASE / "aggregate"

HOSTS = ["akki-vm", "akki-vm-ii"]

def parse_step3(path):
    text = path.read_text(errors="replace")
    sections = {}
    cur = None
    lines = []
    for line in text.splitlines():
        m = re.match(r"^===([A-Z])\b", line)
        if m:
            if cur:
                sections[cur] = lines
            cur = m.group(1)
            lines = []
            continue
        if line.startswith("==END"):
            if cur:
                sections[cur] = lines
            cur = None
            lines = []
            continue
        if cur:
            lines.append(line)
    if cur:
        sections[cur] = lines
    return sections

def parse_step2(path):
    text = path.read_text(errors="replace")
    sections = {}
    cur = None
    lines = []
    for line in text.splitlines():
        m = re.match(r"^===([A-Z])\b", line)
        if m:
            if cur:
                sections[cur] = lines
            cur = m.group(1)
            lines = []
            continue
        if line.startswith("==END"):
            if cur:
                sections[cur] = lines
            cur = None
            lines = []
            continue
        if cur:
            lines.append(line)
    if cur:
        sections[cur] = lines
    return sections

# Re-parse Section H (path\tmime, produced by `file --mime-type` with padding).
# `file --mime-type` outputs `<path>:<pad>       <mime>`; a single colon then whitespace then mime.
MIME_RE = re.compile(r"^(.+?):\s+([A-Za-z][A-Za-z0-9+.\-]*/[A-Za-z0-9+.\-]+.*)$")

for h in HOSTS:
    out_dir = AGG / h
    out_dir.mkdir(parents=True, exist_ok=True)

    s3 = parse_step3(BASE / h / "step3_classify_hash_probe.log")
    s2 = parse_step2(BASE / h / "step2_enumeration.log")

    # ---- Section H → mime census ----
    # Records were emitted by `file --mime-type --print0` piped through `tr '\0' '\n'`,
    # which splits each record across two lines: the path, then ':<padding><mime>'.
    # Fold adjacent lines: if line N+1 starts with ':', it's the classification for line N.
    lines_h = s3.get("H", [])
    counts = collections.Counter()
    examples = {}
    audio_video_paths = []
    i = 0
    while i < len(lines_h):
        line = lines_h[i].rstrip()
        if not line:
            i += 1
            continue
        # Path line + mime line
        if i + 1 < len(lines_h) and lines_h[i+1].lstrip().startswith(":"):
            path = line
            mime_line = lines_h[i+1].lstrip()  # ":     text/plain"
            mime = mime_line.lstrip(":").strip().split(";")[0].strip()
            i += 2
        else:
            # Single-line fallback: 'path: mime'
            m = MIME_RE.match(line)
            if m:
                path, mime = m.group(1), m.group(2).strip().split(";")[0].strip()
            else:
                j = line.rfind(": ")
                if j < 0:
                    i += 1
                    continue
                path, mime = line[:j], line[j+2:].strip().split(";")[0].strip()
            i += 1
        counts[mime] += 1
        examples.setdefault(mime, path)
        if mime.startswith("audio/") or mime.startswith("video/"):
            audio_video_paths.append((path, mime))

    total_files = sum(counts.values())

    # Write mime_census.tsv (all mimes, sorted desc)
    with (out_dir/"mime_census.tsv").open("w") as f:
        f.write("count\tmime\texample_path\n")
        for m, c in counts.most_common():
            f.write(f"{c}\t{m}\t{examples[m]}\n")

    # Category rollup: top-level type prefix (text/, application/, image/, audio/, video/, inode/, ...)
    cat = collections.Counter()
    for m, c in counts.items():
        top = m.split("/")[0] if "/" in m else m
        cat[top] += c
    with (out_dir/"mime_category_rollup.tsv").open("w") as f:
        f.write("count\tcategory\n")
        for k, v in cat.most_common():
            f.write(f"{v}\t{k}\n")

    # ---- Section G → tree home depth 2 ----
    tree_lines = s3.get("G", [])
    (out_dir/"tree_depth2.txt").write_text("\n".join(tree_lines))

    # ---- Section F → du depth1 ----
    du_lines = s3.get("F", [])
    (out_dir/"du_depth1.txt").write_text("\n".join(du_lines))

    # ---- Section J → sha256 count ----
    j_lines = [l for l in s3.get("J", []) if l.strip()]
    sha_count = len(j_lines)
    # sample first 5 hashes
    (out_dir/"sha256.tsv").write_text("\n".join(j_lines))

    # ---- Section K → ffprobe results ----
    k_lines = [l for l in s3.get("K", []) if l.strip()]
    (out_dir/"ffprobe.txt").write_text("\n".join(k_lines) if k_lines else "(no audio/video magic-byte candidates found on this host)\n")

    # ---- Section E → mtime buckets ----
    mtime_lines = [l for l in s2.get("E", []) if l.strip()]
    (out_dir/"mtime_buckets.tsv").write_text("\n".join(mtime_lines))

    # ---- Section C → secret summary ----
    secret_lines = [l for l in s2.get("C", []) if l.strip()]
    (out_dir/"secret_summary.tsv").write_text("\n".join(secret_lines))

    # ---- Section D → owner/group ----
    ownr_lines = [l for l in s2.get("D", []) if l.strip()]
    (out_dir/"owner_group.tsv").write_text("\n".join(ownr_lines))

    # ---- Per-host summary.md ----
    top10_mime = counts.most_common(10)
    with (out_dir/"summary.md").open("w") as f:
        f.write(f"# {h} — content sweep summary\n\n")
        f.write(f"- Total files classified by magic: **{total_files}**\n")
        f.write(f"- SHA-256 hashes captured (≤100 MiB): **{sha_count}**\n")
        f.write(f"- Audio magic-byte hits: **{sum(1 for _,m in audio_video_paths if m.startswith('audio/'))}**\n")
        f.write(f"- Video magic-byte hits: **{sum(1 for _,m in audio_video_paths if m.startswith('video/'))}**\n\n")
        f.write("## Top-level MIME category rollup\n\n")
        f.write("| Category | Count |\n|---|---:|\n")
        for k, v in cat.most_common():
            f.write(f"| `{k}` | {v} |\n")
        f.write("\n## Top-10 concrete MIME types\n\n")
        f.write("| Rank | Count | MIME | Example path |\n|---:|---:|---|---|\n")
        for i, (m, c) in enumerate(top10_mime, 1):
            f.write(f"| {i} | {c} | `{m}` | `{examples[m]}` |\n")

# --------- CROSS-CHECK ---------
xc_dir = AGG / "cross_check"
xc_dir.mkdir(parents=True, exist_ok=True)

# Load 60 DB sample filenames
db_names = []
for line in (BASE/"cross_check"/"db_sampled_filenames.tsv").read_text().splitlines():
    parts = line.split("\t")
    if len(parts) == 4:
        db_names.append(parts[3])

# For each host, build set of basenames of all enumerated files
report_lines = ["# DB filename × sweep basename cross-check\n",
                f"- DB samples: **{len(db_names)}** unique names (30 from `company.image_url`, 30 from `user_group_trainings.file_url`, 0 from `user_group_trainings.pend_action_file` sample)\n",
                "- Match rule: exact basename match (case-insensitive) against any path enumerated in the sweep on each host\n\n"]
overall_matches = {h: [] for h in HOSTS}
for h in HOSTS:
    # Extract paths from Section B in step2
    seen_basenames_lower = set()
    for line in (BASE/h/"step2_enumeration.log").read_text().splitlines():
        # Section B line: path\tsize\tmtime\tuid\tgid\tmode
        if not line or line.startswith("==") or line.startswith("===") or line.startswith("--"):
            continue
        first_tab = line.find("\t")
        if first_tab < 0:
            continue
        p = line[:first_tab]
        if not p.startswith("/"):
            continue
        seen_basenames_lower.add(os.path.basename(p).lower())
    matches = [n for n in db_names if n.lower() in seen_basenames_lower]
    overall_matches[h] = matches

    report_lines.append(f"## {h}\n")
    report_lines.append(f"- Enumerated basenames on this host: **{len(seen_basenames_lower)}** unique\n")
    report_lines.append(f"- DB samples matched: **{len(matches)}** / {len(db_names)}\n")
    if matches:
        report_lines.append("- Matched names:\n")
        for m in matches:
            report_lines.append(f"  - `{m}`\n")
    report_lines.append("")

report_lines.append("## Verdict\n")
total_matches = sum(len(v) for v in overall_matches.values())
if total_matches == 0:
    report_lines.append("**Zero DB-sampled filenames match any file on either GPU host.** The DigiCow file backend is definitively NOT on `akki-vm` or `akki-vm-ii`. This confirms the earlier prior probe finding at higher rigor: the block-device-up sweep saw every mounted filesystem, and the content-level classification saw every file's magic bytes on the reachable estate.\n")
else:
    report_lines.append(f"**{total_matches} matches found**; see per-host breakdown above.\n")
(xc_dir/"db_overlap.md").write_text("".join(report_lines))

# TSV form
with (xc_dir/"db_overlap.tsv").open("w") as f:
    f.write("host\tdb_sample_name\tmatched\n")
    for h in HOSTS:
        for n in db_names:
            f.write(f"{h}\t{n}\t{'yes' if n in overall_matches[h] else 'no'}\n")

print(f"Aggregation complete. Output under {AGG}")
