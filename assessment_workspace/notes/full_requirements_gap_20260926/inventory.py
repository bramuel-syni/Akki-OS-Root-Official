"""Assessment-only raw source inventory; never imports application modules."""
import hashlib
import json
import re
from pathlib import Path
from collections import defaultdict
from openpyxl import load_workbook

ROOT = Path('/app')
HERE = Path(__file__).resolve().parent
BASE = ROOT / 'assessment_workspace/custody/owner_drops/enhancement_specs_18_20260926'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(name, sheet):
    wb = load_workbook(BASE / name, read_only=True, data_only=False)
    values = list(wb[sheet].iter_rows(values_only=True)); wb.close()
    header = values[0]
    return [{**dict(zip(header, r)), 'workbook_row': i} for i, r in enumerate(values[1:], 2) if r[0]]


def save(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str) + '\n')


rules = rows('Master_Requirements_Registry.xlsx', 'System Rules Registry')
assert len(rules) == len({(r['Doc'], r['Rule ID']) for r in rules}) == 648
for i, r in enumerate(rules, 1):
    r['review_id'] = f'REQ-{i:03d}'
    r['composite_id'] = f"{r['Doc']}::{r['Rule ID']}"
save('BASELINE_648.json', rules)

wb = load_workbook(BASE / 'Security_Assurance_Promise_Set.xlsx', read_only=True, data_only=False)
vals = list(wb['Security Assurance Set'].iter_rows(values_only=True)); wb.close()
promises = [{**dict(zip(vals[0], r)), 'workbook_row': i} for i,r in enumerate(vals[1:],2) if str(r[0]).startswith('S-')]
assert len(promises) == 35
save('BASELINE_PROMISES_35.json', promises)

groups = defaultdict(list)
for r in rules:
    groups[r['Doc']].append(r['review_id'])
save('GROUPS.json', dict(groups))
qa = rows('Master_Requirements_Registry.xlsx', 'QA Verification')
save('BASELINE_QA_602.json', qa)

# Filename inventory only; no credentials or arbitrary user data read.
candidates = []
for base in [ROOT/'assessment_workspace/canon', ROOT/'assessment_workspace/custody', ROOT/'assessment_workspace/fixtures', ROOT/'audit/inbox', HERE/'recovered_sources', ROOT/'backend/vendored/extraction_akki/docs', ROOT/'backend/vendored/extraction_akki/backend/docs']:
    if base.exists():
        candidates.extend(p for p in base.rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.txt','.docx'} and not any(x in p.name.lower() for x in ['cred','password','secret','token']))

index = defaultdict(list)
for p in candidates:
    stem = re.sub('[^a-z0-9]','',p.stem.lower())
    index[stem].append(p)
sources = []
for citation in sorted({str(r['Source (file:line)']) for r in rules}):
    name = re.sub(r':\d+.*$', '', citation)
    norm = re.sub('[^a-z0-9]','',Path(name).stem.lower())
    found = index.get(norm, [])
    sources.append({'registry_citation': citation, 'filename_or_spec': name, 'candidates': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p)} for p in found], 'resolution': 'CANDIDATES_REQUIRE_VERSION_CHECK' if found else 'NO_LITERAL_FILENAME_MATCH'})
save('SOURCE_INVENTORY.json', sources)
save('SOURCE_FILES_AVAILABLE.json', [{'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size} for p in candidates])

for start,end in [(1,216),(217,432),(433,648)]:
    batch=[r for r in rules if start<=int(r['review_id'][4:])<=end]
    save(f'BATCH_{start}_{end}.json', batch)
    lines=[]
    for r in batch:
        lines.append(f"{r['review_id']} | {r['Doc']} | {r['Rule ID']} | {r['Status']} | {r['Statement']} | {r['Source (file:line)']}")
    (HERE/f'READ_{start}_{end}.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'rules':len(rules),'promises':len(promises),'doc_families':len(groups),'distinct_source_citations':len(sources),'literal_source_matches':sum(bool(s['candidates']) for s in sources),'available_source_files':len(candidates)},indent=2))