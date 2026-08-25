import React, { useEffect, useState } from "react";

/**
 * DataShield.jsx — Data Shield surface (Trust Center group → Data Shield).
 *
 * Owner Order 2026-08-25 · "W3 go" · Doc 01 (chokepoint · receipt · custody
 * sequence) + Doc 02 (confidentiality · dual-file · CA1-007 dry-run) +
 * CA1-N4 (residency).
 *
 * v7 oracle fabric — extracted verbatim from
 *   fixtures/RMS_AI_Akki_Prototype_v7_Standalone.html at offset 334300-337500
 * (the `isTrustDataShield` block). Landing header, session-timeline card
 * shape, session-headline pattern, sage/paper/ink palette reproduced.
 *
 * REFERENCE-NOT-COPY: every crossing card references a receipt IDENTITY
 * (rcp-<hex>); no receipt content is baked into the DOM. The dry-run
 * preview walks the receipt log by identity and reports would_catch_refs /
 * would_miss_refs — never the receipts' payload content.
 *
 * No fabrication: the session headline renders the honest count from
 * /api/shield/receipts; when no row-bearing crossing exists yet the
 * dry-run's honest_gap sentence is displayed verbatim.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens — extracted verbatim from prototype.html :root vars.
const paper = "#f5f2ea";     // --paper
const surface = "#ffffff";   // --surface
const surface2 = "#f0ebe1";  // --surface2
const ink = "#1b1f27";       // --ink
const ink2 = "#3a3f4a";      // --ink2
const ink3 = "#7a7f8a";      // --ink3
const line = "#e4dccf";      // --line
const blue = "#16274a";      // --blue
const sage = "#1d7a6e";      // --sage
const oxblood = "#8a2a44";   // --oxblood
const oxblood2 = "#b8395b";  // --oxblood2
const brass = "#b08d2e";     // --brass
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';

export default function DataShield() {
  const [receipts, setReceipts] = useState(null);
  const [receiptCount, setReceiptCount] = useState(0);
  const [allowlists, setAllowlists] = useState(null);
  const [loadError, setLoadError] = useState(null);

  useEffect(() => {
    let alive = true;
    const load = async () => {
      try {
        const [r1, r2] = await Promise.all([
          fetch(`${BACKEND_URL}/api/shield/receipts?limit=50`),
          fetch(`${BACKEND_URL}/api/shield/allowlists`),
        ]);
        if (!r1.ok) throw new Error(`receipts HTTP ${r1.status}`);
        if (!r2.ok) throw new Error(`allowlists HTTP ${r2.status}`);
        const [b1, b2] = await Promise.all([r1.json(), r2.json()]);
        if (!alive) return;
        setReceipts(b1.receipts || []);
        setReceiptCount(b1.count || 0);
        setAllowlists(b2);
      } catch (e) {
        if (!alive) return;
        setLoadError(String(e.message || e));
      }
    };
    load();
    return () => { alive = false; };
  }, []);

  return (
    <div data-testid="data-shield-surface"
         style={{ minHeight: "100vh", background: paper, padding: "40px 48px",
                  fontFamily: 'ui-sans-serif, "Söhne", system-ui, sans-serif',
                  color: ink }}>
      <div style={{ maxWidth: 1080, margin: "0 auto" }}>

        {/* Breadcrumb: Trust Center group → Data Shield */}
        <div style={{ display: "flex", alignItems: "center", gap: 8,
                      fontSize: 11, letterSpacing: 1.5, color: ink3,
                      textTransform: "uppercase", marginBottom: 6 }}>
          <a href="/" style={{ color: ink3, textDecoration: "none" }}>Estate</a>
          <span>·</span>
          <span>Trust Center</span>
          <span>·</span>
          <span style={{ color: ink }}>Data Shield</span>
        </div>

        <h1 style={{ fontFamily: head, fontSize: 42, margin: "12px 0 4px",
                     color: blue, letterSpacing: -0.2 }}>
          Data Shield
        </h1>

        <p style={{ fontSize: 14, color: ink2, lineHeight: 1.65,
                    maxWidth: 620, margin: "8px 0 24px" }}>
          Every governed model call is shielded and receipted. The per-message
          pattern lives inline in Chat, on each answer. The full record for a
          session is here.
        </p>

        {loadError && (
          <div style={{ padding: "10px 14px", background: "#f7ecea",
                        borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
                        marginBottom: 20, fontSize: 12, color: oxblood }}>
            The shield log could not be read: {loadError}. This is work done,
            not work lost — try again in a moment.
          </div>
        )}

        {/* Session headline — honest count from /api/shield/receipts */}
        <div data-testid="data-shield-session-headline"
             style={{ fontSize: 13.5, color: ink, fontWeight: 600,
                      background: surface2, padding: "12px 16px",
                      borderRadius: 8, marginBottom: 24, maxWidth: 620 }}>
          {receiptCount} governed calls this session · zero raw content crossed the seam.
        </div>

        {/* Two-column grid: Session timeline / Rules in force + dry-run */}
        <div style={{ display: "grid",
                      gridTemplateColumns: "1fr 380px",
                      gap: 32 }}>

          {/* LEFT: session timeline (crossing-receipt log) */}
          <SessionTimeline receipts={receipts} />

          {/* RIGHT: rules in force + dry-run + refusal example */}
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            <RulesInForce allowlists={allowlists} />
            <DryRunPanel />
            <RefusalExample />
          </div>
        </div>

      </div>
    </div>
  );
}

