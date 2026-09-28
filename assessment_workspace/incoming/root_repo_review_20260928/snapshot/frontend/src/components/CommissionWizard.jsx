/*
 * CommissionWizard.jsx — Canon 5 §14 Shaping Wizard (Phase 7 Stage B-1
 * operator variant · LIFTed from Akki-OS-V1 · Extraction-Akki W11 R3).
 *
 * Canon 5 §14 verbatim (from
 * canon/text/Akki_Canon_5_Interface_Architecture.txt lines 191-197):
 *   "14  Commission — The Shaping Wizard
 *    Layout: a chat pane on one side, an objective draft rail on the
 *    other.
 *    Chat. The operator states intent; the agent asks for mandatory
 *    fields and never proposes on them. An estate-check chip renders
 *    inline before any feasibility-dependent question is asked.
 *    Draft rail. Three dimensions — entry, reach, output — plus the
 *    envelope, each field in one of three visual states: filled with a
 *    check, open and muted, or agent-assumed with the amber chip. The
 *    envelope line lists done-condition, budget, and lawful basis until
 *    each is supplied.
 *    ...
 *    Mandatory fields — reach, the four output fields, done-condition,
 *    budget, lawful basis — are asked, never pre-filled. Preference
 *    fields may carry agent recommendations, but the mandatory set never
 *    does. Every turn is grounded in a real estate read; no fabricated
 *    availability, ever, under any circumstance."
 *
 * Canon 5 §15 verbatim (lines 198-206):
 *   "Frozen is immutable — a changed intent is a new objective."
 *
 * Canon 5 §9.3 verbatim (lines 141-144):
 *   "Agent assumed — confirm or change
 *    Amber, 11px label weight, attached to any field an agent filled
 *    rather than the person."
 *
 * SOLVA.md §5.6 verbatim (lines 396-400):
 *   "One question at a time. One answer surface at a time. Clear
 *    progression indication."
 *
 * Owner supersession note (2026-08-26): where the 2026-08-14
 * Simplification Ruling ("The 5-step wizard is retired as the primary
 * path") conflicts with Canon 5 §14, Canon 5 wins. This component
 * restores the Canon 5 §14 shaping-wizard grammar as the primary
 * commissioning surface.
 */

import React, { useEffect, useRef, useState } from "react";

const BACKEND = process.env.REACT_APP_BACKEND_URL;

// Canon 5 design tokens · restrained palette, amber chip carries the
// agent-assumed grammar per §9.3.
const TOK = {
  ink1: "#111",
  ink2: "#555",
  ink3: "#8b8b8b",
  paper: "#fbfaf7",
  chatPane: "#ffffff",
  draftRail: "#f4f2ec",
  line: "#e6e2d8",
  brass: "#b08d2e",          // §9.3 amber chip
  amberSoft: "#f3e6bd",
  checkGreen: "#4a6b3f",
  oxblood: "#7a2b1e",
  ok: "#4a6b3f",
};

// Canon 5 §14 verbatim: "Mandatory fields — reach, the four output
// fields, done-condition, budget, lawful basis — are asked, never
// pre-filled."
const MANDATORY_FIELDS = [
  { path: "reach",                     label: "Reach",             dim: "reach" },
  { path: "output.form",               label: "Output form",       dim: "output" },
  { path: "output.consumer",           label: "Output consumer",   dim: "output" },
  { path: "output.grain",              label: "Output grain",      dim: "output" },
  { path: "output.standard",           label: "Output standard",   dim: "output" },
  { path: "envelope.done_condition",   label: "Done condition",    dim: "envelope" },
  { path: "envelope.budget",           label: "Budget",            dim: "envelope" },
  { path: "envelope.lawful_basis",     label: "Lawful basis",      dim: "envelope" },
];

// Canon 6 §6 verbatim: five steps · "the need stated in plain words;
// scope selected from what the registry says actually exists; standards
// and rights confirmed against explained defaults; a plan preview ...;
// and commissioning itself".
const FIVE_STEPS = [
  { key: "need",     label: "1 · State the need in plain words" },
  { key: "scope",    label: "2 · Choose scope from what the registry has" },
  { key: "standards",label: "3 · Confirm standards and rights" },
  { key: "preview",  label: "4 · Read the plan preview" },
  { key: "commit",   label: "5 · Commission" },
];

/* ------------------------------------------------------------------ */
/*  Draft rail row · one of {filled ✓, open muted, agent-assumed amber} */
/* ------------------------------------------------------------------ */

