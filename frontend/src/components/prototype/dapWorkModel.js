import { stamp } from './evidence';
import { drawerFor, progress, readyRows, requestName, STATUS } from './dapCommissionDrawer';

export const operationForPath = path => ({ processed: 'processed_intelligence', finetune: 'fine_tune_model', skill: 'develop_skills', raw: 'download_raw_data' }[path.split('/').pop()]);
const titles = { processed_intelligence: 'Processed intelligence', fine_tune_model: 'Trained models', develop_skills: 'Callable skills', download_raw_data: 'Raw data' };
const RAIL = ['All', 'Executing', 'Ready', 'Blocked'];
const railState = r => r.state === 'interrupted' || r.state === 'routing' ? 'executing' : r.state === 'stopped' ? 'blocked' : r.state;
const plain = value => typeof value === 'object' && value ? Object.entries(value).map(([k, v]) => `${k}: ${v}`).join(', ') : String(value);

export function reviewFields(review) {
  if (!review) return [];
  const f = review.feasibility || {};
  if (f.verdict !== 'warm') return [{ l: 'Feasibility', v: f.basis || 'Not assessed' }];
  const rows = [{ l: 'Table read', v: `${f.table.database}.${f.table.table} · ${new Intl.NumberFormat('en').format(f.table.row_count)} rows in the census` },
    { l: 'Records bound', v: `up to ${f.bounds.max_records} records · up to ${f.bounds.max_seconds} s` },
    { l: 'Personal details', v: f.floor?.columns?.length ? `${f.floor.columns.length} column(s) redacted on the worker` : 'None detected in this table' }];
  (review.assumed || []).filter(a => a.field === 'compute' || a.field === 'done_condition').forEach(a => rows.push({ l: a.field === 'compute' ? 'Compute reserved' : 'Done when', v: plain(a.value) }));
  return rows;
}

