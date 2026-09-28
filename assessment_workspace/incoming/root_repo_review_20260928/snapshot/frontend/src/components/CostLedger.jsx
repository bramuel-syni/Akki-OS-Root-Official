import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * CostLedger.jsx — W6 CP2b · CA1-008 surface.
 *
 * Owner Ruling 2026-08-25 · W6 GO §W6-SCOPE-(a):
 *   Cost Ledger per the v7 oracle · real figures only.
 *
 * Canon 1 §4.4 · Measure, do not assert.
 * Canon 1 §4.1 · Cost optimisations fail transparent.
 *
 * CA1-008 · the lever sequence itself (cache → route → narrow → cascade
 * → waste_report) rendered as named ordered steps with saving
 * attributable to each — not just the final per-call cost.
 *
 * Rendering discipline:
 *   · Quantities ALWAYS render (they are measured facts).
 *   · Money renders ONLY when the entry carries cost_total !== null.
 *   · When any entry carries honest_gap_note, the surface renders it
 *     verbatim; no fabricated $ figure.
 *   · Levers named-but-not-yet-attributed render as "honest gap" rows
 *     (drawn-not-blank per the standing rule).
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens.
const paper = "#f5f2ea";
const surface = "#ffffff";
const surface2 = "#f0ebe1";
const ink = "#1b1f27";
const ink2 = "#3a3f4a";
const ink3 = "#7a7f8a";
const line = "#e4dccf";
const blue = "#16274a";
const sage = "#1d7a6e";
const oxblood = "#8a2a44";
const oxblood2 = "#b8395b";
const brass = "#b08d2e";
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';


export default function CostLedger() {
  const [summary, setSummary] = useState(null);
  const [entries, setEntries] = useState(null);
  const [rates, setRates] = useState(null);
  const [error, setError] = useState(null);
  const [kindFilter, setKindFilter] = useState("llm");

  useEffect(() => {
    const load = async () => {
      try {
        const [s, e, r] = await Promise.all([
          fetch(`${BACKEND_URL}/api/cost_ledger/summary?kind=${kindFilter}`).then(x => x.json()),
          fetch(`${BACKEND_URL}/api/cost_ledger/entries?kind=${kindFilter}&limit=25`).then(x => x.json()),
          fetch(`${BACKEND_URL}/api/cost_ledger/rates`).then(x => x.json()),
        ]);
        setSummary(s);
        setEntries(e.entries || []);
        setRates(r);
      } catch (exc) {
        setError(String(exc));
      }
    };
    load();
  }, [kindFilter]);

  return (
    <div style={{ minHeight: "100vh", background: paper, padding: "48px 40px",
                  fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3,
                      textTransform: "uppercase" }}>
          AKKI · COST LEDGER · CA1-008
        </div>
        <div style={{ display: "flex", justifyContent: "space-between",
                      alignItems: "baseline" }}>
          <h1 style={{ fontFamily: head, fontSize: 42, margin: "10px 0 8px 0",
                       color: blue }}>
            Every crossing, measured.
          </h1>
          <Link to="/" style={{ color: ink3, fontSize: 12, textDecoration: "none" }}>
            ← Registry
          </Link>
        </div>
        <p style={{ color: ink2, lineHeight: 1.6, fontSize: 14, marginBottom: 24,
                    maxWidth: 720 }}>
          The ledger reads the crossing receipts. Quantities are measured
          facts. Money renders only when a rate is on record — otherwise
          the gap is named, not papered.
        </p>

        {error && (
          <div data-testid="cost-ledger-error"
               style={{ padding: "10px 14px", background: "#f7ecea",
                        borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
                        marginBottom: 20, fontSize: 12, color: oxblood }}>
            The ledger could not be read: {error}. This is work done, not
            work lost — try again in a moment.
          </div>
        )}

        {/* Filter */}
        <div style={{ marginBottom: 20, display: "flex", gap: 10 }}
             data-testid="cost-ledger-filter">
          {["llm", "seam", ""].map(k => (
            <button key={k || "all"}
                    data-testid={`cost-ledger-filter-${k || "all"}`}
                    onClick={() => setKindFilter(k)}
                    style={{
                      padding: "6px 14px", fontSize: 12,
                      background: kindFilter === k ? blue : surface,
                      color: kindFilter === k ? "#fff" : ink,
                      border: `1px solid ${kindFilter === k ? blue : line}`,
                      borderRadius: 4, cursor: "pointer", fontWeight: 600,
                    }}>
              {k === "llm" ? "LLM crossings" : k === "seam" ? "Compute seam" : "All"}
            </button>
          ))}
        </div>

        {/* Summary */}
        {summary && <CostSummary summary={summary} />}

        {/* Rates on record */}
        {rates && <RatesOnRecord rates={rates} />}

        {/* Ledger rows */}
        <div style={{ marginTop: 32 }}>
          <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                        textTransform: "uppercase", fontWeight: 600,
                        marginBottom: 14 }}>
            Ledger · newest first
          </div>
          {entries === null && (
            <div style={{ fontSize: 12, color: ink3 }}>Reading the ledger…</div>
          )}
          {entries !== null && entries.length === 0 && (
            <div data-testid="cost-ledger-empty"
                 style={{ padding: "18px 20px", border: `1px solid ${line}`,
                          borderRadius: 9, background: surface,
                          fontSize: 12.5, color: ink2, lineHeight: 1.55 }}>
              No crossings on record for this filter. As the estate's
              governed calls run, entries land here.
            </div>
          )}
          {entries !== null && entries.map(e => <LedgerRow key={e.receipt_id} entry={e} />)}
        </div>
      </div>
    </div>
  );
}