function SessionTimeline({ receipts }) {
  return (
    <div data-testid="data-shield-timeline"
         style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                    textTransform: "uppercase", fontWeight: 600 }}>
        Session timeline
      </div>

      {receipts === null && (
        <div style={{ fontSize: 12, color: ink3 }}>Reading the log…</div>
      )}

      {receipts !== null && receipts.length === 0 && (
        <div data-testid="data-shield-timeline-empty"
             style={{ padding: "18px 20px", border: `1px solid ${line}`,
                      borderRadius: 9, background: surface, fontSize: 12.5,
                      color: ink2, lineHeight: 1.55 }}>
          No governed crossings have been made yet. Every outbound call
          transits the chokepoint — this list will populate as the estate's
          real crossings run.
        </div>
      )}

      {receipts !== null && receipts.map((rc) => (
        <div key={rc.receipt_id} data-testid="data-shield-receipt-row"
             style={{ border: `1px solid ${line}`, borderRadius: 9,
                      padding: "14px 16px", background: surface }}>
          <div style={{ display: "flex", justifyContent: "space-between",
                        marginBottom: 6, alignItems: "baseline" }}>
            <span style={{ fontSize: 13, fontWeight: 600, color: ink }}>
              {crossingLabel(rc.kind)}
            </span>
            <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
                           fontSize: 10.5, color: ink3 }}>
              {rc.receipt_id}
            </span>
          </div>
          <div style={{ fontSize: 12, color: ink3, marginBottom: 10 }}>
            {rc.verb} · {rc.endpoint_host}
          </div>
          <div style={{ display: "flex", gap: 18, flexWrap: "wrap" }}>
            <Field label="RESIDENCY" value={rc.residency_region} tone={sage} />
            <Field label="MASKING TIER" value={rc.masking_tier} tone={brass} />
            <Field label="ACTOR" value={rc.actor} tone={ink2} />
            <Field label="AT" value={formatIso(rc.at_iso)} tone={ink3} />
          </div>
          {/* W5 · LLM metering line for reasoning/chat crossings */}
          {isReasoningKind(rc.kind) && rc.payload_shape && (
            <div data-testid="data-shield-llm-metering"
                 style={{ marginTop: 10, paddingTop: 10,
                          borderTop: `1px dashed ${line}`,
                          display: "flex", gap: 18, flexWrap: "wrap",
                          fontSize: 11, color: ink3,
                          fontFamily: "ui-monospace, Menlo, monospace" }}>
              <span>model · <b style={{ color: ink }}>{rc.payload_shape.model_id || "—"}</b></span>
              <span>provider · <b style={{ color: ink }}>{rc.payload_shape.provider || "—"}</b></span>
              <span>tokens_in · <b style={{ color: ink }}>{rc.payload_shape.tokens_in ?? "—"}</b></span>
              <span>tokens_out · <b style={{ color: ink }}>{rc.payload_shape.tokens_out ?? "—"}</b></span>
              <span>latency_ms · <b style={{ color: ink }}>{rc.payload_shape.latency_ms ?? "—"}</b></span>
              <span style={{ color: ink3, fontStyle: "italic" }}>
                metering_source · {rc.payload_shape.metering_source || "unavailable"}
              </span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}


function isReasoningKind(kind) {
  if (!kind) return false;
  return kind.startsWith("solva_") || kind.startsWith("chat_") ||
         kind.startsWith("thinklab_") || kind.startsWith("llm_");
}


function crossingLabel(kind) {
  if (kind === "rds_data_api") return "Data API crossing";
  if (kind === "ssh_seam") return "Compute seam crossing";
  if (kind === "governance_read") return "Governance read";
  if (kind === "llm_synthesis") return "Model synthesis";
  // W5 kinds:
  if (kind === "chat_governed_answer") return "Chat · governed answer";
  if (kind === "solva_frame_audit") return "Solva · frame audit";
  if (kind === "solva_candidate_generation") return "Solva · candidate generation";
  if (kind === "solva_synthesis") return "Solva · synthesis";
  if (kind === "thinklab_direct_answer") return "ThinkLab · direct answer";
  if (kind === "llm_connect_verify") return "LLM · connect verify";
  return kind || "Crossing";
}

function formatIso(iso) {
  if (!iso) return "";
  // Show as YYYY-MM-DD · HH:MM (UTC) — v7 mono-caption style.
  const m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/);
  return m ? `${m[1]} · ${m[2]}Z` : iso;
}

function Field({ label, value, tone }) {
  return (
    <div>
      <div style={{ fontSize: 10, letterSpacing: 1.2, color: ink3,
                    textTransform: "uppercase", marginBottom: 2 }}>
        {label}
      </div>
      <div style={{ fontFamily: head, fontSize: 14, color: tone || ink }}>
        {value || "—"}
      </div>
    </div>
  );
}

function RulesInForce({ allowlists }) {
  if (!allowlists) return (
    <div data-testid="data-shield-rules-in-force"
         style={{ border: `1px solid ${line}`, borderRadius: 9,
                  padding: "18px 20px", background: surface,
                  fontSize: 12, color: ink3 }}>
      Reading the rules in force…
    </div>
  );
  const admissible = (allowlists.masking_tiers || []).filter(
    t => (t.admissible_under_env || []).length > 0
  );
  const declared_only = (allowlists.masking_tiers || []).filter(
    t => (t.admissible_under_env || []).length === 0
  );
  return (
    <div data-testid="data-shield-rules-in-force"
         style={{ border: `1px solid ${line}`, borderRadius: 9,
                  padding: "18px 20px", background: surface }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                    textTransform: "uppercase", fontWeight: 600,
                    marginBottom: 12 }}>
        Rules in force
      </div>

      <div style={{ marginBottom: 14 }}>
        <div style={{ fontSize: 10.5, letterSpacing: 0.5, color: ink2,
                      marginBottom: 6, fontWeight: 600 }}>
          Masking tiers admissible today
        </div>
        {admissible.map(t => (
          <div key={t.tier} data-testid="data-shield-masking-tier-row"
               style={{ fontSize: 12, color: ink2, marginBottom: 6,
                        paddingBottom: 6, borderBottom: `1px dashed ${line}` }}>
            <div style={{ fontFamily: head, color: sage, fontWeight: 600 }}>
              {t.tier}
            </div>
            <div style={{ fontSize: 11, color: ink3, lineHeight: 1.5 }}>
              {t.description}
            </div>
          </div>
        ))}

        {declared_only.length > 0 && (
          <>
            <div style={{ fontSize: 10.5, letterSpacing: 0.5, color: ink2,
                          marginTop: 12, marginBottom: 6, fontWeight: 600 }}>
              Declared but not yet admissible
            </div>
            {declared_only.map(t => (
              <div key={t.tier} data-testid="data-shield-masking-tier-row"
                   style={{ fontSize: 12, color: ink2, marginBottom: 6,
                            paddingBottom: 6, borderBottom: `1px dashed ${line}` }}>
                <div style={{ fontFamily: head, color: brass, fontWeight: 600 }}>
                  {t.tier}
                </div>
                <div style={{ fontSize: 11, color: ink3, lineHeight: 1.5 }}>
                  {t.description}
                </div>
                {t.not_admissible_because && (
                  <div style={{ fontSize: 10.5, color: oxblood, marginTop: 3,
                                fontStyle: "italic" }}>
                    {t.not_admissible_because}
                  </div>
                )}
              </div>
            ))}
          </>
        )}
      </div>

      <div>
        <div style={{ fontSize: 10.5, letterSpacing: 0.5, color: ink2,
                      marginBottom: 6, fontWeight: 600 }}>
          Residency
        </div>
        {(allowlists.residency?.allowlisted_regions || []).map(r => (
          <div key={r} data-testid="data-shield-residency-region-row"
               style={{ fontSize: 12, color: ink2, padding: "3px 0" }}>
            <span style={{ fontFamily: head, color: sage, fontWeight: 600 }}>
              {r}
            </span>
            <span style={{ color: ink3, marginLeft: 8 }}>· on the allowlist</span>
          </div>
        ))}
        <div data-testid="data-shield-residency-honest-gap"
             style={{ fontSize: 11, color: ink3, lineHeight: 1.55,
                      marginTop: 8, fontStyle: "italic" }}>
          {allowlists.residency?.note}
        </div>
      </div>
    </div>
  );
}

