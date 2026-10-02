"""Owner order 2026-10-02: lower the admission floor for Luhya (Wanga) only, to 75%, and admit the completed v3 run. Idempotent;
records the revision on the sign-off register and in the run's thread as the demo operator."""
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv  # noqa: E402

load_dotenv('/app/backend/.env')

from services.training_lab import conversation, signoff, store as lab  # noqa: E402

RUN_ID, LANGUAGE, FLOOR = 'reinforcement-lwg-v3', 'lwg', signoff.LANGUAGE_FLOORS['lwg']


def main():
    user = lab.db().users.find_one({'email': 'demo.operator@demo.rms.example.com'}, {'_id': 1})
    actor = {'tenant_id': 'RMS', 'principal_id': str(user['_id']) if user else 'owner-order-20261002'}
    before = signoff.get('RMS', RUN_ID)
    if not before: raise SystemExit('v3 sign-off record not found')
    already = (before.get('acceptance_revision') or {}).get('language_floors', {}).get(LANGUAGE) == FLOOR
    record = signoff.admit_language_scoped('RMS', actor, RUN_ID, LANGUAGE, FLOOR, signoff.LUHYA_ORDER)
    outcome = record['outcome']
    print('decision', outcome['decision'], outcome.get('scope'), 'floor', outcome.get('floor'))
    for reason in outcome['reasons']: print(' -', reason)
    if not already:
        conversation.record('RMS', RUN_ID, conversation.decision('RMS', 'Lower the Luhya (Wanga) floor to 75% and admit', action='admit_language_scoped', value=f'{LANGUAGE}:{FLOOR}'),
                            conversation.note('RMS', f"Done by your order: the floor for Luhya (Wanga) alone is now 75% — every other language keeps 90%. Against that floor this run's 75.8% on judged windows is met, so it is admitted for Luhya (Wanga) only: Wanga decisions route to this checkpoint, every other language stays with the reference baseline. "
                                                     "The other readings on the run — regressions on Ekegusii, Kikamba, Gikuyu, Kalenjin, Dholuo and Kiswahili and the served-output speaker probe above chance — stay on the record exactly as measured; they are not conditions of this admission.",
                                              widget='checks', origin='owner-order', signoff={'plan_sha256': record['plan_sha256'], 'revision': record['revisions'][-1]['at']}))
        print('thread note recorded')


if __name__ == '__main__':
    main()
