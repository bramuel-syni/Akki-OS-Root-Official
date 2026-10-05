"""Workbook vault intake and reach for the confidentiality register (Doc 2 A4 B26, A5.3 B36 · WP-A1).

The DPO uploads a workbook (CSV or XLSX) to the media library; this module reads it inside the boundary, turns its rows into `pending`
exact/pattern declarations (nothing is in force until approved) and reports every invalid or duplicate row. Reach — what a declaration
would newly redact — is computed over MEASURED material only: text files the library already holds for the tenant. Anything not
measured is stated as such, never implied clean. Values never leave the estate; the reach report carries counts, not excerpts."""
import csv
import io
import re
from collections import defaultdict

from services.synisense.shield import semantic_register as reg

COLUMNS = {'value', 'kind', 'category', 'description', 'action', 'enforcement', 'entity_type'}
MAX_VALUES_PER_DECLARATION = 5000
MEASURED_FILE_LIMIT, MEASURED_BYTES_LIMIT = 25, 5_000_000


def rows_from_bytes(content, extension):
    """Rows (lists of strings) from a CSV or XLSX workbook; refuses binary CSV and unknown formats."""
    if extension == '.csv':
        try: text = content.decode('utf-8-sig')
        except UnicodeError as exc: raise ValueError('The workbook must be UTF-8 CSV') from exc
        if '\x00' in text: raise ValueError('Binary contents are not a CSV workbook')
        return [[c.strip() for c in row] for row in csv.reader(io.StringIO(text)) if any(c.strip() for c in row)]
    if extension == '.xlsx':
        import openpyxl
        try: book = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
        except Exception as exc: raise ValueError('The workbook could not be read as XLSX') from exc
        rows = []
        for sheet in book.worksheets:
            for row in sheet.iter_rows(values_only=True):
                cells = ['' if c is None else str(c).strip() for c in row]
                if any(cells): rows.append(cells)
        return rows
    raise ValueError('A vault workbook is a CSV or XLSX file')


def _declarations(rows):
    header = [h.strip().lower() for h in rows[0]] if rows else []
    if 'value' not in header: raise ValueError("The workbook needs a header row with a 'value' column (optional: kind, category, description, action, enforcement, entity_type)")
    idx = {name: header.index(name) for name in COLUMNS if name in header}
    groups, seen, invalid, duplicates = {}, set(), [], []
    for n, row in enumerate(rows[1:], start=2):
        cell = lambda name, default='': (row[idx[name]] if name in idx and idx[name] < len(row) else '') or default  # noqa: E731
        value, kind, category = cell('value'), cell('kind', 'exact').lower(), re.sub(r'[^a-z0-9_]+', '_', cell('category', 'vault_values').lower()).strip('_') or 'vault_values'
        if not value: invalid.append({'row': n, 'reason': 'empty value'}); continue
        if kind not in ('exact', 'pattern'): invalid.append({'row': n, 'reason': 'unknown kind', 'kind': kind}); continue
        if kind == 'pattern':
            try: re.compile(value)
            except re.error: invalid.append({'row': n, 'reason': 'invalid regular expression'}); continue
        if (category, kind, value.lower()) in seen: duplicates.append({'row': n, 'value': value if kind == 'pattern' else value, 'category': category}); continue
        seen.add((category, kind, value.lower()))
        g = groups.setdefault((category, kind), {'name': category, 'kind': kind, 'items': [], 'description': cell('description'), 'action': cell('action', 'abstract').lower(), 'enforcement': cell('enforcement', 'enforced').lower(), 'entity_type': cell('entity_type') or None})
        if len(g['items']) >= MAX_VALUES_PER_DECLARATION: invalid.append({'row': n, 'reason': f'beyond the {MAX_VALUES_PER_DECLARATION}-value limit for one declaration'}); continue
        g['items'].append(value)
    return groups, invalid, duplicates, len(rows) - 1


def reach(declarations, measured):
    """Counts of measured documents each declaration would touch. `measured` = [(document_id, text)]; the unmeasured is stated, not implied clean.
    Category-3 (contextual) declarations are measured through the contained reader by `reach_contextual`; here they are reported as not measurable
    by pattern, never implied clean."""
    by = {}
    for d in declarations:
        if d['kind'] == 'exact': pats = [re.compile(re.escape(v), re.IGNORECASE) for v in d.get('values') or []]
        elif d['kind'] == 'pattern': pats = [re.compile(p) for p in d.get('patterns') or []]
        else:
            by[d['name']] = {'documents_matched': None, 'matches': None, 'basis': 'contextual declaration: reach is measured by the contained reader (reach_contextual), not by pattern'}; continue
        docs = matches = 0
        for _, text in measured:
            n = sum(len(p.findall(text)) for p in pats)
            if n: docs += 1; matches += n
        by[d['name']] = {'documents_matched': docs, 'matches': matches, 'basis': 'literal/pattern match over the measured material'}
    statement = ('Reach is computed over the measured material only: ' + (f'{len(measured)} text document(s) the library holds for this tenant. ' if measured else 'no document has been measured for this tenant yet. ')
                 + 'Estate audio, object-store and NAS buckets and any file not uploaded to the library are not measured and are not represented here.')
    return {'measured_documents': len(measured), 'measured_ids': [i for i, _ in measured], 'by_declaration': by, 'unmeasured': statement}


