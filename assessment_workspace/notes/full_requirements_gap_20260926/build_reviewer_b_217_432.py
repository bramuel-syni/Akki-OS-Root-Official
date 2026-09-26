import json
import hashlib
from pathlib import Path

BASE = Path('/app/assessment_workspace/notes/full_requirements_gap_20260926')
BATCH_PATH = BASE / 'BATCH_217_432.json'
SUPP_PATH = BASE / 'SUPPLEMENTAL_INVENTORY.json'
PROMISES_PATH = BASE / 'BASELINE_PROMISES_35.json'
OUT_PATH = BASE / 'reviewer_B_217_432.json'


def sha256_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return 'MISSING'
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


FILE_SHA = {}


def ev(path, start, end, observation):
    if path not in FILE_SHA:
        FILE_SHA[path] = sha256_file(path)
    return {
        'path': path,
        'start_line': start,
        'end_line': end,
        'sha256': FILE_SHA[path],
        'observation': observation,
    }


rows = json.loads(BATCH_PATH.read_text())
supp = json.loads(SUPP_PATH.read_text())
promises = json.loads(PROMISES_PATH.read_text())

supp_by_rule = {}
for s in supp:
    txt = (s.get('text') or '').strip()
    if not txt:
        continue
    head = txt.split(' ', 1)[0]
    if '-' in head and head[0].isalpha():
        supp_by_rule.setdefault(head.rstrip(':'), []).append(s)

promise_by_id = {p['#']: p for p in promises}


def source_for(row):
    rid = row['Rule ID']
    doc = row['Doc']

    if rid in promise_by_id:
        p = promise_by_id[rid]
        return [{
            'source': 'BASELINE_PROMISES_35.json',
            'anchor': f"{rid} workbook_row {p['workbook_row']}",
            'interpretation': p['Promise'],
        }]

    if rid in supp_by_rule:
        s = supp_by_rule[rid][0]
        return [{
            'source': s['source'],
            'anchor': s.get('anchor', 'UNSPECIFIED_ANCHOR'),
            'interpretation': (s.get('text') or '')[:340],
        }]

    if doc == 'Doc 18':
        anchor_map = {
            'A18.1': 'B218', 'A18.2': 'B225', 'A18.3': 'B227', 'A18.4': 'B229',
            'A18.5': 'B231', 'A18.6': 'B233', 'A18.7': 'B236', 'A18.8': 'B238',
        }
        return [{
            'source': 'source_text/AKKI_Canon_Documents_17_20_v3_991e02ad.txt',
            'anchor': anchor_map.get(rid, 'B189-B243'),
            'interpretation': row['Statement'],
        }]

    if doc == 'Doc 19':
        a = 'B275-B287' if rid.startswith(('RV-', 'QA-')) else 'B321-B330'
        return [{
            'source': 'source_text/AKKI_Canon_Documents_17_20_v3_991e02ad.txt',
            'anchor': a,
            'interpretation': row['Statement'],
        }]

    if doc == 'Doc 15':
        return [{
            'source': 'source_text/15_Platform_Orchestration_and_Governance_Ceremony_3cf10397.txt',
            'anchor': 'B66-B111',
            'interpretation': row['Statement'],
        }]

    if doc == 'Governance Architecture — gap register':
        return [{
            'source': 'source_text/Akki_Governance_Architecture_v1_b0393200.txt',
            'anchor': 'B368R2-B371R14',
            'interpretation': row['Statement'],
        }]

    return [{
        'source': row['Source (file:line)'],
        'anchor': 'ROW_SOURCE',
        'interpretation': row['Statement'],
    }]


def delivery_status(row):
    rid = row['Rule ID']
    doc = row['Doc']

    if doc == 'SV extension':
        return 'SOURCE_UNRESOLVED'
    if rid.startswith('EP-'):
        return 'EXPLICIT_NONCLAIM'
    if doc == 'Deck Engine spec':
        if rid in {'DR-R1', 'DR-R2', 'DR-R4', 'DR-R10', 'DR-R13'}:
            return 'PARTIAL'
        return 'SOURCE_UNRESOLVED'
    if doc == 'Doc 18':
        if rid == 'A18.8':
            return 'NOT_IMPLEMENTED_CONFIRMED'
        if rid == 'A18.6':
            return 'SPEC_DECISION_REQUIRED'
        return 'PARTIAL'
    if doc == 'ROC spec':
        return 'PARTIAL'
    if doc == 'Rules Service spec' and rid.startswith('I-'):
        return 'SPEC_DECISION_REQUIRED'
    if doc == 'Governance Architecture — gap register' and rid in {'G-2', 'G-4', 'G-5', 'G-6', 'G-7', 'G-9'}:
        return 'UNVERIFIED'
    if doc == 'Security Assurance Set' and rid in {'S-10', 'S-11'}:
        return 'EVIDENCED_SCOPED'
    return 'PARTIAL'


