"""Read-only metadata qualification on estate hosts. Never reseals or reads transcript/audio bodies."""
import hashlib
import json
import time
from pathlib import Path

from services.training_lab.malpha_evaluation import fingerprint, population_support


def inspect_language(rows, clusters, expected_seal):
    split_names = ('train', 'dev', 'admission')
    splits = {s: [r for r in rows if r['split'] == s] for s in split_names}
    assignments = {s: {clusters.get(f"{r['session']}|{r['speaker']}") for r in values} - {None} for s, values in splits.items()}
    sessions = {s: {r['session'] for r in values} for s, values in splits.items()}
    texts = {s: {r.get('text_sha256') for r in values} - {None, ''} for s, values in splits.items()}
    admission = splits['admission']; positives = sum(bool(r.get('mentions')) for r in admission)
    # Match the original sealer's serialization byte-for-byte.
    digest = hashlib.sha256(json.dumps(sorted(r['seg_id'] for r in admission)).encode()).hexdigest()
    missing = sum(clusters.get(f"{r['session']}|{r['speaker']}") is None for r in rows)
    overlaps = {f'{a}_{b}': {'speaker_clusters': len(assignments[a] & assignments[b]),
                'recording_sessions': len(sessions[a] & sessions[b]), 'exact_text_hashes': len(texts[a] & texts[b])}
                for a, b in (('train', 'dev'), ('train', 'admission'), ('dev', 'admission'))}
    no_admission_overlap = all(not any(overlaps[pair].values()) for pair in ('train_admission', 'dev_admission'))
    return {'segments': {s: len(v) for s, v in splits.items()}, 'admission_seal_sha256': digest, 'seal_matches': digest == expected_seal,
            'speaker_assignments_missing': missing, 'overlap_counts': overlaps,
            'admission_independence_verified': digest == expected_seal and missing == 0 and no_admission_overlap,
            'support': population_support(positives, len(admission)-positives, len(sessions['admission'])),
            'reference_qualification': {'verified': False, 'basis': 'transcript alias matching, not independent human annotation'},
            'limitations': ['Speaker-cluster labels inherit clustering error.', 'Exact text overlap can include common phrases; all such cases require review.',
                           'Dev is session-held-out and may share speakers with training; it is not an independent speaker test.']}


def audit(control, state):
    from services.training_lab.malpha_worker import load_rows
    start = time.monotonic(); root = Path(control['aip_db_dir'])
    manifest = json.loads((root / 'manifest.json').read_text())
    clusters_path = Path(control['lab_corpus_root']) / 'speaker_clusters.json'
    clusters_raw = clusters_path.read_bytes() if clusters_path.exists() else b'{}'
    clusters = json.loads(clusters_raw).get('clusters', {})
    reports = {}
    for lang in control['languages']:
        state.update(progress={'stage': 'checking metadata separation and admission support', 'language': lang})
        rows = load_rows(root, lang, with_text=False)
        reports[lang] = inspect_language(rows, clusters.get(lang, {}), manifest['seals'][lang]['admission_seg_ids_sha256'])
    result = {'audit_version': control['audit_version'], 'per_language': reports,
              'speaker_assignments_sha256': hashlib.sha256(clusters_raw).hexdigest(),
              'seal_set_sha256': fingerprint({l: reports[l]['admission_seal_sha256'] for l in control['languages']}),
              'independence_verified': all(v['admission_independence_verified'] for v in reports.values()),
              'support_sufficient': all(v['support']['sufficient'] for v in reports.values()),
              'reference_verified': False, 'test_content_read': False, 'metadata_only': True,
              'sealed_admission_read': False, 'raw_media_exported': False, 'text_exported': False, 'training_started': False,
              'compute': {'device': 'cpu', 'gpu_seconds': 0, 'wall_seconds': round(time.monotonic()-start, 3)}}
    state.stage('corpus_qualification', result)
    return result