"""Repair supplemental crosswalk using explicit source identity and heading IDs.
Never converts a text-match into implementation evidence or invents new rules.
"""
import json,re
from pathlib import Path
from collections import Counter
ROOT=Path('/app');HERE=Path(__file__).resolve().parent
def read(n):return json.loads((HERE/n).read_text())
def save(n,o):(HERE/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
data=read('SUPPLEMENTAL_RECONCILIATION.json');save('SUPPLEMENTAL_REVIEWER_DRAFT.json',data)
base=read('BASELINE_648.json');corpus=read('SOURCE_CORPUS.json')
sources={s['source']:s for s in corpus}
def stem(v):return re.sub('[^a-z0-9]','',Path(re.sub(r':\d+.*$','',v)).stem.lower())
for r in data['rows']:
    text=r['text'];source=r['source'];name=Path(source).name
    candidates=[b for b in base if stem(b['Source (file:line)'])==stem(name)]
    if name=='AKKI_Canon_Documents_17_20_v3.docx':candidates=[b for b in base if b['Doc'] in {'Doc 17','Doc 18','Doc 19','Doc 20'}]
    if name=='spec.docx' and 'whitepaper' in source:candidates=[b for b in base if b['Doc']=='WPW spec']
    normalized=text.replace('‑','-').replace('–','-')
    matches=[b for b in candidates if re.match(r'^'+re.escape(b['Rule ID'])+r'(?![\w.])',normalized)]
    if matches and r['kind'] not in {'RULING','LIMITATION'}:
        r.update(classification='REGISTERED_OBLIGATION_OVERLAP',primary_overlap=[b['composite_id'] for b in matches],rationale='Explicit leading rule identifier AND corresponding source-document identity match. Original statement remains authoritative; no new rule inferred.',obligation_effect='Full source clause elaborates the listed registry obligation.',gap_or_decision='Use full source clause and existing matrix disposition; overlap does not prove implementation.',action='Carry this exact source clause into the referenced rule acceptance evidence; do not ask owner to re-adopt an existing rule.')
    elif r['classification']=='CROSSCUTTING_UNMAPPED_OBLIGATION' and candidates:
        r.update(classification='SOURCE_CONTEXT_REQUIRES_TRACE',related_source_family=sorted({b['Doc'] for b in candidates}),rationale='Corresponding primary source is identified, but this paragraph is not itself an explicit registered rule ID. It may define, qualify or add acceptance detail.',gap_or_decision='Analyst traceability work remains; this is NOT evidence of a new missing product requirement.',action='Resolve paragraph-to-rule/promise dependency and preserve its qualifications before closing the relevant delivery claim. No automatic owner re-ratification request.')
    elif r['classification']=='CROSSCUTTING_UNMAPPED_OBLIGATION':
        r.update(classification='FOUNDATIONAL_CANON_TRACE_PENDING',gap_or_decision='Original Canon or cross-cutting context needs semantic linkage to existing rule/promise coverage. No conclusion of new requirement or implementation absence follows.',action='Complete analyst-owned source-to-requirement reconciliation; escalate only genuine conflicts or unspecified decisions, not this inventory count.')
    if r['supplement_id']=='SUP-0018':
        r.update(classification='HISTORICAL_DIAGNOSIS_NOT_CURRENT_VERDICT',obligation_effect='Describes the pre-amendment output-checking gap, not current code state.',action='Assess the subsequent DAP31-36/output gates and their runtime coverage; do not copy historical absence into current findings.')
    elif r['supplement_id']=='SUP-0061':r.update(classification='EXPLICIT_LIMIT_OR_NONCLAIM',obligation_effect='Method explicitly distinguishes proposed guarantees from implemented facts.',action='Preserve that distinction in delivery status; no new feature follows from this sentence.')
    elif r['supplement_id']=='SUP-0074':r.update(classification='RULING_OR_AUTHORITY_DEPENDENCY',obligation_effect='Document declares R5 resolved by cross-reference.',action='Retain the cited trust-domain resolution; do not reopen R5 from an old OPEN label.')
    elif r['supplement_id']=='SUP-0224':r.update(classification='EXPLICIT_LIMIT_OR_NONCLAIM',obligation_effect='CIF never claims coach independence, permanently.',action='Preserve origination provenance; do not propose independence as a future completion criterion.')
    if r['kind']=='RULING' and text.startswith('R-32'):
        r.update(gap_or_decision='Later owner-whitelist authority is recorded in the assessed content-registry lineage; inherited owner-pending wording is stale, not permission for new generated surfaces.',action='Reconcile source metadata to the already-recorded R32 decision and enforce its whitelist. Code is implementation evidence, not the authority itself; do NOT request redundant ratification.')
    if r['kind']=='RULING' and not re.match('^R-(32|37)\b',text):
        r['action']='Resolve cited ruling against current authority record and DEFAULT binding protocol; do not automatically send every DEFAULT to the owner. '+r['action']
data['meta']['main_reconciliation_counts']=dict(Counter(r['classification'] for r in data['rows']))
data['meta']['scope']='848 inventory members accounted for. Source-context/foundational trace-pending items are unfinished ANALYSIS, NOT missing features or a request for hundreds of owner decisions. No full supplemental semantic coverage claim.'
save('SUPPLEMENTAL_RECONCILIATION.json',data)
print(json.dumps(data['meta']['main_reconciliation_counts'],indent=2))