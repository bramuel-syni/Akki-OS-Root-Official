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

function EmptyState({ anchor, kind, mechanismStatus }) {
  // W11 R7 · Watch/Grey-Mirror honesty. If `mechanismStatus` is
  // "unbuilt", surface the honest state explicitly rather than "no X on
  // record" (which reads as "wired mechanism happens to be empty").
  if (mechanismStatus && mechanismStatus.startsWith("unbuilt")) {
    return (
      <p data-testid={`empty-unbuilt-${kind.replace(/\s+/g, "-")}`}
         style={{ color: oxblood, fontStyle: "italic", margin: "6px 0 0 0" }}>
        mechanism not yet built — {mechanismStatus} · Canon anchor: {anchor}.
      </p>
    );
  }
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

// W11 C CP-C2 · render both MachoVerdict (verdict_class + intensity +
// sever_certainty_signal_id) and legacy WatchVerdictRow_v0
// (signal_class + severity). Doc 8 §Line 30 verbatim closed grammar
// surfaced in-place.
function verdictExtra(e) {
  if (e.verdict_class) {
    const parts = [`class: ${e.verdict_class}`];
    if (e.verdict_class === "externally_steerable" && e.intensity) {
      parts.push(`intensity: ${e.intensity}`);
    }
    if (e.sever_certainty_signal_id) {
      parts.push(`sever_certainty_signal: ${e.sever_certainty_signal_id}`);
    }
    return parts.join(" · ");
  }
  if (e.signal_class) {
    return `signal_class: ${e.signal_class}${e.severity ? ` · severity: ${e.severity}` : ""}`;
  }
  return "";
}

// W11 C CP-C2 · render both WatchActionV0 (four-class ladder +
// ttl_seconds + reversible + sever_certainty_signal_id) and legacy
// WatchActionRecord_v0 (7-verb grammar). Doc 8 §Line 99 verbatim.
function actionExtra(e) {
  if (typeof e.reversible !== "undefined" || typeof e.ttl_seconds !== "undefined") {
    const parts = [`class: ${e.action_class}`];
    if (e.ttl_seconds !== null && typeof e.ttl_seconds !== "undefined") {
      parts.push(`ttl: ${e.ttl_seconds}s`);
    }
    if (typeof e.reversible !== "undefined") {
      parts.push(`reversible: ${String(e.reversible)}`);
    }
    if (e.sever_certainty_signal_id) {
      parts.push(`sever_certainty_signal: ${e.sever_certainty_signal_id}`);
    }
    return parts.join(" · ");
  }
  return e.action_class ? `class: ${e.action_class}` : "";
}

// W11 C CP-C3 · render MirageArtifactV0 rows honestly with the
// §Line 183 isolation invariants surfaced.
function mirageArtifactExtra(e) {
  const parts = [];
  if (e.mirage_session_id) parts.push(`session: ${e.mirage_session_id}`);
  if (typeof e.is_synthetic !== "undefined") parts.push(`synthetic: ${String(e.is_synthetic)}`);
  if (e.production_store_leak_check) parts.push(`leak_check: ${e.production_store_leak_check}`);
  if (typeof e.outward_lie_only !== "undefined") parts.push(`outward_lie_only: ${String(e.outward_lie_only)}`);
  return parts.join(" · ");
}

// W11 C CP-C3 · render MarkV0 dye-pack rows binding all six
// dimensions of §Line 127 verbatim.
function markExtra(e) {
  const parts = [];
  if (e.identity) parts.push(`identity: ${e.identity}`);
  if (e.credentials) parts.push(`cred: ${e.credentials}`);
  if (e.session_id) parts.push(`sess: ${e.session_id}`);
  if (e.device_fingerprint) parts.push(`device: ${e.device_fingerprint}`);
  if (e.behavioural_signature) parts.push(`bh: ${e.behavioural_signature}`);
  if (e.content_hashes && e.content_hashes.length) parts.push(`hashes: ${e.content_hashes.length}`);
  return parts.join(" · ");
}

// W11 C CP-C4 · surface subject_kind + attested_hash for
// witness attestations (§Line 170 sentence 1 discipline).
function witnessAttestationExtra(e) {
  const parts = [];
  if (e.subject_kind) parts.push(`subject_kind: ${e.subject_kind}`);
  if (e.subject_ref) parts.push(`ref: ${e.subject_ref}`);
  if (e.attested_hash) {
    const short = e.attested_hash.length > 24
      ? `${e.attested_hash.slice(0, 24)}…`
      : e.attested_hash;
    parts.push(`hash: ${short}`);
  }
  return parts.join(" · ");
}

// W11 C CP-C4 · surface tamper alarm evidence (§Line 170 last
// sentence: 'this one is a measurement').
function tamperAlarmExtra(e) {
  const parts = [];
  if (e.evidence_kind) parts.push(`kind: ${e.evidence_kind}`);
  if (e.evidence_ref) parts.push(`ref: ${e.evidence_ref}`);
  return parts.join(" · ");
}

function List({ entries, extraFn, extraKey }) {
  if (!entries || entries.length === 0) return null;
  return (
    <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
      {entries.slice(0, 40).map((e, i) => (
        <EntryRow key={`${e.record_id}-${i}`} entry={e}
          extra={extraFn ? extraFn(e) : (extraKey ? String(e[extraKey] || "") : "")} />
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

        <Panel data-testid="watch-verdicts-panel"
               title="Verdicts (Macho)"
               anchor="Canon 8 §7 · §Line 28 · §Line 30 · §Line 31">
          <Count data-testid="watch-verdicts-count" n={gCount("verdicts")} label="verdicts" />
          {gCount("verdicts") === 0 ? <EmptyState anchor="Canon 8 §Line 28" kind="verdicts" /> : null}
          <List entries={g("verdicts") ? g("verdicts").entries : []} extraFn={verdictExtra} />
        </Panel>

        <Panel data-testid="watch-actions-panel"
               title="Actions (Mkono · four-class ladder)"
               anchor="Canon 8 §8 · §Line 28 · §Line 99">
          <Count data-testid="watch-actions-count" n={gCount("actions")} label="actions" />
          {gCount("actions") === 0 ? <EmptyState anchor="Canon 8 §Line 99" kind="actions" /> : null}
          <List entries={g("actions") ? g("actions").entries : []} extraFn={actionExtra} />
        </Panel>

        <Panel data-testid="watch-mirage-artifacts-panel"
               title="Mirage Artifacts (isolated store)"
               anchor="Canon 8 §Line 136 · §Line 183 · CP-C3">
          <Count data-testid="watch-mirage-artifacts-count" n={gCount("mirage_artifacts")} label="mirage artifacts" />
          {gCount("mirage_artifacts") === 0 ? (
            <EmptyState anchor="Canon 8 §Line 183"
                        kind="mirage artifacts" />
          ) : null}
          <List entries={g("mirage_artifacts") ? g("mirage_artifacts").entries : []}
                extraFn={mirageArtifactExtra} />
        </Panel>

        <Panel data-testid="watch-marks-panel"
               title="Marks (dye pack · minted on conviction)"
               anchor="Canon 8 §Line 127 · CP-C3">
          <Count data-testid="watch-marks-count" n={gCount("marks")} label="marks" />
          {gCount("marks") === 0 ? (
            <EmptyState anchor="Canon 8 §Line 127" kind="marks" />
          ) : null}
          <List entries={g("marks") ? g("marks").entries : []} extraFn={markExtra} />
        </Panel>

        <Panel data-testid="watch-containments-panel"
               title="Containments"
               anchor="Canon 8 §14 · §17 expiry · §18 reconciliation · W9 CP5">
          <Count data-testid="watch-containments-count" n={gCount("containments")} label="containments" />
          {gCount("containments") === 0 ? <EmptyState anchor="Canon 8 §14" kind="containments" /> : null}
          <List entries={g("containments") ? g("containments").entries : []} />
        </Panel>

        <Panel data-testid="watch-witness-panel"
               title="Witness Attestations (§Line 170)"
               anchor="Canon 8 §Line 170 · CP-C4">
          <Count data-testid="watch-witness-attestations-count" n={gCount("witness_attestations")} label="attestations" />
          {gCount("witness_attestations") === 0 ? <EmptyState anchor="Canon 8 §Line 170" kind="witness attestations" /> : null}
          <List entries={g("witness_attestations") ? g("witness_attestations").entries : []}
                extraFn={witnessAttestationExtra} />
        </Panel>

        <Panel data-testid="watch-tamper-alarms-panel"
               title="Tamper Alarms (measurement, not assertion)"
               anchor="Canon 8 §Line 170 last sentence · CP-C4">
          <Count data-testid="watch-tamper-alarms-count" n={gCount("tamper_alarms")} label="alarms" />
          {gCount("tamper_alarms") === 0 ? (
            <EmptyState anchor="Canon 8 §Line 170"
                        kind="tamper alarms" />
          ) : null}
          <List entries={g("tamper_alarms") ? g("tamper_alarms").entries : []}
                extraFn={tamperAlarmExtra} />
        </Panel>
      </div>
    </div>
  );
}
