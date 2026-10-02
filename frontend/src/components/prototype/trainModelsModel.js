// Binds the owner's Train Models studio (v2_os.html, lines 201–692) to the live board. Statuses, groups, stage dots and the
// thread widgets follow the owner's prototype logic; every value comes from a record, never a sample.
export const STATUS_COLOR = { Shaping: 'var(--ink3)', 'In Approval': 'var(--accent)', Queued: 'var(--ink3)', 'In training': 'var(--blue)', Testing: 'var(--brass)', 'In service': 'var(--sage)', Refused: 'var(--oxblood)', Retired: 'var(--ink3)' };
export const STATUS_BG = { Shaping: 'var(--surface2)', 'In Approval': 'rgba(76,95,213,.10)', Queued: 'var(--surface2)', 'In training': 'rgba(76,95,213,.10)', Testing: 'rgba(176,141,46,.14)', 'In service': 'rgba(29,122,110,.12)', Refused: 'rgba(184,57,91,.12)', Retired: 'var(--surface2)' };
const GROUPS = [['Running', ['In training', 'Testing', 'Queued']], ['Shaping', ['Shaping']], ['In approval', ['In Approval']], ['In service', ['In service']], ['Refused', ['Refused']], ['Retired', ['Retired']]];
const LIFE = [['shaping', 'Shape'], ['approval', 'Approve'], ['training', 'Train'], ['testing', 'Test'], ['service', 'Accept']];
const STAGE_OF = { Shaping: 0, 'In Approval': 1, Queued: 1, 'In training': 2, Testing: 3, Refused: 3, 'In service': 4, Retired: 4 };
export const FINISHED = ['In service', 'Refused', 'Retired'];
const FAMILY = { text: 'Text language identification', audio: 'Audio language cognition', music: 'Music identification', reinforcement: 'Weak-language reinforcement', owner: 'Opened here' };
const STAGE_BUMP = { approval: 'approval', begin: 'approval', queue: 'approval', status: 'training', checks: 'testing', record: 'testing', suggest: 'testing', refused: 'testing', doc: 'testing', remodel: 'service' };
const ORDER = LIFE.map(([key]) => key);
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const parse = iso => { const ms = iso ? Date.parse(iso) : NaN; return Number.isNaN(ms) ? null : new Date(ms); };
const hm = d => `${String(d.getUTCHours()).padStart(2, '0')}:${String(d.getUTCMinutes()).padStart(2, '0')}`;
export function relative(iso) {
  const d = parse(iso); if (!d) return '';
  const mins = (Date.now() - d.getTime()) / 60000;
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${Math.round(mins)}m ago`;
  if (mins < 1440) return `${Math.floor(mins / 60)}h ago`;
  if (mins < 10080) return `${DAYS[d.getUTCDay()]} ${hm(d)}`;
  return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]}${d.getUTCFullYear() !== new Date().getUTCFullYear() ? ` ${d.getUTCFullYear()}` : ''}`;
}
function dayLabel(iso) {
  const d = parse(iso); if (!d) return '';
  const days = Math.floor((Date.now() - d.getTime()) / 86400000);
  return days < 1 ? 'Today' : days < 2 ? 'Yesterday' : `${DAYS[d.getUTCDay()]} ${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]}`;
}
export const nextVersionName = (name, names) => {
  const base = String(name || 'model').replace(/\s+v\d+$/, '');
  const max = Math.max(1, ...names.map(n => { const m = String(n).match(/^(.*)\s+v(\d+)$/); return m && m[1] === base ? Number(m[2]) : 0; }));
  return `${base} v${max + 1}`;
};

export function progressOf(run) {
  const s = run.status;
  if (s === 'In service' || s === 'Retired') return 100;
  if (s === 'Refused') return 92;
  if (s === 'Testing') return 85;
  if (s === 'In training') return 60;
  if (s === 'Queued') return 50;
  if (s === 'In Approval') return 40;
  if (run.ready) return 34;
  if (run.baseline_card) return 26;
  if (run.progress) return 20;
  const set = Object.values(run.evidence?.fields || {}).filter(Boolean).length;
  return 8 + Math.min(3, set) * 6;
}