function CostSummary({ summary }) {
  const currency = summary.currency || "USD";
  return (
    <div data-testid="cost-ledger-summary"
         style={{ padding: "20px 24px", background: surface,
                  border: `1px solid ${line}`, borderRadius: 10,
                  marginBottom: 24 }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
                    gap: 24 }}>
        <SummaryField label="calls" value={summary.total_calls} />
        <SummaryField label="tokens_in"
                      value={summary.total_tokens_in.toLocaleString()} />
        <SummaryField label="tokens_out"
                      value={summary.total_tokens_out.toLocaleString()} />
        <SummaryField label="latency_total"
                      value={`${(summary.total_latency_ms / 1000).toFixed(1)}s`} />
      </div>

      <div style={{ marginTop: 18, paddingTop: 14, borderTop: `1px solid ${line}`,
                    display: "flex", alignItems: "baseline",
                    justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 11, color: ink3, letterSpacing: 1.2,
                        textTransform: "uppercase" }}>
            Cost · this filter
          </div>
          <div style={{ fontSize: 30, fontFamily: head, color: blue,
                        marginTop: 4 }}>
            {summary.total_cost > 0
              ? `${currency === "USD" ? "$" : currency + " "}${summary.total_cost.toFixed(4)}`
              : summary.total_cost_is_partial
                ? <span style={{ fontSize: 15, color: ink3, fontStyle: "italic" }}>Not yet measured</span>
                : <span style={{ fontSize: 15, color: ink3 }}>$0.00</span>}
            {summary.total_cost_is_partial && summary.total_cost > 0 && (
              <span style={{ fontSize: 12, color: oxblood, marginLeft: 10 }}
                    data-testid="cost-partial-marker">
                (partial · lower bound)
              </span>
            )}
          </div>
        </div>
        {summary.gaps_present && (
          <div style={{ maxWidth: 380, fontSize: 11, color: ink3,
                        fontStyle: "italic", textAlign: "right",
                        lineHeight: 1.55 }}
               data-testid="cost-ledger-honest-gap">
            {summary.honest_gap_note}
          </div>
        )}
      </div>

      {/* CA1-008 lever sequence */}
      <LeverSequence levers={summary.levers} currency={currency} />
    </div>
  );
}


