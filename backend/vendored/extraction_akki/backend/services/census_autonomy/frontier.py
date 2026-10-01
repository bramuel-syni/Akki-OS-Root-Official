"""Census frontier reconciliation (M1-T1/T3 closure on the pinned scope).

The latest terminal census per declared source family is reconciled against the declared estate: every declared
scope is either completed, still advancing (partial), or excluded with a named reason. Exclusions are DECLARED,
not hidden: each carries its plain-English cause and the owner ruling that keeps it in the denominator. No
figure for an excluded or absent scope is inferred. This is a projection of retained records; it writes nothing.
"""
RULINGS = {
    'AUTHENTICATION_FAILED': {'class': 'access_not_granted', 'plain': 'The source refused the census account; the estate must grant read access before this scope can be measured.',
                              'ruling': 'owner-ruling:2026-10-01:3a · retained as a declared exclusion; counted in the denominator, nothing inferred'},
    'NoSuchBucket': {'class': 'declared_but_absent', 'plain': 'Listed in the declared estate but not present at the object store on the day of the census.',
                     'ruling': 'declared scope kept; absence recorded from the store’s own reply, not assumed'},
    'SOURCE_UNREACHABLE': {'class': 'route_unavailable', 'plain': 'The source could not be reached from the admitted worker during this census.',
                           'ruling': 'retained in the denominator; a later census that reaches it supersedes this record without erasing it'},
    'OperationalError': {'class': 'route_unavailable', 'plain': 'The database connection failed during this census.',
                         'ruling': 'retained in the denominator; superseded only by a later successful read'},
    'FileNotFoundError': {'class': 'mount_absent', 'plain': 'The admitted network share was not mounted on the worker; SMB access must be enabled by the estate.',
                          'ruling': 'owner-ruling:2026-10-01:3a · retained as a declared exclusion until the share is mounted'},
}
UNKNOWN = {'class': 'unclassified', 'plain': 'This scope did not complete; the recorded reason is shown as the worker reported it.',
           'ruling': 'retained in the denominator; nothing inferred'}


def exclusion_for(reason_code):
    base = RULINGS.get(reason_code) or next((v for k, v in RULINGS.items() if reason_code and k.lower() in str(reason_code).lower()), UNKNOWN)
    return {**base, 'reason_code': reason_code}


def annotate(sources):
    """Attach the declared-exclusion text to every source scope that did not complete."""
    for s in sources:
        if s.get('status') != 'complete':
            s['exclusion'] = exclusion_for(s.get('reason_code') or s.get('status'))
    return sources


def _family(record):
    ids = record.get('source_ids') or []
    return ids[0] if len(ids) == 1 else ','.join(sorted(ids)) or 'unspecified'


def frontier(records):
    """Latest terminal record per declared source family, reconciled scope by scope."""
    latest = {}
    for record in sorted(records, key=lambda r: r.get('finished_at') or r.get('created_at') or '', reverse=True):
        if str(record.get('status', '')).upper() == 'PENDING' or not record.get('source_details'):
            continue
        latest.setdefault(_family(record), record)
    rows = []
    for family, record in sorted(latest.items()):
        sources = annotate([dict(s) for s in record['source_details']])
        excluded = [s for s in sources if s.get('status') != 'complete']
        by_class = {}
        for s in excluded:
            by_class.setdefault(s['exclusion']['class'], []).append(s.get('label') or s.get('source_ref'))
        complete = [s for s in sources if s.get('status') == 'complete']
        rows.append({'family': family, 'record_id': record.get('record_id') or record.get('census_run_id'), 'finished_at': record.get('finished_at'),
                     'declared': len(sources), 'completed': len(complete), 'partial': sum(1 for s in sources if s.get('status') == 'partial'),
                     'excluded': len(excluded), 'measured_bytes': sum(s.get('volume_bytes') or 0 for s in complete),
                     'state': 'complete' if not excluded else 'partial' if complete else 'blocked',
                     'exclusions': [{'label': s.get('label') or s.get('source_ref'), **s['exclusion']} for s in excluded],
                     'exclusion_classes': by_class,
                     'basis': f"{len(complete)} of {len(sources)} declared scopes completed in census {record.get('record_id') or record.get('census_run_id')}; excluded scopes stay in the denominator."})
    declared = sum(r['declared'] for r in rows)
    completed = sum(r['completed'] for r in rows)
    classes_total = {}
    for r in rows:
        for cls, labels in r['exclusion_classes'].items():
            classes_total[cls] = classes_total.get(cls, 0) + len(labels)
    return {'rows': rows, 'declared_scopes': declared, 'completed_scopes': completed, 'excluded_scopes': declared - completed,
            'exclusion_classes_total': classes_total,
            'pinned_accessible_scope': f"{completed} of {declared} declared scopes across {len(rows)} source families",
            'statement': ('Coverage is reported against the declared estate. Scopes the estate has not yet opened (access not granted, share not mounted) and scopes '
                          'absent at the source are declared exclusions: they stay in the denominator and no figure is inferred for them.'),
            'note': 'Metadata enumeration and sampled checks are what these censuses measured; they are not a full content read.'}