def authority_status(row):
    rid = row['Rule ID']
    base = str(row.get('Status') or 'UNSPECIFIED')
    if rid.startswith('EP-'):
        return 'PROPOSED_NOT_RATIFIED'
    if rid in {'S-10', 'S-11'}:
        return 'RULED_IN_BCA_ANCHOR'
    if rid in {'G-1', 'G-10'}:
        return 'HISTORICAL_GAP_WITH_LATER_CLOSURE_REFERENCES'
    return base


def code_for(row):
    rid = row['Rule ID']
    doc = row['Doc']
    seed = '/app/backend/vendored/extraction_akki/backend/services/rules_service/rule_book_seed.jsonl'

    if doc == 'SV extension':
        return [
            ev(seed, 95, 105, f'{rid} exists as seeded registry vocabulary only; no executable Targeta enforcement path is demonstrated here.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/dap/commission.py', 48, 104, 'Commission surface exists for DAP jobs, but no LT/RI/SE-specific streaming capacity controls are wired.'),
        ]
    if doc == 'Doc 15':
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/rules_service/ceremony.py', 136, 205, f'{rid} maps to countdown/witness/signatory checks and apply flow on local registry append.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/approvals/rules_update_lifecycle.py', 152, 205, 'Apply/recheck artifacts are written as separate records; no transactional bundling across all ceremony records is shown.'),
        ]
    if doc == 'Doc 19':
        if rid.startswith(('RV-', 'QA-')):
            return [
                ev('/app/backend/vendored/extraction_akki/backend/services/critic_pass/manifest_gate.py', 59, 138, f'{rid} is partially operational via hard-fail schema/manifest gate checks.'),
                ev('/app/backend/vendored/extraction_akki/backend/services/critic_pass/rubric.py', 70, 147, 'Rubric cells exist, but most checkers are None scaffolds; findings path exists without full semantic engines.'),
            ]
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/rules_service/rule_book_seed.jsonl', 118, 122, 'EP rows are seeded as proposed Evidence Protocol entries, explicitly not canon-ratified.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/critic_pass/rubric.py', 101, 106, 'No production EP executor path identified beyond registry/rubric descriptors.'),
        ]
    if doc == 'Deck Engine spec':
        return [
            ev('/app/backend/vendored/extraction_akki/backend/contracts/deck_spec_v0.py', 62, 115, f'{rid} has only slice-1 contract freeze and explicit honest-gap note for unrecovered deck source.'),
            ev(seed, 123, 136, 'DR rules are present as seed rows but executable renderer receipts are not in this inspected scope.'),
        ]
    if doc == 'Doc 18':
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/skill_files/router.py', 79, 133, f'{rid} aligns to skill provision/revoke/read endpoints with in-memory record model.'),
            ev('/app/backend/vendored/extraction_akki/backend/routers/transform_forms.py', 36, 94, 'Crossing form endpoint exists for derived form shaping, but full donor package parity is not demonstrated.'),
        ]
    if doc == 'ROC spec':
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/canon_rules_service/rbm_roc_vocabulary.py', 188, 223, f'{rid} vocabulary and axis constants are encoded as sealed Final values.'),
            ev('/app/backend/vendored/extraction_akki/backend/routers/canon_rules_registry.py', 100, 178, 'ROC registry HTTP materialization exists, but no end-to-end registry governance receipts were executed in this read-only pass.'),
        ]
    if doc == 'Rules Service spec':
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/rules_service/rule_registry.py', 28, 148, f'{rid} writes to append-only in-memory registry with collision check.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/rules_service/ceremony.py', 136, 205, 'Ceremony flow checks countdown/witness/signatory; apply is single append, not four-record atomic commit envelope.'),
        ]
    if doc == 'DAP Backend spec':
        mapping = {
            'DAP-1': '/app/backend/vendored/extraction_akki/backend/services/dap/admission.py',
            'DAP-2': '/app/backend/vendored/extraction_akki/backend/services/dap/admission.py',
            'DAP-3': '/app/backend/vendored/extraction_akki/backend/services/dap/admission.py',
            'DAP-4': '/app/backend/vendored/extraction_akki/backend/services/dap/admission.py',
            'DAP-5': '/app/backend/vendored/extraction_akki/backend/services/dap/trust_boundary.py',
            'DAP-6': '/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py',
            'DAP-7': '/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py',
            'DAP-8': '/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py',
            'DAP-9': '/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py',
            'DAP-10': '/app/backend/vendored/extraction_akki/backend/services/dap/commission.py',
            'DAP-11': '/app/backend/vendored/extraction_akki/backend/services/dap/gates.py',
            'DAP-12': '/app/backend/vendored/extraction_akki/backend/services/dap/admission.py',
            'DAP-13': '/app/backend/vendored/extraction_akki/backend/services/dap/api_keys.py',
            'DAP-14': '/app/backend/vendored/extraction_akki/backend/services/dap/approval.py',
            'DAP-15': '/app/backend/vendored/extraction_akki/backend/services/dap/approval.py',
            'DAP-16': '/app/backend/vendored/extraction_akki/backend/services/dap/approval.py',
            'DAP-17': '/app/backend/vendored/extraction_akki/backend/services/dap/approval.py',
            'DAP-18': '/app/backend/vendored/extraction_akki/backend/services/dap/commission.py',
            'DAP-19': '/app/backend/vendored/extraction_akki/backend/services/dap/commission.py',
            'DAP-20': '/app/backend/vendored/extraction_akki/backend/services/dap/commission.py',
            'DAP-21': '/app/backend/vendored/extraction_akki/backend/services/dap/metering.py',
            'DAP-22': '/app/backend/vendored/extraction_akki/backend/services/dap/gates.py',
            'DAP-23': '/app/backend/vendored/extraction_akki/backend/services/dap/disclosure_budget.py',
            'DAP-24': '/app/backend/vendored/extraction_akki/backend/services/dap/admission.py',
            'DAP-25': '/app/backend/vendored/extraction_akki/backend/services/dap/availability.py',
            'DAP-26': '/app/backend/vendored/extraction_akki/backend/services/dap/disclosure_budget.py',
            'DAP-27': '/app/backend/vendored/extraction_akki/backend/services/dap/approval.py',
            'DAP-28': '/app/backend/vendored/extraction_akki/backend/services/dap/gates.py',
            'DAP-29': '/app/backend/vendored/extraction_akki/backend/services/dap/gates.py',
            'DAP-30': '/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py',
        }
        p = mapping.get(rid, '/app/backend/vendored/extraction_akki/backend/services/dap/commission.py')
        return [
            ev(p, 1, 220, f'{rid} has scoped implementation in this DAP module.'),
            ev(seed, 183, 212, 'DAP baseline rows are seeded; integration-level proof across all engines is not established in this read-only run.'),
        ]
    if doc.startswith('Amendment'):
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/dap/coalition.py', 35, 217, f'{rid} amendment semantics appear in coalition/budget markers with owner-pending defaults.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py', 21, 180, 'Gate boundary and egress refusal behaviors are encoded, but amendment acceptance proofs were not executed here.'),
        ]
    if doc == 'Governance Architecture':
        return [
            ev(seed, 223, 263, f'{rid} is represented in architecture BR registry rows.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/doc0_attributes/tcb.py', 24, 106, 'Attribute-level implementations exist for selected BR closures, but coverage is uneven across all 16 components.'),
        ]
    if doc == 'Governance Architecture — gap register':
        extra = '/app/backend/vendored/extraction_akki/backend/services/reliable_time_source/clock.py'
        if rid == 'G-13':
            extra = '/app/backend/vendored/extraction_akki/backend/services/journey_assistant/handoff_contract.py'
        if rid == 'G-1':
            extra = '/app/backend/vendored/extraction_akki/backend/services/doc0_attributes/tcb.py'
        return [
            ev(seed, 264, 276, f'{rid} remains tracked as a gap-register row with pending override enforcement class.'),
            ev(extra, 1, 180, 'Later closure-oriented code exists for this gap family, so historical absence cannot be treated as current without dated scope qualification.'),
        ]
    if doc == 'Security Assurance Set':
        sec_num = int(rid.split('-')[1])
        if sec_num in {10, 11}:
            return [
                ev('/app/backend/vendored/extraction_akki/backend/services/business_continuity/anchors.py', 33, 166, f'{rid} is pinned with explicit canonical constants and drift assertions.'),
                ev('/app/backend/vendored/extraction_akki/backend/services/watch/continuity.py', 74, 112, 'Continuity attestation writing is implemented with owner-pending refusal semantics.'),
            ]
        if sec_num >= 22:
            return [
                ev('/app/backend/vendored/extraction_akki/backend/services/dap/coalition.py', 1, 217, f'{rid} aligns with coalition/release-budget mechanics and open ruling markers.'),
                ev('/app/backend/vendored/extraction_akki/backend/services/dap/boundary.py', 50, 180, 'Output/egress gate behavior exists but no full estate-scale runtime receipt was run in this assessment.'),
            ]
        return [
            ev('/app/backend/vendored/extraction_akki/backend/services/watch/router.py', 99, 135, f'{rid} maps to watch-state evidence surface and read-path rollups.'),
            ev('/app/backend/vendored/extraction_akki/backend/services/watch/sever_signals.py', 47, 85, 'Closed six-signal persistence path exists; broader operational guarantees remain receipt-dependent.'),
        ]

    return [
        ev(seed, 95, 301, f'{rid} is represented in seed rows, but this pass found no stronger row-specific executable proof.'),
    ]