export function dapWorkModel({ work, data, path, draft, setDraft, units, setUnits, params, setParams, search, setSearch, sections, setSections, navigate, ui, setUi }) {
  const operation = operationForPath(path);
  const terms = work.entitlement, review = work.review, selected = work.selected;
  const termsId = terms?.licence?.terms_identifier;
  const open = row => setParams({ request: row.request_id });
  const toggle = key => setSections(v => ({ ...v, [key]: !v[key] }));
  const resetCompose = () => { setDraft(''); setUnits([]); work.setReview(null); work.setError(''); setUi({}); };
  const filter = (search || '').toLowerCase();
  const rows = work.rows.filter(r => !filter || railState(r) === filter || `${r.objective_text} ${STATUS[r.state] || ''}`.toLowerCase().includes(filter));
  const reviewed = review && review.state === 'draft' && review.feasibility?.verdict === 'warm' && review.envelope?.objective_text === draft && (review.envelope?.units || []).join() === units.join();
  const routing = review?.routing;
  const standIns = (routing?.groups || []).filter(g => g.seating === 'interim_pilot_stand_in');
  const unseated = routing?.unseated_groups || [];
  const actions = {
    copyNew: row => { setDraft(row.objective_text); setUnits([...row.units]); work.setReview(null); setUi({ copiedFrom: row }); setParams({}); if (!operation) navigate('/dap/extract/processed'); },
    stopStart: row => setUi(v => ({ ...v, stopRow: row })),
    openReport: row => setUi(v => ({ ...v, reportRow: row })),
    retrieveStart: (row, artifact) => setUi(v => ({ ...v, retrieve: { row, artifact, step: 'dest', pick: null } })),
  };
  const dests = work.destinations?.rows || [];
  const retrieve = ui.retrieve;
  const order = work.run?.work_order;
  const delivery = selected ? work.deliveries[selected.request_id] : null;
  const prog = progress(work.run);
  return {
    isExtract: Boolean(operation), isOverview: path === '/dap/requests', isContract: path === '/dap/governance/contract',
    showPageHead: true, pageEyebrow: operation ? 'Extract' : 'Data access', pageTitle: titles[operation] || (path === '/dap/requests' ? 'Your requests' : 'Contract & access terms'),
    pageSub: work.error || (work.loading ? 'Loading your records…' : operation ? 'Ask for a bounded piece of work on your admitted data. It is reviewed, signed off and run on the estate\u2019s own computers.' : 'Every request you have made, where it stands, and what came back.'),
    isFinetune: false, howOpen: sections.how, howToggle: () => toggle('how'), howChev: sections.how ? '' : 'rotate(-90deg)',
    profileRows: [{ l: 'Request', v: 'You state what you need and which data; the objective and scope are frozen on submission.', notLast: true }, { l: 'Sign-off', v: 'Your estate\u2019s approvers sign with keys held in custody; an interim stand-in signs where no approver is seated yet.', notLast: true }, { l: 'Execution', v: 'A bounded read on the estate\u2019s own worker, sealed, checked independently on a second computer, then recorded.', notLast: false }],
    practiceBg: 'var(--surface)', practice: 'Nothing is widened after submission. Personal details are redacted on the worker before anything is sealed.',
    hasChatLog: true, chatLog: [{ text: 'The request assistant is not available in this estate yet. Review the feasibility check below before you submit.', align: 'flex-start', border: 'var(--line)', bg: 'var(--surface)', hasTag: false }],
    jobShaping: true, setupOpen: sections.setup, setupToggle: () => toggle('setup'), setupChev: sections.setup ? '' : 'rotate(-90deg)',
    hasComposeNote: Boolean(ui.submitted), composeNote: { line: ui.submitted ? `${requestName(ui.submitted, work.rows)} is submitted and frozen. Sign-off and the first step are under way.` : '', onView: () => ui.submitted && open(ui.submitted), hasAssistant: false, onDismiss: () => setUi(v => ({ ...v, submitted: null })) },
    hasCopyBanner: Boolean(ui.copiedFrom), copyBannerId: ui.copiedFrom ? requestName(ui.copiedFrom, work.rows) : '', copyBannerStatus: ui.copiedFrom ? STATUS[ui.copiedFrom.state] || ui.copiedFrom.lifecycle_state : '',
    composeCardOpacity: '1', composeCardPointer: 'auto', composeSubmitBusy: work.busy || !data?.can_run,
    objDraft: draft, objChange: event => { setDraft(event.target.value); if (review) work.setReview(null); }, objPlaceholder: 'State what you need from this data',
    objHint: reviewed ? `Checked against the census: ${review.feasibility.basis}.` : 'What you submit cannot be widened later. Akki checks it against the census before you can submit.',
    scopeChips: (data?.sources || []).map(s => ({ key: s.source_id, label: s.label, meta: s.source_id, cursor: work.busy ? 'wait' : 'pointer', opacity: '1',
      border: units.includes(s.source_id) ? 'var(--blue)' : 'var(--line)', bg: units.includes(s.source_id) ? 'rgba(22,39,74,.08)' : '#fff', color: 'var(--ink)',
      onClick: () => { if (work.busy) return; setUnits(v => v.includes(s.source_id) ? [] : [s.source_id]); if (review) work.setReview(null); } })),
    modeFields: reviewFields(reviewed ? review : null), termsId: termsId || 'Terms not yet resolved', meterUnit: 'records read, records returned and seconds',
    apprColor: reviewed && !unseated.length ? 'var(--sage)' : 'var(--brass)',
    apprHead: !reviewed ? 'Sign-off is worked out when the request is checked' : unseated.length ? `No approver is seated for ${unseated.join(', ')}` : routing.controlled ? 'Needs expenditure and extraction sign-off' : 'Needs expenditure sign-off',
    apprWhy: !reviewed ? 'The census tells Akki whether personal details are involved and who must sign.' : unseated.length ? 'This request cannot be submitted until your estate seats an approver or admits a stand-in.' : standIns.length ? `Digicow has not seated its named approvers yet; the admitted interim stand-in signs for ${standIns.map(g => g.purpose).join(' and ')}. Your own operator standing signs the scope.` : 'Seated approvers of your estate will be asked; your operator standing signs the scope.',
    hasSubmitError: Boolean(work.error), submitErrorMsg: work.error,
    submitBtnOpacity: work.busy || !data?.can_run ? '.55' : '1', submitBtnCursor: work.busy ? 'wait' : 'pointer',
    submitBtnLabel: !data?.can_run ? 'Operator access required' : work.busy ? (reviewed ? 'Submitting…' : 'Checking…') : reviewed ? 'Submit request' : 'Check this request',
    freeze: async () => {
      if (!draft.trim() || !units.length) { work.setError('State what you need and choose one data set.'); return; }
      if (!reviewed) {
        const body = { objective_text: draft, operation: operation || 'processed_intelligence', units };
        if (ui.reach) body.reach = ui.reach;
        const view = await work.saveDraft(body);
        if (view && view.feasibility?.verdict !== 'warm') work.setError(`This request cannot be checked in: ${view.feasibility?.basis || view.feasibility?.reason_code}`);
        return;
      }
      const frozen = await work.freeze(review.draft_id);
      if (frozen?.request_id) { const row = { request_id: frozen.request_id, objective_text: draft, units: [...units], state: 'routing', lifecycle_state: 'Routing' }; setDraft(''); setUnits([]); setUi({ submitted: row }); open(row); }
    },
    railChat: true, railIsNotes: false, railIsChat: true, resetJob: () => operation ? resetCompose() : navigate('/dap/extract/processed'),
    railStatsOpen: sections.stats, railToggleStats: () => toggle('stats'), railStatsChev: sections.stats ? '' : 'rotate(-90deg)',
    railStatsRow: RAIL.map(label => ({ label, count: label === 'All' ? work.rows.length : work.rows.filter(r => railState(r) === label.toLowerCase()).length,
      bg: '#fff', ring: '1px solid var(--line)', numColor: 'var(--ink)', onClick: () => setSearch(label === 'All' ? '' : label.toLowerCase()) })),
    railSearch: search, railSearchChange: e => setSearch(e.target.value), railFilterActive: Boolean(search), railFilterLabel: search, railClearFilter: () => setSearch(''),
    railEmpty: !work.loading && !rows.length,
    railRequests: rows.map(r => {
      const isSel = selected?.request_id === r.request_id, moving = ['executing', 'interrupted', 'routing'].includes(r.state);
      return { key: r.request_id, id: requestName(r, work.rows), objective: r.objective_text, status: STATUS[r.state] || r.lifecycle_state,
        color: r.state === 'ready' ? 'var(--sage)' : r.state === 'blocked' ? 'var(--oxblood)' : 'var(--brass)', bg: 'var(--surface)', slotRows: '1fr', enterOpacity: '1', enterTransform: 'none', highlightBg: isSel ? 'rgba(22,39,74,.06)' : '#fff', highlightTransition: 'background-color .2s', actionBg: 'var(--blue)', slotTransition: 'none', enterTransition: 'none',
        onView: () => open(r), isExecuting: moving, hasPercent: moving && isSel, pctStr: prog.pctStr, eta: '', hasStages: moving && isSel, segments: prog.segments, stepStr: prog.stepStr, stageCaption: prog.stageLabel,
        etaOnly: false, showTimestamp: !moving || !isSel, timestamp: stamp(r.created_at), timestampColor: 'var(--ink3)', isTransferring: false, isTransferFailed: false,
        showAction: r.state === 'ready', actionLabel: 'Open result', actionOnClick: () => open(r), noAction: r.state !== 'ready' };
    }),
    railDrawerOpen: Boolean(params.get('request')) && Boolean(data), railCloseDrawer: () => setParams({}),
    railDrawerVM: selected ? drawerFor({ row: selected, rows: work.rows, run: work.run, approvals: work.approvals, order, delivery, terms: termsId, actions })
      : { id: 'Opening…', statusLabel: work.error ? 'Unavailable' : 'Loading', statusColor: 'var(--ink3)', statusBg: 'var(--surface)', agreement: termsId || '', submitted: '', hasDetail: false, otherStatus: Boolean(work.error) },
    ovEyebrow: 'Work history', ovTitle: 'Your requests.', ovLede: work.error || (work.loading ? 'Loading…' : `${work.rows.length} request(s) on record. Each one is frozen as submitted; nothing is widened afterwards.`),
    ovRows: rows.map(r => ({ n: requestName(r, work.rows), title: r.objective_text, line: stamp(r.created_at), right: STATUS[r.state] || r.lifecycle_state, color: r.state === 'ready' ? 'var(--sage)' : 'var(--brass)', onClick: () => open(r) })),
    ovNote: 'The same requests are visible in Akki OS under My Work.',
    govContractRows: [
      { l: 'Licence', v: terms?.licence?.plan_identifier || 'Unresolved — no owner-admitted licence is available.' },
      { l: 'Status', v: terms?.status || 'Loading' }, { l: 'Terms', v: termsId || 'Unresolved' },
      { l: 'Allowance', v: terms?.allowance_state ? `${terms.allowance_state.credits_remaining} credits · ${terms.allowance_state.period_iso}` : 'Unresolved — not a zero balance or free grant.' },
      { l: 'Catalog', v: terms?.status === 'resolved' ? `${terms.rows.length} admitted listed models` : 'No admitted model picker is available.' },
    ],
    // Dialogs — the original confirm, stop and report surfaces, bound to real custody and run records.
    confirmOpen: Boolean(retrieve), confirmTitle: retrieve?.step === 'dest' ? 'Retrieve this result' : 'Confirm retrieval',
    confirmIsDestStep: retrieve?.step === 'dest' && dests.length > 0, confirmIsNoDest: retrieve?.step === 'dest' && dests.length === 0, confirmIsConfirmStep: retrieve?.step === 'confirm',
    confirmDests: dests.map(d => ({ key: d.destination_id, border: retrieve?.pick?.destination_id === d.destination_id ? 'var(--blue)' : 'var(--line)', bg: '#fff', dotBorder: d.retrievable_over_https ? 'var(--sage)' : 'var(--brass)', dotFill: d.retrievable_over_https ? 'var(--sage)' : 'transparent', label: `${d.provider.replace(/_/g, ' ')} · ${d.region || ''} · ${d.retrievable_over_https ? 'retrieval link available' : 'no retrieval link ruled yet'}`, onPick: () => setUi(v => ({ ...v, retrieve: { ...v.retrieve, pick: d, step: 'confirm' } })) })),
    confirmBody: retrieve?.pick ? (retrieve.pick.retrievable_over_https ? `The custodian (${retrieve.pick.custodian_runtime_id}) will re-measure the sealed result and issue a one-time link. Retrieval is recorded against your request.` : `The sealed result rests with the custodian (${retrieve.pick.custodian_runtime_id}) in ${retrieve.pick.provider.replace(/_/g, ' ')}. No retrieval link is ruled for this destination yet, so Akki will record your request and hold the link; nothing is downloaded.`) : '',
    confirmHasChoice: retrieve?.step === 'confirm', confirmProceedDisabled: work.busy, confirmProceedOpacity: work.busy ? '.55' : '1', confirmProceedCursor: work.busy ? 'wait' : 'pointer', confirmOnCancel: () => setUi(v => ({ ...v, retrieve: null })),
    confirmOnProceed: async () => { const r = retrieve; setUi(v => ({ ...v, retrieve: null })); if (r?.artifact) await work.retrieve(r.row.request_id, r.artifact); },
    copyConfirmOpen: false, withdrawConfirmOpen: false,
    stopConfirmOpen: Boolean(ui.stopRow), stopConfirmCancel: () => setUi(v => ({ ...v, stopRow: null })), stopConfirmProceed: async () => { const r = ui.stopRow; setUi(v => ({ ...v, stopRow: null })); if (r) await work.stop(r.request_id); },
    reportOpen: Boolean(ui.reportRow), reportClose: () => setUi(v => ({ ...v, reportRow: null })), reportToggleExpand: () => setUi(v => ({ ...v, reportWide: !v.reportWide })), reportExpandTitle: ui.reportWide ? 'Narrow' : 'Widen', reportExpandIconD: 'M4 4h12v12H4z',
    reportVM: ui.reportRow ? reportFor(ui.reportRow, work) : {}, reportPanelWidth: ui.reportWide ? 'min(1100px, 96vw)' : 'min(760px, 96vw)',
    hasToasts: false, toasts: [],
  };
}

