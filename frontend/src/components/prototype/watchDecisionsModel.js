import { stamp } from './evidence';

const CLASS_LABEL = { demark_release: 'De-mark and release (dual control)', requirement_ratification: 'Ratify a versioned requirement (dual control)', redeclaration: 'Re-declaration' };
const button = (label, onClick, primary) => ({ label, onClick, bg: primary ? 'var(--blue)' : '#fff', color: primary ? 'var(--paper)' : 'var(--ink)', border: primary ? 'var(--blue)' : 'var(--line)' });

export function watchDecisionsModel({ data, error, state, setState, show, act, navigate }) {
  if (!data) return error ? { decisionsFooter: error } : {};
  const items = data.decisions || [];
  const open = items.filter(d => d.state === 'open');
  const decide = (d, verb) => act(`/api/portal/watch/decisions/${d.decision_id}`, { act: verb, note: state.decisionNote || '' })
    .then(body => { setState(s => ({ ...s, decisionNote: '' })); const r = body.decision;
      show({ title: d.title, subtitle: d.decision_id, code: r.state === 'executed' ? 'Executed' : r.state === 'declined' ? 'Declined' : `${r.approvers.length} of ${r.approvals_needed} approvals`,
        body: verb === 'acknowledge' ? 'Acknowledged on the record. Active protection is unchanged: acknowledging never releases.' :
          r.state === 'executed' ? `Executed by ${r.approvers.join(' and ')}. ${r.protection_changed ? 'Protection changed: the gate now admits the subject again.' : 'A versioned requirement is now in force for new verdicts; history is unchanged.'}` :
          r.state === 'declined' ? 'Declined; protection stays as recorded.' : 'Recorded. A second, different estate operator must approve before anything changes.',
        next: 'Every decision is its own append-only record; a closed item is corrected by a new item.' }); })
    .catch(e => show({ title: d.title, code: 'Refused', body: e.message }));
  const propose = () => act('/api/portal/watch/learning/propose', {})
    .then(body => show({ title: 'Finding → candidate requirement', subtitle: body.decision.decision_id, code: 'On the panel', body: `CIF proposal ${body.decision.refs.proposal_id} passed the acceptance point, was routed ${body.decision.refs.routing} and grounded by ${body.decision.refs.grounding_seam_id}. Two operators must ratify it.` }))
    .catch(e => show({ title: 'Finding → candidate requirement', code: 'Refused', body: e.message }));
  return {
    decisionsView: items.map(d => {
      const done = d.state !== 'open';
      const opened = state.decisionOpen === d.decision_id;
      return {
        key: d.decision_id, text: `${d.title} · ${CLASS_LABEL[d.klass] || d.klass}`,
        meta: `Blast ${d.blast} · opened ${stamp(d.opened_at)} by ${d.opened_by} · ${d.approvers.length} of ${d.approvals_needed} approvals${d.acknowledged_by.length ? ` · acknowledged by ${d.acknowledged_by.length}` : ''}`,
        isDone: done, done: done ? `${d.state === 'executed' ? `Executed by ${d.approvers.join(' and ')}` : `Declined by ${d.declined?.by}`} — ${d.executed?.at ? stamp(d.executed.at) : stamp(d.declined?.at)}` : '',
        open: opened, toggleLabel: opened ? 'Close' : 'Review', onToggle: () => setState(s => ({ ...s, decisionOpen: opened ? null : d.decision_id })),
        hasAccounts: true, leftTitle: "The Watch's record", leftLines: d.watch_record.map((t, i) => ({ key: String(i), text: t })),
        rightTitle: d.klass === 'requirement_ratification' ? 'Research loop' : "Governance's record", rightLines: d.governance_record.map((t, i) => ({ key: String(i), text: t })),
        needsNote: true,
        actions: [button(`Approve (${d.approvers.length + 1} of ${d.approvals_needed})`, () => decide(d, 'approve'), true), button('Decline', () => decide(d, 'decline')), button('Acknowledge only', () => decide(d, 'acknowledge'))],
        onWalk: () => show({ title: d.title, subtitle: d.decision_id, code: d.state, body: `${d.watch_record.join(' · ')} · ${d.governance_record.join(' · ')}`, next: 'Acknowledging does not release; only two distinct operators can.' }),
      };
    }),
    decisionsFooter: `${open.length} open · ${items.length - open.length} closed · ranked by blast radius · ${data.learning?.label || ''}`,
    decisionsProposeLabel: 'Enter a finding into the research loop', decisionsPropose: propose,
    openBriefGmTable: () => navigate('/os/admin/greymirror/watch/decisions'),
  };
}