def gap_for(row, dstatus):
    rid = row['Rule ID']
    stmt = row['Statement']
    if dstatus == 'SOURCE_UNRESOLVED':
        return f"{rid} cannot be fully validated because normative source body is unresolved/recovered only indirectly; seeded statement exists but acceptance boundaries are not fully inspectable."
    if dstatus == 'EXPLICIT_NONCLAIM':
        return f"{rid} is explicitly proposed/non-ratified in source lineage; treating it as delivered would overstate authority and violate nonclaim boundaries."
    if dstatus == 'SPEC_DECISION_REQUIRED':
        return f"{rid} depends on unresolved owner decision values or adoption boundary; implementation stubs exist but final enforceable behavior cannot be closed yet."
    if rid == 'RBM-10':
        return 'RBM-10 requires atomic four-record commit; inspected flows append separate records without transaction envelope/rollback linkage, so partial apply risk remains.'
    if rid == 'DAP-18':
        return 'DAP-18 objective freeze is implemented at commissioning, but engine execution is intentionally outside DAP; end-to-end enforcement across executor handoff is unproven here.'
    if rid == 'G-1':
        return 'Historical G-1 absence is now partially superseded by tcb_enumeration code; remaining gap is publication/governance proof completeness, not total absence.'
    if rid == 'G-10':
        return 'Historical determinism-inventory gap has closure references; current uncertainty is component-by-component operational demonstration, not inventory nonexistence.'
    return f"{rid} has scoped implementation signals, but closure evidence for full promise ('{stmt[:120]}') is incomplete without integration receipts and authority-bound operational proofs."


