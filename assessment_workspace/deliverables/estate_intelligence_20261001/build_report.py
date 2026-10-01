"""Offline, source-pinned owner report. Does not register a UI commission or touch source estates."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / 'evidence'
FIXTURE = HERE / 'commission'
ROOT = Path('/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, str(ROOT))
from services.transform_forms.doc_studio.frames import frame_for, verdict_from_frame
from services.transform_forms.doc_studio.manifest_template import manifest_from_brief


def read(name):
    return json.loads((EVIDENCE / name).read_text())


estate = read('estate_report.json')
audio_job = read('m9j-3e0dcb1bd16e.json')
audio = audio_job['receipt']['result']
text = read('m9j-9a46b862f339.json')['receipt']['result']
trained = read('m9j-74af7cef0a85.json')['receipt']['result']
head, obs, nas = estate['headline'], estate['stores']['obs'], estate['stores']['nas']
lang = audio['per_language_folder']
hours = sum(r['hours'] for r in lang.values())
audio_bytes = sum(r['bytes'] for r in lang.values())
transcripts = sum(r['transcripts'] for r in lang.values())
transcript_bytes = sum(r['transcript_bytes'] for r in lang.values())
labels = {'bxk': 'Bukusu (folder label)', 'guz': 'Ekegusii', 'kam': 'Kikamba', 'kik': 'Kikuyu', 'kln': 'Kalenjin', 'luo': 'Dholuo', 'lwg': 'Wanga / Luhya label', 'swa': 'Kiswahili'}
NATURAL_SPLITS = ['train', 'dev', 'held', 'archive_test']
text_lang = {k: sum(v[x] for x in NATURAL_SPLITS) for k, v in text['per_stratum'].items()}

receipts = {
    'R01': {'resolves_to': 'RMS estate census, eij-1b359b3cbd2e; measured 29 September 2026. Exact source hashes in the Word appendix.'},
    'R02': {'resolves_to': 'OBS and NAS retained listings embedded in the census; 29 September 2026. Metadata scope, not language or music analysis.'},
    'R03': {'resolves_to': 'Staged-audio header inspection, m9j-3e0dcb1bd16e; verified receipt. Folder labels are not content verification.'},
    'R04': {'resolves_to': 'RMS transcript assembly, m9j-9a46b862f339; sealed 29 September 2026. Natural units exclude added canaries.'},
    'R05': {'resolves_to': 'Text language-ID run, m9j-74af7cef0a85; measured per-stratum results. Not an ASR or general-language certificate.'},
    'R06': {'resolves_to': 'Measurement status, m9j-c47f01c0b945; last retained heartbeat 1 October 2026 at 04:33 UTC. No final quality receipt.'},
    'R07': {'resolves_to': 'Report analysis and explicitly labelled planning calculations, derived from the pinned evidence; not forecasts or new measurements.'},
    'R08': {'resolves_to': 'Documentation and governance references: Datasheets, Data Cards, NIST AI RMF and Kenya data-protection law; full references in Word.'},
}
content = {'content_id': 'rms-estate-and-local-language-opportunities', 'version': 1,
    'title': 'RMS estate & language intelligence', 'organisation': 'Royal Media Services · Owner briefing',
    'receipts': receipts, 'facts': {}, 'series': {}, 'options': {}, 'calculations': {}, 'claims': {},
    'coverage': {'covers': 'Retained RMS relational census, OBS/NAS listings, an authorised staged-audio subset, a separately assembled transcript corpus and a narrow language-identification evaluation. Evidence cut: 1 October 2026, 19:12 UTC.',
        'cannot_say': [
            {'gap': 'Estate-wide non-English, non-music eligible audio hours', 'reason': 'No joined asset inventory with verified segment-level language, music and rights labels', 'closes_with': 'Complete the coverage ledger and stratified content qualification'},
            {'gap': 'Estate-wide non-English natural-text tokens or clean aligned speech–text hours', 'reason': 'Database storage is not natural-text volume; text and audio populations are not joined', 'closes_with': 'Versioned exports, tokenizer-specific counts, alignments and independent audits'},
            {'gap': 'Studio/telephone quality or transcript error-rate distributions', 'reason': 'Header properties do not establish audio quality; no final waveform/annotation certificate', 'closes_with': 'Measured observables plus task-specific human-reference evaluation'},
            {'gap': 'External licensing, open release or realised savings and revenue', 'reason': 'Internal custody and indicative tariffs do not establish onward rights or commercial demand', 'closes_with': 'Rights review, actual invoices, retrieval charges and paid pilot validation'}]}}


def fact(key, value, unit, source, cls='measured'):
    ref = f'F{len(content["facts"])+1:03}'
    content['facts'][ref] = {'label': key, 'value': value, 'unit': unit, 'class': cls, 'receipt': source}
    return ref


facts = {}
for key, value, unit, source, cls in [
    ('Database catalogue bytes', head['bytes_total'], 'bytes', 'R01', 'measured'),
    ('Estimated database rows', head['rows_estimate'], 'rows', 'R01', 'estimated'),
    ('Observed rows in census', head['rows_measured'], 'rows', 'R01', 'measured'),
    ('Catalogued tables', 1006, 'tables', 'R01', 'measured'),
    ('Measured table entries', 638, 'tables', 'R01', 'measured'),
    ('OBS listed bytes', obs['bytes'], 'bytes', 'R02', 'measured'),
    ('OBS listed objects', obs['units'], 'objects', 'R02', 'measured'),
    ('NAS listed bytes', nas['bytes'], 'bytes', 'R02', 'measured'),
    ('NAS listed files', nas['units'], 'files', 'R02', 'measured'),
    ('Staged audio files', audio['files'], 'files', 'R03', 'measured'),
    ('Staged audio duration', hours, 'hours', 'R03', 'measured'),
    ('Staged audio bytes', audio_bytes, 'bytes', 'R03', 'measured'),
    ('Companion transcript files', transcripts, 'files', 'R03', 'measured'),
    ('Companion transcript bytes', transcript_bytes, 'bytes', 'R03', 'measured'),
    ('Assembled natural text units', text['units'], 'units', 'R04', 'measured'),
    ('Assembled text characters', text['chars'], 'characters', 'R04', 'measured'),
    ('Source files in text assembly', text['source']['files'], 'files', 'R04', 'measured'),
    ('Text-ID evaluated units', 2800, 'units', 'R05', 'measured'),
    ('Text-ID conditional macro accuracy', trained['adapter_eval']['held']['macro_accuracy'], 'pct', 'R05', 'measured'),
]: facts[key] = fact(key, value, unit, source, cls)


def series(key, label, categories, values, unit, source, cls='measured'):
    content['series'][key] = {'label': label, 'categories': categories, 'values': values, 'unit': unit, 'class': cls, 'receipt': source}


series('S001', 'Listed storage by separate inventory; not additive unique content', ['Database catalogue', 'OBS objects', 'NAS files'],
       {'Decimal TB': [round(head['bytes_total']/1e12, 3), round(obs['bytes']/1e12, 3), round(nas['bytes']/1e12, 3)]}, 'TB', 'R02')
series('S002', 'Readiness grades of measured relational-table entries only', ['A', 'B', 'C', 'D', 'E'], {'Tables': [head['grades'][k] for k in 'ABCDE']}, 'tables', 'R01')
series('S003', 'Measured staged-audio duration by folder label, not certified speech hours', [f'{labels[k]} ({k})' for k in lang], {'Hours': [round(v['hours'], 2) for v in lang.values()]}, 'hours', 'R03')
series('S004', 'Staged-audio file counts by sample rate; not a quality grade', ['11.025 kHz', '16 kHz', '22.05 kHz', '32 kHz', '44.1 kHz', '48 kHz'], {'Files': [audio['sample_rate_counts'][k] for k in ['11025','16000','22050','32000','44100','48000']]}, 'files', 'R03')
series('S005', 'Natural assembled text units by language label', [f'{labels[k]} ({k})' for k in text_lang], {'Natural units': list(text_lang.values())}, 'units', 'R04')
series('S006', 'Natural text partition counts; added synthetic canaries excluded', ['Train', 'Development', 'Held-out', 'Archive test'], {'Natural units': [text['splits'][k] for k in NATURAL_SPLITS]}, 'units', 'R04')
checks = trained['adapter_eval']['held']['per_stratum']
series('S007', 'Text-ID measured conditional accuracy and coverage on equal strata', [labels[k] for k in checks],
    {'Accuracy among judged (%)': [round(v['accuracy']*100, 2) for v in checks.values()], 'Coverage (%)': [round((1-v['abstention_rate'])*100, 2) for v in checks.values()]}, 'percent', 'R05')
series('S008', 'Staged audio and companion transcript inventory; different units by column', [f'{k} · {labels[k]}' for k in lang],
    {'Audio files': [v['files'] for v in lang.values()], 'Hours': [round(v['hours'],2) for v in lang.values()],
     'Audio GB': [round(v['bytes']/1e9,3) for v in lang.values()], 'Text files': [v['transcripts'] for v in lang.values()],
     'Text MB': [round(v['transcript_bytes']/1e6,3) for v in lang.values()]}, '', 'R03')
series('S009', 'Natural transcript partitions by language label', [f'{k} · {labels[k]}' for k in text_lang],
       {name: [text['per_stratum'][k][field] for k in text_lang] for name,field in [('Train','train'),('Dev','dev'),('Held','held'),('Archive','archive_test')]}, 'units', 'R04')
series('S010', 'Database-estate readiness distribution; not speech or text quality', list('ABCDE'),
    {'Tables': [head['grades'][k] for k in 'ABCDE'], 'Share (%)': [round(head['grades'][k]/638*100,2) for k in 'ABCDE']}, '', 'R01')
series('S011', 'Text language-ID: conditional accuracy, coverage and correct-of-all; percentages', [labels[k] for k in checks],
    {'Conditional accuracy (%)': [round(v['accuracy']*100, 2) for v in checks.values()],
     'Coverage (%)': [round((1-v['abstention_rate'])*100, 2) for v in checks.values()],
     'Correct of all (%)': [round(v['correct']/v['units']*100, 2) for v in checks.values()]}, '', 'R05')

claims, sections, slides = content['claims'], [], []


def c(text_, source='R07', supports=None, classification='analysis'):
    ref = f'C{len(claims)+1:03}'
    claims[ref] = {'text': text_, 'supports': supports or source.split('/'), 'evidence_source': source, 'statement_class': classification}
    return '{' + ref + '}'


def paragraph(text_, source='R07', supports=None):
    return {'para': c(text_ + f' [{source}]', source, supports)}


def chapter(title, paras, source='R07', exhibit=None, table=None, points=None, slide_title=None, kicker=None):
    blocks = [paragraph(p, source) for p in paras]
    if exhibit == 'S007':
        blocks.append({'table': {'series_ref': 'S011', 'caption': content['series']['S011']['label']}})
    elif exhibit:
        blocks.append({'figure': {'plate': 'bar', 'series_ref': exhibit, 'caption': content['series'][exhibit]['label']}})
    if table:
        blocks.append({'table': {'series_ref': table, 'caption': content['series'][table]['label']}})
    sections.append({'heading': title, 'blocks': blocks})
    if exhibit == 'S007':
        slides.append({'type': 'assertion_points', 'kicker': (kicker or title) + ' · ' + source, 'title': c(slide_title or title, source),
            'points': [c('The held-out evaluation presents 400 examples per language; 2,800 in total. Conditional macro accuracy is 97.213%.', source),
                       c('Kikamba: 91.349% conditional accuracy; 98.25% coverage; 89.75% correct across all presented examples.', source),
                       c('Kiswahili: 98.950% conditional accuracy; 95.25% coverage; 94.25% correct across all presented examples.', source),
                       c('This measures language identification—not ASR fidelity, general reasoning, linguistic purity or data rights.', source)]})
    elif exhibit:
        slides.append({'type': 'assertion_exhibit', 'kicker': (kicker or title) + ' · ' + source, 'title': c(slide_title or title, source),
            'exhibit': {'plate': 'bar', 'series_ref': exhibit, 'so_what': c((points or [paras[-1]])[0], source)}})
    elif points:
        slides.append({'type': 'assertion_points', 'kicker': (kicker or title) + ' · ' + source, 'title': c(slide_title or title, source),
                       'points': [c(p, source) for p in points]})


slides.append({'type': 'cover', 'title': '{content.title}', 'subtitle': 'Evidence-led owner and AI-lab briefing · 1 October 2026', 'org': '{content.organisation}'})
slides.append({'type': 'exec_summary', 'kicker': 'The answer in brief · R03/R04', 'title': 'The estate has valuable language assets, but its eligible corpus is not yet certified',
    'situation': c(f'The authorised staged subset contains {hours:,.2f} audio hours and {audio["files"]:,} files. A separate transcript build contains {text["units"]:,} natural text units. These are candidate inventories, not an estate-wide qualified total.', 'R03/R04'),
    'complication': c('Language-folder labels do not prove linguistic purity. Music exclusion, independent quality distributions, audio–text alignment and onward rights remain unresolved.', 'R03/R04'),
    'question': 'What should be protected, qualified and productised—and what can responsibly be offered to an AI lab?',
    'answer': 'Treat estate stewardship, corpus qualification and product development as separate workstreams. Pilot controlled-access products while building a defensible data card; do not sell a storage total as training-ready language data.'})

chapter('Executive interpretation', [
    f'The strongest defensible quantitative statement is narrower than an estate-wide sales claim: an authorised staged subset contains {audio["files"]:,} readable-header audio files, totalling {hours:,.2f} file-duration hours and {audio_bytes/1e9:,.2f} decimal GB. A separately assembled, labelled transcript corpus contains {text["units"]:,} natural units and {text["chars"]:,} characters from {text["source"]["files"]:,} source files. Neither statement certifies the intersection of non-English content, non-music speech, acceptable quality and external-use rights.',
    'This is not a finding that the estate has no suitable material. It is a finding that candidate inventory and eligible corpus have not yet been reconciled. A global AI lab should receive both the positive inventory and the disqualifying uncertainties, not a headline with its qualifiers hidden in an appendix.',
    'There is a credible near-term route to value: owner-controlled search and cited context, editorial archive workflows, specialised evaluation and carefully scoped local-language tooling. Open-source software can be released independently of raw data. Corpus licensing, broad model releases and voice products require additional evidence and permission. The options later in this report are advisory propositions, not booked revenue or authorisation to use the data.'
], 'R07')
chapter('How to read this report', [
    'Measured means a retained census, listing, header or worker record reports an observation within a stated scope. It does not mean every observation is independently certified. Derived means transparent arithmetic over those observations. Estimated means sampling, inference or an indicative tariff is involved. Proposed means a recommended design, commercial option or future work item. Unknown means the required evidence is absent; it never means zero.',
    'Counts refer to the named snapshot, not necessarily the live estate today. The relational census was measured on 29 September 2026; listings have their own timestamps. The reporting evidence cut is 1 October 2026 at 19:12 UTC. Audio hours sum file headers; overlapping, replayed or copied recordings may represent the same underlying speech. GB and TB in this report are decimal; GiB and TiB are binary. Character counts, source bytes, training units and tokenizer-specific tokens are deliberately kept separate.',
    'Duplication and storage rationalisation belong in Part I. Part II answers corpus quantity, content qualification and task quality; it uses the already assembled natural-unit counts and refers back to Part I for uniqueness controls rather than conflating file counts with independent examples. No destructive data operation, external release or new model training was commissioned to produce this report.'
], 'R07', points=['Measured, estimated, proposed and unknown are different evidence classes.', 'Each number has a named population; database rows are not text examples.', 'File duration is not speech-only duration; unknown is not zero.', 'Storage units and snapshot dates are explicit throughout.'], slide_title='The accounting rules prevent a large inventory from becoming an inflated AI claim')

slides.append({'type': 'section', 'number': 1, 'title': 'Estate intelligence: condition, duplication and stewardship'})
chapter('Part I · The estate is three overlapping inventories, not one clean corpus', [
    f'The relational catalogue covers {head["databases"]} databases and {head["tables"]:,} table entries across {head["connections"]} measured connections, with {head["bytes_total"]/1e9:,.2f} GB ({head["bytes_total"]/2**30:,.1f} GiB) and an estimated {head["rows_estimate"]:,} rows. These include operational, transaction, catalogue, log and content-related records. Their storage cannot be reported as natural-language training volume.',
    f'The OBS inventory lists {obs["units"]:,} objects occupying {obs["bytes"]/1e12:,.3f} TB ({obs["bytes"]/2**40:,.1f} TiB). The NAS inventory lists {nas["units"]:,} files occupying {nas["bytes"]/1e12:,.3f} TB ({nas["bytes"]/2**40:,.1f} TiB). OBS and NAS can contain copies, off-air captures, proxies, mixed media and versions of material also described in database tables. Adding their bytes does not produce a unique-content or local-language total.',
    'The practical stewardship question is therefore which assets are authoritative, accessible, used, legally retained and valuable for specific purposes. Establish a source-of-record map before deleting copies or quoting the size of a licensable corpus. Media metadata can make the larger archive searchable without exporting raw content or assuming training rights.'
], 'R01/R02', exhibit='S001', points=['These are separate storage inventories. Overlap is unresolved; no unique-estate total is asserted.'], slide_title='Most observed storage is media infrastructure, not a qualified language corpus')

chapter('Coverage is substantial but not complete or perfectly reconciled', [
    f'The census reports {head["rows_measured"]:,} observed rows and {head["tables_measured"]} measured table entries, compared with an estimated {head["rows_estimate"]:,} catalogue rows. The ratio is {head["rows_measured"]/head["rows_estimate"]*100:.2f}%, but it is not a random-sample coverage probability or a basis for a single estate-wide confidence interval. Small tables were fully read; large tables used stratified keyset samples; some lacked a suitable key and used a head sample.',
    'The retained counts require an explicit reconciliation note. Complete, stratified-sample and head-sample method counts are 513, 83 and 41, totalling 637 rather than the headline 638 measured entries. The report also flags 44 failed table reads and 368 empty entries; these indicators overlap catalogue classifications and must not be forced into a mutually exclusive pie chart. The artists_app connection is reported blocked. The method-ledger discrepancy is a release issue for precise statistical claims, not a reason to discard the measured evidence.',
    f'OBS coverage is {obs["sources_complete"]} completed sources out of {obs["sources"]} listed sources; {obs["sources_blocked"]} are blocked or missing. That is {obs["sources_complete"]/obs["sources"]*100:.1f}% by source count, not by bytes or eligible hours. NAS enumeration covered {nas["sources_complete"]} of {nas["sources"]} registered roots. Enumeration-complete still does not mean language, music, rights or semantic content were inspected.'
], 'R01/R02', points=['Relational methods mix full reads, stratified samples and head samples.', 'OBS: 66 of 106 sources completed; 40 blocked or missing.', 'NAS: 16 of 16 registered roots enumerated; content qualification is separate.', 'Method counts and failure flags need reconciliation before statistical certification.'], slide_title='Access coverage and content coverage must be reported separately')

chapter('Relational readiness is uneven and is not an audio-quality assessment', [
    'Across the measured relational-table entries, the internal readiness distribution is A: 171, B: 62, C: 191, D: 189 and E: 25. These sum to 638. Their respective shares are 26.80%, 9.72%, 29.94%, 29.62% and 3.92%, subject to rounding. The denominator excludes unmeasured entries; these grades must never be applied to the audio or transcript corpus.',
    'The grade is a heuristic stewardship index, not an external AI-lab certification. The implemented score weights completeness at 35%, exact-duplicate absence at 20%, degradation absence at 20%, freshness at 15% and absence of personal-data markers at 10%. Grade cut-offs are 85, 70, 55 and 40. Optional null fields, legitimate personal data, incomplete marker checks and unknown freshness can materially change the interpretation. Inspect the underlying column contract rather than equating every null with missing mandatory information.',
    'Use the index to choose inspection order and remediation owners. A high grade does not establish rights or semantic usefulness; a low grade does not prove that every record is unusable. Preserve task-specific quality dimensions and coverage alongside any summary score.'
], 'R01', exhibit='S002', table='S010', points=['The grades describe relational stewardship only; they do not classify speech quality, transcript accuracy or legal eligibility.'], slide_title='The readiness grades prioritise remediation; they do not certify a training dataset')

chapter('Quality and privacy signals are material, but their denominators differ', [
    'The headline weighted signals are 1.537% exact duplicate rows, 3.584% normalised duplicates, 22.957% degraded rows, 81.695% null-bearing rows, 71.833% personal-data-marker rows and 85.313% near-duplicate text. These measures concern different measured or sampled populations. Personal-data checking covered 1,011,330 rows. The report does not establish a common independent sampling design; the percentages cannot be multiplied by the entire estimated row inventory as if they were population parameters.',
    'Degradation-kind signals include truncation at 21.91%, invalid format at 6.26%, placeholder content at 1.26% and whitespace anomalies at 0.94% of the relevant weighted measurement. A row may exhibit several kinds. The census also identifies 983 near-empty columns among 7,563 measured columns. These are operational leads, not proof of semantic corruption in every affected value.',
    'The condition-byte indicators overlap. In particular, null-bearing, degraded and stale byte estimates are not disjoint partitions; an apparent zero “clean bytes” residual is not proof that no useful material exists. Recompute an exclusive condition taxonomy only after defining what completeness and fitness mean for each data product. Personal-data markers trigger minimisation and review, not an automatic blanket prohibition or legal conclusion.'
], 'R01', points=['Null-bearing is not the same as missing a mandatory field.', 'PII markers are a risk-screening signal, not a legal determination.', 'Degradation and stale-byte measures overlap; do not sum them.', 'Audio and transcript quality need their own independent measurements.'], slide_title='The measured warning signals justify targeted inspection, not blanket rejection')

chapter('Duplication has several meanings and several confidence levels', [
    'Within-table exact matching excludes the primary key. Normalised matching applies additional normalisation; near-duplicate text uses text sketches rather than semantic embeddings. The large near-duplicate-text signal may include repeated templates, boilerplate or log formats. It does not mean that the same fraction of the whole estate is safely deletable. Similarly, same-schema table overlap is a sketch-based estimate, not an authoritative row-by-row equivalence proof.',
    'The relational report identifies 71 cross-table overlap pairs, approximately 1.302 GB of within-table duplicate-byte candidates and 0.0566 GB of cross-table duplicate-byte candidates. Separately, the transcript assembly removed 2,525 repeated units before its natural-unit inventory was emitted. Those are different operations on different populations; neither should be subtracted again from the counts in Part II.',
    'For AI use, duplication has a second consequence: evaluation contamination. The same recording can appear under different files, exports, presenters or programme names. Canonical asset IDs, exact hashes, acoustic fingerprints and segment provenance should feed group-aware train/development/evaluation partitions. Removing storage copies is not sufficient to prove an independent held-out set.'
], 'R01/R04', points=['Exact, normalised, sketch-near and semantic overlap are not interchangeable.', 'Relational candidates and transcript-cleaning counts are different populations.', 'Retain a canonical asset and lineage before retiring any copy.', 'Use identity controls to protect evaluation independence as well as storage.'], slide_title='Duplicate candidates are an investigation queue, not a deletion instruction')

chapter('Object-store overlap and archive candidates offer leverage with qualifications', [
    f'OBS contains {obs["duplicate_candidates"]:,} ETag-plus-size duplicate candidates—about {obs["duplicate_candidates"]/obs["units"]*100:.2f}% of listed objects—with {obs["duplicate_bytes_estimate"]/1e12:.3f} TB of estimated candidate bytes. Multipart ETags are not universal content hashes, and candidate counts are not necessarily the number of removable extra copies. Confirm canonical identity and multiplicity before converting this into a reclamation estimate.',
    f'The retained listing marks {obs["cold_sources"]} sources, holding {obs["cold_bytes"]/1e12:.3f} TB, as not written for over a year. This is a write-age observation, not a read-frequency measurement. A large archive may still be heavily read for editorial retrieval, compliance or revenue. NAS duplicate content and speech durations are not established by its directory enumeration.',
    'A conservative execution sequence is to observe access, simulate lifecycle changes, verify hashes on candidates, review contractual retention and restore obligations, then pilot a reversible tiering policy. Keep operationally required copies until ownership and recovery requirements are explicit. Do not delete a music-labelled bucket merely because music is outside the present AI use case.'
], 'R02', points=['1.14 million object candidates are flagged by ETag and size, not universal hashes.', '46.054 TB of old-write storage is an archive candidate, not proven unused.', 'Read demand, restore time, retrieval fees and retention must be checked.', 'Identity validation and reversible pilots precede reclamation.'], slide_title='Archive and duplicate candidates are substantial, but net savings are not yet proven')

chapter('Freshness and growth need field-level interpretation', [
    'The census flags 290 tables with a latest selected timestamp older than a year, representing approximately 58.132 GB. It also records future-dated or extreme historical values in some timestamp columns. Examples include dates beyond the reporting cut and sentinel-like ancient values. These can be legitimate event dates, entry errors, schema defaults or the wrong field for measuring modification age.',
    'A selected latest timestamp is not automatically a last-write time. Validate each field’s semantics, time zone, clock behaviour and update path. Repeated identical byte counts are not proof of zero business activity; catalogue size estimates can remain flat while rows change. Likewise, small row deltas between snapshots may reflect estimates or asynchronous measurement rather than a reliable growth rate.',
    'Define a freshness contract for each product: publication time for editorial context, last confirmed validity for reference data, transaction settlement time for operational analytics and last content observation for media. Recompute staleness under that contract. This is more actionable than applying a single age threshold to the entire estate.'
], 'R01', points=['Selected timestamps can represent events rather than writes.', 'Future dates and sentinel values need explicit treatment.', 'Storage deltas are not automatically business growth rates.', 'Freshness must be defined for each intended product.'], slide_title='Freshness is a product-specific property, not a universal timestamp rule')

gross_decimal = obs['cold_bytes']/1e9*.023
gross_binary = obs['cold_bytes']/2**30*.023
chapter('Storage economics should be quoted as conditional bounds', [
    f'The retained report uses reference tariffs of USD 0.1095 per database GB-month and USD 0.023 per object-storage GB-month, not the owner’s invoice. For the old-write OBS candidate alone, applying the object tariff gives a gross full-standard-storage ceiling of USD {gross_decimal:,.2f} per month if “GB” is decimal, or USD {gross_binary:,.2f} if the billing unit is GiB. The retained figure follows the latter convention. Billing-unit semantics must be confirmed before presenting a payable saving.',
    'Neither gross ceiling is a net archive saving: cold-tier storage, retrieval, restore operations, egress, minimum retention charges, migration effort, ongoing monitoring and service risk must be deducted. Reclamation and archival candidates can overlap; adding their separate quoted savings double counts value. Currency, region, tax, reserved commitments and effective billing rates also require reconciliation.',
    'A decision model should separately show verified removable bytes, archive-eligible bytes, operational cost avoided, one-off migration cost and downside scenarios. Price it with actual owner rates. The current evidence supports a controlled cost-reduction investigation, not a guaranteed savings claim or a valuation of the language corpus.'
], 'R01/R02/R07', points=['Use the owner’s effective tariff and actual billing units.', 'Gross standard-tier cost is not net archive savings.', 'Do not add overlapping reclamation and tiering opportunities.', 'Model restore, egress, retention and migration costs explicitly.'], slide_title='The economics are useful bounds, not an invoice-backed savings commitment')

chapter('Stewardship priorities should protect value before removing cost', [
    'Begin with a canonical source and access ledger, then resolve blocked high-value sources. Assign owners to large operational logs, replicated business schemas and media archives. Confirm which copies serve staging, backup, audit or contractual purposes. For each proposed action record its evidence, intended benefit, dependency, reversibility and approver.',
    'Next, establish query and retrieval baselines before altering indexes or storage tiers. Prefix-covered indexes are candidates, not guaranteed redundant operationally: workload, statistics, uniqueness, hints and write/read balance matter. Retention windows and restore exercises should be demonstrated before archival cut-over. Only then automate a reviewed policy.',
    'The language-data workstream should use the same identity and rights ledger, but should not wait for every general estate-cleanup item. A well-scoped, traceable local-language subset can be qualified and piloted while broader stewardship continues. Keep infrastructure savings and data-product value as separate business cases.'
], 'R07', points=['Establish ownership and canonical identity first.', 'Validate read workloads and restore obligations before tiering.', 'Review index candidates against real queries, not schema shape alone.', 'Run corpus qualification alongside—not behind—the entire cleanup programme.'], slide_title='Stewardship and corpus qualification can proceed together without conflating their goals')

slides.append({'type': 'section', 'number': 2, 'title': 'Non-English, non-music audio and text: a defensible accounting'})
chapter('Part II · The precise answer is a bounded candidate inventory', [
    f'Audio: {audio["files"]:,} files with readable headers, {hours:,.2f} file-duration hours and {audio_bytes/1e9:,.3f} GB ({audio_bytes/2**30:,.3f} GiB) in the authorised staged corpus. These files are grouped under eight local-language labels. Their content has not been independently shown to exclude English, music, silence, mixed programmes or unusable intervals. The record cannot support a certified non-English, non-music speech-hour total.',
    f'Text: {text["units"]:,} natural units, {text["chars"]:,} characters and {text["source"]["files"]:,} source files in a separately versioned transcript build covering seven labels. This establishes a labelled candidate corpus, not a human-audited non-English natural-text total, a translation corpus or a clean speech–text alignment. Text language purity, transcript fidelity and lyrical/music contamination remain unquantified.',
    f'The staged-audio inspection also lists {transcripts:,} companion transcript files occupying {transcript_bytes/1e6:,.3f} MB. These companion files and the separate assembled-text population have different scope and provenance. They must not be added together as disjoint text holdings or treated as proof that every audio hour has a verified aligned transcript.',
    'The whole-estate eligible total is unknown on the present record. It is not defensible to extrapolate this staged subset to the millions of OBS/NAS objects, or to convert database bytes into language hours or tokens. The right external statement presents the candidate inventory, explains the narrower qualified slice and supplies a concrete closure programme.'
], 'R03/R04', points=[f'{hours:,.2f} staged audio hours; {audio_bytes/1e9:,.2f} GB; music and language purity unverified.', f'{text["units"]:,} natural text units; {text["chars"]/1e6:.2f} million characters; separate source population.', 'Estate-wide eligible totals and quality distributions remain unmeasured.', 'The uncertainty is a qualification gap, not evidence that suitable data is absent.'], slide_title='The verified inventory is sizeable; the strictly eligible total remains unknown')

chapter('The audio-duration distribution is highly uneven', [
    'Six folder groups contain roughly eighty to ninety-two hours each, whereas Wanga/Luhya and Bukusu are much smaller in the staged audio snapshot. This matters operationally: a pooled metric can hide weak dialect coverage, and the smallest groups will need purposeful qualification or collection rather than proportional random sampling alone.',
    f'Wanga/Luhya has {lang["lwg"]["hours"]:.4f} staged hours and Bukusu has {lang["bxk"]["hours"]:.4f}; together they represent {(lang["lwg"]["hours"]+lang["bxk"]["hours"])/hours*100:.2f}% of staged file duration. These are folder assignments. A linguist should validate language names, code mappings, dialect relationships and any code-switching convention before a global dataset card treats them as certified language strata.',
    'The eight audio labels and seven text labels are not contradictory: the assembled transcript build lacks a Bukusu stratum. Nor does the large number of Wanga text units prove correspondingly large aligned audio. The corpus-build populations differ and need a source-level join.'
], 'R03/R04', exhibit='S003', table='S008', points=['Folder labels are provisional linguistic metadata; file duration is not isolated speech time.'], slide_title='The smallest audio strata need deliberate qualification, not pooled reporting')

chapter('Capture properties are measurable; quality grades are not yet established', [
    'The measured sample-rate distribution is 3,126 files at 44.1 kHz; 162 at 48 kHz; 49 at 22.05 kHz; 597 at 11.025 kHz; 22 at 16 kHz; and 2 at 32 kHz. These counts sum to the staged inventory. No unreadable headers were reported. This supports header accessibility and capture-format accounting only; it does not establish successful full decoding, low noise, intelligibility or correct transcripts.',
    'A low sampling rate limits available bandwidth, but a high sampling rate cannot restore information already lost upstream. Container size also depends on encoding, bit depth, channels, metadata and compression—not just duration or quality. Do not assign “studio”, “telephone” or “broadcast-clean” grades from sample rate or file extension.',
    'A proper audio-quality distribution needs full-decode success, effective bandwidth, clipped-sample share, silence and speech-active duration, loudness variability, channel consistency, noise and reverberation measures, overlapping speech, intelligibility and task-relevant human evaluation. Thresholds should be chosen for the intended task and validated on native-speaker references rather than guessed from file metadata.'
], 'R03', exhibit='S004', points=['Sample rate and readable headers are observed properties, not a measured clean-speech distribution.'], slide_title='The evidence describes capture formats, not yet the quality of usable speech')

chapter('The waveform measurement record is incomplete and stale', [
    'The retained measurement status reports progress on 1,900 of 3,958 files, but its last heartbeat is 1 October 2026 at 04:33 UTC. At the reporting cut there is no digest-verified final result and no stored completed measurement rows in the inspected measurement record. The elapsed reporting interval means “running” must be read as last recorded state, not confirmation that the remote process is still healthy.',
    'Consequently, no signal-to-noise, clipping, speech fraction, music fraction, studio-versus-telephone or quality-band percentages are published here. A progress counter is not an analyzable dataset, and it cannot be used as a quality denominator. Recover or complete the measurement receipt, including failures and excluded files, before publishing distributions.',
    'The priority is not simply to finish a batch. The record must reconcile input assets, completed analyses, errors, segment durations, classification uncertainty, code/configuration hashes and the original capture inventory. The raw observables then need a task-specific interpretation layer that clearly separates automated indicators from independently established labels.'
], 'R06', points=['The retained progress counter is not a completed measurement dataset.', 'Its stale heartbeat cannot establish current remote process health.', 'No completed quality-band percentages are defensible from that record.', 'Finish and reconcile the measurement receipt before publishing distributions.'], slide_title='A stale progress record cannot stand in for a completed quality measurement')

chapter('Define non-English and non-music at the segment level', [
    'Use mutually understandable content categories: local-language speech without music; English-only speech; code-switched speech; music-only; speech with music underneath; other sound; silence; and unresolved. A file can contain several categories, so file-level inclusion is too coarse for a strict speech inventory. Speech over a music bed is not automatically “non-music”; classify it separately unless the recipient explicitly accepts it.',
    'Define the target before counting. Strict non-English speech can exclude any English-bearing segment; a local-language-dominant product can instead retain code-switched segments with token- or time-based proportions and explicit flags. These are different products and cannot share an unqualified headline. Lyric text, songs, station jingles and promotional beds also need treatment when qualifying transcripts.',
    'Automated speech/music and language scores can prioritise review, but their errors must be measured on independent native-speaker annotations. Unknown labels stay unknown. A bucket named for music is a useful exclusion lead, not proof that music is absent elsewhere. Likewise a local-language folder can contain English quotations, presenters introducing songs or mixed programmes.'
], 'R07', points=['Count segments, not entire programmes, for strict eligibility.', 'Separate English-only, code-switched and local-language-only speech.', 'Separate music-only and speech-with-music; keep unresolved content explicit.', 'Agree the recipient’s acceptance definition before producing the final quantity.'], slide_title='The target corpus is an intersection of verified properties, not a folder selection')

chapter('Text quantity is real, but units, characters and tokens are different', [
    'The assembled corpus is dominated by Kalenjin and Wanga-labelled text units, followed by Dholuo, Ekegusii, Kiswahili, Kikuyu and Kikamba. Unit counts reflect the assembly’s segmentation rule; they are not word counts, unique speakers or independent documents. A short sentence and a longer utterance can both count as one unit, so a row-count comparison alone does not describe training mass.',
    'The character count is an observed assembly measure. It is not UTF-8 bytes, and a generic characters-per-token divisor would not produce a defensible multilingual token inventory. Tokenisation varies by model vocabulary and language. Report tokenizer name/version, normalisation, special tokens, truncation and whether counts are unique input tokens or repeated training exposure.',
    'For context, the recorded 8B run reports 9,502,124 training-input tokens after its own preprocessing and sequence cap, including its added canary/reference material. Inspection of the worker implementation shows this field counts the tokenised input dataset, not the epoch-multiplied exposure counter. It is therefore not a whole-estate token total and should not be marketed as unrestricted natural text.'
], 'R04/R05', exhibit='S005', table='S009', points=['The text-unit inventory is verified within this build; token mass and alignment require their own definitions.'], slide_title='Text units establish a corpus inventory, not a universal token or speech equivalent')

chapter('The existing partitions provide useful structure, not final independence proof', [
    'Natural units are partitioned into 129,984 training units, 8,280 development units, 18,980 held-out units and 269 archive-test units. These sum to 157,513. The source records a group-disjoint split by presenter for transcripts. That is useful lineage, but a presenter-group rule is not independent proof that the same voice, programme, event or semantic content never appears across partitions.',
    'The assembly separately records 60 inserted canaries and 80 reference canaries. They are deliberate evaluation material, not naturally occurring language inventory. Do not count them as a commercial data asset. The recorded train artefact includes them in addition to the natural training subset.',
    'Preserve the original sealed-set digest, but recognise that repeatedly inspecting results during recipe selection changes what the set can support. A sealed set can remain byte-immutable while ceasing to be a blind final evaluation. A new independent final set, with source-, session- and speaker-aware reconciliation, is required before claiming generalisation after further selection.'
], 'R04', exhibit='S006', points=['Partition integrity, speaker independence and final-evaluation blindness are separate requirements.'], slide_title='A sealed evaluation file is not automatically an untouched final benchmark')

chapter('Transcript quality and aligned speech hours are still open', [
    'No independent word-error-rate or character-error-rate distribution has been established for the transcript corpus in the reviewed evidence. Folder language, successful assembly and high language-identification performance cannot substitute for transcript fidelity. Punctuation, diacritics, named entities, local orthography, borrowed words and code-switches deserve separate treatment.',
    'Paired speech–text value requires a verified join: canonical audio ID and hash, segment start/end, transcript version, alignment confidence, annotation or ASR origin, language/dialect, speaker/session grouping, rights basis and quality state. The difference between companion-transcript counts and the assembled-text sources means the paired-hour quantity is presently unknown. Do not infer it from the smaller file count or from total header duration.',
    'Create a stratified human reference with native-speaker adjudication, record annotator disagreement, and publish errors by language, dialect, acoustic condition and content type. Evaluate alignment separately from transcription. A corpus may be useful for language identification or retrieval before it is suitable for ASR supervision; release it under the narrower supported use.'
], 'R03/R04/R07', points=['WER/CER and clean paired hours are not measured in the current record.', 'Language-ID accuracy does not validate every transcript.', 'Audio–text joins need timestamps, hashes, provenance and rights.', 'Qualify by intended task rather than inventing a single “good data” grade.'], slide_title='The transcript corpus is promising, but supervised-speech quality is not yet quantified')

chapter('The text model proves a narrow capability, not corpus-wide quality', [
    'The retained 8B text language-identification evaluation uses 2,800 held-out examples, with 400 per language stratum. Conditional macro accuracy among judged examples is 97.213%. The reported figure is not accuracy over every example regardless of abstention, nor does it certify grammar, factuality, translation, ASR fidelity, broad language modelling or privacy.',
    'Kikamba records 359 correct of 393 judged, with 7 abstentions: conditional accuracy is 91.349%, coverage is 98.25%, and correct predictions as a share of all 400 presented examples are 89.75%. Kiswahili has 377 correct, 381 judged and 19 abstentions: conditional accuracy is 98.950%, coverage is 95.25%, and correct-of-all is 94.25%. A lab should see all these denominators, not just the highest-looking percentage.',
    'The language-ID result is evidence that the staged labels carry a learnable signal. It is not independent evidence that those labels are linguistically perfect or that all source data meets an external use licence. Earlier audio runs also showed that language accuracy did not establish speaker privacy. Use these findings to design qualification work, not to imply that the broader cognition programme or a general local-language foundation model is complete.'
], 'R05', exhibit='S007', points=['Conditional accuracy must be read with coverage and independent source-quality evidence.'], slide_title='The admitted text classifier validates one task; it does not certify the whole estate')

chapter('Compute eligible hours with an auditable segment ledger', [
    'For a strict speech corpus, eligible hours equal the sum of segment duration in seconds divided by 3,600, restricted to segments whose language policy, music policy, quality policy, rights basis and intended use all pass. Unresolved gates remain unresolved; they do not become pass values or count as zero-duration assets. Report known-included, known-excluded and unresolved duration separately.',
    'The asset ledger should include source system, canonical ID, cryptographic hash, recording timestamp, duration, channel and codec properties, source rights, segment labels, confidence, annotation origin, quality indicators and all exclusions. Retain the versioned policy applied. When only a sample is annotated, distinguish the observed qualifying hours from an estimated population yield.',
    'Use duration-weighted, stratified estimation with the actual inclusion probabilities. Cluster by programme/session or speaker where appropriate; an asset-count sample can be biased toward short files. Confidence intervals must reflect the sampling design and classifier validation, not just a binomial formula over correlated segments. No estate-wide confidence interval is claimed in this report because the necessary design and labels are not yet present.'
], 'R07', points=['Eligible hours are the duration-weighted intersection of explicit gates.', 'Separate included, excluded and unresolved duration.', 'Stratify by language, source, time, programme and acoustic condition.', 'Use design-aware uncertainty; do not multiply marginal percentages.'], slide_title='An auditable ledger can turn the candidate inventory into a credible lab offer')

chapter('A sampling illustration is not a substitute for the actual design', [
    'As a planning illustration only, a simple random sample of independent observations needs about 385 observations to estimate a proportion within five percentage points at approximately 95% confidence under the worst-case proportion of one half. This follows the normal-approximation expression n = z² p(1−p) / e² with z = 1.96. It is not an adopted requirement or a measured sample size for this estate.',
    'Broadcast segments are clustered and languages are imbalanced, so effective sample size can be far smaller than the raw segment count. Rare languages, music beds, code-switching and failure cases may require deliberate oversampling. Weight results back to the population design and preserve separate per-stratum uncertainty. Confirm exact or bootstrap intervals where assumptions warrant them.',
    'Even a sample with no detected contamination does not prove zero contamination in the population. The recipient and data owner must agree tolerances and escalation rules. The operational aim is an honest, reproducible statement of expected quality and uncertainty, not a convenient green badge.'
], 'R07', points=['Illustrative sample formulas assume independence and a defined population.', 'Correlated recordings and rare strata change the effective sample size.', 'No detected contamination is not proof of zero contamination.', 'Tolerance, adjudication and release policy must be agreed explicitly.'], slide_title='The qualification design should expose uncertainty rather than hide it')

chapter('What a global AI lab should receive', [
    'Provide a versioned data card and machine-readable manifest with source provenance; permitted and prohibited uses; recording and publication dates; language/dialect and code-switch distributions; hours and bytes by segment category; encoding and sampling properties; verified quality metrics and uncertainty; annotation and transcript provenance; rights and privacy exclusions; and known representational limitations. The data card should identify who is responsible for corrections and withdrawals.',
    'The acceptance pack should include sample selection and adjudication protocols, inter-annotator disagreement, task-specific validation, complete failure/exclusion counts, canonical split IDs, contamination controls, exact tokenizer counts where relevant, reproducible code/configuration hashes, and a documented way to reproduce the reported figures. It should distinguish source-level consent from processing agreements, model-training permissions, redistribution and public release.',
    'A lab may accept a useful research subset with declared limitations; it should not be asked to infer missing evidence from a model demo. Offer a controlled evaluation path first, with independently selected samples and a secure review process. Only widen access after the claims in the intended offer can be independently checked.'
], 'R07/R08', points=['A data card, manifest and rights matrix must travel with the corpus.', 'Provide per-stratum quality, uncertainty and failure counts—not one pooled score.', 'Supply independently reproducible partitions and evaluation evidence.', 'Offer controlled qualification before promising unrestricted licensing.'], slide_title='A lab-ready offer is a reproducible evidence package, not a storage statistic')

slides.append({'type': 'section', 'number': 3, 'title': 'A broader portfolio: commercial services and local-language enablement'})

chapter('Part III · Data value depends on the product and the permitted use', [
    'The following portfolio is broader than context services and open-source support. It separates enterprise service revenue, data and evaluation products, and public-interest ecosystem investment. A good option does not require every asset in the estate: a narrow, rights-cleared slice with a clear buyer and measurable benefit can be more valuable than a larger undocumented archive.',
    'These options are proposed uses, not evidence that the current estate is already eligible for them. Several can begin with owner-controlled access and a limited qualified subset. Others depend on independent speech labels, aligned transcripts, additional permissions or new data collection. A realistic roadmap sequences those dependencies rather than treating all options as immediately launchable.',
    'Commercial validation should identify the buyer, the workflow cost or risk being reduced, the unit of value, the service-level obligation and the cost of rights and curation. Avoid valuing the data solely by raw hours, gigabytes or model-training compute. No revenue forecast, market-size estimate or customer demand claim is asserted here.'
], 'R07', points=['Enterprise services, research products and ecosystem investment have different economics.', 'Start with a narrow qualified slice and a named user problem.', 'Do not equate an attractive use case with present eligibility.', 'Validate willingness to pay before treating the portfolio as revenue.'], slide_title='The estate supports several product hypotheses—not one undifferentiated data sale')

OPPORTUNITIES = [
('Context as a service', 'Enterprise assistants, newsrooms, research teams and approved local-language applications',
 'Versioned, cited retrieval of authorised local context through a governed interface; language routing, provenance, freshness and correction are part of the product.',
 'Begin with a small, rights-cleared text slice and named domains. Retain document-level access controls, source dates, quote limits, correction history and withdrawal propagation. An answer must cite evidence and abstain when coverage is weak; the service must not disguise missing local knowledge with fluent generation.',
 'Subscription, usage or enterprise agreement; validate retention, citation utility, answer coverage and workflow savings.',
 'Retrieval relevance, faithfulness, language/dialect coverage, freshness, refusal quality and cost per accepted answer. Citation is not itself proof of truth.',
 'Source rights for retrieval and excerpting; publication updates; factual review; privacy and content-access boundaries.'),
('Private archive search and editorial intelligence', 'RMS editorial teams and authorised institutional archive users',
 'Search, discovery, timeline building and reusable editorial context across a curated subset of transcripts and metadata.',
 'Start inside the owner boundary, where a private assistant can reduce archive-search time without exporting raw media. Preserve the distinction between archival claims and current facts. Attach programme/date context, version history and retention rules; do not turn named people in an archive into an unrestricted profiling service.',
 'Internal productivity case first; institutional access or managed archive service where rights permit.',
 'Time to find usable evidence, recall on representative editorial tasks, false-match rate, citation completeness and corrected-record propagation.',
 'Canonical asset links, editorial validation and role-based access; not every archive item is current or factually endorsed.'),
('Local-language transcription, captions and media accessibility', 'Broadcasters, archives, public-service content teams and accessibility programmes',
 'Task-specific ASR, captions, alignment and searchable timecodes for qualified language/acoustic strata.',
 'Use the current corpus only after a human-reference ASR and alignment audit. Treat music beds, overlap, names, local spelling and code-switches as explicit conditions. Keep native-speaker correction in the workflow and price difficult audio separately rather than promising a single accuracy level for every programme.',
 'Per-minute processing, managed service or enterprise contract; quality-linked acceptance and rework costs determine margin.',
 'WER/CER by stratum, timing error, named-entity error, subtitle readability, review effort and turnaround time.',
 'Clean paired segments, independently checked references, lawful processing and a supported rather than assumed model capability.'),
('Independent local-language benchmark and evaluation service', 'Model developers, global AI labs and local-language application buyers',
 'A controlled, blind benchmark with per-language/dialect scoring, abstention and coverage, leakage checks and human adjudication.',
 'Keep benchmark material out of training and routine public examples. Use a rotated independent final set after recipe selection, publish task definitions and sampling limitations, and make evaluation reproducible without disclosing restricted raw data. Separate research feedback from final adjudication.',
 'Evaluation engagements, secure benchmark access or recurring independent assessments.',
 'Label agreement, coverage of intended strata, statistical uncertainty, contamination resistance and repeatability.',
 'Independent labels and partitions; benchmark rights; conflict-of-interest controls. The current language-ID score alone is not a benchmark product.'),
('Rights-cleared research corpus licensing', 'AI labs and research institutions with a defined training or evaluation objective',
 'Versioned corpus slices with a data card, manifest, permissible-use terms, correction/withdrawal process and documented quality.',
 'Offer specific content categories and verified quantities rather than the whole raw estate. Licensing terms should distinguish evaluation, adaptation, foundation-model training, redistribution and derived model publication. Price the curation, assurance and update service, not just transfer volume.',
 'Scoped licence, time-bound access, support or recurring updates, subject to actual rights and demonstrated buyer need.',
 'Qualified hours/units delivered, label quality, traceability, update reliability, withdrawal compliance and buyer acceptance.',
 'Onward-use rights, contributor and programme permissions, privacy review, geographic transfer terms and verified quality. Not cleared by internal training authorisation alone.'),
('Secure research enclave and compute-to-data access', 'Research partners unable to receive unrestricted source copies',
 'Approved code executes against a controlled dataset slice; reviewed metrics and permitted outputs leave the environment.',
 'An enclave can reduce raw-data movement but does not remove the need for lawful purpose, output review and leakage controls. Define what models, embeddings, examples and logs may leave; monitor query patterns and cumulative disclosure, and plan revocation and destruction evidence.',
 'Project access, managed research environment or jointly funded programme.',
 'Time to approved experiment, reproducibility, output-review quality, isolation and operating cost per engagement.',
 'Approved partner and purpose, adequate controls, contractual liability and a qualified dataset. This is not a loophole around data-protection law.'),
('Terminology, entities and multilingual knowledge resources', 'Search, translation, education and public-service application developers',
 'Curated local-language terminology, place/name variants, domain concepts and source-linked entity relationships.',
 'A carefully curated lexicon or knowledge resource may deliver more immediate utility than a large model trained from scratch. Use native-speaker and domain review, dates and regional scope. Preserve ambiguous names and contested terminology; do not infer personal attributes or sensitive facts from co-occurrence.',
 'Specialised reference-data service, integration or support; an appropriately licensed public subset can strengthen adoption.',
 'Term precision, language/dialect coverage, provenance, update latency and downstream search or translation gains.',
 'Annotation, semantic validation and source rights. Corpus co-occurrence is not automatically factual knowledge.'),
('Translation and localisation support', 'Publishers, civic services, education providers and local-language content teams',
 'Reviewed glossaries, translation memories and domain-specific assistance, with human approval for consequential content.',
 'The present transcript corpus is not a verified parallel corpus. Start with terminology and controlled human translation, then commission aligned source/target material where rights permit. Evaluate meaning, dialect, register and named entities rather than relying on a single automatic similarity score.',
 'Managed localisation, specialist tooling or domain-specific translation support.',
 'Human adequacy and fluency, terminology consistency, edit distance or review effort, and harmful mistranslation rate.',
 'Parallel references, native-speaker review and domain safeguards; especially stringent review for legal, health or emergency content.'),
('Specialised small models and adapters', 'Enterprises and developers needing bounded local-language tasks',
 'Language routing, archive classification or other measured narrow capabilities with an explicit supported-use envelope.',
 'The existing text language-ID result is a useful starting point for a narrowly scoped adapter service. Do not claim general reasoning or foundation-model competitiveness from it. Match calibration and comparison to the selected base, qualify a fresh final evaluation and review both base-model and dataset licences before distributing weights.',
 'Hosted inference, adaptation work, support or licensed model distribution where permitted.',
 'Per-stratum accuracy times coverage, latency, compute cost, robustness, privacy and withdrawal obligations.',
 'Actual task evidence, base licence compatibility, data rights and complete admission/serving controls.'),
('Aggregate media intelligence and public-interest analytics', 'Editorial planning, researchers and approved institutional users',
 'Source-linked trends, topic coverage and language-presence analysis at aggregate levels, with uncertainty and representation limits.',
 'Broadcast content reflects editorial selection and audience context; it is not a random sample of public opinion. Avoid individual profiling and unsupported demographic or political inference. Publish the sampling frame, missing channels and changes in programme composition, and retain editorial review of consequential conclusions.',
 'Research briefs, controlled analytics subscriptions or public-interest partnerships.',
 'Coverage, stability across sources/time, annotation validity, interpretability and risk of misleading population claims.',
 'Content access, validated taxonomy, aggregation/privacy safeguards and a clearly bounded claim about the represented population.'),
('Native-speaker annotation and data-quality services', 'Corpus owners, research institutions and model developers',
 'Adjudicated labels, transcript correction, dialect validation, quality audits and reproducible evaluation packs.',
 'Build a fair, documented contributor programme with training, disagreement handling, quality review and appropriate compensation. The resulting capability can improve the owner corpus and become a service to other datasets. Avoid using an opaque model label as human ground truth or rewarding workers solely for agreement with an uncertain machine.',
 'Project services, managed annotation operations or recurring quality assurance.',
 'Agreement and adjudication outcomes, error audits, turnaround, effective cost per accepted label and contributor retention.',
 'Qualified reviewers, governance, safe handling of sensitive material and clear permitted use of contributed annotations.'),
('Open-source local-language enablement and heritage access', 'Local researchers, universities, developers and language communities',
 'Open tools, schemas, evaluation harnesses and documentation; separately approved dataset or model releases where rights allow.',
 'Separate open-source code, open data, model weights and a hosted service: each has a different licence and operating obligation. Begin with reusable tools and synthetic or clearly licensed demonstrations. A public heritage or educational collection requires its own source review, community participation and withdrawal/correction policy; broadcasting a voice is not consent to every downstream use.',
 'Grant or consortium support, sponsorship, hosted/support services and partnership adoption; open-source itself is not a guaranteed revenue stream.',
 'Independent reproducibility, useful contributions, native-language adoption, responsible reuse and sustainable maintenance.',
 'Licence compatibility, release-specific rights, community stewardship, hosting support and an explicit sustainability plan.'),
]

product_titles = {1: 'Cited context can support bounded enterprise workflows', 3: 'Transcription services require validated speech–text alignment',
    4: 'Independent evaluation can turn language coverage into a service', 5: 'Corpus licensing is a rights-and-assurance product, not a raw data sale',
    6: 'Compute-to-data access limits raw-data movement, not the underlying obligations',
    12: 'Open-source tools can build an ecosystem without premature corpus release'}
for index, (name,buyer,offer,detail,econ,success,gates) in enumerate(OPPORTUNITIES, 1):
    sections.append({'heading': f'Opportunity · {name}', 'blocks': [paragraph(f'User and problem. {buyer}. {offer}'), paragraph(f'Practical offer. {detail}'),
        paragraph(f'Commercial or ecosystem model. {econ}'), paragraph(f'Evidence of success. {success}'), paragraph(f'Prerequisites and limits. {gates}')]})
    if index in [1,3,4,5,6,12]:
        slides.append({'type': 'assertion_points', 'kicker': name + ' · R07', 'title': c(product_titles[index]),
            'points': [c('Offer: ' + offer), c('Users: ' + buyer + '.'), c('Value model: ' + econ), c('Gate: ' + gates)]})

chapter('The wider portfolio extends beyond corpus sales and context APIs', [
    'The remaining options strengthen the portfolio without requiring an unqualified wholesale data release: private editorial search, terminology and knowledge resources, translation/localisation support, bounded adapters, aggregate media intelligence and native-speaker data-quality services. Several reinforce one another; annotation improves the benchmark, the benchmark strengthens the licence offer, and a curated lexicon improves retrieval and localisation.',
    'Sequence by evidence readiness and reversibility, not by the most ambitious marketing label. An internal archive-search pilot or an open tooling release is generally easier to scope than external raw-corpus licensing or broad weight release, but neither is automatically ready: rights, accurate claims and operational support still matter. Use paid or institutionally funded pilots to test demand and delivery cost.',
    'Avoid starting a voice-cloning product from existing broadcast voices. If synthetic voice is ever considered, use a separately commissioned, explicitly consented voice-actor programme and a distinct risk review. Similarly, synthetic training augmentation should be a labelled, auditable derived dataset with compatible teacher-model rights—not an unmarked addition to the natural-data inventory.'
], 'R07', points=['Private archive search and terminology resources can build on smaller curated slices.', 'Localisation and adapters need task-specific evidence, not broad model claims.', 'Annotation and independent evaluation improve the defensibility of later offers.', 'Voice synthesis and unmarked synthetic augmentation are not shortcuts around rights.'], slide_title='The strongest portfolio combines services, assurance and local-language capability')

chapter('Context as a service needs a product contract, not just a vector index', [
    'The service contract should state the domains and languages covered, source freshness, citation behaviour, permissible excerpts, access roles, abstention policy and correction obligations. Maintain document-level permissions through retrieval and generation. A changed or withdrawn source must propagate to the index, cache and downstream response policy.',
    'Assess retrieval separately from answer generation. A model can write fluently from the wrong source, while a correct retriever can feed an overconfident answer. Evaluate citation entailment, missing-evidence refusal, stale-context handling and local-language meaning with representative users. Distinguish access to source content from rights to train an external model on user queries or retrieved passages.',
    'Track the unit economics of an accepted, useful answer: licensed content cost, curation, indexing refresh, inference, human escalation, support and monitoring. The service should earn a place in a real workflow rather than be positioned as a generic chatbot. A narrowly scoped pilot with correction and withdrawal capability is a stronger first offer than an unbounded “ask the estate anything” promise.'
], 'R07', points=['Define domains, languages, freshness, citation and abstention behaviour.', 'Carry source permissions into retrieval, caches and generated answers.', 'Evaluate faithful answers separately from retrieval relevance.', 'Price the full cost of an accepted answer, including curation and escalation.'], slide_title='A defensible context service sells trustworthy workflow support, not raw retrieval')

chapter('An open ecosystem and a commercial service can coexist', [
    'Release boundaries should be explicit. Code can use an open-source licence while restricted data stays private. A dataset can permit research without permitting redistribution; that is not the same as open data. Open weights still depend on base-model terms, training-data rights and downstream restrictions. A hosted API can be public to access without its code, weights or underlying data being open.',
    'A practical public-interest track is to publish schemas, data-card templates, language/dialect documentation, safe examples, evaluation methods and tooling that local teams can reproduce. Create mechanisms for native-speaker corrections and community governance. When suitable content is cleared, release a deliberately bounded subset with provenance and a contact/withdrawal process.',
    'Fund maintenance rather than only the initial launch: documentation, security updates, issue triage, evaluation refresh, contributor support and hosting all require ownership. Measure useful independent reuse, not just repository stars or download counts. Commercial support, consortium funding and hosted services can help sustainability, but their economics should be validated rather than assumed.'
], 'R07/R08', points=['Open code, open data, open weights and a hosted service are different choices.', 'Start with reproducible tools and clear documentation; clear data separately.', 'Native-speaker participation and correction channels are part of the product.', 'Assign funding and ownership for maintenance, not just launch.'], slide_title='Openness is a set of deliberate release decisions, not a single licence label')

chapter('Rights, privacy and community legitimacy constrain the offer', [
    'An internal custody or training authorisation is not evidence of external sublicensing, public redistribution, model-weight release or voice synthesis rights. Separate copyright in recordings and transcripts, performer or contributor permissions, programme and third-party content agreements, personal-data processing and cross-border transfer obligations. A music-exclusion filter does not clear all these issues.',
    'Kenya’s Data Protection Act and applicable regulations are relevant to personal-data use and transfers. The report does not certify compliance or offer a legal conclusion; counsel should assess the actual processing purpose, parties, risks, safeguards and contractual terms. Where a global lab is involved, document where data, logs, embeddings, checkpoints and derived outputs will be processed and retained.',
    'Community legitimacy matters alongside formal paperwork. Language names, dialect groupings, representational gaps, compensation, harmful downstream uses and correction rights should be discussed with qualified local contributors. Minimise unnecessary person-level data and avoid implying that “de-identified” text or embeddings cannot be re-identified. Secure access reduces some exposure but does not remove the underlying obligations.'
], 'R08/R07', points=['Internal authorisation does not establish onward licensing or open-release rights.', 'Assess source, performer, transcript, personal-data and derived-output rights separately.', 'Cross-border processing requires a documented legal and operational review.', 'Community participation and correction rights strengthen long-term legitimacy.'], slide_title='Rights and stewardship must be designed into each offer, not appended at release')

chapter('Commercial validation should precede a revenue forecast', [
    'For each option, identify a specific buyer and quantify the existing task cost or loss that the service could reduce. Run a time-bounded pilot with agreed acceptance criteria and a clear paid or funded continuation decision. Distinguish expressions of interest from signed commitments, and distinguish usage from useful outcomes.',
    'Model contribution per delivery unit as realised price minus variable licensing, annotation, inference, storage/transfer, human review and support costs. Then deduct fixed engineering, legal, governance and maintenance costs for the full business case. The relevant unit may be an accepted answer, qualified audio minute, validated example, benchmark engagement or supported institution; raw GB is rarely the complete value unit.',
    'Use low/base/high sensitivities for qualification yield, human review time, update frequency, query load and retention. Do not double count the same asset’s revenue across overlapping products without accounting for exclusivity, capacity, licence constraints and channel conflict. The evidence available here is insufficient for a credible total-addressable-market or revenue projection, so none is presented.'
], 'R07', points=['Validate a named buyer problem and acceptance criteria in a scoped pilot.', 'Use accepted outputs—not raw gigabytes—as the economic unit.', 'Include rights, annotation, review, maintenance and support costs.', 'No revenue forecast is justified before yield, demand and delivery costs are measured.'], slide_title='A paid qualification or workflow pilot is stronger evidence than a speculative valuation')

chapter('A staged programme turns the inventory into a responsible offer', [
    'First establish the coverage and identity ledger: reconcile blocked sources, snapshot dates, canonical asset relationships, permitted uses and the conflicting method counts. In parallel, recover the staged-audio measurement result and audit a language/dialect reference. Deliver a source-pinned candidate inventory, not a premature sales brochure.',
    'Then define the intended task and acceptance policy, draw a documented stratified sample, complete independent speech/music/language annotations, assess waveform and transcript quality, and verify audio–text joins. Publish per-stratum included, excluded and unresolved duration with design-aware uncertainty. Build a fresh blind final set if models or recipes will be selected on the development material.',
    'Next run a controlled product pilot on the qualified slice. Suitable pilot tracks include cited editorial/context retrieval, a narrowly supported adapter or an independent evaluation engagement. Keep any open-source/tooling release on a separately cleared track. Widen the offer only after the pilot demonstrates user value, unit economics, corrections and withdrawal handling.',
    'Elapsed time and budget depend on eligible volume, annotation yield and the required languages—not on a fixed slide deadline. Commission a measured calibration for decoding, annotation and review throughput, then quote a bounded programme. Preserve stop conditions for low rights clearance, inadequate label agreement, poor smallest-stratum quality or uneconomic review load.'
], 'R07', points=['Establish source identity, coverage and rights before a sale claim.', 'Qualify segments and alignments with independent native-speaker evidence.', 'Pilot one bounded commercial workflow and a separately cleared open track.', 'Scale only after measured quality, demand, correction and unit economics are credible.'], slide_title='The next investment should buy qualification and a pilot, not a larger unverified claim')

chapter('Decisions for the owner and prospective partner', [
    'Choose the first target use and the populations it must serve. Decide whether the initial offer is private operational use, controlled research access, a commercial licence or an open release. Agree how mixed-language and speech-over-music material will be treated, which quality dimensions matter, and who can accept the residual uncertainty.',
    'Assign a data owner, rights lead, language/annotation lead, engineering custodian and product owner. Require one evidence pack linking the approved purpose to the relevant inventory, measurements, source rights, exclusions, model or dataset evaluation and release terms. Keep the original records and derivations so a partner can reproduce the claims.',
    'The decision is not whether the estate is “good” or “bad”. It is which bounded slice can responsibly support which product, at what cost and with which limitations. The evidence supports proceeding with disciplined qualification and specific pilots; it does not yet support an estate-wide certified non-English, non-music corpus claim.'
], 'R07', points=['Select the intended use, target strata and release model.', 'Agree treatment of mixed content and unresolved quality.', 'Name accountable owners for rights, language validation and delivery.', 'Approve the qualification programme and a bounded pilot—not unsupported totals.'], slide_title='The next decision is the first defensible product and its qualification contract')

sections.append({'heading': 'Coverage, limits and non-claims', 'blocks': [{'coverage_limits': True}]})
slides.append({'type': 'coverage_limits'})

method_paras = [
    f'Audio sums use the eight per-language-folder entries in the verified header inspection. Exact retained sum: {hours:.4f} hours; {audio_bytes:,} bytes; {audio["files"]:,} files; {transcripts:,} companion transcript files; {transcript_bytes:,} companion transcript bytes. The source hours are already rounded per folder, so precision beyond the retained inputs is not implied.',
    'Text natural-unit totals are the sum of train, development, held and archive-test partitions. Their sum reconciles to the reported natural-unit inventory. Canaries are reported separately. No correspondence between the standalone text build and the staged audio is assumed without an explicit join.',
    'Quality-grade percentages divide each grade count by the measured relational-table denominator. Storage conversions use decimal GB = bytes / 10^9, TB = bytes / 10^12, GiB = bytes / 2^30 and TiB = bytes / 2^40. Percentages and display values are rounded after calculation. None of the separately observed storage inventories is treated as an additive unique-content total.',
    'The archived tariff calculation is illustrative and conditional on the displayed reference rate and billing convention. It is not a current vendor quotation or the owner’s invoice. Economic recommendations are not a valuation, forecast or instruction to delete assets.',
    'Language-ID conditional accuracy is correct / judged. Coverage is judged / presented, equivalent to one minus abstention rate in the retained record. Correct-of-all is correct / presented. These metrics have different interpretations and are not substituted for transcript fidelity or rights clearance.',
    'The report contains no raw recordings, raw transcripts, row-level personal data, API credentials, access tokens or infrastructure login details. The supporting evidence has been retained internally; redistribution of this aggregate briefing should still follow the owner’s confidentiality policy.'
]
sections.append({'heading': 'Appendix A · Definitions, calculations and reconciliation', 'blocks': [paragraph(p) for p in method_paras]})

hash_paras=[]
for name, label in [('estate_report.json','Relational and storage report'),('m9j-3e0dcb1bd16e.json','Staged audio header evidence'),('m9j-9a46b862f339.json','Text assembly and seal'),('m9j-74af7cef0a85.json','Text language-ID evaluation'),('m9j-c47f01c0b945.json','Incomplete measurement status')]:
    digest=hashlib.sha256((EVIDENCE/name).read_bytes()).hexdigest()
    hash_paras.append(f'{label}. Retained source reference: {name}. SHA-256: {digest}. This hash pins the local record used for this briefing; the record’s own receipt verification is a separate property.')
sections.append({'heading': 'Appendix B · Source provenance and evidence hashes', 'blocks':[paragraph(p) for p in hash_paras]+[{'receipts':True}]})

references=[
    'Gebru et al., Datasheets for Datasets. Dataset motivation, composition, collection, use and maintenance. https://arxiv.org/abs/1803.09010',
    'Pushkarna et al., Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI. https://arxiv.org/abs/2204.01075 ; implementation playbook: https://github.com/pair-code/datacardsplaybook',
    'NIST, AI Risk Management Framework. Voluntary risk-management framework; this report is not a conformance certification. https://www.nist.gov/itl/ai-risk-management-framework',
    'Kenya, Data Protection Act, 2019, official ODPC-hosted text. Applicability and obligations require legal review of the actual processing arrangement. https://www.odpc.go.ke/wp-content/uploads/2024/02/TheDataProtectionAct__No24of2019.pdf',
    'Kenya, Data Protection (General) Regulations, 2021, official ODPC-hosted text. https://www.odpc.go.ke/wp-content/uploads/2024/03/THE-DATA-PROTECTION-GENERAL-REGULATIONS-2021-1.pdf',
    'External references were consulted as documentation and governance guidance on 1 October 2026. They do not validate the estate figures or certify rights, model performance, representativeness or legal compliance.'
]
sections.append({'heading':'Appendix C · Documentation and governance references','blocks':[paragraph(p,'R08') for p in references]})
slides.append({'type':'appendix'})

brief={'brief_id':'BR-RMS-ESTATE-20261001','content_ref':content['content_id']+'@1',
    'purpose':{'kind':'decide','statement':'Understand estate condition, establish a defensible local-language corpus claim, and select responsible commercial and public-interest options.'},
    'audience':{'who':'Estate owner, executive stakeholders and global AI-lab technical/research partners','knowledge':'mixed executive and expert; detailed scrutiny expected','priorities':['quantitative honesty','traceability','quality and rights','commercial and ecosystem utility'],'detail':'substantive unattended read with full supporting paper'},
    'setting':{'mode':'read-ahead','read_unattended':True,'printed':True,'ongoing_use':False},
    'content':{'evidence':True,'narrative':True,'financial':False,'diagrams':True,'imagery':False,'appendix':True},
    'brand':{'house':'house-neutral','formality':'formal','expressiveness':'restrained','variation_allowed':'within-family'},
    'outputs':[{'format':'pptx','role':'rigorous self-contained briefing','editable_charts':True},{'format':'docx','role':'detailed stand-alone analytical report','editable_charts':False}],
    'constraints':{'page_size':'A4','confidentiality':'Owner confidential · controlled circulation'}}
frame=frame_for(brief); stamp='2026-10-01T19:12:00Z'; seed='rms/estate-language-opportunities/20261001'
verdict=verdict_from_frame(frame,brief,'V-RMS-ESTATE-20261001',manifest_from_brief(brief,False),'owner-approved combined rigorous briefing; standing strategy frame',stamp)
base={'content_ref':brief['content_ref'],'brief_ref':brief['brief_id'],'verdict_ref':verdict['verdict_id'],'objective':'decide','family':frame['family'],'voice':frame['voice'],'seed':seed,'build_stamp':stamp,
      'furniture':{'confidentiality':'Owner confidential · controlled circulation'}}
deck={**base,'spec_type':'deck','spec_id':'DK-RMS-ESTATE-20261001','slides':slides}
paper={**base,'spec_type':'paper','spec_id':'PP-RMS-ESTATE-20261001','title':content['title'],'subtitle':'A rigorous accounting and opportunity assessment · evidence cut 1 October 2026','sections':sections}
FIXTURE.mkdir(parents=True,exist_ok=True)
for name,data in [('brief.json',brief),('content.json',content),('verdict.json',verdict),('deck.json',deck),('paper.json',paper)]:
    (FIXTURE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'slides':len(slides),'paper_sections':len(sections),'claims':len(claims),'audio_hours':hours,'audio_bytes':audio_bytes,'text_units':text['units'],'fixture':str(FIXTURE)},indent=2))