"""Mα iteration 90: speaker-cluster-level reseal (split v2), audit v2 independence, preflight with the native-review panel, and the review workflow."""
import hashlib
import json
import os
import random
import sys
import uuid

import pytest
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.training_lab import malpha_corpus_audit as audit  # noqa: E402
from services.training_lab import malpha_evaluation as me  # noqa: E402
from services.training_lab import malpha_review as review  # noqa: E402
from services.training_lab import malpha_splits as splits  # noqa: E402
from services.training_runner import m9_dispatch  # noqa: E402


def _corpus(seed=7, presenters=3, callers=60, sessions=40):
    """Radio-like synthetic metadata: a few presenters in every session, many callers in one or two sessions, brand mentions sprinkled."""
    rng = random.Random(seed); rows = []; clusters = {}
    for s in range(sessions):
        session = f'S{s:03d}'
        speakers = [f'P{p}' for p in range(presenters)] + [f'C{c}' for c in rng.sample(range(callers), 4)]
        for sp in speakers:
            clusters[f'{session}|{sp}'] = (1000 + int(sp[1:])) if sp[0] == 'P' else (2000 + int(sp[1:]))
            for k in range(rng.randint(6, 14)):
                words = rng.choice(['a b', 'habari ya leo', 'safaricom ni bora kabisa sana', 'nunua tusker leo jioni', 'karibu tena rafiki yangu', 'x'])
                text_hash = hashlib.sha256(f'{words}:{rng.random() if rng.random() > 0.02 else ""}'.encode()).hexdigest()  # a few exact repeats, as in radio
                rows.append({'seg_id': hashlib.sha256(f'{session}:{sp}:{k}'.encode()).hexdigest()[:16], 'session': session, 'speaker': sp, 'start': k * 5.0, 'end': k * 5.0 + 4.0,
                             'words': len(words.split()), 'text_sha256': text_hash, 'mentions': ['Safaricom'] if 'safaricom' in words else ['Tusker'] if 'tusker' in words else [],
                             'features': {'duration_s': 4.0}, 'pcm_offset': 0, 'pcm_bytes': 128000, 'split': 'train'})
    for r in rows[:5]: r['speaker'] = 'UNK'; clusters.pop(f"{r['session']}|{r['speaker']}", None)  # unknown-speaker rows
    twins = []
    for r in rows[10:16]:  # overlapping speech: a presenter talks over a caller on the same audio window (same seg_id, another speaker)
        twins.append({**r, 'speaker': 'P0', 'mentions': []}); clusters[f"{r['session']}|P0"] = 1000
    rows.extend(twins)
    return rows, clusters


def test_cluster_level_reseal_is_speaker_disjoint_and_excludes_unknowns():
    rows, clusters = _corpus()
    rep = splits.cluster_level_reseal(rows, clusters, 20261004, 'swa')
    adm = [r for r in rows if r['split'] == 'admission']; train = [r for r in rows if r['split'] == 'train']; dev = [r for r in rows if r['split'] == 'dev']
    assert adm and train and dev
    adm_clusters = {clusters[f"{r['session']}|{r['speaker']}"] for r in adm}
    other_clusters = {clusters.get(f"{r['session']}|{r['speaker']}") for r in train + dev} - {None}
    assert not adm_clusters & other_clusters, 'admission speakers must never appear in train or dev'
    assert all(c >= 2000 for c in adm_clusters), 'presenters (many sessions) are never held out'
    assert all(r['split'] == 'excluded_unknown_speaker' for r in rows if r['speaker'] == 'UNK')
    substantive_adm = {r['text_sha256'] for r in adm if r['words'] >= splits.SUBSTANTIVE_WORDS}
    assert not any(r['text_sha256'] in substantive_adm for r in train + dev if r['words'] >= splits.SUBSTANTIVE_WORDS)
    assert rep['admission']['segments'] == len(adm) and rep['admission']['positives'] == sum(bool(r['mentions']) for r in adm)
    assert rep['protocol'] == splits.SPLIT_PROTOCOL_V2 and rep['dev']['basis'] == 'session_holdout'
    by_window = {}
    for r in rows: by_window.setdefault(r['seg_id'], set()).add(r['split'])
    assert all(len(v) == 1 for v in by_window.values()), 'rows sharing an audio window share a split'
    assert not any('admission' in v and len({clusters.get(f"{x['session']}|{x['speaker']}") for x in rows if x['seg_id'] == k}) > 1 for k, v in by_window.items()), 'no admission window carries a non-admission speaker'
    assert rep['duplicate_audio_windows'] >= 6