function DryRunPanel() {
  const [kind, setKind] = useState("pattern");
  const [inputValue, setInputValue] = useState("SELECT.*information_schema");
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const run = async () => {
    setRunning(true);
    setError(null);
    setResult(null);
    try {
      const body = { candidate_declaration: buildCandidate(kind, inputValue) };
      const r = await fetch(`${BACKEND_URL}/api/shield/dry-run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const j = await r.json();
      if (!r.ok) {
        setError(j.detail || `HTTP ${r.status}`);
      } else {
        setResult(j);
      }
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setRunning(false);
    }
  };

  return (
    <div data-testid="data-shield-dry-run-panel"
         style={{ border: `1px solid ${line}`, borderRadius: 9,
                  padding: "18px 20px", background: surface }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                    textTransform: "uppercase", fontWeight: 600,
                    marginBottom: 6 }}>
        Dry-run preview
      </div>
      <div style={{ fontSize: 12, color: ink2, lineHeight: 1.55,
                    marginBottom: 12 }}>
        Preview what a confidentiality declaration would catch against the
        crossing-receipt log, before adopting it.
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 8,
                    marginBottom: 10 }}>
        <label style={{ fontSize: 11, color: ink3 }}>
          Declaration kind
          <select data-testid="data-shield-dry-run-kind-select"
                  value={kind}
                  onChange={(e) => setKind(e.target.value)}
                  style={{ display: "block", marginTop: 4, padding: "6px 8px",
                           fontSize: 12, border: `1px solid ${line}`,
                           borderRadius: 5, width: "100%",
                           background: surface, color: ink }}>
            <option value="exact_value">Exact value</option>
            <option value="pattern">Pattern (regex)</option>
            <option value="category">Category</option>
          </select>
        </label>
        <label style={{ fontSize: 11, color: ink3 }}>
          {kind === "pattern" ? "Regex" : kind === "category" ? "Category name" : "Value"}
          <input data-testid="data-shield-dry-run-input"
                 value={inputValue}
                 onChange={(e) => setInputValue(e.target.value)}
                 style={{ display: "block", marginTop: 4, padding: "6px 8px",
                          fontSize: 12, border: `1px solid ${line}`,
                          borderRadius: 5, width: "100%",
                          background: surface, color: ink,
                          fontFamily: "ui-monospace, Menlo, monospace" }} />
        </label>
      </div>

      <button data-testid="data-shield-dry-run-run"
              onClick={run}
              disabled={running || !inputValue.trim()}
              style={{ padding: "8px 14px", background: blue,
                       color: surface, border: "none", borderRadius: 6,
                       cursor: "pointer", fontSize: 12, fontWeight: 600,
                       opacity: (running || !inputValue.trim()) ? 0.6 : 1 }}>
        {running ? "Previewing…" : "Preview against receipts"}
      </button>

      {error && (
        <div style={{ marginTop: 12, fontSize: 12, color: oxblood,
                      background: "#f7ecea", padding: "8px 12px",
                      borderRadius: 6, borderLeft: `2px solid ${oxblood2}` }}>
          {error}
        </div>
      )}

      {result && (
        <div data-testid="data-shield-dry-run-result"
             style={{ marginTop: 14, paddingTop: 12,
                      borderTop: `1px solid ${line}` }}>
          <div style={{ fontSize: 11, color: ink3, marginBottom: 6 }}>
            Preview <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
                                    color: ink2 }}>{result.preview_id}</span>
            <span> · {result.sample_size} receipts walked</span>
          </div>
          <div style={{ display: "flex", gap: 20, marginBottom: 10 }}>
            <div>
              <div style={{ fontSize: 10, letterSpacing: 1.2, color: ink3 }}>
                WOULD CATCH
              </div>
              <div style={{ fontFamily: head, fontSize: 20, color: sage }}>
                {result.would_catch_refs.length}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 10, letterSpacing: 1.2, color: ink3 }}>
                WOULD MISS
              </div>
              <div style={{ fontFamily: head, fontSize: 20, color: ink2 }}>
                {result.would_miss_refs.length}
              </div>
            </div>
          </div>
          {/* REFERENCE-NOT-COPY: render the caught refs as identity chips */}
          {result.would_catch_refs.length > 0 && (
            <div style={{ fontSize: 11, color: ink3, marginBottom: 8,
                          lineHeight: 1.55 }}>
              First matches (by identity):{" "}
              {result.would_catch_refs.slice(0, 3).map(id => (
                <span key={id}
                      style={{ fontFamily: "ui-monospace, Menlo, monospace",
                               background: surface2, padding: "1px 5px",
                               borderRadius: 3, marginRight: 4,
                               color: ink2 }}>
                  {id}
                </span>
              ))}
            </div>
          )}
          {result.honest_gap && (
            <div style={{ fontSize: 11.5, color: ink2, lineHeight: 1.55,
                          fontStyle: "italic", borderLeft: `2px solid ${brass}`,
                          paddingLeft: 10, marginTop: 8 }}>
              {result.honest_gap}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function buildCandidate(kind, value) {
  if (kind === "exact_value") return { kind, value };
  if (kind === "pattern") return { kind, regex: value };
  return { kind, category: value };
}

function RefusalExample() {
  // Doc 01 §A5.5 · closed outbound network except at crossing. The example
  // renders the actual refusal grammar the chokepoint would produce for an
  // out-of-allowlist region — a governed teaching pattern, not a fabricated
  // event. If a real refusal has ever fired, it will appear here in future
  // waves; today the estate has zero real refusals on record (drawn-not-
  // blank posture).
  return (
    <div data-testid="data-shield-refusal-example"
         style={{ border: `1px solid ${line}`, borderRadius: 9,
                  padding: "18px 20px", background: surface }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                    textTransform: "uppercase", fontWeight: 600,
                    marginBottom: 6 }}>
        What a refused crossing looks like
      </div>
      <div style={{ fontSize: 12, color: ink2, lineHeight: 1.55,
                    marginBottom: 10 }}>
        The chokepoint refuses at the endpoint, not at a UI button. The
        refusal carries a plain sentence naming what would have gone wrong.
      </div>
      <div style={{ fontSize: 11.5, color: ink2, lineHeight: 1.55,
                    background: "#f7ecea", borderLeft: `2px solid ${oxblood2}`,
                    padding: "10px 12px", borderRadius: 6,
                    fontFamily: "ui-monospace, Menlo, monospace" }}>
        residency_refused — region_off_allowlist — 'us-east-1' not admissible
        for this estate. Allowlisted regions on record: ['eu-west-1'].
        Adding a region requires an Owner ruling (CA1-N4 · residency).
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 8, fontStyle: "italic",
                    lineHeight: 1.55 }}>
        No real refusals are on record yet — every crossing since the
        chokepoint landed has been residency-clean.
      </div>
    </div>
  );
}
