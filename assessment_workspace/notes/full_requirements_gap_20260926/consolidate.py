"""Read-only assessment assembly and citation checks. No application imports."""
import csv,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path('/app');HERE=Path(__file__).resolve().parent
CODE=ROOT/'backend/vendored/extraction_akki/backend'
def read(name):return json.loads((HERE/name).read_text())
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n')
def array(x):return x if isinstance(x,list) else [x] if x else []
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(name):
    if not name:return None
    name=str(name); p=Path(name)
    candidates=[p] if p.is_absolute() else [ROOT/p,HERE/p,CODE/p]
    if name.startswith('backend/services/') or name.startswith('backend/contracts/'):
        candidates.append(CODE/name[len('backend/'):])
    return next((x for x in candidates if x.is_file()),None)

base=read('BASELINE_648.json');prior={}
for file in HERE.glob('reviewer_*.json'):
    for row in read(file.name):prior[row['review_id']]=row
corrections={}
for file in sorted(HERE.glob('correction_*.json')):
    for row in read(file.name):
        key=row['review_id']
        if key in corrections:raise ValueError(f'Duplicate correction {key}')
        corrections[key]=(row,file.name)
assert set(corrections)=={r['review_id'] for r in base}

allrows=[];issues=[];filehashes={}
adjudication={r['review_id']:r for r in read('MAIN_ADJUDICATIONS.json')} if (HERE/'MAIN_ADJUDICATIONS.json').exists() else {}
for original in base:
    ident=original['review_id'];r,pack=corrections[ident];raw=prior.get(ident,{})
    assert r['composite_id']==original['composite_id']
    state=r.get('delivery_status',r.get('deliverystatus',r.get('status_scope_confidence',r.get('status','UNVERIFIED'))))
    if isinstance(state,dict):
        confidence=state.get('confidence',r.get('confidence','unrated'));scope=state.get('scope','Static source/body inspection');state=state.get('status','UNVERIFIED')
    else:confidence=r.get('confidence','unrated');scope='Static source/body inspection; no new runtime calls'
    original_state=state
    # Local evidence cannot establish repo-wide absence. Preserve proposal, do not certify it.
    if state in {'MISSING','NOT_IMPLEMENTED_CONFIRMED','NOT_IMPLEMENTED','SOURCE_UNRESOLVED'}:
        state='SOURCE_UNRESOLVED' if state=='SOURCE_UNRESOLVED' else 'UNVERIFIED'
    if state not in {'PARTIAL','UNVERIFIED','EVIDENCED_SCOPED','BLOCKED','SOURCE_UNRESOLVED','SPEC_DECISION_REQUIRED','EXPLICIT_NONCLAIM'}:state='UNVERIFIED'
    citations=[];rowissues=[]
    for e in array(r.get('code_evidence')):
        if not isinstance(e,dict):
            rowissues.append('UNSTRUCTURED_CITATION');continue
        path=resolve(e.get('path',e.get('file','')))
        if not path:
            rowissues.append('UNRESOLVED_CODE_PATH');citations.append({**e,'verified':False});continue
        lines=path.read_text(errors='replace').splitlines()
        rng=str(e.get('lines',e.get('line_range','')));nums=re.findall(r'\d+',rng)
        start=e.get('start_line',int(nums[0]) if nums else 1)
        end=e.get('end_line',int(nums[-1]) if nums else len(lines))
        if not isinstance(start,int) or not isinstance(end,int):start,end=1,len(lines);rowissues.append('INVALID_LINE_RANGE')
        declared=e.get('sha256',e.get('hash'));actual=sha(path)
        part='\n'.join(lines[max(0,start-1):end])
        variants=[part,part+'\n']
        hash_kind='whole-file' if declared==actual else 'quoted-lines' if any(hashlib.sha256(v.encode()).hexdigest()==declared for v in variants) else 'not-supplied' if not declared else 'unreproduced'
        if hash_kind=='unreproduced':rowissues.append('REVIEWER_HASH_UNREPRODUCED')
        original_range_valid=1<=start<=end<=len(lines)
        # File viewers accept an upper bound beyond EOF. Publish the real range,
        # retaining the proposed upper bound and an explicit normalization note.
        valid_range=1<=start<=min(end,len(lines))
        if not valid_range:rowissues.append('CITATION_RANGE_OUTSIDE_FILE')
        filehashes[str(path.relative_to(ROOT))]=actual
        citations.append({'path':str(path.relative_to(ROOT)),'start_line':start,'end_line':min(end,len(lines)),'reviewer_end_line':end,'current_file_sha256':actual,'reviewer_hash':declared,'reviewer_hash_kind':hash_kind,'range_valid':valid_range,'range_note':'Upper read bound clipped to actual EOF; original retained.' if not original_range_valid and valid_range else '', 'observation':e.get('observation',e.get('actualbehavior',e.get('behavior',''))),'snapshot_scope':'Current raw file hash banked; existence is not semantic proof.'})
    gap=r.get('exact_gap','');action=r.get('required_action',r.get('concrete_action',''))
    demo=r.get('closure_demonstration',r.get('unique_closure_demo',r.get('unique_closure_demo_requirement_edge','')))
    if not gap or not action or not demo:rowissues.append('MISSING_SUBSTANTIVE_FIELD')
    sources=array(r.get('source_evidence'))
    if not sources:rowissues.append('SOURCE_DETAIL_NOT_SUPPLIED')
    # Accept raw workbook as exactly identified authority, without faking derivative source lines.
    primary_source={'file':'assessment_workspace/custody/owner_drops/enhancement_specs_18_20260926/Master_Requirements_Registry.xlsx','sheet':'System Rules Registry','row':original['workbook_row'],'original_reference':original['Source (file:line)']}
    if ident in adjudication:
        state=adjudication[ident]['delivery_status'];gap=adjudication[ident]['reason']+' '+gap
    if ident.startswith('REQ-') and 408<=int(ident[4:])<=432 and (HERE/'PROMISE_GAPS_35.json').exists():
        promise=next(x for x in read('PROMISE_GAPS_35.json') if x['promise_id']==original['Rule ID'])
        gap=promise['exact_unproven_or_missing_guarantee'];action=promise['concrete_work_to_deliver'];demo=promise['requirement_specific_closure_scenario']
    allrows.append({
      'review_id':ident,'composite_id':original['composite_id'],'workbook_row':original['workbook_row'],'doc':original['Doc'],'rule_id':original['Rule ID'],'statement':original['Statement'],'product_promise_or_source':original['Promise / Source Document'],'objective':original['Objective'],'registry_authority_status':original['Status'],
      'authority_assessment':r.get('authority_status',r.get('authority',{'source_status':original['Status'],'note':'Not automatically ratified or reopened by this assessment'})),
      'intended_outcome':r.get('intended_outcome',original['Statement']),
      'delivery_status':state,'reviewer_status_raw':original_state,'confidence':confidence,'scope':scope,
      'source':primary_source,'additional_source_evidence':sources,'code_evidence':citations,
      'exact_gap':gap,'required_action':action,'closure_demonstration':demo,
      'dependencies':r.get('dependencies',raw.get('dependencies',[])),
      'evidence_limit':r.get('evidence_limit',r.get('limit',r.get('limits','No new runtime evidence generated. Static scope only.'))),
      'mocked_or_stubbed_note':r.get('mocked_or_stubbed',raw.get('mocked_or_stubbed','See cited body/receipts; no new integration executed')),
      'assessment_pack':pack,'citation_flags':sorted(set(rowissues)),
      'review_outcome':'EVIDENCE_INSUFFICIENT' if rowissues else 'ASSESSED_SCOPED',
    })
    issues.extend({'review_id':ident,'flag':v} for v in sorted(set(rowissues)))

