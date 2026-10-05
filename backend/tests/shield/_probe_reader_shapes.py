"""Read-only quality/latency probe of the contained reader on realistic SYNTHETIC payload shapes (WP-A4 design input)."""
import json
import sys
import time

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.synisense.shield import contained_reader as cr  # noqa: E402
from services.synisense.shield import semantic_register as reg  # noqa: E402

CATS = [{'name': c['name'], 'description': c.get('description') or ''} for c in reg.categories('RMS') if c['kind'] == 'contextual']
print('CATS', [c['name'] for c in CATS])
SAMPLES = {
    'harmless_system': 'You are Akki, a governed answerer. You may use ONLY the qualified units supplied in the window. Every statement must be supported by those units. Reply with one JSON object and nothing else. The project is internal; token accounting applies to every reply; schema keys: answer, cited_units, sufficient, unsupported.',
    'chat_prompt_window': 'OBJECTIVE (frozen for this session): Identify the topics of interest in farmer training questions\n\nQUESTION: Which of those were about minerals specifically?\n\nWINDOW (2 whole qualified units, one JSON per line):\n{"unit_id": "u1", "text": "Farmer asked which mineral lick suits dairy cows in the dry season", "region": "digicow.training_questions"}\n{"unit_id": "u2", "text": "Question about feeding napier grass with maize bran", "region": "digicow.training_questions"}',
    'doc_studio_brief': json.dumps({'task': 'author_estate_pack', 'brief': {'report_scope': 'Lead with answers about what the estate holds', 'audience': 'board', 'constraints': ['no invented figures', 'cite receipts']}, 'facts': [{'id': 'F130', 'value': '500,290 hours', 'label': 'estate forecast total'}], 'internal_notes': 'project Papaya Comet reserve fee KES 147300; uplift 0.73 times the rival floor', 'schema': {'sections': [{'title': 'str', 'body': 'str'}]}}),
    'swahili_contract': 'MKATABA WA HUDUMA (SYNTHETIC). Mteja: Ushirika wa Majaribio wa Nuru Orchard. Ada ya kuhifadhi ni KES 147,300 kwa mwezi na fomula ya ongezeko ni mara 0.73 ya bei ya chini ya mshindani. Jina la mradi wa ndani: Papaya Comet. Tafadhali andaa muhtasari wa kurasa moja.',
    'audit_excerpt_indirect': 'Audit note (SYNTHETIC): the counterparty is the only cooperative in Nyeri exporting macadamia to one Dutch buyer, so naming the county and the crop identifies it. Their margin is thinner than disclosed to lenders; the board has not been told. Prepare a neutral summary for the external reviewer.',
}
for name, text in SAMPLES.items():
    t0 = time.monotonic()
    try:
        out = cr.read(text, CATS, f'wp_a4_probe:{name}')
        r = out['reading']
        print(name, '| host_s', out['seconds'], '| wall', round(time.monotonic() - t0, 1), '| privileged', [(p['category'], p['span'][:40]) for p in r['privileged']], '| indirect', r['indirect_disclosures'][:3], '| coherent', r['objective']['coherent'])
    except Exception as exc:  # noqa: BLE001
        print(name, '| FAILED', round(time.monotonic() - t0, 1), str(exc)[:300])
