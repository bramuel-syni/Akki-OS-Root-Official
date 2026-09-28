"""Offline credential-artifact inventory only. No network, admission or source read.

Reports contain structural booleans/counts and whole-artifact custody hashes only.
Never emit endpoints, database names, usernames, passwords or ARN/account values.
This tool cannot install a runtime, mutate Registry or validate estate access.
"""
import argparse
import csv
import hashlib
import ipaddress
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
import openpyxl


def rms_summary(rows):
    complete, incomplete = 0, 0
    for row in rows:
        fields = [str(v or '').strip() for v in row]
        fields += [''] * max(0, 4 - len(fields))
        try:
            ipaddress.ip_address(fields[1])
        except ValueError:
            continue
        if fields[2] and fields[3]:
            complete += 1
        else:
            incomplete += 1
    return {'endpoint_account_secret_shaped_rows': complete,
            'endpoint_rows_missing_account_or_secret': incomplete,
            'row_count': len(rows), 'source_types_verified': False,
            'scope_semantics_verified': False, 'live_credentials_validated': False}


def digicow_summary(rows):
    expected = {'region', 'cluster arn', 'secret arn', 'database name'}
    values, duplicates = {}, set()
    for row in rows:
        for value in row:
            if not isinstance(value, str) or ':' not in value:
                continue
            label, content = value.split(':', 1)
            label = label.strip().lower()
            if label not in expected:
                continue
            if label in values:
                duplicates.add(label)
            values[label] = content.strip()
    cluster, secret = values.get('cluster arn', ''), values.get('secret arn', '')
    a, b = cluster.split(':'), secret.split(':')
    cluster_valid = bool(re.fullmatch(r'arn:aws(?:-[a-z]+)?:rds:[a-z0-9-]+:\d{12}:cluster:[A-Za-z0-9_.-]+', cluster))
    secret_valid = bool(re.fullmatch(r'arn:aws(?:-[a-z]+)?:secretsmanager:[a-z0-9-]+:\d{12}:secret:[A-Za-z0-9/_+=.@-]+', secret))
    return {'recognized_reference_fields_present': sorted(k for k in expected if values.get(k)),
            'duplicate_reference_labels': sorted(duplicates),
            'cluster_arn_well_formed': cluster_valid, 'secret_arn_well_formed': secret_valid,
            'region_consistent': cluster_valid and secret_valid and a[3] == b[3] == values.get('region'),
            'account_consistent': cluster_valid and secret_valid and a[4] == b[4],
            'native_secret_resolver_required': True, 'native_identity_admission_verified': False,
            'live_credentials_validated': False, 'classification': 'connection_references_not_dataset'}


def custody(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('Regular credential custody file required.')
    mode = path.stat().st_mode & 0o777
    if mode & 0o077:
        raise ValueError('Credential artifact must not be accessible to group or others.')
    return {'filename': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size, 'mode': oct(mode)}


def inventory(rms, digicow):
    rms_custody, digicow_custody = custody(rms), custody(digicow)
    with rms.open(encoding='utf-8-sig', newline='') as stream:
        rms_rows = list(csv.reader(stream))
    workbook = openpyxl.load_workbook(digicow, read_only=True, data_only=True)
    try:
        cow_rows = [row for sheet in workbook.worksheets for row in sheet.values]
    finally:
        workbook.close()
    return {'version': 'akki.offline-credential-intake/1', 'created_at': datetime.now(timezone.utc).isoformat(),
            'classification': 'credential_custody_and_shape_only',
            'registry_registered': False, 'admission_issued': False, 'source_connection_attempted': False,
            'census_run': False, 'extraction_run': False, 'gpu_contacted': False,
            'required_journey': ['read_only_registry_link', 'native_census', 'separately_authorised_specific_extraction'],
            'rms': {**rms_custody, **rms_summary(rms_rows)},
            'digicow': {**digicow_custody, **digicow_summary(cow_rows)},
            'blocker': 'ADMITTED_NON_GPU_INGESTION_WORKER_AND_NATIVE_CREDENTIAL_RESOLUTION_NOT_ESTABLISHED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rms', type=Path, required=True)
    parser.add_argument('--digicow', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = inventory(args.rms, args.digicow)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print('Offline intake report written. No estate connection, Registry admission or source read performed.')


if __name__ == '__main__':
    main()