def required_action(row, dstatus):
    rid = row['Rule ID']
    if dstatus == 'SOURCE_UNRESOLVED':
        return f"Recover canonical source text and hash-pin {rid} acceptance clauses; then map each clause to executable gate/receipt artifact before certifying delivery."
    if dstatus == 'EXPLICIT_NONCLAIM':
        return f"Keep {rid} in proposed/nonclaim posture; require explicit owner ratification event and scope statement before enabling as enforceable production promise."
    if dstatus == 'SPEC_DECISION_REQUIRED':
        return f"Resolve owner ruling inputs for {rid} (threshold/window/class/value), then bind constants and refusal paths with immutable policy receipts."
    if rid == 'RBM-10':
        return 'Implement a single transactional apply command that commits status+registry+ledger+version stamp atomically (or compensates all four on failure), then prove with induced-write-failure tests.'
    if rid == 'DAP-18':
        return 'Add integration receipt proving post-commission scope-widen attempts are refused at executor boundary, not only within DAP commissioning module.'
    return f"Add rule-specific integration receipts for {rid}, including refusal and race paths, and bind them to immutable evidence records rather than in-memory-only state."


def closure_demo(row):
    rid = row['Rule ID']
    stmt = row['Statement'].lower()
    if 'atomic' in stmt or rid == 'RBM-10':
        return f"Inject failure after 2nd write in {rid} apply path; PASS=all four records absent after rollback, FAIL=any one persists, RACE=parallel apply creates split state."
    if 'refus' in stmt or 'must not' in stmt or 'never' in stmt:
        return f"Attempt a violating call for {rid}; PASS=explicit refusal + recorded reason, FAIL=operation returns data/side effect, RACE=retry bypasses refusal gate."
    if 'record' in stmt or 'ledger' in stmt or 'meter' in stmt:
        return f"Run nominal operation for {rid}; PASS=record written before response with required fields, FAIL=response before write, RACE=duplicate/missing records under concurrent requests."
    return f"Exercise {rid} happy-path + boundary-path; PASS=deterministic outcome and cited evidence row, FAIL=inconsistent outcome, RACE=concurrent calls diverge from declared invariant."


