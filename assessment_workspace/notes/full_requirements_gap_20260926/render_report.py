"""Render complete assessment appendices from the adjudicated datasets."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def load(n):return json.loads((HERE/n).read_text())
def text(x):return x if isinstance(x,str) else json.dumps(x,ensure_ascii=False)
rows=load('REQUIREMENT_GAPS_648.json')
out=['# Akki — all648requirement dispositions','',
     'Read REPORT.md for scope, source gaps and unfinished supplemental traceability. No row is a new runtime certification.','']
for r in rows:
    out.extend([f"## {r['review_id']} — {r['composite_id']}",
        f"Workbook row: {r['workbook_row']} · Authority: {r['registry_authority_status']} · Static delivery disposition: **{r['delivery_status']}** · Confidence: {r['confidence']}",'',
        '> '+str(r['statement']).replace('\n','\n> '),'',
        '**Intended outcome:** '+text(r['intended_outcome']),
        '**Gap:** '+text(r['exact_gap']),
        '**Required work:** '+text(r['required_action']),
        '**Closure demonstration (not executed here):** '+text(r['closure_demonstration']),
        '**Scope/limit:** '+text(r['evidence_limit']),
        '**Dependencies:** '+text(r['dependencies']),
        '**Primary source:** '+text(r['source']),
        '**Additional source evidence:** '+text(r['additional_source_evidence']),
        '**Code evidence:**'])
    for c in r['code_evidence']:
        out.append(f"- `{c.get('path','unresolved')}:{c.get('start_line','?')}–{c.get('end_line','?')}` SHA256 `{c.get('current_file_sha256','unverified')}` — {c.get('observation','')} {c.get('range_note','')}")
    out.append('')
(HERE/'REQUIREMENTS_LINE_BY_LINE.md').write_text('\n\n'.join(out)+'\n')
out=['# Akki — all35assurance promises','Product promise#N is distinct from S-N. Read-only assessment; closure scenarios below have NOT been executed.','']
for r in load('PROMISE_GAPS_35.json'):
    out.extend([f"## {r['promise_id']}",'> '+r['original_promise_text'],
      '**Bound/ruling:** '+text(r['bound_ruling']),
      '**Requirement links:** '+text(r['related_req_ids']),
      '**Gap:** '+text(r['exact_unproven_or_missing_guarantee']),
      '**Work to deliver:** '+r['concrete_work_to_deliver'],
      '**Acceptance demonstration:** '+r['requirement_specific_closure_scenario'],
      '**Status and limits:** '+text(r['current_status_scope_confidence_authority'])+' '+r['uncertainty_note'],
      '**Code evidence:** '+text(r['existing_mechanism_file_line_hash']),''])
(HERE/'PROMISES_LINE_BY_LINE.md').write_text('\n\n'.join(out)+'\n')
print('Rendered648requirement cards and35promise cards')