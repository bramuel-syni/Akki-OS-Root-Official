"""Prospective split construction: connected recordings/speakers stay together.

Never applied to the existing corpus in place. Missing speaker assignments stay
train-only and prevent any assertion of full identity independence.

v2 (owner decision 2026-10-04, 1a): admission is sealed at the SPEAKER-CLUSTER level.
Radio sessions share the same presenters across almost every recording (measured: one
connected component holds 465/513 Kikuyu, 271/288 Kamba and 407/411 Kiswahili sessions),
so a session-level speaker-disjoint admission set with enough brand mentions does not
exist. Clusters that appear in few sessions (callers, guests, voiced adverts) are held
out whole; their segments never train. Session/channel overlap with training is
expected and disclosed; speaker and substantive-text overlap are zero by construction.
"""
import hashlib
from collections import defaultdict

SPLIT_PROTOCOL_V2 = 'akki-malpha-split-v3-cluster-level'  # v3 = cluster-level selection + overlapping-speech exclusion (v2 was superseded before any sealed read)
SPLIT_VERSION = 3
SUBSTANTIVE_WORDS = 4  # exact-text union/overlap applies to utterances of at least this many words; shorter ones are common phrases, reported not unioned
RESEAL_TARGETS = {'admission': {'positives': 100, 'negatives': 100, 'sessions': 20, 'max_cluster_sessions': 5, 'max_share': 0.30},
                  'dev': {'segments': 300, 'mention_segments': 30, 'max_session_segments': 300, 'max_share': 0.25}}


def connected_splits(rows, clusters, seed, lang, admission_pct=10, dev_pct=10):
    if not 0 <= admission_pct <= 100 or not 0 <= dev_pct <= 100 or admission_pct + dev_pct > 100:
        raise ValueError('Invalid split percentages')
    sessions = sorted({r['session'] for r in rows}); parent = {s: s for s in sessions}

    def root(s):
        while parent[s] != s:
            parent[s] = parent[parent[s]]; s = parent[s]
        return s

    def union(a, b):
        a, b = root(a), root(b)
        if a != b: parent[max(a, b)] = min(a, b)

    owners = {}; unknown = set()
    for row in rows:
        session = row['session']; cid = clusters.get(f"{session}|{row['speaker']}")
        if cid is None: unknown.add(session)
        else:
            key = ('speaker', str(cid))
            if key in owners: union(session, owners[key])
            else: owners[key] = session
        # Identical text cannot straddle splits either. Common utterances can
        # create large components; report that shortage rather than weaken it.
        text_hash = row.get('text_sha256')
        if text_hash:
            key = ('text', text_hash)
            if key in owners: union(session, owners[key])
            else: owners[key] = session
    groups = {}
    for session in sessions: groups.setdefault(root(session), []).append(session)
    mapping = {}
    for members in groups.values():
        canonical = '|'.join(sorted(members))
        bucket = int(hashlib.sha256(f'{seed}:{lang}:{canonical}'.encode()).hexdigest()[:8], 16) % 100
        split = 'train' if set(members) & unknown else 'admission' if bucket < admission_pct else 'dev' if bucket < admission_pct + dev_pct else 'train'
        for session in members: mapping[session] = split
    for row in rows: row['split'] = mapping[row['session']]
    return mapping


def _bucket(seed, lang, key):
    return int(hashlib.sha256(f'{seed}:{lang}:{key}'.encode()).hexdigest()[:8], 16)


