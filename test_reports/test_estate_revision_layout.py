"""Final targeted checks against actual frozen native build, not synthetic output."""
import json
from pathlib import Path

ROOT = Path('/app/assessment_workspace/phase0/doc_studio_state/RMS/com-1f3a3606e140')


def documents():
    record = json.loads((ROOT / 'record.json').read_text())
    version = ROOT / f"v{record['current_content_version']}"
    content = json.loads((version / 'content.json').read_text())
    deck = json.loads((version / 'deck.json').read_text())
    plan = json.loads((ROOT / 'builds' / record['builds'][-1]['build_id'] / 'a/resolved/deck.resolved.json').read_text())
    return content, deck, plan


def test_pagination_preserves_all_requested_rows_and_fits_zones():
    content, deck, plan = documents()
    for table_id, table in content['tables'].items():
        requested = [s for s in deck['slides'] if s.get('table_ref') == table_id]
        if not requested:
            continue
        pages = [s for s in plan['slides'] if s['type'] == 'table' and s['table']['id'] == table_id]
        expected = sum(len(table['rows'][s.get('rows_from', 0):s.get('rows_to')]) for s in requested)
        assert sum(len(s['table']['rows']) for s in pages) == expected
        for s in pages:
            assert sum(s['table']['row_heights']) <= s['zones']['table']['h'] + 0.001
            assert len(s['table']['rows']) <= 9
    assert [s['n'] for s in plan['slides']] == list(range(1, len(plan['slides']) + 1))


def test_coverage_and_receipts_preserved_without_overflow():
    content, _, plan = documents()
    coverage = [s for s in plan['slides'] if s['type'] == 'coverage_limits']
    assert [g for s in coverage for g in s['coverage']['cannot_say']] == content['coverage']['cannot_say']
    for s in coverage:
        c = s['coverage']
        assert c['cover_height'] + 0.55 + sum(c['row_heights']) + len(c['row_heights']) * 0.1 <= s['zones']['body']['h'] + 0.001
    receipts = [r for s in plan['slides'] if s['type'] == 'appendix' for r in s['receipts']]
    assert {r['id']: r['text'] for r in receipts} == {k: v['resolves_to'] for k, v in content['receipts'].items()}


def test_final_editorial_findings_are_corrected_and_tokens_exist():
    content, _, _ = documents()
    claims = content['claims']
    assert 'one bounded product pilot' in claims['C909']['text']
    assert 'forecasting' in claims['C1034']['text'] and 'transaction analytics' in claims['C1034']['text']
    assert 'unknown classes are assumed' not in claims['C1023']['text'].lower()
    assert 'No invoice-backed baseline was available to the census' in claims['C1069']['text']
    assert 'separate' in claims['C1025']['text']
    assert 'accessible material now' in claims['C909']['text']
    for token in ('F015', 'F018', 'F009', 'F082'):
        assert token in content['facts'] and content['facts'][token]['receipt'] in content['receipts']