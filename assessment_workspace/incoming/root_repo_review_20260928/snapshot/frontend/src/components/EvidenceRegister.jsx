import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * EvidenceRegister.jsx — W11 B · CP6 · Doc 19B §19B.4-6 · EP-1/EP-2/EP-3.
 *
 * Doc 19B PROPOSED · never confirmed adopted (Doc 19 §19B.1 verbatim).
 * The register + protocol are load-bearing before the terminal test
 * runs (EP-4 · OPEN ordering constraint · Owner ratification pending).
 *
 * Verbatim surface anchors (canon Doc 19 §19B.5-6):
 *   §19B.6 absolute: "No figure reaches an external document without
 *                     a resolvable register row."
 *   §19B.6:          "A-4 never becomes a gate by drift — its scope
 *                     is validation and re-entry, and staying there
 *                     is a condition of adoption, not a detail."
 *
 * Data sources:
 *   GET /api/evidence-register   → EP-1 register rows (empty at ship)
 *   GET /api/claims-validation   → EP-3 A-4 rows (empty at ship)
 *
 * NO judging fires from this surface. Adding a figure requires an
 * Owner-side dual-judge protocol; this surface renders lineage only.
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
const brass = "#b08d2e";
const oxblood = "#8a2a44";
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';


function Panel({ dt, title, anchor, children }) {
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

function ProposedBadge() {
  return (
    <span data-testid="proposed-status-badge" style={{
      display: "inline-block", padding: "2px 8px", fontSize: 10, letterSpacing: 1.5,
      color: paper, background: brass, borderRadius: 2, marginLeft: 8,
    }}>PROPOSED</span>
  );
}

export default function EvidenceRegister() {
  const [reg, setReg] = useState(null);
  const [claims, setClaims] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/evidence-register`)
      .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
      .then(setReg)
      .catch((e) => setErr(String(e)));
    fetch(`${BACKEND_URL}/api/claims-validation`)
      .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
      .then(setClaims)
      .catch(() => { /* empty ledger is honest default */ });
  }, []);

  return (
    <div data-testid="evidence-register-page" style={{
      minHeight: "100vh", background: paper, padding: "48px 40px",
      fontFamily: "ui-sans-serif",
    }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>
          AKKI · EVIDENCE REGISTER
          <ProposedBadge />
        </div>
        <h1 style={{ fontFamily: head, fontSize: 40, margin: "10px 0 6px 0", color: blue }}>
          Evidence register & claims validation
        </h1>
        <p data-testid="evidence-register-19b6-anchor"
           style={{ color: ink2, maxWidth: 720, lineHeight: 1.55, margin: "0 0 26px 0" }}>
          Doc 19B §19B.6 · "No figure reaches an external document without a
          resolvable register row." The register is PROPOSED (Owner-noted as
          not-yet-canon 2026-08-26); rows carry status_class=PROPOSED until
          ratified.
        </p>

        {err && (
          <Panel dt="evidence-register-error" title="Surface unreachable" anchor="§19B.6">
            <p style={{ color: oxblood }}>Backend refused this request: {err}</p>
          </Panel>
        )}

        <Panel dt="evidence-register-panel"
               title="Evidence register · EP-1"
               anchor="Doc 19B §19B.5 · Wave B CP6">
          {!reg && !err && <p style={{ color: ink3 }}>Loading…</p>}
          {reg && reg.count === 0 && (
            <>
              <p data-testid="evidence-register-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
                No evidence-register row on record. Canon anchor: Doc 19B §19B.5. Drawn, never left blank.
              </p>
              <p style={{ color: ink3, fontSize: 12, marginTop: 8, lineHeight: 1.5 }}>
                {reg.status_class_note}
              </p>
            </>
          )}
          {reg && reg.count > 0 && (
            <div data-testid="evidence-register-list">
              <p style={{ color: ink3, fontSize: 12, marginBottom: 12 }}>
                {reg.count} figure{reg.count === 1 ? "" : "s"} on record.
              </p>
              {reg.rows.map((r) => (
                <article key={r.figure_id} data-testid={`register-row-${r.figure_id}`}
                         style={{ borderTop: `1px solid ${line}`, padding: "12px 0" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                    <h3 style={{ fontFamily: head, fontSize: 15, color: ink, margin: 0 }}>
                      {r.figure_id}
                    </h3>
                    <span style={{ fontSize: 11, color: sage, letterSpacing: 1.2 }}>
                      {r.named_site.toUpperCase()}
                    </span>
                  </div>
                  <div style={{ fontSize: 13, color: ink2, marginTop: 4 }}>
                    figure: <code data-testid="register-figure">{r.figure}</code>
                    {" · κ = "}
                    <code data-testid="register-kappa">{r.kappa}</code>
                    {" · "}{r.date}
                  </div>
                  <div style={{ fontSize: 12, color: ink3, marginTop: 4 }}>
                    method: {r.method}
                  </div>
                  <div style={{ fontSize: 12, color: ink3, marginTop: 2 }}>
                    judges ({r.judges.length}): {r.judges.join(", ")} ·
                    rubric {r.rubric_version} · source_rows: {r.source_rows.join(", ")}
                  </div>
                </article>
              ))}
            </div>
          )}
        </Panel>

        <Panel dt="claims-validation-panel"
               title="Claims validation · EP-3 · A-4"
               anchor="Doc 19B §19B.4 · never a build gate">
          {!claims && !err && <p style={{ color: ink3 }}>Loading…</p>}
          {claims && claims.count === 0 && (
            <>
              <p data-testid="claims-validation-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
                No claims-validation row on record. Canon anchor: Doc 19B §19B.4. Drawn, never left blank.
              </p>
              <p style={{ color: ink3, fontSize: 12, marginTop: 8, lineHeight: 1.5 }}>
                {claims.never_a_gate_note}
              </p>
            </>
          )}
          {claims && claims.count > 0 && (
            <ul data-testid="claims-validation-list" style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {claims.rows.map((c) => (
                <li key={c.claim_id} style={{ borderTop: `1px solid ${line}`, padding: "12px 0" }}>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
                      {c.claim_id}
                    </span>
                    <span style={{ fontSize: 11, letterSpacing: 1.2, color: brass, textTransform: "uppercase" }}>
                      {c.verdict}
                    </span>
                  </div>
                  <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
                    kind {c.claim_kind} · subject {c.subject}
                  </div>
                  <div style={{ fontSize: 12, color: ink3, marginTop: 2 }}>
                    arms: {c.three_arms.join(" · ")}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </Panel>

        <div data-testid="ep5-non-adoption-note" style={{
          background: surface, border: `1px dashed ${line}`,
          padding: "14px 16px", fontSize: 12, color: ink3, lineHeight: 1.55,
        }}>
          <strong>EP-5 · explicit non-adoption.</strong> Doc 19B §19B.5 verbatim:
          "Explicitly not adopted, per the same proposal: the source spec's
          'insurance telemetry' aside (serves a goal never named) and its
          internal reduction-skill mandate." No such services exist on this
          estate. See test_ep5_non_adoption_invariant.py.
        </div>

        <div style={{ marginTop: 30, fontSize: 12, color: ink3 }}>
          <Link to="/" style={{ color: blue }} data-testid="evidence-register-back">← Registry</Link>
          <span style={{ margin: "0 10px" }}>·</span>
          <Link to="/training" style={{ color: blue }} data-testid="evidence-register-training">Training →</Link>
        </div>
      </div>
    </div>
  );
}
