import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * Training.jsx — W11 CP3 · Multidimensional Training Engine surface.
 *
 * Doc 17 · Incremental Training & Capacity + Owner-approved CP3 slice:
 *   1. Demand Table panel  (§4.1 · admissibility + §3.5 · E = B + I).
 *   2. Capacity Ledger panel (§4.2 · empty-at-ship · provenance day-one).
 *   3. Test-set Seal panel (A17.11 · live-verify FIRST · honest hold).
 *
 * Data source: GET /api/training/state. Every row cites its on-disk
 * artifact by objective_id / seal_id (REFERENCE-NOT-COPY · Design
 * Law A8). Empty stores render an honest sentence citing the canon
 * anchor. Refusals (stale verification, link_working=false, no record)
 * are surfaced verbatim; the seal never lies about hold-state.
 *
 * NO trainer run fires from this surface. Sampling & Reflection remains
 * unbuilt; CP8 will bring the trainer runner. This surface's job is to
 * let the Owner see the Demand-Table + Capacity-Ledger + Test-set-Seal
 * ceremony end to end on real DigiCow strata BEFORE any GPU-hours are
 * spent (per Owner directive at W11 open).
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette · matched to Governance/Watch/GreyMirror.
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

function DemandTableRow({ table }) {
  return (
    <li style={{ borderBottom: `1px dotted ${line}`, padding: "10px 0" }}>
      <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}
           data-testid="demand-table-objective-id">
        {table.objective_id}
      </div>
      <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
        compiled {table.compiled_at} · {table.schemes_count} scheme{table.schemes_count === 1 ? "" : "s"}
        {" "}· {table.strata_count} stratum row{table.strata_count === 1 ? "" : "s"}
      </div>
      {table.schemes && table.schemes.length > 0 && (
        <details style={{ marginTop: 8 }}>
          <summary style={{ cursor: "pointer", fontSize: 12, color: ink2 }}>
            Named-failure list (admissibility rule · §4.1)
          </summary>
          <ul style={{ margin: "6px 0 0 20px", padding: 0 }}>
            {table.schemes.map((s, i) => (
              <li key={i} style={{ fontSize: 12, color: ink, marginBottom: 4 }}>
                <span style={{ fontFamily: "ui-monospace, monospace", color: blue }}>{s.id}</span>
                {" — "}
                <span style={{ color: ink2 }}>{s.named_failure}</span>
              </li>
            ))}
          </ul>
        </details>
      )}
      {table.per_stratum && table.per_stratum.length > 0 && (
        <table data-testid="demand-table-strata" style={{
          marginTop: 10, borderCollapse: "collapse", fontSize: 12, color: ink2,
        }}>
          <thead>
            <tr style={{ background: paper }}>
              <th style={{ padding: "4px 12px", textAlign: "left" }}>stratum</th>
              <th style={{ padding: "4px 12px", textAlign: "right" }}>B</th>
              <th style={{ padding: "4px 12px", textAlign: "right" }}>I</th>
              <th style={{ padding: "4px 12px", textAlign: "right" }}>E</th>
            </tr>
          </thead>
          <tbody>
            {table.per_stratum.map((r, i) => (
              <tr key={i}>
                <td style={{ padding: "4px 12px", fontFamily: "ui-monospace, monospace" }}>
                  {r.stratum_id}
                </td>
                <td style={{ padding: "4px 12px", textAlign: "right" }}>{r.B}</td>
                <td style={{ padding: "4px 12px", textAlign: "right", color: r.I ? oxblood : ink2 }}>
                  {r.I}
                </td>
                <td style={{ padding: "4px 12px", textAlign: "right", color: brass, fontWeight: 600 }}>
                  {r.E}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </li>
  );
}

function CapacityRow({ row }) {
  return (
    <li style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
      <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
        {row.scheme_id} <span style={{ color: ink3 }}>· {row.stratum}</span>
      </div>
      <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>
        level {row.level.toFixed(3)} · state {row.state}
        {" · "}
        {row.provenance_count} commission{row.provenance_count === 1 ? "" : "s"}
      </div>
    </li>
  );
}

function SealRow({ seal }) {
  return (
    <li style={{ borderBottom: `1px dotted ${line}`, padding: "10px 0" }}>
      <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 12, color: blue }}
           data-testid="test-set-seal-id">
        {seal.seal_id}
      </div>
      <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
        objective {seal.objective_id} · table {seal.target_table} · sample_size {seal.sample_size}
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 4, fontFamily: "ui-monospace, monospace" }}>
        manifest_sha256: {seal.manifest_sha256 && seal.manifest_sha256.slice(0, 24)}…
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
        sealed {seal.sealed_at} · rds link verified at {seal.rds_link_verified_at}
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
        strata: {(seal.strata || []).join(", ") || "(none named)"}
      </div>
    </li>
  );
}

