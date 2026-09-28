import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * Governance.jsx — W10 CP8 · Governance surface.
 *
 * Composes three panels sharing REFERENCE-NOT-COPY posture (Design Law
 * A8 · 2026-08-19):
 *   1. Reserved-Decisions Panel · Canon 8 §19 + §32.6 · W10 CP4.
 *      The five closed reserved kinds are named verbatim (R3
 *      ratification 2026-08-26T04:20Z · closed Literal enum · no
 *      free-text kinds).
 *   2. Rules-Updates Timeline · Doc 15 §17 · W8 CP6 · countdown /
 *      apply / re-check lifecycle stages surfaced from disk.
 *   3. Approvals Ledger · Doc 15 · W8 CP3 · full request+decision
 *      pairs (rules-updates · spend-requests · generic).
 *
 * Data source: GET /api/governance/state. Every row cites its on-disk
 * source_path; the surface renders record ids + short provenance
 * rather than embedding record bodies (REFERENCE-NOT-COPY). Empty
 * stores render an honest sentence naming the canon anchor.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens (matched to Registry / CostLedger).
const paper = "#f5f2ea";
const surface = "#ffffff";
const ink = "#1b1f27";
const ink2 = "#3a3f4a";
const ink3 = "#7a7f8a";
const line = "#e4dccf";
const blue = "#16274a";
const oxblood = "#8a2a44";
const brass = "#b08d2e";
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';

const RESERVED_KINDS = [
  "promote_containment",
  "extend_expiry",
  "sign_de_mark",
  "resolve_authority_disagreement",
  "cancel_ceremony_in_countdown",
];

function Panel({ "data-testid": dt, title, anchor, children }) {
  return (
    <section data-testid={dt} style={{
      background: surface, border: `1px solid ${line}`, padding: "22px 24px",
      marginBottom: 20,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
        <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
        <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
      </div>
      {children}
    </section>
  );
}

function EmptyState({ anchor, kind }) {
  return (
    <p style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
      No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
    </p>
  );
}

function EntryRow({ entry, extra }) {
  return (
    <li style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
      <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
        {entry.record_id}
      </div>
      {extra ? <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>{extra}</div> : null}
      <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
        {entry.source_path}
      </div>
    </li>
  );
}

export default function Governance() {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${BACKEND_URL}/api/governance/state`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        setState(await r.json());
      } catch (e) {
        setError(String(e));
      }
    })();
  }, []);

  return (
    <div data-testid="governance-view" style={{
      minHeight: "100vh", background: paper, padding: "40px 48px",
      fontFamily: "ui-sans-serif, system-ui",
    }}>
      <div style={{ maxWidth: 1080, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · GOVERNANCE</div>
        <h1 data-testid="governance-title" style={{
          fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
        }}>Governance Surface</h1>
        <p data-testid="governance-reference-note" style={{
          color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 20,
        }}>
          REFERENCE-NOT-COPY (Design Law A8). Every entry cites its
          on-disk source_path; record bodies live under
          <code style={{ margin: "0 4px" }}>phase0/</code> where each
          producer wrote them. Reserved-Decisions Panel anchor: Canon 8 §19
          + §32.6. Rules-Updates Timeline anchor: Doc 15 §17.
        </p>

        <nav style={{ marginBottom: 24, fontSize: 13 }}>
          <Link data-testid="nav-to-watch" to="/watch" style={{ color: blue, marginRight: 20 }}>
            → The Watch
          </Link>
          <Link data-testid="nav-to-grey-mirror" to="/grey-mirror" style={{ color: blue, marginRight: 20 }}>
            → Grey Mirror
          </Link>
          <Link to="/" style={{ color: ink3 }}>← Registry</Link>
        </nav>

        {error ? (
          <div style={{ color: oxblood, marginBottom: 12 }}>
            Failed to load governance state: {error}
          </div>
        ) : null}

        <Panel data-testid="reserved-decisions-panel"
               title="Reserved Decisions"
               anchor="Canon 8 §19 · §32.6 · W10 CP4">
          <div data-testid="reserved-decisions-count" style={{
            fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
          }}>
            {state ? `${state.reserved_decisions.count} on record` : "loading…"}
          </div>
          <p style={{ fontSize: 12, color: ink3, margin: "6px 0" }}>
            Reserved kinds (closed Literal · R3 ratification): {RESERVED_KINDS.join(" · ")}. No reserved decision is executed by machine (§32.6); the operator authors the next call after ApprovalDecision.verdict == "approved".
          </p>
          {state && state.reserved_decisions.count === 0 ? (
            <div data-testid="reserved-decisions-empty-state">
              <EmptyState anchor="Canon 8 §19" kind="reserved decisions" />
            </div>
          ) : null}
          {state && state.reserved_decisions.count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {state.reserved_decisions.entries.map((e) => (
                <EntryRow key={e.record_id} entry={e}
                  extra={`kind: ${e.reserved_decision_kind} · subject: ${e.subject_ref || "—"}`} />
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="rules-updates-timeline"
               title="Rules-Updates Timeline"
               anchor="Doc 15 §17 · W8 CP6">
          <div data-testid="rules-updates-count" style={{
            fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
          }}>
            {state ? `${state.rules_updates.count} lifecycle rows` : "loading…"}
          </div>
          {state && state.rules_updates.count === 0 ? (
            <EmptyState anchor="Doc 15 §17" kind="rules-updates lifecycle rows" />
          ) : null}
          {state && state.rules_updates.count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {state.rules_updates.entries.map((e) => (
                <EntryRow key={`${e.record_id}-${e.lifecycle_stage}`} entry={e}
                  extra={`stage: ${e.lifecycle_stage}`} />
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="approvals-ledger"
               title="Approvals Ledger"
               anchor="Doc 15 · W8 CP3">
          <div data-testid="approvals-count" style={{
            fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
          }}>
            {state ? `${state.approvals.count} request+decision rows` : "loading…"}
          </div>
          {state && state.approvals.count === 0 ? (
            <EmptyState anchor="Doc 15" kind="approvals" />
          ) : null}
          {state && state.approvals.count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {state.approvals.entries.slice(0, 40).map((e, i) => (
                <EntryRow key={`${e.record_id}-${i}`} entry={e}
                  extra={e.kind ? `kind: ${e.kind}` : ""} />
              ))}
            </ul>
          ) : null}
        </Panel>
      </div>
    </div>
  );
}