function SummaryField({ label, value }) {
  return (
    <div>
      <div style={{ fontSize: 10, color: ink3, letterSpacing: 1.5,
                    textTransform: "uppercase" }}>
        {label}
      </div>
      <div style={{ fontSize: 22, color: ink, fontFamily: head,
                    marginTop: 4 }}>
        {value}
      </div>
    </div>
  );
}


function LeverSequence({ levers, currency }) {
  const order = ["cache", "route", "narrow", "cascade", "waste_report"];
  return (
    <div style={{ marginTop: 20, paddingTop: 16, borderTop: `1px solid ${line}` }}
         data-testid="cost-ledger-levers">
      <div style={{ fontSize: 11, color: ink3, letterSpacing: 1.2,
                    textTransform: "uppercase", marginBottom: 10 }}>
        CA1-008 · savings by lever · in order
      </div>
      <div style={{ display: "grid",
                    gridTemplateColumns: "repeat(5, 1fr)",
                    gap: 12 }}>
        {order.map(name => {
          const l = levers[name] || { saving: 0, attributed_calls: 0 };
          const attributed = l.attributed_calls > 0;
          return (
            <div key={name} data-testid={`cost-lever-${name}`}
                 style={{ padding: "10px 12px", background: surface2,
                          borderLeft: `3px solid ${attributed ? sage : brass}`,
                          borderRadius: 5 }}>
              <div style={{ fontSize: 10, color: ink3, letterSpacing: 1,
                            textTransform: "uppercase", fontWeight: 700 }}>
                {name.replace("_", " ")}
              </div>
              {attributed ? (
                <>
                  <div style={{ fontSize: 16, color: sage, marginTop: 4,
                                fontFamily: head }}>
                    {currency === "USD" ? "$" : currency + " "}
                    {l.saving.toFixed(4)}
                  </div>
                  <div style={{ fontSize: 10, color: ink3, marginTop: 2 }}>
                    {l.attributed_calls} attributed call{l.attributed_calls === 1 ? "" : "s"}
                  </div>
                </>
              ) : (
                <div style={{ fontSize: 11, color: ink3, marginTop: 6,
                              fontStyle: "italic", lineHeight: 1.4 }}>
                  Not yet attributed. Landing as levers become measurable.
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}


function RatesOnRecord({ rates }) {
  const hasModels = rates.models && rates.models.length > 0;
  const hasGpu = rates.gpu_hours && rates.gpu_hours.length > 0;
  return (
    <div data-testid="cost-ledger-rates"
         style={{ marginBottom: 24, padding: "16px 20px", background: surface,
                  border: `1px solid ${line}`, borderRadius: 10 }}>
      <div style={{ fontSize: 11, color: ink3, letterSpacing: 1.5,
                    textTransform: "uppercase", fontWeight: 600,
                    marginBottom: 10 }}>
        Rates on record
      </div>
      {!hasModels && !hasGpu && (
        <div data-testid="rates-honest-gap"
             style={{ fontSize: 12, color: ink3, fontStyle: "italic",
                      lineHeight: 1.55 }}>
          {rates.honest_gap_note || "No rates on record."} 
          Owner-supplied only · never invented.
        </div>
      )}
      {hasModels && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, color: ink3, marginBottom: 6 }}>
            Model rates ({rates.models.length})
          </div>
          {rates.models.map(r => (
            <div key={r.model_id}
                 style={{ fontSize: 12, color: ink, padding: "4px 0",
                          fontFamily: "ui-monospace, Menlo, monospace" }}>
              <b>{r.model_id}</b>{" · "}
              {r.rate_per_million_tokens_in}/M in{" · "}
              {r.rate_per_million_tokens_out}/M out{" · "}
              {r.currency}{" · "}
              <span style={{ color: ink3, fontStyle: "italic" }}>
                {r.source}@{r.authored_at?.substring(0, 10)}
              </span>
            </div>
          ))}
        </div>
      )}
      {hasGpu && (
        <div>
          <div style={{ fontSize: 11, color: ink3, marginBottom: 6 }}>
            GPU-hour rates ({rates.gpu_hours.length})
          </div>
          {rates.gpu_hours.map(r => (
            <div key={r.node_id}
                 style={{ fontSize: 12, color: ink, padding: "4px 0",
                          fontFamily: "ui-monospace, Menlo, monospace" }}>
              <b>{r.node_id}</b>{" · "}{r.rate_per_hour}/hr · {r.currency}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


function LedgerRow({ entry }) {
  const hasCost = entry.cost_total !== null;
  return (
    <div data-testid="cost-ledger-entry"
         style={{ border: `1px solid ${line}`, borderRadius: 9,
                  padding: "14px 16px", background: surface,
                  marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "baseline", marginBottom: 6 }}>
        <div>
          <span style={{ fontSize: 13, fontWeight: 600, color: ink }}>
            {crossingLabel(entry.kind)}
          </span>
          <span style={{ marginLeft: 12, fontSize: 11, color: ink3,
                         fontFamily: "ui-monospace, Menlo, monospace" }}>
            {entry.receipt_id}
          </span>
        </div>
        <div style={{ fontSize: 11, color: ink3,
                      fontFamily: "ui-monospace, Menlo, monospace" }}>
          {formatIso(entry.at_iso)}
        </div>
      </div>

      <div style={{ fontSize: 11, color: ink3, marginBottom: 8,
                    fontFamily: "ui-monospace, Menlo, monospace" }}>
        {entry.model_id && (
          <><b style={{ color: ink }}>{entry.model_id}</b> via {entry.provider}{" · "}</>
        )}
        {entry.purpose_declared || entry.masking_tier}{" · "}
        {entry.actor}
      </div>

      <div style={{ display: "flex", gap: 20, flexWrap: "wrap",
                    fontSize: 11, fontFamily: "ui-monospace, Menlo, monospace",
                    color: ink3 }}>
        <span>tokens_in · <b style={{ color: ink }}>{entry.tokens_in}</b></span>
        <span>tokens_out · <b style={{ color: ink }}>{entry.tokens_out}</b></span>
        <span>latency · <b style={{ color: ink }}>{entry.latency_ms}ms</b></span>
        {entry.gpu_hours > 0 && (
          <span>gpu_hours · <b style={{ color: ink }}>{entry.gpu_hours}</b></span>
        )}
        {hasCost ? (
          <span style={{ color: sage }}>
            cost · <b>{entry.currency === "USD" ? "$" : entry.currency + " "}
                       {entry.cost_total.toFixed(6)}</b>
          </span>
        ) : (
          <span style={{ color: oxblood, fontStyle: "italic" }}
                data-testid="entry-honest-gap">
            cost · not yet measured
          </span>
        )}
      </div>

      {/* Route lever · surfaced on the row when attributed */}
      {entry.levers && entry.levers.some(l => l.name === "route" && l.attributed) && (
        <div style={{ marginTop: 10, padding: "8px 10px", background: surface2,
                      borderLeft: `3px solid ${sage}`, borderRadius: 4,
                      fontSize: 11, color: ink }}
             data-testid="entry-route-lever">
          {entry.levers.find(l => l.name === "route").evidence}
        </div>
      )}
    </div>
  );
}


function crossingLabel(kind) {
  if (kind === "rds_data_api") return "Data API";
  if (kind === "ssh_seam") return "Compute seam";
  if (kind === "chat_governed_answer") return "Chat";
  if (kind === "solva_frame_audit") return "Solva · frame audit";
  if (kind === "solva_candidate_generation") return "Solva · candidates";
  if (kind === "solva_synthesis") return "Solva · synthesis";
  if (kind === "thinklab_direct_answer") return "ThinkLab · direct";
  if (kind === "llm_connect_verify") return "LLM · connect verify";
  return kind || "Crossing";
}


function formatIso(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toISOString().substring(0, 19).replace("T", " ");
  } catch {
    return iso;
  }
}