if (HERE/'MAIN_ROW_REFINEMENTS.json').exists():
    refinements=read('MAIN_ROW_REFINEMENTS.json')
    for row in allrows:
        if row['review_id'] in refinements:
            row.update(refinements[row['review_id']])
            row['main_refinement_note']='Sampled uncertainty retained; precise clause-specific assessment added after direct source/body re-read. No new independent runtime proof.'

save('REQUIREMENT_GAPS_648.json',allrows);save('CODE_SOURCE_HASHES.json',filehashes)
save('CITATION_FINDINGS.json',issues)
fields=['review_id','composite_id','workbook_row','statement','registry_authority_status','delivery_status','confidence','exact_gap','required_action','closure_demonstration','citation_flags']
with (HERE/'REQUIREMENT_GAPS_648.csv').open('w') as out:
    w=csv.DictWriter(out,fieldnames=fields);w.writeheader()
    for r in allrows:w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],(dict,list)) else r[k] for k in fields})

product=defaultdict(list)
for r in allrows:
    for match in re.finditer(r'#(\d+)\b',r['product_promise_or_source'] or ''):product[f"P-{int(match[1]):02d}"].append(r['review_id'])
save('PRODUCT_PROMISE_CROSSWALK.json',{'namespace':'Product promise #N, NOT assurance S-N','direct_registry_refs':dict(product),'numbers_1_to_32_without_direct_hash_reference':[f'P-{i:02d}' for i in range(1,33) if f'P-{i:02d}' not in product],'limit':'Absence of a literal#reference is not evidence the promise is missing. Canon body mapping must resolve it.'})
groups=defaultdict(list)
for r in allrows:groups[r['doc']].append(r)
family=[]
for name,items in groups.items():
    family.append({'doc':name,'rows':len(items),'ids':[r['review_id'] for r in items],'status_counts':dict(Counter(r['delivery_status'] for r in items)),'flagged_rows':sum(bool(r['citation_flags']) for r in items)})
save('FAMILY_COVERAGE_56.json',family)
save('COVERAGE_RECEIPT.json',{'primary_required':648,'primary_rows':len(allrows),'primary_unique_keys':len({r['composite_id'] for r in allrows}),'corrected_packs':len(set(x['assessment_pack'] for x in allrows)),'document_families':len(groups),'status_counts':dict(Counter(r['delivery_status'] for r in allrows)),'citation_flags':dict(Counter(x['flag'] for x in issues)),'scope':'648 dispositions, NOT648delivered features or fully verified citations. Citation and semantic limits must remain visible.','no_runtime_tests':True,'no_code_changes':True})
print(json.dumps(read('COVERAGE_RECEIPT.json'),indent=2))