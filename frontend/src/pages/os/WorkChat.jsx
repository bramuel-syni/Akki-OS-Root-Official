import React, { useEffect, useState } from 'react';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { useChatSessions } from '@/components/workchat/useChatSessions';
import { TurnWorking } from '@/components/workchat/TurnWorking';
import { SessionMemory } from '@/components/workchat/SessionMemory';
import { readableText } from '@/components/shared/PresentationDetails';
import { stamp } from '@/components/prototype/evidence';

export default function WorkChat() {
  const session = usePrototypeSession(), chat = useChatSessions(Boolean(session.data));
  const [draft, setDraft] = useState(''), [rail, setRail] = useState(false), [audit, setAudit] = useState(false), [turnId, setTurnId] = useState(null), [copyStatus, setCopyStatus] = useState('');
  const send = async () => { if (!draft.trim() || chat.pending) return; const result = await chat.ask(draft.trim()); if (result) setDraft(''); };
  const turns = chat.active?.turns || [];
  const selected = turns.find(t => t.turn_id === turnId) || turns.at(-1);
  useEffect(() => { const log = document.querySelector('[data-testid="workchat-thread"]'); if (log) log.scrollTop = log.scrollHeight; }, [chat.active, chat.pending]);
  const copy = async text => { try { await navigator.clipboard.writeText(text); setCopyStatus('Copied'); } catch { setCopyStatus('Copy unavailable'); } };
  const messages = turns.flatMap(t => {
    const refused = t.refused || t.decision === 'refused';
    const slice = t.decision_detail?.slice;
    const freshAnswer = slice && t.decision === 'fresh' ? `More data is needed from ${slice.database}.${slice.table}.${t.decision_detail?.draft ? ' A data request has been drafted; it needs review and approval before it can run.' : ' No data request has been confirmed.'}` : null;
    const answer = readableText(refused ? t.refusal_reason : freshAnswer || t.answer || t.fresh_message || 'No answer recorded.');
    return [{ key: `${t.turn_id}-q`, id: t.turn_id, isUser: true, isEditing: false, text: t.question, time: stamp(t.asked_at), showActions: false, onCopy: () => copy(t.question) },
      { key: `${t.turn_id}-a`, id: t.turn_id, isUser: false, isAnswered: true, claimText: answer, honesty: refused ? 'No supported answer available.' : t.decision === 'fresh' ? 'More data needed. Any request remains a draft.' : `${t.evidence?.cited_refs?.length || 0} sources cited`, time: stamp(t.asked_at), auditTriggerColor: 'var(--sage)', auditTriggerLabel: 'Sources & answer limits', onToggleAudit: () => { setTurnId(t.turn_id); setAudit(true); }, onCopy: () => copy(answer), onRetry: () => { if (!chat.pending) chat.ask(t.question); }, onRegenerate: () => { if (!chat.pending) chat.ask(t.question); } }];
  });
  if (chat.pending) messages.push({ key: 'pending-q', isUser: true, isEditing: false, text: chat.pending }, { key: 'pending-a', isUser: false, isThinking: true, stepsView: [{ mark: '·', text: 'Checking available evidence…', color: 'var(--ink3)' }] });
  const model = { isChatActive: true, shellHeight: 'calc(100dvh - 152px)', akkiTitleIdle: Boolean(chat.active), akkiActiveTitle: readableText(chat.active?.title || ''), hasSessionBanner: Boolean(chat.error || copyStatus), sessionBanner: readableText(chat.error || copyStatus), sessionBannerColor: chat.error ? 'var(--oxblood)' : 'var(--sage)',
    akkiConvRailClosed: !rail, akkiConvRailOpen: rail, akkiToggleConvRail: () => setRail(v => !v), akkiConvCountLabel: `${chat.rows.length} conversations`,
    akkiNewConversation: () => { chat.fresh(); setDraft(''); setTurnId(null); }, akkiThreadEmpty: !messages.length, akkiMessagesView: messages,
    akkiConversationsView: chat.rows.map(c => ({ key: c.session_id, title: readableText(c.title), lastActive: stamp(c.updated_at), isRenaming: false, menuOpen: false, bg: c.session_id === chat.active?.session_id ? 'var(--surface2)' : 'transparent', borderColor: c.session_id === chat.active?.session_id ? 'var(--blue)' : 'transparent', onSelect: () => { if (!chat.pending) chat.open(c.session_id); } })),
    akkiComposerText: draft, akkiComposerChange: e => setDraft(e.target.value), akkiComposerKeyDown: e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }, akkiSend: send,
    akkiModelChip: 'Governed model', akkiShieldChip: 'Shield', akkiSettingsOpen: false, akkiShieldPanelOpen: false,
    akkiAuditCollapsed: !audit, akkiAuditExpanded: audit, akkiAuditExpand: () => setAudit(true), akkiAuditCollapse: () => setAudit(false),
    askSuggestionAnswered: () => setDraft('What does our latest estate census show?'), askSuggestionEvidence: () => setDraft('Which data needs a quality review?'), askSuggestionEntitlement: () => setDraft('Which sources have verified access rights?'), askSuggestionVendor: () => setDraft('Where are the largest duplicate candidates?') };
  return <OwnerWorkspace session={session} title="Chat" group="WorkStudio" section="chat" model={model}
    replace={{ 754: 'What do you need to know?', 756: 'What does our latest estate census show?', 757: 'Which data needs a quality review?', 758: 'Which sources have verified access rights?', 759: 'Where are the largest duplicate candidates?', 955: selected ? 'Selected answer' : 'No answer selected' }}
    enhance={{ 750: { 'data-testid': 'workchat-thread' }, 876: { 'data-testid': 'workchat-composer', 'aria-label': 'Your question', disabled: Boolean(chat.pending), maxLength: 8000 }, 936: { 'data-testid': 'workchat-send', disabled: Boolean(chat.pending) || !draft.trim() }, 708: { 'data-testid': 'workchat-new', 'aria-disabled': Boolean(chat.pending), onClick: () => { if (!chat.pending) model.akkiNewConversation(); } }, 715: { 'data-testid': 'workchat-new-expanded', disabled: Boolean(chat.pending) }, 729: c => ({ 'data-testid': `workchat-session-${c.c.key}` }), 733: { hidden: true }, 716: { hidden: true }, 178: { onClick: undefined, onKeyDown: undefined, role: undefined, tabIndex: undefined, title: undefined }, 934: { disabled: true, title: 'Chat-to-document handoff is not available yet' }, 880: { 'aria-disabled': true, onClick: undefined, onKeyDown: undefined, title: 'Model selection is managed by your workspace' }, 922: { 'aria-disabled': true, onClick: undefined, onKeyDown: undefined, title: 'Shield settings are enforced by the workspace' }, 707: { 'data-testid': 'workchat-toggle-conversations' }, 943: { 'data-testid': 'workchat-open-evidence' }, 953: { 'data-testid': 'workchat-close-evidence' } }}
    slots={{ 957: <>{selected ? <TurnWorking key={selected.turn_id} turn={selected} /> : <p className="owner-status" data-testid="workchat-evidence-empty">No answer evidence yet.</p>}<SessionMemory session={chat.active} memory={chat.memory} onCompact={chat.compact} onReload={chat.reload} onArchive={chat.archive} /></> }}>
  </OwnerWorkspace>;
}