def test_reseal_retains_legacy_admission_and_is_deterministic():
    rows, clusters = _corpus()
    legacy = [r for r in rows if r['session'] == 'S001' and r['speaker'] == 'C7']
    for r in legacy: r['split'] = 'admission'
    rep1 = splits.cluster_level_reseal([dict(r) for r in rows], clusters, 1, 'kik')
    rows2 = [dict(r) for r in rows]; rep2 = splits.cluster_level_reseal(rows2, clusters, 1, 'kik')
    assert rep1 == rep2
    if legacy:
        assert all(r['split'] in ('admission', 'excluded_overlapping_speech') for r in rows2 if r['speaker'] == 'C7' and r['session'] == 'S001')
    rows3 = [dict(r) for r in rows2]; rep3 = splits.cluster_level_reseal(rows3, clusters, 1, 'kik')  # re-run from an already cluster-sealed state keeps the same small clusters
    assert rep3['admission']['segments'] == rep2['admission']['segments'] and [r['split'] for r in rows3] == [r['split'] for r in rows2]


def test_reseal_reports_short_support_instead_of_inventing_it():
    rows, clusters = _corpus(seed=3, callers=6, sessions=6)
    rep = splits.cluster_level_reseal(rows, clusters, 5, 'kam')
    assert rep['admission']['targets_met'] is False
    assert rep['admission']['positives'] < splits.RESEAL_TARGETS['admission']['positives']


def test_audit_v2_verifies_independence_only_under_the_v2_rule():
    rows, clusters = _corpus()
    splits.cluster_level_reseal(rows, clusters, 20261004, 'swa')
    seal = hashlib.sha256(json.dumps(sorted(r['seg_id'] for r in rows if r['split'] == 'admission')).encode()).hexdigest()
    v2 = audit.inspect_language(rows, clusters, seal, splits.SPLIT_PROTOCOL_V2)
    assert v2['seal_matches'] and v2['admission_independence_verified'] is True
    assert v2['overlap_counts']['train_admission']['speaker_clusters'] == 0 and v2['overlap_counts']['train_admission']['substantive_text_hashes'] == 0
    assert v2['overlap_counts']['train_admission']['recording_sessions'] > 0, 'channel overlap is expected and disclosed'
    assert v2['excluded']['unknown_speaker'] == 5
    v1 = audit.inspect_language(rows, clusters, seal, None)
    assert v1['admission_independence_verified'] is False, 'the v1 rule counts session overlap as leakage'
    assert audit.inspect_language(rows, clusters, 'f' * 64, splits.SPLIT_PROTOCOL_V2)['admission_independence_verified'] is False


def _records(seals, support_ok=True, independence=True):
    sup = {l: {'positive_segments': 120 if support_ok else 20, 'negative_segments': 150, 'recording_groups': 25, 'targets_met': support_ok} for l in ('kik', 'kam', 'swa')}
    reseal = {'job_id': 'm9j-' + 'a' * 12, 'phase': 'malpha_aip_reseal', 'status': 'completed', 'result': {'seals': {l: {'admission_seg_ids_sha256': seals[l]} for l in seals}, 'support': sup, 'split_version': 2}}
    per = {l: {'admission_seal_sha256': seals[l], 'support': me.population_support(sup[l]['positive_segments'], sup[l]['negative_segments'], sup[l]['recording_groups'])} for l in seals}
    aud = {'job_id': 'm9j-' + 'b' * 12, 'phase': 'malpha_corpus_audit', 'status': 'completed', 'result': {'per_language': per, 'independence_verified': independence, 'reference_verified': False}}
    return [reseal, aud]


def test_preflight_requires_verified_panel_for_the_same_seal_set():
    seals = {l: hashlib.sha256(l.encode()).hexdigest() for l in ('kik', 'kam', 'swa')}
    records = _records(seals)
    pf = me.admission_preflight(records)
    assert pf['independence_verified'] is True and pf['reference_verified'] is False and pf['ready'] is False and pf['split_version'] == 2
    panel = {'panel_id': pf['panel_id'], 'verified': True, 'status': 'verified', 'per_language': {}}
    assert me.admission_preflight(records, reference_panel=panel)['ready'] is True
    assert me.admission_preflight(records, reference_panel={**panel, 'panel_id': 'other'})['ready'] is False
    assert me.admission_preflight(records, reference_panel={**panel, 'verified': False})['ready'] is False
    assert me.admission_preflight(_records(seals, support_ok=False), reference_panel=panel)['ready'] is False
    assert me.admission_preflight(_records(seals, independence=False), reference_panel=panel)['ready'] is False


