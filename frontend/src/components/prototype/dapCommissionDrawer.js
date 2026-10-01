import { stamp } from './evidence';

const PHASES = ['Commissioned', 'Reserved', 'Limits agreed', 'Sent to worker', 'Worker reported', 'Independently verified', 'Usage recorded', 'Finished'];
export const STATUS = { ready: 'Ready', executing: 'Executing', interrupted: 'Interrupted', routing: 'Waiting for sign-off', stopped: 'Stopped', blocked: 'Blocked', refused: 'Refused' };
export const requestName = (row, rows) => { const i = rows.findIndex(r => r.request_id === row.request_id); return `Request ${rows.length - (i < 0 ? 0 : i)}`; };
const pct = n => `${Math.round(n * 100)}%`;
const n = v => v == null ? 'Not recorded' : new Intl.NumberFormat('en').format(Number(v));

export function progress(run) {
  const reached = (run?.phases || []).filter(p => p.reached).length;
  const last = (run?.timeline || []).slice(-1)[0];
  return { reached, total: PHASES.length, pctStr: pct(reached / PHASES.length), stepStr: `Step ${Math.max(1, reached)} of ${PHASES.length}`, stageLabel: PHASES[Math.max(0, reached - 1)],
    caption: last?.detail || 'Waiting for the first step.', updated: last ? `Updated ${stamp(last.at)}` : '', segments: PHASES.map((label, i) => ({ key: label, label, done: i < reached, bg: i < reached ? 'var(--blue)' : 'var(--hair)', opacity: i < reached ? '1' : '.5' })) };
}

const consumed = (run, dim) => (run?.budget || []).find(b => b.dimension === dim)?.consumed;
const usage = (run, unit) => (run?.terminal?.usage || []).find(u => u.unit === unit)?.quantity;

export function readyRows(run) {
  const sealed = run?.sealed || {}, quality = sealed.quality || {}, registry = run?.registry || {};
  return [
    { l: 'Records read', v: n(consumed(run, 'scanned_records') ?? usage(run, 'records_scanned')) },
    { l: 'Qualified units delivered', v: n(quality.qualified_units ?? consumed(run, 'returned_records') ?? usage(run, 'records_returned')) },
    { l: 'Personal details redacted', v: n(quality.redactions ?? quality.floor_redactions) },
    { l: 'Sealed result', v: sealed.object?.size_bytes ? `${n(sealed.object.size_bytes)} bytes · fingerprinted` : 'Recorded on the worker' },
    { l: 'Independent check', v: registry.inspection_ref ? `Verified on ${run?.work_order?.inspector_runtime_id || 'a second computer'}` : 'Not recorded' },
    { l: 'Time used', v: usage(run, 'seconds') ? `${Number(usage(run, 'seconds')).toFixed(1)} s` : 'Not recorded' },
    { l: 'Charged', v: usage(run, 'usd_spend') != null ? `${usage(run, 'usd_spend')} USD · ${run?.terminal?.terms_ref || 'pilot terms'}` : 'Not recorded' },
  ];
}

export function signoff(groups, standIns) {
  const seats = g => Array.isArray(g.members) ? g.members.length : g.members;
  const named = (groups || []).map(g => g.purpose === 'scope' ? 'you (scope)' : `${g.purpose} · ${(standIns || []).some(s => s.group === g.group) ? 'interim pilot stand-in' : `${seats(g) || ''} seated approver(s)`}`);
  return { approvedLine: named.length ? `Signed off by ${named.join(', ')}.` : 'Sign-off recorded with the request.',
    signoffReason: (standIns || []).length ? 'Digicow has not yet seated its named approvers; the admitted interim stand-in signs in their place and says so on every approval.' : 'Each approver signed with a key held in estate custody.',
    waitLine: 'Approval expires with the request; nothing wider can be run under it.' };
}

