import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * Watch.jsx — W10 CP8 · The Watch surface.
 *
 * Composes seven panels sharing REFERENCE-NOT-COPY posture (Design
 * Law A8):
 *   1. Verdicts (Canon 8 §7 · Macho sensor · W9 CP1)
 *   2. Actions (Canon 8 §8 · Mkono responder · W9 CP1)
 *   3. Containments + Reconciliations (Canon 8 §14 + §18 · W9 CP5)
 *   4. Continuity Attestations (Canon 8 §9 · CA1-N5 · W9 CP4)
 *   5. Witness Attestations (Canon 8 §9 · W10 CP5)
 *   6. Tamper Alarms (Canon 8 §9 · W10 CP5)
 *   7. Fitness Summary (Canon 8 §25-§28 · W10 CP3 · demonstrated
 *      firings over observation window · Ruling-1 precondition (b)
 *      demonstrated status)
 *
 * Data source: GET /api/watch/state.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

const paper = "#f5f2ea";
const surface = "#ffffff";
const ink = "#1b1f27";
const ink2 = "#3a3f4a";
const ink3 = "#7a7f8a";
const line = "#e4dccf";
const blue = "#16274a";
const sage = "#1d7a6e";
const oxblood = "#8a2a44";
const brass = "#b08d2e";
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';

function Panel({ "data-testid": dt, title, anchor, children }) {
  return (
    <section data-testid={dt} style={{
      background: surface, border: `1px solid ${line}`, padding: "20px 22px",
      marginBottom: 18,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }}>
        <h2 style={{ fontFamily: head, fontSize: 19, color: blue, margin: 0 }}>{title}</h2>
        <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
      </div>
      {children}
    </section>
  );
}

function Count({ "data-testid": dt, n, label }) {
  return (
    <div data-testid={dt} style={{
      fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
    }}>{n === null ? "loading…" : `${n} ${label}`}</div>
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
      <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>{entry.source_path}</div>
    </li>
  );
}

function List({ entries, extraKey }) {
  if (!entries || entries.length === 0) return null;
  return (
    <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
      {entries.slice(0, 40).map((e, i) => (
        <EntryRow key={`${e.record_id}-${i}`} entry={e}
          extra={extraKey ? String(e[extraKey] || "") : ""} />
      ))}
    </ul>
  );
}

export default function Watch() {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${BACKEND_URL}/api/watch/state`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        setState(await r.json());
      } catch (e) {
        setError(String(e));
      }
    })();
  }, []);

  const g = (k) => (state ? state[k] : null);
  const gCount = (k) => (g(k) ? g(k).count : null);

  return (
    <div data-testid="watch-view" style={{
      minHeight: "100vh", background: paper, padding: "40px 48px",
      fontFamily: "ui-sans-serif, system-ui",
    }}>
      <div style={{ maxWidth: 1080, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · THE WATCH</div>
        <h1 data-testid="watch-title" style={{
          fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
        }}>The Watch</h1>
        <p data-testid="watch-reference-note" style={{
          color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 12,
        }}>
          REFERENCE-NOT-COPY (Design Law A8). Every Watch entry cites its
          on-disk source_path; raw signing material never appears on this
          surface (Owner Order 2026-08-25 §4). Anchors: Canon 8 §7 (verdicts) ·
          Canon 8 §8 (actions) · Canon 8 §9 (witness) · Canon 8 §14 (containments) ·
          Canon 8 §25 (fitness).
        </p>
        <p style={{ color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 18 }}>
          Ruling-1 precondition (b) — Watch reconciler demonstrated firing —
          {state && state.fitness && state.fitness.ruling_1_precondition_b_demonstrated
            ? <span style={{ color: sage }}> DEMONSTRATED (see phase0/drill_receipts/ruling_1_drill_witness_note.md).</span>
            : <span style={{ color: oxblood }}> not yet on record.</span>}
        </p>

        <nav style={{ marginBottom: 24, fontSize: 13 }}>
          <Link data-testid="nav-to-governance" to="/governance" style={{ color: blue, marginRight: 20 }}>
            → Governance
          </Link>
          <Link data-testid="nav-to-grey-mirror" to="/grey-mirror" style={{ color: blue, marginRight: 20 }}>
            → Grey Mirror
          </Link>
          <Link to="/" style={{ color: ink3 }}>← Registry</Link>
        </nav>

        {error ? (
          <div style={{ color: oxblood, marginBottom: 12 }}>Failed to load: {error}</div>
        ) : null}

        <Panel data-testid="watch-fitness-summary"
               title="Fitness Summary"
               anchor="Canon 8 §25-§28 · W10 CP3">
          {state && state.fitness ? (
            <div style={{ fontSize: 13, color: ink2, lineHeight: 1.7 }}>
              Verdicts over window: <strong>{state.fitness.verdicts_over_window}</strong> ·
              Actions over window: <strong>{state.fitness.actions_over_window}</strong> ·
              Drill green receipts on record: <strong>{state.fitness.drill_green_receipts_on_record}</strong> ·
              Ruling-1 precondition (b) demonstrated:{" "}
              <strong>{String(state.fitness.ruling_1_precondition_b_demonstrated)}</strong>
            </div>
          ) : "loading…"}
        </Panel>

        <Panel data-testid="watch-verdicts-panel" title="Verdicts" anchor="Canon 8 §7 · Macho">
          <Count data-testid="watch-verdicts-count" n={gCount("verdicts")} label="verdicts" />
          {gCount("verdicts") === 0 ? <EmptyState anchor="Canon 8 §7" kind="verdicts" /> : null}
          <List entries={g("verdicts") ? g("verdicts").entries : []} extraKey="verdict_kind" />
        </Panel>

        <Panel data-testid="watch-actions-panel" title="Actions" anchor="Canon 8 §8 · Mkono">
          <Count data-testid="watch-actions-count" n={gCount("actions")} label="actions" />
          {gCount("actions") === 0 ? <EmptyState anchor="Canon 8 §8" kind="actions" /> : null}
          <List entries={g("actions") ? g("actions").entries : []} extraKey="action_class" />
        </Panel>

        <Panel data-testid="watch-containments-panel"
               title="Containments"
               anchor="Canon 8 §14 · §17 expiry · §18 reconciliation · W9 CP5">
          <Count data-testid="watch-containments-count" n={gCount("containments")} label="containments" />
          {gCount("containments") === 0 ? <EmptyState anchor="Canon 8 §14" kind="containments" /> : null}
          <List entries={g("containments") ? g("containments").entries : []} />
        </Panel>

        <Panel data-testid="watch-witness-panel"
               title="Witness Attestations"
               anchor="Canon 8 §9 · W10 CP5">
          <Count data-testid="watch-witness-attestations-count" n={gCount("witness_attestations")} label="attestations" />
          {gCount("witness_attestations") === 0 ? <EmptyState anchor="Canon 8 §9" kind="witness attestations" /> : null}
          <List entries={g("witness_attestations") ? g("witness_attestations").entries : []} />
        </Panel>

        <Panel data-testid="watch-tamper-alarms-panel"
               title="Tamper Alarms"
               anchor="Canon 8 §9 · W10 CP5">
          <Count data-testid="watch-tamper-alarms-count" n={gCount("tamper_alarms")} label="alarms" />
          {gCount("tamper_alarms") === 0 ? <EmptyState anchor="Canon 8 §9" kind="tamper alarms" /> : null}
          <List entries={g("tamper_alarms") ? g("tamper_alarms").entries : []} />
        </Panel>
      </div>
    </div>
  );
}