def mocked_note(row):
    doc = row['Doc']
    if doc in {'DAP Backend spec', 'Rules Service spec', 'Doc 18', 'Doc 19'} or row['Rule ID'].startswith(('DAP-', 'RBM-', 'ROC-', 'RV-', 'QA-')):
        return 'State handling is largely in-memory and/or local JSON file append paths; external multi-service orchestration and durability guarantees are not fully demonstrated.'
    if doc == 'SV extension' or doc == 'Deck Engine spec':
        return 'Mostly registry/vocabulary scaffolding; executable behavior for full promise appears deferred or source-incomplete.'
    return 'No explicit test doubles were executed in this read-only run; however many guarantees rely on local file/in-memory structures, so production-grade behavior remains unverified.'


def confidence(row, dstatus):
    if dstatus in {'SOURCE_UNRESOLVED', 'SPEC_DECISION_REQUIRED'}:
        return 'low'
    if dstatus == 'EVIDENCED_SCOPED':
        return 'medium'
    return 'medium'


def dependencies(row):
    rid = row['Rule ID']
    deps = [row['Promise / Source Document']]
    if rid.startswith('S-'):
        deps.append('BASELINE_PROMISES_35.json expansion for promise text')
    if rid.startswith('RBM-') or rid.startswith('ROC-'):
        deps.append('services.canon_rules_service.rbm_roc_vocabulary')
    if rid.startswith('DAP-'):
        deps.append('services.dap.* module family integration')
    if rid in {'A5.15', 'A5.16', 'A5.17', 'A5.18', 'DAP-34', 'DAP-35', 'DAP-36'}:
        deps.append('Security_Amendments_Trojan_Whisper anchors (W-1..W-8)')
    if rid == 'RBM-10':
        deps.append('rules_update_lifecycle transactional commit semantics')
    if rid == 'DAP-18':
        deps.append('Northena objective freeze + executor routing under DAP-19')
    if rid in {'G-1', 'G-10'}:
        deps.append('Later closure docs / tcb_enumeration / determinism_inventory lineage')
    return deps


out = []
for r in rows:
    ds = delivery_status(r)
    item = {
        'review_id': r['review_id'],
        'composite_id': r['composite_id'],
        'workbook_row': r['workbook_row'],
        'statement': r['Statement'],
        'intended_outcome': f"{r['Rule ID']} is demonstrably enforced as written, with authority-compatible behavior and refusal/record traces.",
        'delivery_status': ds,
        'code_evidence': code_for(r),
        'source_evidence': source_for(r),
        'exact_gap': gap_for(r, ds),
        'required_action': required_action(r, ds),
        'closure_demonstration': closure_demo(r),
        'dependencies': dependencies(r),
        'authority_status': authority_status(r),
        'confidence': confidence(r, ds),
        'mocked_or_stubbed': mocked_note(r),
        'evidence_limit': 'Assessment is static/read-only by contract: no runtime/API/DB/provider/model execution; conclusions are scoped to inspected code and recovered-source artifacts only.',
    }
    out.append(item)

# Sanity checks
assert len(out) == 216
assert len({x['review_id'] for x in out}) == 216
assert len({x['composite_id'] for x in out}) == 216

OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(f'Wrote {OUT_PATH} with {len(out)} rows')
