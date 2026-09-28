"""Offline-only intake tests with SYNTHETIC fields; no native source invocation."""
import importlib.util
import json
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('safe_estate_intake', '/app/assessment_workspace/tools/estate_intake_20260928.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


def test_rms_shape_report_has_no_credentials_or_scope_assumptions():
    rows = [['DATABASE NAME', 'HOST', 'USERNAME', 'PASSWORD'],
            ['private-db-marker', '192.0.2.13', 'private-user-marker', 'private-secret-marker'],
            ['other-db-marker', '192.0.2.14', '', '']]
    result = intake.rms_summary(rows)
    assert result['endpoint_account_secret_shaped_rows'] == 1
    assert result['endpoint_rows_missing_account_or_secret'] == 1
    assert result['live_credentials_validated'] is False
    assert result['scope_semantics_verified'] is False
    assert all(value not in json.dumps(result) for row in rows[1:] for value in row if value)


def test_digicow_references_are_not_a_data_import_or_aws_identity():
    rows = [['region: eu-test-1'], ['cluster arn: arn:aws:rds:eu-test-1:123456789012:cluster:private-cluster-marker'],
            ['secret arn: arn:aws:secretsmanager:eu-test-1:123456789012:secret:private-secret-marker'], ['database name: private-db-marker']]
    result = intake.digicow_summary(rows)
    assert result['region_consistent'] and result['account_consistent']
    assert result['native_secret_resolver_required'] and not result['native_identity_admission_verified']
    assert result['classification'] == 'connection_references_not_dataset'
    assert all(word not in json.dumps(result) for word in ['eu-test-1', '123456789012', 'private-'])


def test_digicow_mismatch_and_duplicates_never_become_validated_credentials():
    result = intake.digicow_summary([['region: a'], ['region: b'], ['secret arn: not-a-secret-arn'], ['cluster arn: not-an-arn']])
    assert result['duplicate_reference_labels'] == ['region']
    assert not result['region_consistent'] and not result['account_consistent']
    assert not result['live_credentials_validated']


def test_unsafe_file_modes_and_symlinks_are_rejected(tmp_path):
    path = tmp_path/'credential.csv'
    path.write_text('SYNTHETIC secret')
    path.chmod(0o644)
    with pytest.raises(ValueError): intake.custody(path)
    path.chmod(0o600)
    report = intake.custody(path)
    assert report['mode'] == '0o600' and 'SYNTHETIC' not in json.dumps(report)
    link = tmp_path/'link.csv'
    link.symlink_to(path)
    with pytest.raises(ValueError): intake.custody(link)


def test_progress_does_not_convert_old_scoped_evidence_or_tests_to_completion():
    report = json.loads(Path('/app/assessment_workspace/notes/designer_handoff_20260928/PROGRESS_EVIDENCE.json').read_text())
    assert sum(report['historical_dispositions'].values()) == report['historical_registered_rows'] == 648
    assert report['completion_percent'] is None
    assert report['accepted_requirement_numerator'] is None
    assert report['historical_counts_are_current_completion'] is False
    assert report['all_backend_integrations_complete'] is False


def test_brief_covers_complete_experiences_and_keeps_machine_components_out():
    path = Path('/app/assessment_workspace/notes/designer_handoff_20260928/AKKI_EXPERIENCE_BRIEF.md')
    text = path.read_text()
    for i in range(1, 15):
        assert f'### E{i:02}' in text
    for i in range(1, 6):
        assert f'### V{i:02}' in text
    assert 'not a wireframe, navigation map' in text
    assert 'Do not create applications, primary navigation entries' in text
    assert 'SYNTHETIC/MOCKED' in text


def test_word_brief_export_contains_all_feature_headings():
    from docx import Document
    path = Path('/app/frontend/public/briefs/Akki_Designer_Brief.docx')
    document = Document(path)
    text = '\n'.join(p.text for p in document.paragraphs)
    for i in range(1, 15):
        assert f'E{i:02}' in text
    assert 'Requested designer deliverables' in text