export function drawerFor({ row, rows, run, approvals, order, delivery, terms, actions }) {
  if (!row) return {};
  const prog = progress(run), state = row.state, approvalState = approvals?.state;
  const refused = state === 'routing' && approvalState === 'refused';
  const waiting = state === 'routing' && approvalState === 'pending';
  const executing = state === 'executing' || state === 'interrupted' || (state === 'routing' && !refused && !waiting);
  const standIns = order?.stand_ins || [];
  const sign = signoff(order?.groups, standIns);
  const base = { id: requestName(row, rows), statusLabel: refused ? 'Refused' : executing && state === 'routing' ? 'Starting' : STATUS[state] || row.lifecycle_state,
    statusColor: state === 'ready' ? 'var(--sage)' : refused || state === 'blocked' ? 'var(--oxblood)' : 'var(--brass)', statusBg: 'var(--surface)',
    agreement: terms || 'Pilot terms', submitted: stamp(row.created_at), hasDetail: true, objective: row.objective_text, scope: row.units.join(', '),
    hasAssistant: false, noAssistant: true, convChev: '', convOpen: false, onCopyNew: () => actions.copyNew(row), showCopyNew: true, otherStatus: false };
  if (refused) return { ...base, isRefused: true, refusedLine: 'An approver refused this request.', reason: row.reason, refusalReason: (approvals.groups || []).flatMap(g => g.decisions || []).filter(d => d.decision === 'refused').map(d => `${d.group}: ${d.reason}`).join(' ') || 'No reason text was recorded.' };
  if (waiting) {
    const pending = (approvals.groups || []).filter(g => !g.satisfied).map(g => g.purpose);
    return { ...base, isInApproval: true, reason: row.reason, addressedTo: `Addressed to the ${pending.join(' and ') || 'seated'} approver(s) of your estate.`,
      deadlineLine: approvals.deadline_epoch ? `If nobody decides by ${stamp(new Date(approvals.deadline_epoch * 1000).toISOString())} the request expires unrun.` : '', canWithdraw: false };
  }
  if (executing) {
    const interrupted = state === 'interrupted';
    return { ...base, isExecuting: true, hasPercent: true, pctStr: prog.pctStr, hasStages: true, stepStr: prog.stepStr, stageLabel: prog.stageLabel, segments: prog.segments,
      etaLine: interrupted ? `Interrupted: ${row.reason}${row.next_action ? ` ${row.next_action}` : ''}` : state === 'routing' ? 'Approved. The first bounded step starts when you open the request.' : prog.caption,
      updated: prog.updated, canStop: (row.permitted_actions || []).includes('stop'), onStopStart: () => actions.stopStart(row),
      signoffRequired: true, ...sign, signoffNotRequired: false };
  }
  if (state === 'ready') {
    const d = delivery || {}, artifact = run?.terminal?.artifact_refs?.[0];
    const history = (run?.deliveries || []).map(x => `${stamp(x.at)} · ${x.state === 'completed' ? 'Retrieved' : x.state === 'offered' ? 'Retrieval offered' : x.state === 'uncertain' ? 'Retrieval outcome uncertain' : 'Retrieval requested'}`);
    return { ...base, showReadyBlocks: true, readyEyebrow: 'Ready', readyEyebrowColor: 'var(--sage)', block2Rows: readyRows(run), isProcessedMode: true, onOpenReport: () => actions.openReport(row),
      showDrawerAction: true, isTransferring: d.state === 'pending', transferPctStr: '', isTransferFailed: d.state === 'held', showDrawerButton: d.state !== 'pending',
      actionBg: d.state === 'held' ? 'var(--oxblood)' : 'var(--blue)', drawerActionLabel: d.state === 'held' ? 'Retrieval held — see why' : d.state === 'offered' || d.state === 'completed' ? 'Retrieve again' : 'Retrieve result', onAction: () => actions.retrieveStart(row, artifact),
      hasCountedSentence: true, countedLine: d.state === 'held' ? d.reason : history.length ? `${history.length} retrieval request(s) recorded for this result.` : 'No retrieval has been requested yet. The sealed result stays with your estate\u2019s custodian.',
      hasCountedRows: history.length > 0, countedRows: history, readySignoffApproved: true, ...sign, readySignoffNotRequired: false, readySignoffStanding: false };
  }
  const stopped = state === 'stopped';
  return { ...base, isBlocked: true, stoppedHasPercent: stopped, stoppedPctStr: prog.pctStr, stoppedHasStages: stopped, stoppedSegments: prog.segments,
    suspendedWaiting: false, suspendedUnspecified: false, hasStoppedProgress: stopped, stoppedCaption: 'Stopped at your request. Work done so far is recorded and charged; nothing partial was delivered.',
    blockedAtLine: `${stopped ? 'Stopped' : 'Blocked'} at ${prog.stepStr.toLowerCase()} — ${prog.stageLabel}.`, isEstateBlock: !stopped,
    kindLine: stopped ? 'Stopped by you' : 'Held by the estate\u2019s checks', hasBlockedBy: false, hasBlockReason: true, blockReason: row.reason,
    hasBlockRef: Boolean(row.reason_receipt_ref), blockRef: row.reason_receipt_ref, whatNextLine: row.next_action || 'Nothing further will run under this request.',
    showBlockedSignoff: true, signoffRequired: true, ...sign, signoffNotRequired: false };
}