const tone = t => ['estimate'].includes(t) ? 'var(--brass)' : ['you said', 'measured', 'measured gap', 'contract'].includes(t) ? 'var(--sage)' : 'var(--ink3)';
const classTone = cls => cls === 'Regulatory' ? ['var(--oxblood)', 'rgba(184,57,91,.12)'] : cls === 'Internal' ? ['var(--accent)', 'rgba(76,95,213,.10)'] : ['var(--brass)', 'rgba(176,141,46,.16)'];

function checksOf(run) {
  return run.checks.map((c, j) => ({ key: `c${j}`, n: c.n, v: c.v || '', label: c.passes ? 'Settled' : 'Below floor', color: c.passes ? 'var(--sage)' : 'var(--oxblood)', nameColor: 'var(--ink2)' }));
}

export function threadItems(run, { state, names, pendingText, canOperate, toggleThink, pickBaseline }) {
  const out = []; let stage = 'shaping', previous = null;
  const bump = key => { if (ORDER.indexOf(key) > ORDER.indexOf(stage)) stage = key; };
  const requested = run.messages.some(m => m.widget === 'action' && m.action === 'record_training_request' && !/^Not done/.test(m.text || ''));
  const dismissed = Boolean(state.tmDismiss?.[run.run_id]);
  const altsShown = Boolean(state.tmAlts?.[run.run_id]);
  const card = run.baseline_card;
  const checks = checksOf(run);
  run.messages.forEach((m, i) => {
    const at = parse(m.at);
    if (at && (previous === null || Math.abs(at - previous) > 6 * 3600000)) out.push({ key: `d${i}`, isDivider: true, isMsg: false, label: dayLabel(m.at), stage, align: 'center' });
    if (at) previous = at;
    if (STAGE_BUMP[m.widget]) bump(STAGE_BUMP[m.widget]);
    const user = m.role === 'user';
    const think = [...(m.think || []), ...(m.flags?.length ? [`Check: ${m.flags.length} figure${m.flags.length > 1 ? 's' : ''} in this reply (${m.flags.join(', ')}) could not be matched to the record — treat as unverified.`] : [])];
    const key = m.id || `${run.run_id}-${i}`;
    const thinkKey = `${run.run_id}:${key}`;
    out.push({
      key, stage, isDivider: false, isMsg: true, who: user ? 'You' : 'Akki', text: m.text?.includes('unknown protected boundary') ? 'The action could not be completed at that time. No training or admission was started.' : m.text || '', ts: relative(m.at), align: user ? 'flex-end' : 'flex-start',
      bubbleBg: user ? 'rgba(76,95,213,.07)' : m.status === 'unavailable' ? 'rgba(176,141,46,.10)' : 'var(--surface)', bubbleBorder: user ? 'rgba(76,95,213,.20)' : 'var(--line)', hasBubble: Boolean(m.text),
      hasThink: think.length > 0, thinkLabel: `How I got here · ${think.length} step${think.length === 1 ? '' : 's'}`, thinkOpen: Boolean(state.tmThink?.[thinkKey]), thinkClosed: !state.tmThink?.[thinkKey], onThink: () => toggleThink(thinkKey),
      thinkSteps: think.map((t, j) => ({ key: `k${j}`, t, line: j === think.length - 1 ? 'transparent' : 'var(--line)', pad: j === think.length - 1 ? '0' : '14px' })),
      hasChecks: m.widget === 'checks' && checks.length > 0, checks, checksTitle: `${checks.length} ${run.family === 'music' ? 'measures' : 'languages'} on the sealed held-out set`,
      hasRecord: m.widget === 'record', recRows: run.record_rows.map((row, j) => ({ key: `r${j}`, k: row[0], v: row[1] })), recLearnings: run.learnings || 'No reading recorded beyond the certificate.',
      hasRefused: m.widget === 'refused', reason: run.reason || '', retired: run.status === 'Retired' || !canOperate,
      hasApproval: m.widget === 'approval', apprLine: run.approval?.line || '', signed: Boolean(run.approval?.signed), canRemind: Boolean(run.approval?.plan_sha256) && !run.approval?.signed && canOperate,
      remindDisabled: Boolean(run.approval?.signed) || (!canOperate && Boolean(run.approval?.plan_sha256)) || !run.approval?.plan_sha256,
      remindLabel: run.approval?.signed ? `Signed off by ${run.approval.signed.by} · ${relative(run.approval.signed.at)} · ${run.approval.signed.plan_sha256.slice(0, 12)}` : run.approval?.plan_sha256 ? `Awaiting the owner's signature · ${run.approval.plan_sha256.slice(0, 12)}` : 'No signable plan yet',
      hasBegin: m.widget === 'begin' && !requested && canOperate && run.family === 'owner',
      hasReflect: m.widget === 'reflect' && run.reflect_rows.length > 0, reflHead: `Committing to ${run.name}`,
      reflRows: run.reflect_rows.map((r, j) => ({ key: `f${j}`, k: r.k, v: r.v, t: r.t || '', hasT: Boolean(r.t), tColor: tone(r.t) })),
      hasBaseline: m.widget === 'baseline' && Boolean(card), blName: card?.name || '', blBecause: card?.because || '', blEvidence: card?.evidence || '', blShowToggle: !altsShown && Boolean(card?.alts?.length), altCount: card?.alts?.length || 0, onUseSug: () => pickBaseline('learned'),
      hasSources: m.widget === 'sources' && run.sources.length > 0, srcRows: run.sources.map((s, j) => ({ key: `s${j}`, n: s.n, v: s.v, cls: s.cls, clsColor: classTone(s.cls)[0], clsBg: classTone(s.cls)[1] })),
      hasStatus: m.widget === 'status', statusLabel: m.status_label || 'Measuring', statusLine: m.status_line || '',
      hasSuggest: m.widget === 'suggest' && !dismissed, hasDoc: m.widget === 'doc', hasRemodel: m.widget === 'remodel', remodelName: nextVersionName(run.name, names),
      hasBaselineAlts: false, hasQueue: false, hasContinue: false, hasRights: false, altCards: [],
    });
    if (m.widget === 'baseline' && altsShown && card?.alts?.length) {
      out.push({ key: `${key}-alts`, stage, isDivider: false, isMsg: true, who: 'Akki', text: '', hasBubble: false, align: 'flex-start', ts: '', hasBaselineAlts: true,
        altCards: card.alts.map((a, j) => ({ key: `a${j}`, name: a.name, because: a.because, evidence: a.evidence, onUse: () => pickBaseline('reading') })) });
    }
  });
  if (pendingText) {
    out.push({ key: 'pending-you', stage, isDivider: false, isMsg: true, who: 'You', text: pendingText, ts: 'Just now', align: 'flex-end', bubbleBg: 'rgba(76,95,213,.07)', bubbleBorder: 'rgba(76,95,213,.20)', hasBubble: true });
    out.push({ key: 'pending-akki', stage, isDivider: false, isMsg: true, who: 'Akki', text: 'Reading the record…', ts: '', align: 'flex-start', bubbleBg: 'var(--surface)', bubbleBorder: 'var(--line)', hasBubble: true });
  }
  return out;
}

