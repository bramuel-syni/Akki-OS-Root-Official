"""Read-only metadata qualification on estate hosts. Never reseals or reads transcript/audio bodies."""
import hashlib
import json
import time
from pathlib import Path

from services.training_lab.malpha_evaluation import fingerprint, population_support
from services.training_lab.malpha_splits import SPLIT_PROTOCOL_V2, SUBSTANTIVE_WORDS


def inspect_language(rows, clusters, expected_seal, protocol=None):
    split_names = ('train', 'dev', 'admission')
    splits = {s: [r for r in rows if r['split'] == s] for s in split_names}
    assignments = {s: {clusters.get(f"{r['session']}|{r['speaker']}") for r in values} - {None} for s, values in splits.items()}
    sessions = {s: {r['session'] for r in values} for s, values in splits.items()}
    texts = {s: {r.get('text_sha256') for r in values} - {None, ''} for s, values in splits.items()}
    substantive = {s: {r.get('text_sha256') for r in values if (r.get('words') or 0) >= SUBSTANTIVE_WORDS} - {None, ''} for s, values in splits.items()}
    admission = splits['admission']; positives = sum(bool(r.get('mentions')) for r in admission)
    # Match the original sealer's serialization byte-for-byte.
    digest = hashlib.sha256(json.dumps(sorted(r['seg_id'] for r in admission)).encode()).hexdigest()
    used = [r for s in split_names for r in splits[s]]
    missing = sum(clusters.get(f"{r['session']}|{r['speaker']}") is None for r in (used if protocol == SPLIT_PROTOCOL_V2 else rows))
    overlaps = {f'{a}_{b}': {'speaker_clusters': len(assignments[a] & assignments[b]),
                'recording_sessions': len(sessions[a] & sessions[b]), 'exact_text_hashes': len(texts[a] & texts[b]), 'substantive_text_hashes': len(substantive[a] & substantive[b]),
                'shared_audio_windows': len({r['seg_id'] for r in splits[a]} & {r['seg_id'] for r in splits[b]})}
                for a, b in (('train', 'dev'), ('train', 'admission'), ('dev', 'admission'))}
    if protocol == SPLIT_PROTOCOL_V2:
        # v3: admission is held out by speaker cluster; the same radio sessions/channels may appear in train (disclosed); speakers, substantive text and audio windows may not
        no_admission_overlap = all(overlaps[pair]['speaker_clusters'] == 0 and overlaps[pair]['substantive_text_hashes'] == 0 and overlaps[pair]['shared_audio_windows'] == 0 for pair in ('train_admission', 'dev_admission'))
        rule = 'v3 speaker-cluster-disjoint admission: zero shared speaker clusters, zero shared substantive (≥4-word) texts and zero shared audio windows with train/dev; shared sessions are channel overlap, disclosed'
        limitations = ['Speaker-cluster labels inherit clustering error.', 'Admission shares recording sessions/channels with training by design (same stations, same days); it does not share speakers.',
                       'Short-phrase text overlap (<4 words) is reported, not treated as leakage.', 'Dev is session-held-out and may share speakers with training; it is not an independent speaker test.']
    else:
        no_admission_overlap = all(not any(v for k, v in overlaps[pair].items() if k not in ('substantive_text_hashes', 'shared_audio_windows')) for pair in ('train_admission', 'dev_admission'))
        rule = 'v1: zero shared speaker clusters, sessions and exact texts with admission'
        limitations = ['Speaker-cluster labels inherit clustering error.', 'Exact text overlap can include common phrases; all such cases require review.',
                       'Dev is session-held-out and may share speakers with training; it is not an independent speaker test.']
    return {'segments': {s: len(v) for s, v in splits.items()}, 'excluded': {'unknown_speaker': sum(r['split'] == 'excluded_unknown_speaker' for r in rows), 'text_overlap': sum(r['split'] == 'excluded_text_overlap' for r in rows), 'overlapping_speech': sum(r['split'] == 'excluded_overlapping_speech' for r in rows)},
            'admission_seal_sha256': digest, 'seal_matches': digest == expected_seal, 'independence_rule': rule,
            'speaker_assignments_missing': missing, 'overlap_counts': overlaps,
            'admission_independence_verified': digest == expected_seal and missing == 0 and no_admission_overlap,
            'support': population_support(positives, len(admission)-positives, len(sessions['admission'])),
            'reference_qualification': {'verified': False, 'basis': 'transcript alias matching, not independent human annotation'},
            'limitations': limitations}


def audit(control, state):
    from services.training_lab.malpha_worker import load_rows
    start = time.monotonic(); root = Path(control['aip_db_dir'])
    manifest = json.loads((root / 'manifest.json').read_text())
    clusters_path = Path(control['lab_corpus_root']) / 'speaker_clusters.json'
    clusters_raw = clusters_path.read_bytes() if clusters_path.exists() else b'{}'
    clusters = json.loads(clusters_raw).get('clusters', {})
    protocol = manifest.get('split_protocol')
    reports = {}
    for lang in control['languages']:
        state.update(progress={'stage': 'checking metadata separation and admission support', 'language': lang})
        rows = load_rows(root, lang, with_text=False)
        reports[lang] = inspect_language(rows, clusters.get(lang, {}), manifest['seals'][lang]['admission_seg_ids_sha256'], protocol)
    result = {'audit_version': control['audit_version'], 'split_protocol': protocol, 'split_version': int(manifest.get('split_version') or 1), 'per_language': reports,
              'speaker_assignments_sha256': hashlib.sha256(clusters_raw).hexdigest(),
              'seal_set_sha256': fingerprint({l: reports[l]['admission_seal_sha256'] for l in control['languages']}),
              'independence_verified': all(v['admission_independence_verified'] for v in reports.values()),
              'support_sufficient': all(v['support']['sufficient'] for v in reports.values()),
              'reference_verified': False, 'test_content_read': False, 'metadata_only': True,
              'sealed_admission_read': False, 'raw_media_exported': False, 'text_exported': False, 'training_started': False,
              'compute': {'device': 'cpu', 'gpu_seconds': 0, 'wall_seconds': round(time.monotonic()-start, 3)}}
    state.stage('corpus_qualification', result)
    return result
