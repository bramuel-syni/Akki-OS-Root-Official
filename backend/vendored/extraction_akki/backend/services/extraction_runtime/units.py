"""Five-ring unit composition for structured records; runs on the admitted runtime.

Provenance · Signal · Relational · Re-extraction handle · Defensibility (contracts/five_rings).
Verdicts are declaration-baseline; the structured-records matrix row activates from the
first human-verified sample, so units carry `utterance` until that number exists.
"""
import base64
import decimal
import hashlib
import json
from datetime import date, datetime, time as dtime

PERSONAL_ROLES = {'role.phone', 'role.email', 'role.person_name', 'role.national_id', 'role.address',
                  'role.ip_address', 'role.password', 'role.token', 'role.dob'}
PERSONAL_NAME_HINTS = ('email', 'phone', 'msisdn', 'mobile', 'password', 'token', 'secret', 'ip_address',
                       'first_name', 'last_name', 'surname', 'full_name', 'national_id', 'id_number',
                       'passport', 'address', 'contact', 'dob', 'birth', 'payment_phone', 'client_email')


def personal_columns(columns, role_signals):
    flagged = {s['column'] for s in role_signals or () if s.get('role') in PERSONAL_ROLES}
    for column in columns:
        name = column['column_name'].lower() if isinstance(column, dict) else str(column).lower()
        if any(h in name for h in PERSONAL_NAME_HINTS):
            flagged.add(column['column_name'] if isinstance(column, dict) else column)
    return sorted(flagged)


def plain(value):
    if isinstance(value, (datetime, date, dtime)):
        return value.isoformat()
    if isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, (bytes, bytearray)):
        return 'base64:' + base64.b64encode(bytes(value)).decode()
    if isinstance(value, (int, float, str, bool)) or value is None:
        return value
    return str(value)


def redacted(value, column):
    return 'redacted:' + hashlib.sha256(f'{column}|{value}'.encode()).hexdigest()[:16]


def compose(row, columns, meta, floor_columns):
    """Return (unit, unqualified_reason). Unqualified units are retained, never delivered."""
    from services.mtafiti.detectors.pii_redaction_guard import redact_row
    record = {c: plain(v) for c, v in zip(columns, row)}
    if len(row) != len(columns):
        return None, 'SCHEMA_INCOMPLETE'
    pk = meta['primary_key']
    if record.get(pk) is None:
        return None, 'PRIMARY_KEY_NULL'
    redactions = 0
    for column in floor_columns:
        if record.get(column) is not None:
            record[column] = redacted(record[column], column)
            redactions += 1
    guarded = redact_row({k: v for k, v in record.items() if isinstance(v, str)})
    for key, value in guarded.items():
        if record[key] != value:
            record[key] = value
            redactions += 1
    filled = sum(1 for v in record.values() if v is not None)
    locator = {'database': meta['database'], 'table': meta['table'], 'primary_key': pk, 'key_value': str(record[pk])}
    unit_id = 'unit-' + hashlib.sha256(json.dumps([meta['source_ref'], locator], sort_keys=True).encode()).hexdigest()[:32]
    unit = {
        'unit_id': unit_id,
        'provenance': {'source_ref': meta['source_ref'], 'modality': 'structured_record', 'locator': locator,
                       'speaker_or_author': None, 'context': f"{meta['database']}.{meta['table']}"},
        'signal': {'dimensions': {'completeness': round(filled / max(1, len(columns)), 4),
                                  'redaction_ratio': round(redactions / max(1, len(columns)), 4)},
                   'depth_judged': False, 'depth_notes': None},
        'relational': {'edges': [{'type': 'references', 'target_unit_ref': f"column:{meta['database']}.{meta['table']}.{s['column']}",
                                  'evidence_ref': None} for s in meta.get('role_signals', ()) if s.get('role') == 'role.fk_candidate']},
        'reextraction_handle': {'raw_pointer': f"{meta.get('driver', 'mysql')}://{meta['source_ref']}/{meta['database']}.{meta['table']}?{pk}={record[pk]}",
                                'model_id': 'deterministic.structured_records', 'model_version': '1',
                                'extraction_params': {'columns': list(columns), 'floor_columns': list(floor_columns),
                                                      'job_kind': meta['job_kind']}},
        'defensibility': {'defensibility_class': 'utterance',
                          'score_vector': {'genre_ceiling': 0.0, 'source_standing': 0.0, 'corroboration': 0.0,
                                           'recency': 0.0, 'contested_status': 0.0},
                          'matrix_rule_ref': 'matrix.structured_records.v0:pending_first_verified_sample',
                          'runtime_mode': 'declaration_baseline'},
        'record': record,
    }
    return unit, None