export function reportOf(run) {
  const rows = Object.fromEntries(run.record_rows);
  const secs = [];
  if (run.status === 'Refused' || run.status === 'Retired') secs.push({ key: 'short', k: run.status === 'Refused' ? 'Where it fell short' : 'Why it stopped', v: run.reason || '—' });
  const named = [['Checks', 'Performance against the floor'], ['Recipe', 'Training recipe'], ['Data', 'Material it read'], ['Compute & time', 'Compute and time'], ['Compute', 'Compute and time'], ['Improvement over the base', 'Improvement over the base'], ['Admission', 'Admission'], ['Serving', 'Serving'], ['Privacy budget', 'Privacy budget'], ['Baseline', 'Starting point']];
  named.forEach(([k, label]) => { if (rows[k]) secs.push({ key: k, k: label, v: rows[k] }); });
  if (!secs.length) secs.push({ key: 'none', k: 'Acceptance record', v: 'None written for this run.' });
  const signed = Boolean(run.approval?.signed);
  const lead = run.status === 'In service' ? (signed ? `Admitted against the acceptance that was signed: ${rows.Acceptance || 'every check cleared'}.` : 'Cleared every per-language check against the sealed held-out set and was admitted under the owner\'s per-stratum ruling.')
    : run.status === 'Refused' ? 'Stopped at acceptance. Nothing about the run is hidden, and the reason travels with it.' : 'Retired with its reason recorded. The record stays as written.';
  const obs = run.learnings || (run.status === 'Refused' ? 'A new version opens in the same lineage; the refusal is never overwritten.'
    : run.status === 'In service' ? (signed ? 'The artefact stays on the GPU host under tenant custody; serving is a separate operation. Open the next version to widen the evidence.' : 'Serving is a separate operation from admission.') : 'Nothing further was observed after retirement.');
  return { lead, secs, obs };
}