function DraftRailRow({ field, committed }) {
  // committed is a CommittedValue_v0 dict or undefined
  const state = !committed
    ? "open"
    : committed.source === "agent_assumed"
      ? "agent-assumed"
      : "operator-supplied";

  return (
    <div data-testid={`draft-rail-row-${field.path.replace(/\./g, "_")}`}
         style={{
           display: "flex", alignItems: "center", justifyContent: "space-between",
           padding: "8px 12px", borderBottom: `1px solid ${TOK.line}`,
           background: state === "open" ? "transparent" : TOK.paper,
         }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        {state === "operator-supplied" && (
          <span data-testid="check-icon" style={{ color: TOK.checkGreen, fontSize: 14 }}>✓</span>
        )}
        {state === "agent-assumed" && (
          <span data-testid="amber-chip"
                style={{
                  fontSize: 11, fontWeight: 500,
                  color: TOK.ink1, background: TOK.amberSoft,
                  border: `1px solid ${TOK.brass}`,
                  padding: "2px 6px", borderRadius: 3,
                }}>
            {/* Canon 5 §9.3 verbatim binding copy */}
            Agent assumed — confirm or change
          </span>
        )}
        <div style={{
          color: state === "open" ? TOK.ink3 : TOK.ink1,
          fontSize: 13,
        }}>
          {field.label}
        </div>
      </div>
      <div style={{ color: TOK.ink2, fontSize: 13, maxWidth: 220, textAlign: "right" }}>
        {committed ? String(committed.value) : "—"}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Chat pane · one question at a time (SOLVA §5.6)                   */
/* ------------------------------------------------------------------ */

function ChatPane({ turns, onReply, disabled }) {
  const [input, setInput] = useState("");
  const [askingField, setAskingField] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns.length]);

  const lastTurn = turns[turns.length - 1];

  function submit() {
    if (!input.trim()) return;
    onReply(lastTurn?.turn_ref, input.trim(), askingField || null);
    setInput("");
    setAskingField("");
  }

  return (
    <div data-testid="chat-pane" style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{
        padding: "10px 14px", borderBottom: `1px solid ${TOK.line}`,
        fontSize: 13, color: TOK.ink2,
      }}>
        The chat pane. The operator states intent; the agent asks for mandatory
        fields and never proposes on them.
      </div>

      <div style={{ flex: 1, overflow: "auto", padding: "12px 14px" }}>
        {turns.length === 0 && (
          <div style={{ color: TOK.ink3, fontSize: 13 }}>
            (waiting for the first question — the agent opens by asking about reach)
          </div>
        )}
        {turns.map((t, i) => (
          <div key={i} data-testid={`turn-${i}`}
               style={{ marginBottom: 10 }}>
            {t.agent_content && (
              <div style={{ color: TOK.ink1, fontSize: 14 }}>
                <strong style={{ color: TOK.ink2, fontWeight: 500 }}>Agent:</strong>{" "}
                {t.agent_content}
              </div>
            )}
            {t.user_content && (
              <div style={{ color: TOK.ink1, fontSize: 14, marginLeft: 12 }}>
                <strong style={{ color: TOK.ink2, fontWeight: 500 }}>You:</strong>{" "}
                {t.user_content}
              </div>
            )}
            {t.feasibility_snapshot_ref && (
              <div data-testid="estate-check-chip"
                   style={{
                     fontSize: 11, color: TOK.ink2, background: TOK.paper,
                     border: `1px solid ${TOK.line}`,
                     padding: "2px 6px", borderRadius: 3,
                     display: "inline-block", marginTop: 4,
                   }}>
                {/* Canon 5 §14: "An estate-check chip renders inline before any
                    feasibility-dependent question is asked." */}
                estate-check · grounded by {t.feasibility_snapshot_ref}
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div style={{ padding: "10px 14px", borderTop: `1px solid ${TOK.line}` }}>
        <input data-testid="chat-input" value={input}
               onChange={(e) => setInput(e.target.value)}
               onKeyDown={(e) => { if (e.key === "Enter") submit(); }}
               placeholder="Type your reply and press Enter..."
               disabled={disabled}
               style={{
                 width: "100%", padding: "8px 10px",
                 border: `1px solid ${TOK.line}`, borderRadius: 4,
                 fontSize: 14, background: TOK.chatPane,
               }} />
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Draft rail · three dimensions + envelope (Canon 5 §14)            */
/* ------------------------------------------------------------------ */

function DraftRail({ state, onCommit }) {
  const committed = (state && state.committed_values) || {};
  const dimensions = ["entry", "reach", "output"];
  const envelopeFields = MANDATORY_FIELDS.filter((f) => f.dim === "envelope");
  const outputFields = MANDATORY_FIELDS.filter((f) => f.dim === "output");
  const reachField = MANDATORY_FIELDS.find((f) => f.path === "reach");

  return (
    <div data-testid="draft-rail"
         style={{
           background: TOK.draftRail, borderLeft: `1px solid ${TOK.line}`,
           height: "100%", overflow: "auto",
         }}>
      <div style={{ padding: "12px 14px", borderBottom: `1px solid ${TOK.line}` }}>
        <div style={{ fontSize: 14, color: TOK.ink1, fontWeight: 500 }}>
          Objective draft rail
        </div>
        <div style={{ fontSize: 12, color: TOK.ink2, marginTop: 2 }}>
          Three dimensions — entry, reach, output — plus the envelope.
        </div>
      </div>

      {/* Dimension: entry (no mandatory fields at v0; preference-only) */}
      <div style={{ padding: "10px 14px" }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
          entry
        </div>
        <div style={{ padding: "6px 0", fontSize: 13, color: TOK.ink3 }}>
          (preference · agent may recommend)
        </div>
      </div>

      {/* Dimension: reach */}
      <div style={{ padding: "10px 14px", borderTop: `1px solid ${TOK.line}` }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
          reach
        </div>
        <DraftRailRow field={reachField} committed={committed[reachField.path]} />
      </div>

      {/* Dimension: output · four fields */}
      <div style={{ padding: "10px 14px 0 14px", borderTop: `1px solid ${TOK.line}` }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
          output
        </div>
      </div>
      {outputFields.map((f) => (
        <DraftRailRow key={f.path} field={f} committed={committed[f.path]} />
      ))}

      {/* Envelope */}
      <div style={{ padding: "10px 14px 0 14px", borderTop: `1px solid ${TOK.line}` }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
          envelope
        </div>
      </div>
      {envelopeFields.map((f) => (
        <DraftRailRow key={f.path} field={f} committed={committed[f.path]} />
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Canon 6 §6 · five-step progression strip                           */
/* ------------------------------------------------------------------ */

function FiveStepStrip({ committedCount, frozen }) {
  const step = frozen
    ? 4
    : committedCount === 0
      ? 0
      : committedCount < MANDATORY_FIELDS.length
        ? 2
        : 3;

  return (
    <div data-testid="five-step-strip"
         style={{
           display: "flex", gap: 8, padding: "8px 14px",
           borderBottom: `1px solid ${TOK.line}`,
           background: TOK.paper,
         }}>
      {FIVE_STEPS.map((s, i) => (
        <div key={s.key}
             style={{
               fontSize: 11, padding: "3px 8px", borderRadius: 3,
               background: i === step ? TOK.brass : "transparent",
               color: i === step ? "#fff" : TOK.ink2,
               border: i === step ? "none" : `1px solid ${TOK.line}`,
             }}>
          {s.label}
        </div>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Root                                                              */
/* ------------------------------------------------------------------ */

export default function CommissionWizard() {
  const [session, setSession] = useState(null);
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);
  const [frozen, setFrozen] = useState(false);

  async function startSession() {
    setError(null);
    try {
      const r = await fetch(`${BACKEND}/api/wizard/operator/session`, { method: "POST" });
      if (!r.ok) throw new Error(`session start failed · HTTP ${r.status}`);
      const s = await r.json();
      setSession(s);
      // First agent turn
      await advanceTurn(s.session_id, null, "");
    } catch (e) {
      setError(e.message);
    }
  }

  async function advanceTurn(sessionId, turnRef, userContent, field, value) {
    try {
      const body = {};
      if (turnRef) body.turn_ref = turnRef;
      if (userContent) body.user_content = userContent;
      if (field) body.field = field;
      if (value !== undefined) body.value = value;
      const r = await fetch(`${BACKEND}/api/wizard/operator/${sessionId}/turn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!r.ok) throw new Error(`turn failed · HTTP ${r.status}`);
      // Reload state after every turn
      const stateResp = await fetch(`${BACKEND}/api/wizard/operator/${sessionId}`);
      if (stateResp.ok) setState(await stateResp.json());
    } catch (e) {
      setError(e.message);
    }
  }

  async function commitReview() {
    if (!session) return;
    try {
      const r = await fetch(`${BACKEND}/api/wizard/operator/${session.session_id}/commit-review`);
      if (r.ok) setState(await r.json());
    } catch (e) { setError(e.message); }
  }

  async function freeze() {
    if (!session) return;
    try {
      const r = await fetch(`${BACKEND}/api/wizard/operator/${session.session_id}/freeze`, {
        method: "POST",
      });
      if (!r.ok) throw new Error(`freeze refused · HTTP ${r.status}`);
      setFrozen(true);
      const stateResp = await fetch(`${BACKEND}/api/wizard/operator/${session.session_id}`);
      if (stateResp.ok) setState(await stateResp.json());
    } catch (e) { setError(e.message); }
  }

  const turns = (state && state.turns) || [];
  const committedCount = state ? Object.keys(state.committed_values || {}).length : 0;

  return (
    <div data-testid="commission-wizard"
         style={{ display: "flex", flexDirection: "column", height: "100vh",
                  fontFamily: "system-ui, -apple-system, sans-serif",
                  background: TOK.paper, color: TOK.ink1 }}>

      <header style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "12px 18px", borderBottom: `1px solid ${TOK.line}`,
      }}>
        <div>
          <div style={{ fontSize: 16, fontWeight: 500 }}>Commission — The Shaping Wizard</div>
          <div style={{ fontSize: 12, color: TOK.ink2, marginTop: 2 }}>
            Canon 5 §14 · turns a need into governed work in five steps
          </div>
        </div>
        {!session ? (
          <button data-testid="start-session-btn" onClick={startSession}
                  style={{ background: TOK.brass, color: "#fff", border: "none",
                            padding: "8px 16px", borderRadius: 4, cursor: "pointer" }}>
            Start commissioning
          </button>
        ) : (
          <div style={{ fontSize: 11, color: TOK.ink3 }}>
            session {session.session_id.slice(0, 8)}…
          </div>
        )}
      </header>

      {session && (
        <FiveStepStrip committedCount={committedCount} frozen={frozen} />
      )}

      {error && (
        <div data-testid="wizard-error" style={{
          padding: "10px 14px", background: TOK.paper,
          color: TOK.oxblood, borderBottom: `3px solid ${TOK.oxblood}`,
          fontSize: 13,
        }}>
          {error}
        </div>
      )}

      <div style={{ flex: 1, display: "grid",
                     gridTemplateColumns: session ? "1fr 380px" : "1fr",
                     minHeight: 0 }}>
        {session ? (
          <ChatPane turns={turns}
                    disabled={frozen}
                    onReply={(turnRef, content, field) =>
                      advanceTurn(session.session_id, turnRef, content, field)
                    } />
        ) : (
          <div style={{ padding: 24, color: TOK.ink2 }}>
            The shaping wizard opens with a chat pane and a draft rail. The
            operator states intent; the agent asks for mandatory fields and
            never proposes on them.
          </div>
        )}
        {session && (
          <DraftRail state={state} />
        )}
      </div>

      {session && (
        <footer style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          padding: "10px 18px", borderTop: `1px solid ${TOK.line}`,
          background: TOK.paper,
        }}>
          <div style={{ fontSize: 11, color: TOK.ink3 }}>
            {/* Canon 5 §15 verbatim binding copy */}
            Frozen is immutable — a changed intent is a new objective.
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <button onClick={commitReview}
                    data-testid="commit-review-btn"
                    disabled={frozen}
                    style={{ padding: "6px 12px", border: `1px solid ${TOK.line}`,
                              background: TOK.chatPane, borderRadius: 4,
                              cursor: frozen ? "not-allowed" : "pointer" }}>
              Commit review
            </button>
            <button onClick={freeze}
                    data-testid="freeze-btn"
                    disabled={frozen || committedCount < MANDATORY_FIELDS.length}
                    style={{ padding: "6px 12px", border: "none",
                              background: frozen ? TOK.ink3 : TOK.checkGreen,
                              color: "#fff", borderRadius: 4,
                              cursor: (frozen || committedCount < MANDATORY_FIELDS.length) ? "not-allowed" : "pointer" }}>
              {frozen ? "Frozen" : "Freeze objective"}
            </button>
          </div>
        </footer>
      )}
    </div>
  );
}
