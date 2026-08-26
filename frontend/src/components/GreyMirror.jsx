import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * GreyMirror.jsx — W10 CP8 · Grey Mirror surface.
 *
 * Composes three panels sharing REFERENCE-NOT-COPY posture (Design
 * Law A8):
 *   1. Mirages (Canon 8 §15 · installed lures)
 *   2. Mirage Touches (Canon 8 §15 · touch_kind CONTRACT-TIME closed
 *      to {'innocent_read', 'guilty_use'} per R2 · 2026-08-26T04:20Z)
 *   3. Severances (Canon 8 §16 · outcome for guilty_use touches)
 *
 * BUILD-not-LIFT rationale: Executive-Core carries no mirage-machinery
 * material (verified at W10 CP2 grounding brief §4). The whole Grey
 * Mirror stack was built fresh from Canon 8 §§15-16 verbatim.
 *
 * Data source: GET /api/grey_mirror/state.
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

const TOUCH_KINDS = ["innocent_read", "guilty_use"];

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

function Count({ "data-testid": dt, n, label }) {
  return (
    <div data-testid={dt} style={{
      fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
    }}>{n === null ? "loading…" : `${n} ${label}`}</div>
  );
}

function EmptyState({ anchor, kind, mechanismStatus }) {
  // W11 R7 · Watch/Grey-Mirror honesty. Grey Mirror is Wave-C-target
  // BUILD material across all three panels (planting · touch detection ·
  // severance). Explicit unbuilt copy per owner directive 2026-08-26.
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

export default function GreyMirror() {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${BACKEND_URL}/api/grey_mirror/state`);
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
    <div data-testid="grey-mirror-view" style={{
      minHeight: "100vh", background: paper, padding: "40px 48px",
      fontFamily: "ui-sans-serif, system-ui",
    }}>
      <div style={{ maxWidth: 1080, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · GREY MIRROR</div>
        <h1 data-testid="grey-mirror-title" style={{
          fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
        }}>Grey Mirror</h1>
        <p data-testid="grey-mirror-reference-note" style={{
          color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 12,
        }}>
          REFERENCE-NOT-COPY (Design Law A8). Grey Mirror is a BUILD
          (not LIFT · Executive-Core carries no mirage-machinery
          material · verified W10 CP2 grounding). Anchors: Canon 8 §15
          (mirages · touches) · Canon 8 §16 (severances). Every entry
          cites its on-disk source_path.
        </p>
        <p style={{ color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 18 }}>
          touch_kind grammar is CONTRACT-TIME closed to <code>{TOUCH_KINDS.join(", ")}</code>
          {" "}per R2 ratification (2026-08-26T04:20Z · no service-time extensibility).
          An <code>innocent_read</code> is a bookkeeping event; a <code>guilty_use</code>
          {" "}is the trigger for a severance (§16).
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
          <div style={{ color: oxblood, marginBottom: 12 }}>Failed to load: {error}</div>
        ) : null}

        <Panel data-testid="mirages-panel" title="Mirages" anchor="Canon 8 §15 · installed lures">
          <Count data-testid="mirages-count" n={gCount("mirages")} label="mirages" />
          {gCount("mirages") === 0 ? (
            <EmptyState anchor="Canon 8 §15" kind="mirages" />
          ) : null}
          {g("mirages") && g("mirages").count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {g("mirages").entries.slice(0, 40).map((e, i) => (
                <EntryRow key={`${e.record_id}-${i}`} entry={e}
                  extra={e.lure_class ? `lure: ${e.lure_class}` : ""} />
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="mirage-touches-panel"
               title="Mirage Touches"
               anchor="Canon 8 §15 · touch_kind CONTRACT-TIME (R2)">
          <Count data-testid="mirage-touches-count" n={gCount("touches")} label="touches" />
          {gCount("touches") === 0 ? (
            <EmptyState anchor="Canon 8 §15" kind="mirage touches" />
          ) : null}
          {g("touches") && g("touches").count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {g("touches").entries.slice(0, 40).map((e, i) => (
                <EntryRow key={`${e.record_id}-${i}`} entry={e}
                  extra={
                    e.touch_kind
                      ? `kind: ${e.touch_kind}${e.touch_kind === "guilty_use" ? " ← triggers severance (§16)" : ""}`
                      : ""
                  } />
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="severances-panel" title="Severances" anchor="Canon 8 §16">
          <Count data-testid="severances-count" n={gCount("severances")} label="severances" />
          {gCount("severances") === 0 ? (
            <EmptyState anchor="Canon 8 §16" kind="severances" />
          ) : null}
          {g("severances") && g("severances").count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {g("severances").entries.slice(0, 40).map((e, i) => (
                <EntryRow key={`${e.record_id}-${i}`} entry={e}
                  extra={e.cites_touch_id ? `cites touch: ${e.cites_touch_id}` : ""} />
              ))}
            </ul>
          ) : null}
        </Panel>

        <Panel data-testid="mirage-artifacts-panel"
               title="Mirage Artifacts (§Line 183 isolated store)"
               anchor="Canon 8 §Line 136 · §Line 183 · CP-C3">
          <Count data-testid="mirage-artifacts-count" n={gCount("mirage_artifacts")} label="mirage artifacts" />
          {gCount("mirage_artifacts") === 0 ? (
            <EmptyState anchor="Canon 8 §Line 183" kind="mirage artifacts" />
          ) : null}
          {g("mirage_artifacts") && g("mirage_artifacts").count > 0 ? (
            <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
              {g("mirage_artifacts").entries.slice(0, 40).map((e, i) => {
                const parts = [];
                if (e.mirage_session_id) parts.push(`session: ${e.mirage_session_id}`);
                if (typeof e.is_synthetic !== "undefined") parts.push(`synthetic: ${String(e.is_synthetic)}`);
                if (e.production_store_leak_check) parts.push(`leak_check: ${e.production_store_leak_check}`);
                return <EntryRow key={`${e.record_id}-${i}`} entry={e} extra={parts.join(" · ")} />;
              })}
            </ul>
          ) : null}
        </Panel>
      </div>
    </div>
  );
}