export function dashCards(run) {
  const rows = run.record_rows.filter(([k]) => k !== 'Checks');
  const passing = run.checks.filter(c => c.passes).length;
  const cards = (run.checks.length ? [{ key: 't1', l: 'Checks cleared', v: `${passing}/${run.checks.length}`, vSize: '19px', vFam: 'var(--head)', wide: false }] : [])
    .concat(rows.map(([k, v], j) => ({ key: `c${j}`, l: k, v, vSize: '12px', vFam: 'inherit', wide: String(v).length > 40 })));
  // Two-column grid with no empty cells: a narrow card followed by a wide one takes the full row itself.
  let column = 0;
  return cards.map((card, i) => {
    const wide = card.wide || (column === 0 && (cards[i + 1]?.wide || i === cards.length - 1));
    column = wide ? 0 : (column + 1) % 2;
    return { ...card, span: wide ? 'span 2' : 'auto' };
  });
}

export function journalMeta(counts) {
  const live = counts['In service'] || 0, refused = counts.Refused || 0, retired = counts.Retired || 0, n = live + refused + retired;
  return n ? `${n} finished · ${live} in service, ${refused} refused, ${retired} retired` : 'Nothing finished yet';
}

export function stageDots(run, go) {
  const at = run ? (STAGE_OF[run.status] ?? 0) : -1;
  return LIFE.map(([key, label], i) => ({ key, label, onGo: () => go(key), size: i === at ? '13px' : '8px', bg: i <= at ? 'var(--accent)' : '#fff', border: i <= at ? '1px solid var(--accent)' : '1px solid var(--line)',
    lineBg: i === LIFE.length - 1 ? 'transparent' : i < at ? 'var(--accent)' : 'var(--line)', labelColor: i === at ? 'var(--accent)' : i < at ? 'var(--ink2)' : 'var(--ink3)', labelWeight: i === at ? '700' : '500' }));
}

export function groupsOf(runs, selected, select, remove) {
  return GROUPS.map(([label, statuses]) => ({ key: label, label, runs: runs.filter(r => statuses.includes(r.status)) })).filter(g => g.runs.length).map(g => ({ ...g, n: String(g.runs.length),
    runs: g.runs.map(r => { const p = progressOf(r); return { key: r.run_id, name: r.name, obj: r.objective || 'Objective still forming', eta: r.eta || '', unread: null, pct: `${p}%`, pctW: `${p}%`,
      statusColor: STATUS_COLOR[r.status] || 'var(--ink3)', rowBorder: r.run_id === selected ? 'var(--accent)' : 'var(--line)', rowBg: r.run_id === selected ? 'rgba(76,95,213,.06)' : '#fff',
      canDelete: Boolean(r.deletable), onDelete: e => { e.stopPropagation(); remove(r); }, onSelect: () => select(r.run_id, false) }; }) }));
}

export const familyLabel = run => FAMILY[run.family] || 'Training run';