function reportFor(row, work) {
  const run = work.run, rows = readyRows(run), order = run?.work_order || {}, sel = order.selection || {};
  return { title: `${requestName(row, work.rows)} · result record`, objective: row.objective_text, metaLine: `Submitted ${stamp(row.created_at)} · ${STATUS[row.state] || row.lifecycle_state}`,
    referenceLine: run?.terminal?.terms_ref ? `Charged under ${run.terminal.terms_ref}` : '', isProse: true,
    paragraphs: [`This result was produced by a bounded read of ${sel.database ? `${sel.database}.${sel.table}` : 'the selected table'} on ${order.worker_runtime_id || 'the estate worker'}, sealed, then checked independently on ${order.inspector_runtime_id || 'a second computer'}. ${sel.columns ? `${sel.columns.length} columns were read.` : ''}`],
    hasSections: true, sections: [{ key: 'measures', title: 'What was measured', paragraphs: [], isBarChart: false, isCompareChart: false, hasTable: true, tableColCount: 2, tableHeaders: ['Measure', 'Recorded'], tableRows: rows.map(r => ({ key: r.l, cells: [{ v: r.l }, { v: r.v }] })) },
      { key: 'steps', title: 'Steps completed', paragraphs: [], isBarChart: false, isCompareChart: false, hasTable: true, tableColCount: 2, tableHeaders: ['When', 'Step'], tableRows: (run?.timeline || []).map((t, i) => ({ key: `${t.receipt_hash}-${i}`, cells: [{ v: stamp(t.at) }, { v: t.detail || t.slot }] })) }] };
}
