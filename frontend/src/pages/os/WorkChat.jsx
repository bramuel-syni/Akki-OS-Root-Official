/*
 * WorkChat.jsx — v2 OS · Work tab · WORKSTUDIO · chat leaf, LIVE (M4 grounded answers · M5 durable sessions).
 *
 * Every question transits one decision (warm | fresh | refused) recorded on the one ledger; warm answers read
 * only sealed, rights-bearing qualified units of the signed-in tenant (zero source reads) through a measured,
 * whole-unit window whose loss is disclosed with the answer. Sessions are durable; compaction turns the closed
 * working context into a hash-verified artefact behind a ledger row. Nothing here is tenant-specific.
 */
import React, { useEffect, useRef } from 'react';
import { CensusAccess } from '@/components/census/CensusAccess';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { Composer } from '@/components/workchat/Composer';
import { SessionMemory } from '@/components/workchat/SessionMemory';
import { SessionRail } from '@/components/workchat/SessionRail';
import { TurnCard } from '@/components/workchat/TurnCard';
import { useChatSessions } from '@/components/workchat/useChatSessions';
import '@/components/census/census.css';
import '@/components/workchat/workchat.css';

function Intro() {
  return <section className="workchat-intro" data-testid="workchat-intro">
    <h2>Ask; the shield stays on.</h2>
    Your first question freezes the objective of a new conversation. Each turn is decided once:
    <ul>
      <li><b>Warm</b> — qualified units already verified for your estate answer it; no source is read.</li>
      <li><b>Fresh</b> — nothing qualified covers it yet; the specific missing slice is named and drafted, never dispatched from here.</li>
      <li><b>Refused</b> — nothing in your estate names the subject; the refusal is recorded and shown verbatim.</li>
    </ul>
  </section>;
}

export default function WorkChat() {
  const session = usePrototypeSession();
  const signedIn = Boolean(session.data);
  const chat = useChatSessions(signedIn);
  const end = useRef(null);
  useEffect(() => { end.current?.scrollIntoView({ block: 'nearest' }); }, [chat.active?.turns?.length, chat.pending]);

  return <div className="workchat" data-testid="work-chat-surface">
    <header className="workchat-head">
      <div className="workchat-crumb" data-testid="work-chat-breadcrumb">WORKSTUDIO · Chat{session.data?.tenant_id ? ` · ${session.data.tenant_id}` : ''}</div>
      <h1 className="workchat-title" data-testid="work-chat-title">Chat</h1>
      <p className="workchat-lead" data-testid="work-chat-lead">Ask a question; the shield stays on. Every answer traces to a qualified unit or says plainly why it can't, and every conversation is kept.</p>
    </header>
    {!signedIn && <CensusAccess error={session.error} loading={session.loading} retry={session.reload} />}
    {signedIn && <div className="workchat-body">
      <SessionRail rows={chat.rows} active={chat.active} onOpen={chat.open} onFresh={chat.fresh} />
      <main className="workchat-thread" data-testid="workchat-thread">
        {chat.active
          ? <>
            <div className="workchat-objective" data-testid="workchat-objective"><span>Objective · frozen {new Date(chat.active.objective.frozen_at).toLocaleString()}</span><strong>{chat.active.objective.text}</strong><span>{chat.active.session_id}</span></div>
            <SessionMemory session={chat.active} memory={chat.memory} onCompact={chat.compact} onReload={chat.reload} onArchive={chat.archive} />
            {chat.active.turns.map(turn => <TurnCard key={turn.turn_id} turn={turn} />)}
          </>
          : <Intro />}
        {chat.pending && <div className="workchat-turn" data-testid="workchat-pending"><div className="workchat-who">You</div><div className="workchat-q">{chat.pending}</div>
          <div className="workchat-pending"><span className="workchat-dot" /><span className="workchat-dot" /><span className="workchat-dot" /> deciding, reading qualified units, measuring the window…</div></div>}
        {chat.error && <div className="workchat-alert" role="alert" data-testid="workchat-error"><span>{chat.error}</span><button className="workchat-btn quiet" data-testid="workchat-error-dismiss" onClick={chat.dismiss}>Dismiss</button></div>}
        <div ref={end} />
        <Composer busy={Boolean(chat.pending)} disabled={!signedIn} onAsk={chat.ask} hasSession={Boolean(chat.active)} />
      </main>
    </div>}
  </div>;
}
