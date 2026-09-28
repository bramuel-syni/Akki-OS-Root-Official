import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * AuditTrail.jsx — Wave F Cleanup · CP · audit-trail Overview surface.
 *
 * Canon rows landed by this surface (verbatim from AKKI CANON —
 * ADDENDUM 1 §1 Confirmed Closures):
 *
 *   #4 · CA1-001 · Doc02-020a — "Closed by the audit trail Overview
 *        stating when an answer drew on 2+ independently-governed units."
 *
 *   #17 · CA1-002 · Doc06-016 — "Closed by the audit trail Overview
 *        stating how many available source units were actually served."
 *
 *   #19/#20/#21 · CA1-003 · Doc07-019 · Doc08-017 — "Closed by a
 *        Registry densification stat and a per-turn warm/fresh tag —
 *        flagged here as a partial closure, not a full one."
 *
 * Data source: GET /api/audit_trail/overview. Every row cites its
 * on-disk source_path (REFERENCE-NOT-COPY · Design Law A8). Empty
 * stores render an honest sentence naming the canon anchor.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens (matched to Governance / Watch / Grey-Mirror).
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

function Panel({ "data-testid": dt, title, anchor, canonQuote, children }) {
  return (
    <section data-testid={dt} style={{
      background: surface, border: `1px solid ${line}`, padding: "22px 24px",
      marginBottom: 20,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
        <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
        <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
      </div>
      {canonQuote ? (
        <blockquote style={{
          margin: "8px 0 12px 0", padding: "8px 12px", borderLeft: `3px solid ${brass}`,
          color: ink2, fontStyle: "italic", fontSize: 13, lineHeight: 1.5,
        }}>
          {canonQuote}
        </blockquote>
      ) : null}
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

export default function AuditTrail() {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${BACKEND_URL}/api/audit_trail/overview`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        setState(await r.json());
      } catch (e) {
        setError(String(e));
      }
    })();
  }, []);

  return (
    <div data-testid="audit-trail-view" style={{
      minHeight: "100vh", background: paper, padding: "40px 48px",
      fontFamily: "ui-sans-serif, system-ui",
    }}>
      <div style={{ maxWidth: 1080, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · AUDIT TRAIL</div>
        <h1 data-testid="audit-trail-title" style={{
          fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
        }}>Audit Trail Overview</h1>
        <p data-testid="audit-trail-reference-note" style={{
          color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 20,
        }}>
          REFERENCE-NOT-COPY (Design Law A8). Every entry cites its
          on-disk source_path; record bodies live under
          <code style={{ margin: "0 4px" }}>phase0/</code> where each
          producer wrote them. Canon anchors: Addendum §1 CA1-001 · CA1-002 ·
          CA1-003 (partial closure).
        </p>

        <nav style={{ marginBottom: 24, fontSize: 13 }}>
          <Link data-testid="nav-to-governance" to="/governance" style={{ color: blue, marginRight: 20 }}>
            → Governance
          </Link>
          <Link data-testid="nav-to-watch" to="/watch" style={{ color: blue, marginRight: 20 }}>
            → The Watch
          </Link>
          <Link to="/" style={{ color: ink3 }}>← Registry</Link>
        </nav>

        {error ? (
          <div style={{ color: oxblood, marginBottom: 12 }}>
            Failed to load audit-trail overview: {error}
          </div>
        ) : null}

        <Panel data-testid="multi-unit-answers-panel"
               title="Multi-Unit Answers"
               anchor="CA1-001 · Doc02-020a · Promise #4"
               canonQuote={state?.multi_unit_answers?.canon_text}>
          <div data-testid="multi-unit-answers-count" style={{
            fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
          }}>
            {state ? `${state.multi_unit_answers.count} answers drew on 2+ independently-governed units` : "loading…"}
          </div>
          {state && state.multi_unit_answers.count === 0 ? (
            <div data-testid="multi-unit-answers-empty-state">
              <EmptyState anchor="Addendum §1 CA1-001"
                          kind="multi-unit answers" />
            </div>
          ) : null}
          {state && state.multi_unit_answers.count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {state.multi_unit_answers.entries.slice(0, 40).map((e) => (
                <li key={e.trace_id} style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
                  <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
                    {e.trace_id}
                  </div>
                  <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>
                    {e.unit_count} units · {e.source_units.join(" · ")}
                  </div>
                  <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
                    {e.source_path}
                  </div>
                </li>
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="units-served-panel"
               title="Units Served"
               anchor="CA1-002 · Doc06-016 · Promise #17"
               canonQuote={state?.units_served?.canon_text}>
          <div data-testid="units-served-count" style={{
            fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
          }}>
            {state
              ? `${state.units_served.served} of ${state.units_served.available} available source units were actually served`
              : "loading…"}
          </div>
          {state && state.units_served.available === 0 ? (
            <div data-testid="units-served-empty-state">
              <EmptyState anchor="Addendum §1 CA1-002"
                          kind="available source units" />
            </div>
          ) : null}
          {state && state.units_served.available > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {state.units_served.entries.slice(0, 40).map((e) => (
                <li key={e.source_id} style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
                  <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
                    {e.source_id}
                  </div>
                  <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>
                    served_receipts: {e.served_receipts}
                  </div>
                  <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
                    {e.source_path}
                  </div>
                </li>
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="densification-panel"
               title="Registry Densification"
               anchor="CA1-003 · Doc07-019 · Doc08-017 · Promises #19/#20/#21"
               canonQuote={state?.densification?.canon_text}>
          <div data-testid="densification-partial-closure-badge" style={{
            display: "inline-block", padding: "2px 8px",
            background: "#f5e3c8", color: oxblood,
            fontSize: 11, letterSpacing: 1, marginBottom: 8,
          }}>
            PARTIAL CLOSURE (canon-designated)
          </div>
          <div data-testid="densification-facts-registered" style={{
            fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
          }}>
            {state ? `${state.densification.facts_registered} facts registered` : "loading…"}
          </div>
          {state ? (
            <p style={{ fontSize: 12, color: ink3, margin: "6px 0" }}>
              Warm/fresh tag wired through by reference: <code>{state.densification.warm_fresh_reference}</code>
            </p>
          ) : null}
        </Panel>
      </div>
    </div>
  );
}
