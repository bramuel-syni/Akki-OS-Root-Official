"""Read headers of already-authorized staged data. Never stage new objects or export samples."""
import json
from collections import Counter
from pathlib import Path


def inspect_corpus(control, state):
    import soundfile as sf
    root = Path(control['lab_corpus_root']).resolve()
    corpus = root/'corpus'/'datasets'
    if not corpus.is_dir():
        raise ValueError('AUTHORIZED_STAGED_CORPUS_NOT_FOUND')
    languages = {}; rates = Counter(); unreadable = 0; files = 0
    for language in sorted(corpus.iterdir()):
        if not language.is_dir() or language.is_symlink():
            continue
        row = {'files':0,'bytes':0,'seconds':0.,'transcripts':0,'transcript_bytes':0,'unreadable_headers':0}
        for audio in sorted(language.glob('*/audio/*')):
            if audio.suffix.lower() not in {'.wav','.flac','.mp3','.ogg','.m4a'} or audio.is_symlink() or not audio.resolve().is_relative_to(corpus):
                continue
            row['files'] += 1; files += 1; row['bytes'] += audio.stat().st_size
            transcript = audio.parent.parent/'transcript'/(audio.stem+'.txt')
            if transcript.is_file() and not transcript.is_symlink() and transcript.resolve().is_relative_to(corpus):
                row['transcripts'] += 1; row['transcript_bytes'] += transcript.stat().st_size
            try:
                info = sf.info(audio)
                row['seconds'] += info.duration; rates[str(info.samplerate)] += 1
            except Exception:
                row['unreadable_headers'] += 1; unreadable += 1
            if files % 100 == 0:
                state.update(progress={'stage':'inspecting staged audio headers','files':files})
        row['hours'] = round(row.pop('seconds')/3600,4)
        if row['files']:
            languages[language.name] = row
    # No filename/folder heuristics are trusted as music annotations.
    result = {'scope':'authorized staged language-cognition corpus only; not the whole RMS estate',
              'evidence_class':'measured_headers', 'per_language_folder':languages,'files':files,
              'sample_rate_counts':dict(rates),'unreadable_headers':unreadable,
              'music_labels':{'status':'not_established','verified_labelled_examples':None,
                              'reason':'Existing corpus supplies language/transcript labels, not a verified speech/music/mixed annotation contract.'},
              'quality':{'studio_or_telephony':'unknown','note':'Sample rate is a capture property, not proof of recording quality.'},
              'training_started':False,'raw_media_exported':False}
    # Actual GPU arithmetic tests ONLY, not training and not a trained detector.
    import torch
    if not torch.cuda.is_available():
        raise ValueError('GPU_SMOKE_REQUIRES_CUDA')
    torch.cuda.set_device(control['gpu_index'])
    torch.manual_seed(41)
    head = torch.nn.Linear(64,2).cuda()
    features = torch.randn(8,64,device='cuda'); targets = torch.randint(0,2,(8,2),device='cuda').float()
    loss = torch.nn.functional.binary_cross_entropy_with_logits(head(features),targets)
    loss.backward()
    result['music_head_smoke'] = {'evidence_class':'SYNTHETIC', 'device':torch.cuda.get_device_name(),
                                  'outputs':2,'finite_gradients':all(bool(torch.isfinite(p.grad).all()) for p in head.parameters()),
                                  'quality_claim':False,'weights_saved':False}
    state.update(progress={'stage':'inspection complete','files':files})
    return result