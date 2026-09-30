"""Allowlisted aggregate projection. Never forward transcripts, logs or arbitrary labels."""
import math

LANGUAGES = {'guz','kam','kik','kln','luo','lwg','swa','eng','sheng','bxk'}


def number(value):
    return value if type(value) in (int,float) and math.isfinite(value) else None


def metrics(report):
    result = {}
    for lang,row in (report or {}).items():
        if lang in LANGUAGES and isinstance(row,dict):
            result[lang] = {key:number(row.get(key)) for key in ('accuracy','abstention_rate','windows')}
    return result


def historical_evidence():
    from services.audio_plane_v1 import language_cognition_dispatch as lc
    rows = []
    for job in lc.list_jobs():
        cert = job.get('run_certificate') or {}
        if job.get('phase') != 'train_corrective' or job.get('status') != 'completed' or not cert:
            continue
        compute = cert.get('compute') or {}; contract = cert.get('sealed_contract_check') or {}
        rows.append({'ref':'historical_audio_'+str(len(rows)+1),'evidence_class':'historical_measured_not_blind',
                     'per_language':metrics(cert.get('per_stratum')),
                     'compute':{k:number(compute.get(k)) for k in ('epochs_completed','windows_per_second','gpu_max_memory_gb','batch_size')},
                     'epsilon':number((cert.get('dp_sgd') or {}).get('epsilon')),
                     'speaker_privacy_passed':contract.get('no_speaker_id_probe',{}).get('strict_chance_met') is True,
                     'code_switch_labels_present':contract.get('code_switch_material_present') is True})
        if len(rows)==4:
            break
    return {'historical_audio':rows,'authority':{'ref':'owner_scope','training_authorized':False,
             'new_estate_sampling_authorized':False,'music_detector_admitted':False}}


def inspection_evidence(result):
    langs = {}
    for language,row in result.get('per_language_folder',{}).items():
        if language in LANGUAGES:
            langs[language] = {key:number(row.get(key)) for key in ('files','bytes','hours','transcripts','transcript_bytes','unreadable_headers')}
    rates = {key:number(value) for key,value in result.get('sample_rate_counts',{}).items() if key.isdigit() and len(key)<=6}
    return {'ref':'staged_corpus_headers','evidence_class':'measured_headers','per_language':langs,
            'sample_rate_counts':rates,'music_label_contract_verified':False,
            'recording_quality_measured':False,'scope':'staged_authorized_corpus_not_whole_estate'}


def checkpoint_evidence(job):
    progress = (job.get('remote_state') or {}).get('progress') or {}
    dev = (job.get('remote_state') or {}).get('lab_checkpoint') or progress.get('latest_dev') or {}
    if not dev or not isinstance(dev.get('dev'),dict):
        return None
    return {'checkpoint':{'ref':'development_checkpoint','epoch':number(dev.get('epoch')),
            'step':number(dev.get('step')),'epsilon':number(dev.get('epsilon')),
            'per_language':metrics(dev['dev'].get('per_language')),
            'windows_per_second':number(progress.get('windows_per_second')),
            'evaluation_split':'development_only'},
            'authority':{'ref':'owner_scope','training_authorized':False,'recipe_changes_authorized':False}}


def references(value):
    if isinstance(value,dict):
        out = {value['ref']} if isinstance(value.get('ref'),str) else set()
        for item in value.values():
            out |= references(item)
        return out
    if isinstance(value,list):
        return set().union(*(references(item) for item in value)) if value else set()
    return set()