import { useCallback, useEffect } from 'react';
import { useTrainModels } from './useTrainModels';
import { FINISHED, STATUS_BG, STATUS_COLOR, dashCards, familyLabel, groupsOf, journalMeta, relative, reportOf, stageDots, threadItems } from './trainModelsModel';

const EMPTY_COPY = 'No models trained yet. Say what the model should do and how you will know it is working; every field you leave unset, Akki asks for rather than fills in. Nothing runs, and no compute is spent, until you freeze the objective.';
const LOG = '.owner-prototype-os [data-proto-line="363"]';
const scrollLog = (toStage) => requestAnimationFrame(() => {
  const log = document.querySelector(LOG); if (!log) return;
  if (!toStage) { log.scrollTop = log.scrollHeight; return; }
  const el = log.querySelector(`[data-stage="${toStage}"]`); if (el) log.scrollTop += el.getBoundingClientRect().top - log.getBoundingClientRect().top - 14;
});

export function useTrainModelsExperience({ active, session, navigate, params, setParams, state, setState, unavailable }) {
  const principal = session.data?.principal_id;
  const data = useTrainModels(active ? principal : null);
  const canOperate = Boolean(session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)));
  const runs = data.board?.runs || [];
  const names = runs.map(r => r.name);
  const selectedId = params.get('run');
  const sel = runs.find(r => r.run_id === selectedId) || null;
  const search = (state.tmSearch || '').trim().toLowerCase();
  const filtered = runs.filter(r => !search || r.name.toLowerCase().includes(search) || (r.objective || '').toLowerCase().includes(search));
  const counts = data.board?.counts || {};
  const tab = state.tmTab || 'overview';
  const patch = useCallback(update => setState(s => ({ ...s, ...update })), [setState]);
  const select = useCallback((id, fromJournal) => { setParams(id ? { run: id } : {}); patch({ tmComposer: '', tmTab: 'overview', tmJournalMode: Boolean(fromJournal) }); }, [setParams, patch]);
  const selKey = sel ? `${sel.run_id}:${sel.messages.length}` : '';
  useEffect(() => { if (active && selKey) scrollLog(); }, [active, selKey]);
  const guard = fn => (...args) => canOperate ? fn(...args) : unavailable('Operator access required', 'Your admitted role may read every run and its record, but may not send messages or record decisions here. No change was made.');
  const failed = exc => unavailable('Not done', exc.message || 'The training lab did not accept that. Nothing about the run has changed.');
  const act = (action, value) => sel && data.act(sel.run_id, action, value).then(scrollLog).catch(failed);
  const openVersion = mode => sel && data.create({ from_run: sel.run_id, mode }).then(r => select(r.run_id)).catch(failed);
  const send = () => {
    const text = (state.tmComposer || '').trim(); if (!text || !sel || data.pending[sel.run_id]) return;
    patch({ tmComposer: '' }); scrollLog();
    data.send(sel.run_id, text).then(scrollLog).catch(failed);
  };
  const finished = Boolean(sel && FINISHED.includes(sel.status));
  const report = sel ? reportOf(sel) : null;
  const placeholder = !sel ? 'Write a message...' : finished ? 'Ask about this model, or say what to change...' : sel.status === 'In Approval' ? 'Ask about the plan, or say you are ready...'
    : sel.family === 'owner' ? (sel.ready ? 'Change something, or say you\'re ready...' : 'Answer in plain language...') : 'Say "run the baseline", or ask what it reads...';
  const model = !active ? {} : {
    isBuildRunPage: true, isRegistryGroup: false, isRegEstate: false, appTitle: 'Train Models', appGroupLabel: 'Build Your Resources', exitApp: () => navigate('/os?nav=build&app=train'),
    openShieldReport: () => unavailable('Shield report', 'Every run here is read from its own record under your admitted identity. Training starts only from a recorded sign-off on the run itself; the signature binds the plan by digest.'),
    hasSessionBanner: Boolean(data.error), sessionBanner: data.error || '', sessionBannerColor: 'var(--oxblood)',
    tmPageEmpty: !data.loading && Boolean(data.board) && runs.length === 0, tmPageFull: data.loading || !data.board || runs.length > 0,
    tmEmptyCopy: EMPTY_COPY, tmNewLabel: 'Train a new model', tmNewModel: guard(() => data.create().then(r => select(r.run_id)).catch(failed)),
    tmStats: ['Shaping', 'In Approval', 'In training', 'In service', 'Refused', 'Retired'].map(l => ({ key: l, v: String(counts[l] ?? 0), l })),
    tmTopOpen: state.tmTopOpen !== false, tmTopClosed: state.tmTopOpen === false, tmTopToggle: () => patch({ tmTopOpen: state.tmTopOpen === false }), tmTopCollapse: () => { if (state.tmTopOpen !== false) patch({ tmTopOpen: false }); },
    tmSearch: state.tmSearch || '', tmSearchChange: e => patch({ tmSearch: e.target.value }), tmSearchPlaceholder: 'Search runs...',
    tmNoMatch: Boolean(data.board) && filtered.length === 0 && runs.length > 0, tmNoMatchCopy: 'No runs match your search', tmHasList: filtered.length > 0,
    tmGroups: groupsOf(filtered, selectedId, select, guard(r => data.remove(r.run_id).then(() => { if (r.run_id === selectedId) select(null); }).catch(failed))),
    tmPlaceholder: !sel, tmPlaceholderCopy: data.loading ? 'Reading the training record…' : 'Select a run on the left to see its full training conversation, or start a new one.', tmHasThread: Boolean(sel),
    tmThreadTitle: sel?.name || '', tmThreadStatus: sel?.status || '', tmThreadStatusColor: STATUS_COLOR[sel?.status] || 'var(--ink3)', tmThreadStatusBg: STATUS_BG[sel?.status] || 'var(--surface2)', tmThreadMeta: sel?.meta || '',
    tmHasDetails: finished, tmTabOverview: finished && tab === 'overview', tmTabReport: finished && tab === 'report', tmSetOverview: () => patch({ tmTab: 'overview' }), tmSetReport: () => patch({ tmTab: 'report' }),
    tmTabOvColor: tab === 'overview' ? 'var(--ink)' : 'var(--ink3)', tmTabOvLine: tab === 'overview' ? '2px solid var(--accent)' : '2px solid transparent', tmTabRpColor: tab === 'report' ? 'var(--ink)' : 'var(--ink3)', tmTabRpLine: tab === 'report' ? '2px solid var(--accent)' : '2px solid transparent',
    tmShowDots: !finished, tmStageDots: stageDots(sel, scrollLog),
    tmReportLead: report?.lead || '', tmReportSecs: report?.secs || [], tmReportObs: report?.obs || '', tmGenPaper: guard(() => act('white_paper')),
    tmObjectiveText: sel?.objective || '', tmDashCards: sel ? dashCards(sel) : [], tmDetailLearnings: sel?.learnings || '',
    tmShowLog: Boolean(sel) && !(finished && state.tmJournalMode), tmThread: sel ? threadItems(sel, { state, names, pendingText: data.pending[sel.run_id], canOperate, toggleThink: key => patch({ tmThink: { ...(state.tmThink || {}), [key]: !state.tmThink?.[key] } }), pickBaseline: guard(value => act('use_baseline', value)) }) : [],
    tmShowSummary: false, tmShowComposer: Boolean(sel) && canOperate, tmComposer: state.tmComposer || '', tmComposerChange: e => patch({ tmComposer: e.target.value }),
    tmComposerKey: e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }, tmComposerPlaceholder: placeholder, tmSend: send, tmSending: Boolean(sel && data.pending[sel.run_id]),
    tmAttach: () => unavailable('Attach a file', 'Recordings and labels travel through the Media Library, where rights and retention are recorded. Upload there, then name the recording in this thread.'),
    tmJournalTitle: 'Trained model journal', tmJournalMeta: journalMeta(counts), tmJournalEmpty: !runs.some(r => FINISHED.includes(r.status)), tmJournalEmptyCopy: 'Nothing has finished yet. Models arrive here once they enter service, are refused, or are retired.',
    tmJournal: runs.filter(r => FINISHED.includes(r.status)).map(r => ({ key: r.run_id, name: r.name, status: r.status, color: STATUS_COLOR[r.status], bg: STATUS_BG[r.status], rowBg: r.run_id === selectedId ? 'rgba(76,95,213,.06)' : '#fff',
      meta: `${familyLabel(r)} · last entry ${relative(r.messages.at(-1)?.at || r.finished_at) || '—'}`, onToggle: () => select(r.run_id, true) })),
    tmBegin: guard(() => act('record_training_request')), tmRemind: guard(() => sel?.approval?.plan_sha256 && !sel.approval.signed && act('approve_plan', sel.approval.plan_sha256)), tmWhitePaper: guard(() => act('white_paper')), tmNotNow: () => sel && patch({ tmDismiss: { ...(state.tmDismiss || {}), [sel.run_id]: true } }),
    tmViewDoc: () => { const id = sel?.messages.filter(m => m.commission_id).at(-1)?.commission_id; navigate(`/os/work/documents${id ? `?commission=${encodeURIComponent(id)}` : ''}`); }, tmShowAlts: () => sel && patch({ tmAlts: { ...(state.tmAlts || {}), [sel.run_id]: true } }),
    tmContinueExisting: () => unavailable('Carry on an existing model', 'Open a model in service from the list and choose "Open the next version"; it inherits the record and starts in Shaping. Nothing was opened by this action.'),
    tmOwnBaseline: () => unavailable('Bring your own model', 'An outside model needs its licence and a security scan recorded through Model Approval before it can be a starting point. That path is not connected yet; nothing was added.'),
    tmRemodel: guard(() => openVersion('next_version')), tmResubmit: guard(() => openVersion('next_version')), tmAdjust: guard(() => openVersion('adjust')), tmRetire: guard(() => act('retire')),
  };
  const enhance = !active ? {} : {
    205: { 'data-testid': 'train-new-run-empty' }, 213: { 'data-testid': 'train-new-run' }, 237: { 'data-testid': 'train-search' }, 284: { 'data-testid': 'train-new-run-placeholder' },
    250: ctx => ({ 'data-testid': `train-run-${ctx.r.key}` }), 257: ctx => ({ 'data-testid': `train-run-delete-${ctx.r.key}` }),
    290: { 'data-testid': 'train-thread-title' }, 291: { 'data-testid': 'train-thread-status' }, 293: { 'data-testid': 'train-thread-meta' },
    298: { 'data-testid': 'train-tab-overview' }, 299: { 'data-testid': 'train-tab-report' }, 306: ctx => ({ 'data-testid': `train-stage-${ctx.d.key}` }), 331: { 'data-testid': 'train-generate-paper' },
    363: { 'data-testid': 'train-thread' }, 365: ctx => ({ 'data-testid': `train-thread-item-${ctx.it.key}` }), 374: ctx => ({ 'data-testid': `train-think-${ctx.it.key}` }),
    400: ctx => ({ 'data-testid': `train-bubble-${ctx.it.key}` }), 416: { 'data-testid': 'train-use-baseline' }, 420: { 'data-testid': 'train-show-alternatives' }, 447: ctx => ({ 'data-testid': `train-use-alt-${ctx.ac.key}` }),
    533: { 'data-testid': 'train-approve-plan' }, 536: { 'data-testid': 'train-signoff-label' }, 543: { 'data-testid': 'train-begin-training' }, 571: { 'data-testid': 'train-open-next-version' }, 577: { 'data-testid': 'train-prepare-paper' }, 578: { 'data-testid': 'train-not-now' }, 585: { 'data-testid': 'train-view-document' },
    618: ctx => ({ 'data-testid': 'train-resubmit', hidden: ctx.it.retired }), 619: ctx => ({ 'data-testid': 'train-adjust', hidden: ctx.it.retired }), 620: ctx => ({ 'data-testid': 'train-retire', hidden: ctx.it.retired }),
    668: { 'data-testid': 'train-composer', disabled: model.tmSending }, 670: { 'data-testid': 'train-send', disabled: model.tmSending || !(state.tmComposer || '').trim() },
    687: ctx => ({ 'data-testid': `train-journal-${ctx.j.key}` }), 601: ctx => ({ 'data-testid': `train-checks-${ctx.it.key}` }), 616: { 'data-testid': 'train-refused-reason' }, 530: { 'data-testid': 'train-approval-line' },
  };
  const replace = !active ? {} : {
    421: ctx => `Show ${ctx.it.altCount} other option${ctx.it.altCount === 1 ? '' : 's'}`, 528: ctx => (ctx.it.signed ? 'Signed off' : 'Awaiting signature'), 533: 'Approve and start', 551: 'Run certificate', 601: ctx => ctx.it.checksTitle,
    519: 'Regulated or restricted sources lift the approval to a higher signature tier automatically.', 584: 'It is written in Documents by the frontier writer from this run\'s own record, every figure by reference.',
  };
  return { active, model, enhance, replace, counts, loading: data.loading };
}