def test_dispatch_contract_accepts_reseal_and_reference_labels_and_refuses_bad_shapes():
    host = m9_dispatch.hosts()[0]; root = os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']
    common = {'commission_id': 'LISTEN-KIK-KAM-SWA', 'languages': ['kik', 'kam', 'swa'], 'gpu_index': 0, 'budget_mode': 'uncapped_until_billing', 'owner_order_ref': 'o', 'seed': 1, 'iteration': 0, 'aip_db_dir': f'{root}/malpha/aip_db_v1'}
    m9_dispatch.validate('malpha_aip_reseal', {**common, 'lab_corpus_root': root, 'split_version': splits.SPLIT_VERSION}, host)
    with pytest.raises(ValueError): m9_dispatch.validate('malpha_aip_reseal', {**common, 'lab_corpus_root': '/tmp/x', 'split_version': 2}, host)
    with pytest.raises(ValueError): m9_dispatch.validate('malpha_aip_reseal', {**common, 'lab_corpus_root': root, 'split_version': '2'}, host)
    ev = {**common, 'artefact_path': f"{os.environ['M9_REMOTE_ROOT']}/jobs/x/artefact/model.pt", 'artefact_sha256': 'c' * 64, 'brand_lexicon': [{'brand': 'B', 'aliases': ['b']}], 'admission_target': 0.9, 'trained_job_id': 'm9j-' + 'd' * 12, 'split_version': 2}
    m9_dispatch.validate('malpha_evaluate', {**ev, 'reference_labels': {'a' * 16: ['B']}}, host)
    with pytest.raises(ValueError): m9_dispatch.validate('malpha_evaluate', {**ev, 'reference_labels': {'bad': ['B']}}, host)
    with pytest.raises(ValueError): m9_dispatch.validate('malpha_listener_train', {**common, 'recipe': {'max_steps': 10}, 'brand_lexicon': [{'brand': 'B', 'aliases': ['b']}], 'reference_labels': {}}, host)


@pytest.fixture
def mongo_panel():
    suffix = uuid.uuid4().hex[:8]
    result = {'seals': {l: {'admission_seg_ids_sha256': hashlib.sha256(f'{suffix}{l}'.encode()).hexdigest()} for l in ('kik', 'kam', 'swa')}, 'split_version': 2, 'aip_db_dir': f"{os.environ['LANGUAGE_COGNITION_REMOTE_ROOT']}/malpha/aip_db_v1",
              'confirmation_panel': {l: [{'seg_id': hashlib.sha256(f'{suffix}{l}{i}'.encode()).hexdigest()[:16], 'session': 'S1', 'start': 0.0, 'end': 4.0, 'duration_s': 4.0, 'pcm_offset': 0, 'pcm_bytes': 128000, 'transcript_mentions': ['Tusker'] if i else [], 'stratum': 'positive' if i else 'negative'} for i in range(2)] for l in ('kik', 'kam', 'swa')}}
    panel = review.open_panel(result, 'akki-vm')
    yield panel, result
    review.db().malpha_review_tasks.delete_many({'panel_id': panel['panel_id']}); review.db().malpha_review_panels.delete_one({'panel_id': panel['panel_id']})


def test_review_workflow_double_annotation_adjudication_and_reference(mongo_panel):
    panel, _ = mongo_panel; pid = panel['panel_id']
    assert panel['tasks_created'] == 6 and panel['verified'] is False
    assert review.open_panel(mongo_panel[1], 'akki-vm')['tasks_created'] == 0, 'idempotent'
    t = review.next_task(pid, 'rev-a', 'kik'); assert t and 'transcript_mentions' not in t and 'pcm_offset' not in t
    names = {'Tusker', 'Safaricom'}
    with pytest.raises(ValueError): review.annotate(t['task_id'], 'rev-a', [], False, False, names)
    with pytest.raises(ValueError): review.annotate(t['task_id'], 'rev-a', ['Nope'], False, False, names)
    assert review.annotate(t['task_id'], 'rev-a', ['Tusker'], False, False, names)['status'] == 'partial'
    with pytest.raises(ValueError): review.annotate(t['task_id'], 'rev-a', ['Tusker'], False, False, names)
    assert review.next_task(pid, 'rev-a', 'kik')['task_id'] != t['task_id'], 'a reviewer never gets the same segment twice'
    assert review.annotate(t['task_id'], 'rev-b', ['Tusker'], False, False, names)['status'] == 'agreed'
    with pytest.raises(ValueError): review.annotate(t['task_id'], 'rev-c', ['Tusker'], False, False, names)
    for lang in ('kik', 'kam', 'swa'):
        for task in review.tasks(pid, lang, 'open'):
            review.annotate(task['task_id'], 'rev-a', [], True, False, names); review.annotate(task['task_id'], 'rev-b', ['Safaricom'], False, False, names)
    p = review.panel(pid); assert p['verified'] is False and sum(v['disagreement'] for v in p['per_language'].values()) == 5
    assert review.reference_labels(pid) == {}, 'no reference until every task is final'
    dis = [x for x in review.tasks(pid, None, 'disagreement')]
    with pytest.raises(ValueError): review.adjudicate(dis[0]['task_id'], 'rev-a', ['Safaricom'], names)
    for d in dis: review.adjudicate(d['task_id'], 'rev-owner', [], names)
    p = review.panel(pid); assert p['verified'] is True and p['status'] == 'verified' and all(v['complete'] for v in p['per_language'].values())
    ref = review.reference_labels(pid); assert len(ref) == 6 and sorted(ref.values(), key=len)[-1] == ['Tusker']
    pf = me.admission_preflight(_records({l: mongo_panel[1]['seals'][l]['admission_seg_ids_sha256'] for l in ('kik', 'kam', 'swa')}), reference_panel=p)
    assert pf['ready'] is True and pf['reference_verified'] is True