READER_REACH_DOCS = 8


def reach_contextual(declaration, measured, tenant, recognise):
    """Review reach of a Category-3 declaration (Doc 2 A5.2/A5.3): the contained reader reads a bounded number of measured documents against this
    one description; documents beyond the bound are stated as not read. Counts only — values never leave."""
    read, docs, spans, errors = 0, 0, 0, []
    for doc_id, text in measured[:READER_REACH_DOCS]:
        try: out = recognise(text[:9000], tenant, f'register.reach:{declaration["name"]}', categories=[declaration])
        except Exception as exc:  # noqa: BLE001 — disclosed, not hidden
            errors.append({'document_id': doc_id, 'error': type(exc).__name__}); continue
        read += 1; n = sum(1 for s in out['spans'] if s['category'] == declaration['name'])
        if n: docs += 1; spans += n
    return {'recogniser': 'contained_reader', 'documents_read': read, 'documents_not_read': max(0, len(measured) - READER_REACH_DOCS), 'documents_matched': docs, 'spans': spans, 'errors': errors,
            'basis': f'the contained reader applied the declaration description to up to {READER_REACH_DOCS} measured documents; the rest are not read and not implied clean'}


def measured_material(tenant, exclude_file_id=None):
    """Text files the media library already holds for the tenant (bounded), read inside the boundary. Storage trouble is disclosed, not hidden."""
    from services.media_library import storage, store
    rows = store.db().media_files.find({'tenant_id': tenant, 'kind': {'$in': ['transcript', 'labels']}, 'status': 'available', 'is_deleted': False, 'extension': {'$in': ['.txt', '.vtt', '.srt', '.csv', '.json']}}, {'_id': 0, 'file_id': 1, 'storage_path': 1, 'size_bytes': 1}).sort('created_at', -1).limit(MEASURED_FILE_LIMIT)
    out, total, errors = [], 0, []
    for row in rows:
        if row['file_id'] == exclude_file_id or total + row['size_bytes'] > MEASURED_BYTES_LIMIT: continue
        try:
            response = storage.download(row['storage_path'])
            try: text = response.content.decode('utf-8', errors='replace')
            finally: response.close()
        except storage.StorageError as exc: errors.append({'file_id': row['file_id'], 'error': str(exc)}); continue
        out.append((row['file_id'], text)); total += row['size_bytes']
    return out, errors


def intake_rows(tenant, actor, rows, *, source_ref, measured, file_id=None, sha256=None):
    groups, invalid, duplicates, total = _declarations(rows)
    pending = []
    for (category, kind), g in groups.items():
        body = {'name': g['name'], 'kind': kind, 'action': g['action'] if g['action'] in reg.ACTIONS else 'abstract', 'enforcement': g['enforcement'] if g['enforcement'] in reg.ENFORCEMENT else 'enforced',
                'description': g['description'] or f'{len(g["items"])} {kind} declaration(s) from the vault workbook {source_ref}', 'values': g['items'] if kind == 'exact' else None, 'patterns': g['items'] if kind == 'pattern' else None,
                'entity_type': g['entity_type'] if kind == 'exact' and g['entity_type'] and re.fullmatch(r'[A-Z][A-Z0-9_]{1,30}', g['entity_type']) else None}
        try:
            pending.append(reg._pending_from(tenant, actor, body, None, f'adopted from vault workbook {source_ref}: {len(g["items"])} row(s); awaits approval', provenance='vault_intake', source={'source_ref': source_ref, 'source_file_id': file_id, 'source_sha256': sha256}))
        except reg.Conflict as exc:
            invalid.append({'row': None, 'reason': str(exc), 'category': category})
    return {'pending': pending, 'rows': {'total': total, 'accepted': sum(len(g['items']) for g in groups.values()), 'invalid': len(invalid), 'duplicate': len(duplicates)}, 'invalid': invalid, 'duplicates': duplicates,
            'reach': reach(pending, measured)}


def intake_file(tenant, actor, file_id, source_ref=None):
    """Read a media-library workbook upload inside the boundary and turn it into pending declarations."""
    from services.media_library import storage, store
    row = store.get(tenant, file_id)
    if not row: raise LookupError('No such upload in this tenant\'s library')
    if row['is_deleted'] or row['status'] != 'available': raise ValueError('The upload is not available (archived or still uploading)')
    if row['extension'] not in ('.csv', '.xlsx'): raise ValueError('A vault workbook is a CSV or XLSX file in the library')
    response = storage.download(row['storage_path'])
    try: content = response.content
    finally: response.close()
    rows = rows_from_bytes(content, row['extension'])
    measured, errors = measured_material(tenant, exclude_file_id=file_id)
    out = intake_rows(tenant, actor, rows, source_ref=source_ref or row['filename'], measured=measured, file_id=file_id, sha256=row['sha256'])
    if errors: out['reach']['measurement_errors'] = errors
    store.audit(actor if isinstance(actor, dict) else {'tenant_id': tenant, 'principal_id': actor}, 'shield_vault_intake', file_id, row['revision'], {'pending': [d['name'] for d in out['pending']], 'rows': out['rows']})
    return out
