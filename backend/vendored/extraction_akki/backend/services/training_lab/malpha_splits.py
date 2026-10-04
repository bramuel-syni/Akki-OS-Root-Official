"""Prospective split construction: connected recordings/speakers stay together.

Never applied to the existing corpus in place. Missing speaker assignments stay
train-only and prevent any assertion of full identity independence.
"""
import hashlib


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