def cluster_level_reseal(rows, clusters, seed, lang, targets=RESEAL_TARGETS):
    """Assign every row a split in place and return the selection report.

    admission: whole speaker clusters seen in ≤ max_cluster_sessions sessions, taken in seeded hash order until the
               positive/negative/session targets are met (clusters already sealed as admission and small enough stay: they were never trained).
    dev:       whole remaining sessions in seeded order until the dev targets are met (session holdout; presenters overlap train — disclosed).
    excluded_unknown_speaker: rows without a cluster label never train, develop or evaluate.
    excluded_overlapping_speech: audio windows (same seg_id) shared by an admission speaker and another speaker — nobody trains or is tested on them.
    excluded_text_overlap: train/dev rows whose substantive text also occurs in admission.
    """
    adm, dev_t = targets['admission'], targets['dev']
    cl = [clusters.get(f"{r['session']}|{r['speaker']}") for r in rows]
    by_cluster = defaultdict(list); sessions_of = defaultdict(set)
    for r, c in zip(rows, cl):
        if c is not None: by_cluster[str(c)].append(r); sessions_of[str(c)].add(r['session'])
    legacy_admission = {str(c) for r, c in zip(rows, cl) if c is not None and r.get('split') == 'admission' and len(sessions_of[str(c)]) <= adm['max_cluster_sessions']}
    eligible = sorted((c for c in by_cluster if len(sessions_of[c]) <= adm['max_cluster_sessions']), key=lambda c: (c not in legacy_admission, _bucket(seed, lang, 'admission-cluster-v2:' + c)))
    total = sum(len(v) for v in by_cluster.values()); cap = int(adm['max_share'] * total)
    chosen, a_segs = set(), []
    for c in eligible:
        pos = sum(bool(r.get('mentions')) for r in a_segs); neg = len(a_segs) - pos; sess = len({r['session'] for r in a_segs})
        if pos >= adm['positives'] and neg >= adm['negatives'] and sess >= adm['sessions']: break
        segs = by_cluster[c]
        if c not in legacy_admission and len(a_segs) + len(segs) > cap: continue
        c_pos = sum(bool(r.get('mentions')) for r in segs)
        if c in legacy_admission or (pos < adm['positives'] and c_pos) or (neg < adm['negatives'] and len(segs) - c_pos) or sess < adm['sessions']:
            chosen.add(c); a_segs.extend(segs)
    windows = defaultdict(set)  # seg_id → clusters heard in that audio window (duplicate rows = overlapping speakers on the same window)
    for r, c in zip(rows, cl): windows[r['seg_id']].add(str(c) if c is not None else None)
    overlapping = {sid for sid, cs in windows.items() if len(cs) > 1 and cs & chosen}
    admission_rows = [r for r, c in zip(rows, cl) if c is not None and str(c) in chosen and r['seg_id'] not in overlapping]
    admission_texts = {r['text_sha256'] for r in admission_rows if r.get('text_sha256') and (r.get('words') or 0) >= SUBSTANTIVE_WORDS}
    for r, c in zip(rows, cl):
        if c is None: r['split'] = 'excluded_unknown_speaker'
        elif r['seg_id'] in overlapping: r['split'] = 'excluded_overlapping_speech'
        elif str(c) in chosen: r['split'] = 'admission'
        elif r.get('text_sha256') in admission_texts and (r.get('words') or 0) >= SUBSTANTIVE_WORDS: r['split'] = 'excluded_text_overlap'
        else: r['split'] = 'train'
        r.pop('dev_basis', None)
    by_session = defaultdict(list)
    for r in rows:
        if r['split'] == 'train': by_session[r['session']].append(r)
    promoted = []; train_total = sum(len(v) for v in by_session.values()); dev_cap = int(dev_t.get('max_share', 0.25) * train_total)
    for session in sorted(by_session, key=lambda s: _bucket(seed, lang, 'dev-holdout-v2:' + s)):
        dev = [r for r in rows if r['split'] == 'dev']
        if len(dev) >= dev_t['segments'] and sum(1 for r in dev if r.get('mentions')) >= dev_t['mention_segments']: break
        if len(by_session[session]) > dev_t['max_session_segments'] or len(dev) + len(by_session[session]) > dev_cap: continue
        for r in by_session[session]: r['split'] = 'dev'; r['dev_basis'] = 'session_holdout'
        promoted.append(session)
    a_pos = sum(bool(r.get('mentions')) for r in admission_rows)
    report = {'protocol': SPLIT_PROTOCOL_V2, 'targets': targets, 'admission': {'clusters': len(chosen), 'legacy_clusters_retained': len(legacy_admission & chosen), 'segments': len(admission_rows), 'positives': a_pos, 'negatives': len(admission_rows) - a_pos,
                                                                              'sessions': len({r['session'] for r in admission_rows}), 'share_of_known_segments': round(len(admission_rows) / total, 4) if total else None,
                                                                              'targets_met': a_pos >= adm['positives'] and len(admission_rows) - a_pos >= adm['negatives'] and len({r['session'] for r in admission_rows}) >= adm['sessions']},
              'dev': {'segments': sum(1 for r in rows if r['split'] == 'dev'), 'mention_segments': sum(1 for r in rows if r['split'] == 'dev' and r.get('mentions')), 'sessions_promoted': len(promoted), 'basis': 'session_holdout'},
              'excluded_unknown_speaker': sum(1 for r in rows if r['split'] == 'excluded_unknown_speaker'), 'excluded_text_overlap': sum(1 for r in rows if r['split'] == 'excluded_text_overlap'),
              'excluded_overlapping_speech': sum(1 for r in rows if r['split'] == 'excluded_overlapping_speech'), 'duplicate_audio_windows': sum(1 for cs in windows.values() if len(cs) > 1),
              'train': {'segments': sum(1 for r in rows if r['split'] == 'train')}}
    return report