export default function Training() {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let alive = true;
    fetch(`${BACKEND_URL}/api/training/state`, { credentials: "include" })
      .then(r => (r.ok ? r.json() : Promise.reject(r.statusText)))
      .then(body => { if (alive) setState(body); })
      .catch(e => { if (alive) setError(String(e)); });
    return () => { alive = false; };
  }, []);

  return (
    <div data-testid="training-surface" style={{
      minHeight: "100vh", background: paper, padding: "40px 32px",
      fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif", color: ink,
    }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3, marginBottom: 6 }}>
          AKKI · TRAINING PLANE · W11 CP3
        </div>
        <h1 style={{ fontFamily: head, fontSize: 40, margin: "0 0 6px 0", color: blue }}>
          The Training Plane
        </h1>
        <p style={{ color: ink2, marginTop: 0, marginBottom: 30, maxWidth: 720, lineHeight: 1.5 }}>
          Doc 17 · Multidimensional Training Engine + Incremental Training & Capacity
          module. Demand travels with the objective. Capacity stays with the trainer.
          Test-sets precede training. Nothing on this surface fires a training run —
          the trainer runner lands at CP8, gated on the SSH key.
        </p>

        <nav style={{ marginBottom: 22, fontSize: 12, color: ink3 }}>
          <Link to="/" style={{ color: blue, marginRight: 12 }}>Registry</Link>·
          <Link to="/governance" style={{ color: blue, margin: "0 12px" }}>Governance</Link>·
          <Link to="/watch" style={{ color: blue, margin: "0 12px" }}>Watch</Link>·
          <Link to="/grey-mirror" style={{ color: blue, margin: "0 12px" }}>Grey Mirror</Link>·
          <span style={{ color: brass, marginLeft: 12 }}>Training (you are here)</span>
        </nav>

        {error && (
          <div data-testid="training-load-error" style={{
            background: "#fff6f6", border: `1px solid ${oxblood}`, color: oxblood,
            padding: "12px 16px", marginBottom: 20, fontFamily: "ui-monospace, monospace",
            fontSize: 12,
          }}>
            /api/training/state unreachable: {error}
          </div>
        )}

        {state && (
          <>
            <div data-testid="training-ship-state" style={{
              fontSize: 12, color: state.ship_state === "empty" ? ink3 : sage,
              marginBottom: 20, fontFamily: "ui-monospace, monospace",
            }}>
              ship_state: {state.ship_state}
            </div>

            <Panel dt="training-demand-tables-panel" title="Demand Tables"
                   anchor="Doc 17 §4.1 · admissibility · E = B + I">
              {state.demand_tables.length === 0
                ? <EmptyState anchor="Doc 17 §4.1" kind="compiled demand tables" />
                : (
                  <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                    {state.demand_tables.map((t, i) => <DemandTableRow key={i} table={t} />)}
                  </ul>
                )}
            </Panel>

            <Panel dt="training-capacity-panel" title="Capacity Ledger"
                   anchor="Doc 17 §4.2 · empty-at-ship · provenance day-one">
              <div data-testid="capacity-row-count" style={{
                fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 8,
              }}>
                {state.capacity_ledger_rows} row{state.capacity_ledger_rows === 1 ? "" : "s"}
              </div>
              {state.capacity_ledger_rows === 0
                ? <EmptyState anchor="Doc 17 §4.2" kind="capacity rows" />
                : (
                  <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                    {state.capacity_ledger.map((r, i) => <CapacityRow key={i} row={r} />)}
                  </ul>
                )}
              <p style={{ fontSize: 11, color: ink3, marginTop: 12, fontStyle: "italic" }}>
                Deprioritized at CP3 open: marginal-gain writer and forecasting.
                Rows appear here as calibration probes execute (CP8).
              </p>
            </Panel>

            <Panel dt="training-seals-panel" title="Test-set Seals"
                   anchor="Doc 17 A17.11 · test-set-precedes-training">
              {state.test_set_seals.length === 0
                ? <EmptyState anchor="Doc 17 A17.11" kind="test-set seals" />
                : (
                  <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                    {state.test_set_seals.map((s, i) => <SealRow key={i} seal={s} />)}
                  </ul>
                )}
              <p style={{ fontSize: 11, color: ink3, marginTop: 12, fontStyle: "italic" }}>
                Sealing refuses honestly when the on-disk data_connection_record is
                stale (older than 24h), link_working=false, or missing. The seal
                references a freshly verified live probe — never a stale cache.
              </p>
            </Panel>

            <div data-testid="training-reference-note" style={{
              fontSize: 11, color: ink3, borderTop: `1px solid ${line}`,
              marginTop: 30, paddingTop: 12, lineHeight: 1.5,
            }}>
              {state.reference_note}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
