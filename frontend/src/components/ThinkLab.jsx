import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";

/**
 * ThinkLab.jsx — Doc 05 Northena · direction/scope + ThinkLab surfaces.
 *
 * Owner Order 2026-08-25 · "W4 go" · v7 oracle fabric EXACT per T1.
 *
 * Four destinations under the thinklab group:
 *   - /thinklab              landing (mode tiles + Outputs)
 *   - /thinklab/clarity      Seek clarity
 *   - /thinklab/strategy     Develop strategy
 *   - /thinklab/hypothesis   Simulate a hypothesis
 *   - /thinklab/perspective  Get perspectives
 *
 * Mode registry, LANDING_TIPS, TL_STAGE_LABELS, TL_OUTPUTS, and the
 * dormant-state sentence come from GET /api/thinklab/config —
 * REFERENCE-NOT-COPY: this file does not bake the copy inline.
 *
 * Direction capture is LIVE and admits into Northena via
 * POST /api/thinklab/admit. On admission the frozen artifact renders
 * with its judgement_provenance (Solva-boundary stub annotated
 * honestly) and the 5-stage strip (Frame -> Name -> Challenge ->
 * Weigh -> Lock-in) as navigation ONLY; the body carries the
 * dormant-state sentence because the reasoning faculty (Solver)
 * lands in a later wave. No fake LLM responses. No canned reasoning.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens (paper / ink / blue / sage / oxblood / brass) —
// extracted verbatim from prototype.html :root vars.
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


export default function ThinkLab() {
  const { mode } = useParams();
  if (mode) return <ThinkLabMode modeKey={mode} />;
  return <ThinkLabLanding />;
}


function ThinkLabLanding() {
  const [config, setConfig] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let alive = true;
    fetch(`${BACKEND_URL}/api/thinklab/config`)
      .then(r => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
      .then(j => { if (alive) setConfig(j); })
      .catch(e => { if (alive) setErr(String(e.message || e)); });
    return () => { alive = false; };
  }, []);

  return (
    <div data-testid="thinklab-surface"
         style={{ minHeight: "100vh", background: paper, padding: "48px 56px",
                  fontFamily: 'ui-sans-serif, "Söhne", system-ui, sans-serif',
                  color: ink }}>
      <div style={{ maxWidth: 1120, margin: "0 auto" }}>

        {/* Breadcrumb */}
        <div style={{ display: "flex", alignItems: "center", gap: 8,
                      fontSize: 11, letterSpacing: 1.5, color: ink3,
                      textTransform: "uppercase", marginBottom: 6 }}>
          <Link to="/" style={{ color: ink3, textDecoration: "none" }}>Estate</Link>
          <span>·</span>
          <span style={{ color: ink }}>ThinkLab</span>
        </div>

        <h1 style={{ fontFamily: head, fontSize: 44, margin: "12px 0 6px",
                     color: blue, letterSpacing: -0.2 }}>
          ThinkLab
        </h1>
        <p style={{ fontSize: 15, color: ink2, lineHeight: 1.6,
                    maxWidth: 720, margin: "8px 0 32px" }}>
          Four ways to think through a governed session. Choose the shape of
          the work you are about to do.
        </p>

        {err && (
          <div style={{ padding: "10px 14px", background: "#f7ecea",
                        borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
                        marginBottom: 20, fontSize: 12, color: oxblood }}>
            ThinkLab configuration could not be read: {err}
          </div>
        )}

        {config && (
          <>
            <div style={{ display: "grid",
                          gridTemplateColumns: "repeat(2, 1fr)",
                          gap: 20 }}>
              {(config.modes || []).map((m) => (
                <ModeTile key={m.key} mode={m} tips={config.landing_tips?.[m.key] || []} />
              ))}
            </div>

            <h2 data-testid="thinklab-outputs"
                style={{ fontFamily: head, fontSize: 20, marginTop: 44,
                         marginBottom: 12, color: blue }}>
              What every session produces
            </h2>
            <ul style={{ paddingLeft: 22, color: ink2, fontSize: 13.5,
                         lineHeight: 1.7 }}>
              {(config.outputs || []).map(o => <li key={o}>{o}</li>)}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}


function ModeTile({ mode, tips }) {
  // Explicit testid map — the tests file-scan for each literal.
  const testidByKey = {
    clarity: "thinklab-mode-tile-clarity",
    strategy: "thinklab-mode-tile-strategy",
    hypothesis: "thinklab-mode-tile-hypothesis",
    perspective: "thinklab-mode-tile-perspective",
  };
  const testid = testidByKey[mode.key] || `thinklab-mode-tile-${mode.key}`;
  return (
    <Link data-testid={testid}
          to={`/thinklab/${mode.key}`}
          style={{ display: "block", background: surface,
                   border: `1px solid ${line}`, borderRadius: 12,
                   padding: "22px 24px", textDecoration: "none",
                   color: ink, transition: "border-color 120ms" }}
          onMouseEnter={(e) => e.currentTarget.style.borderColor = sage}
          onMouseLeave={(e) => e.currentTarget.style.borderColor = line}>
      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "baseline", marginBottom: 6 }}>
        <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
                       fontSize: 11, color: brass, letterSpacing: 1.5 }}>
          {mode.num}
        </span>
        <span style={{ fontSize: 10, color: ink3, letterSpacing: 1 }}>
          {mode.duration}
        </span>
      </div>
      <div style={{ fontFamily: head, fontSize: 22, color: blue,
                    marginBottom: 6 }}>
        {mode.title}
      </div>
      <div style={{ fontSize: 13, color: ink2, lineHeight: 1.55,
                    marginBottom: tips?.length ? 12 : 0 }}>
        {mode.objective}
      </div>
      {tips.map((t, i) => (
        <div key={i} style={{ fontSize: 11.5, color: ink3, fontStyle: "italic",
                              lineHeight: 1.55, marginTop: 4 }}>
          {t}
        </div>
      ))}
    </Link>
  );
}


function ThinkLabMode({ modeKey }) {
  const nav = useNavigate();
  const [config, setConfig] = useState(null);
  const [direction, setDirection] = useState("");
  const [scopeText, setScopeText] = useState("registry.estate.audit");
  const [lawfulBasis, setLawfulBasis] = useState("declared_purpose:thinklab_session");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/thinklab/config`)
      .then(r => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
      .then(setConfig)
      .catch(e => setErr(String(e.message || e)));
  }, []);

  const mode = config?.modes?.find(m => m.key === modeKey);

  const submitAdmit = async () => {
    setBusy(true);
    setErr(null);
    setResult(null);
    try {
      const r = await fetch(`${BACKEND_URL}/api/thinklab/admit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mode: modeKey,
          artifact_id: `tl-${modeKey}-${Date.now()}`,
          scope: scopeText.split(/[\n,]/).map(s => s.trim()).filter(Boolean),
          lawful_basis: lawfulBasis,
          direction_statement: direction,
          commissioner: "operator@estate",
        }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j.detail || `HTTP ${r.status}`);
      setResult(j);
    } catch (e) {
      setErr(String(e.message || e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div data-testid="thinklab-surface"
         style={{ minHeight: "100vh", background: paper, padding: "40px 56px",
                  fontFamily: 'ui-sans-serif, "Söhne", system-ui, sans-serif',
                  color: ink }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>

        {/* Breadcrumb */}
        <div style={{ display: "flex", alignItems: "center", gap: 8,
                      fontSize: 11, letterSpacing: 1.5, color: ink3,
                      textTransform: "uppercase", marginBottom: 6 }}>
          <Link to="/" style={{ color: ink3, textDecoration: "none" }}>Estate</Link>
          <span>·</span>
          <Link to="/thinklab" style={{ color: ink3, textDecoration: "none" }}>ThinkLab</Link>
          <span>·</span>
          <span style={{ color: ink }}>{modeKey}</span>
        </div>

        {mode && (
          <div data-testid="thinklab-mode-entry"
               style={{ marginBottom: 32 }}>
            <div style={{ display: "flex", justifyContent: "space-between",
                          alignItems: "baseline", marginBottom: 4 }}>
              <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
                             fontSize: 11, color: brass, letterSpacing: 1.5 }}>
                {mode.num}
              </span>
              <span style={{ fontSize: 10, color: ink3, letterSpacing: 1 }}>
                {mode.duration}
              </span>
            </div>
            <h1 style={{ fontFamily: head, fontSize: 36, color: blue,
                         margin: "4px 0 8px" }}>
              {mode.title}
            </h1>
            <p style={{ fontSize: 14, color: ink2, lineHeight: 1.6,
                        maxWidth: 720 }}>
              {mode.objective}
            </p>
          </div>
        )}

        {/* Stage strip */}
        <StageStrip labels={config?.stage_labels || []} activeIdx={result?.decision === "admitted" ? 0 : -1} />

        {err && (
          <div style={{ padding: "10px 14px", background: "#f7ecea",
                        borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
                        margin: "16px 0", fontSize: 12, color: oxblood }}>
            {err}
          </div>
        )}

        {!result && (
          <DirectionCaptureForm
            direction={direction}    setDirection={setDirection}
            scopeText={scopeText}    setScopeText={setScopeText}
            lawfulBasis={lawfulBasis} setLawfulBasis={setLawfulBasis}
            onSubmit={submitAdmit}
            busy={busy}
          />
        )}

        {result && result.decision === "refused" && (
          <RefusalCard reason={result.reason} row={result.ledger_row} onRetry={() => setResult(null)} />
        )}

        {result && result.decision === "admitted" && (
          <>
            <FrozenArtifactCard artifact={result.frozen_artifact} row={result.ledger_row} />
            <ReasoningDormantPanel dormantSentence={config?.reasoning_dormant_state} />
          </>
        )}

      </div>
    </div>
  );
}


function StageStrip({ labels, activeIdx = -1 }) {
  return (
    <div data-testid="thinklab-stage-strip"
         style={{ display: "flex", gap: 6, alignItems: "center",
                  padding: "10px 0", borderTop: `1px solid ${line}`,
                  borderBottom: `1px solid ${line}` }}>
      {labels.map((label, i) => (
        <React.Fragment key={label}>
          <div style={{
            padding: "6px 12px",
            fontSize: 12,
            fontWeight: 600,
            color: i === activeIdx ? sage : ink3,
            background: i === activeIdx ? surface2 : "transparent",
            borderRadius: 4,
            fontFamily: "ui-monospace, Menlo, monospace",
            letterSpacing: 0.3,
          }}>{label}</div>
          {i < labels.length - 1 && (
            <div style={{ fontSize: 11, color: ink3 }}>·</div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}


function DirectionCaptureForm({ direction, setDirection, scopeText, setScopeText,
                                lawfulBasis, setLawfulBasis, onSubmit, busy }) {
  return (
    <div style={{ marginTop: 20, padding: "22px 24px", background: surface,
                  border: `1px solid ${line}`, borderRadius: 10 }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
                    textTransform: "uppercase", fontWeight: 600,
                    marginBottom: 12 }}>
        Direction & scope
      </div>

      <label style={{ display: "block", marginBottom: 12 }}>
        <div style={{ fontSize: 11, color: ink3, marginBottom: 4 }}>
          What are you thinking through?
        </div>
        <textarea data-testid="thinklab-direction-input"
                  value={direction}
                  onChange={(e) => setDirection(e.target.value)}
                  rows={3}
                  placeholder="State the question, the decision, or the hypothesis in plain language."
                  style={{ width: "100%", padding: "10px 12px",
                           fontSize: 13, border: `1px solid ${line}`,
                           borderRadius: 5, background: surface, color: ink,
                           fontFamily: "inherit", resize: "vertical" }} />
      </label>

      <label style={{ display: "block", marginBottom: 12 }}>
        <div style={{ fontSize: 11, color: ink3, marginBottom: 4 }}>
          Scope (comma or newline separated; strict set-membership at Gate)
        </div>
        <input data-testid="thinklab-scope-input"
               value={scopeText}
               onChange={(e) => setScopeText(e.target.value)}
               style={{ width: "100%", padding: "8px 12px", fontSize: 13,
                        border: `1px solid ${line}`, borderRadius: 5,
                        background: surface, color: ink,
                        fontFamily: "ui-monospace, Menlo, monospace" }} />
      </label>

      <label style={{ display: "block", marginBottom: 16 }}>
        <div style={{ fontSize: 11, color: ink3, marginBottom: 4 }}>
          Lawful basis (declared purpose)
        </div>
        <input data-testid="thinklab-lawful-basis-input"
               value={lawfulBasis}
               onChange={(e) => setLawfulBasis(e.target.value)}
               style={{ width: "100%", padding: "8px 12px", fontSize: 13,
                        border: `1px solid ${line}`, borderRadius: 5,
                        background: surface, color: ink,
                        fontFamily: "ui-monospace, Menlo, monospace" }} />
      </label>

      <button data-testid="thinklab-admit-button"
              onClick={onSubmit}
              disabled={busy || !direction.trim() || !lawfulBasis.trim()}
              style={{ padding: "10px 18px", background: sage,
                       color: surface, border: "none", borderRadius: 6,
                       cursor: "pointer", fontSize: 13, fontWeight: 600,
                       opacity: (busy || !direction.trim() || !lawfulBasis.trim()) ? 0.6 : 1 }}>
        {busy ? "Admitting…" : "Admit & freeze objective"}
      </button>

      <div style={{ fontSize: 11, color: ink3, marginTop: 10,
                    fontStyle: "italic", lineHeight: 1.55 }}>
        A changed intent is a new admission — the objective is frozen once
        the run starts.
      </div>
    </div>
  );
}


function FrozenArtifactCard({ artifact, row }) {
  const prov = artifact?.judgement_provenance || {};
  return (
    <div data-testid="thinklab-admit-result"
         style={{ marginTop: 20, padding: "22px 24px", background: surface,
                  borderLeft: `3px solid ${sage}`, borderRadius: 6,
                  border: `1px solid ${line}` }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: sage,
                    textTransform: "uppercase", fontWeight: 700 }}>
        Admitted · frozen
      </div>
      <div data-testid="thinklab-frozen-artifact"
           style={{ marginTop: 12 }}>
        <Row label="run_id"     value={artifact?.run_id} />
        <Row label="trace_id"   value={artifact?.trace_id} />
        <Row label="lawful basis" value={artifact?.lawful_basis} />
        <Row label="scope" value={(artifact?.scope || []).join(" · ")} />
        <Row label="defensibility floor"
             value={`${artifact?.defensibility_floor} (${prov.defensibility_floor})`} />
        <Row label="preservation depth"
             value={`${artifact?.preservation_depth} (${prov.preservation_depth})`} />
        <Row label="frozen at" value={artifact?.frozen_at_iso} />
        <Row label="ledger row" value={row?.row_id} />
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 12,
                    fontStyle: "italic", lineHeight: 1.55 }}>
        Solva-assisted judgement pending — the fields marked
        <code style={{ background: surface2, padding: "1px 4px", margin: "0 3px",
                       borderRadius: 3 }}>stub_awaiting_solva</code>
        will resolve through the depth governor when it lands.
      </div>
    </div>
  );
}


function Row({ label, value }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "180px 1fr",
                  fontSize: 12, padding: "4px 0", color: ink }}>
      <div style={{ letterSpacing: 0.5, color: ink3 }}>{label}</div>
      <div style={{ fontFamily: "ui-monospace, Menlo, monospace",
                    wordBreak: "break-all" }}>
        {value || "—"}
      </div>
    </div>
  );
}


function ReasoningDormantPanel({ dormantSentence }) {
  return (
    <div data-testid="thinklab-reasoning-dormant"
         style={{ marginTop: 20, padding: "18px 22px", background: surface2,
                  borderLeft: `3px solid ${brass}`, borderRadius: 6 }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: brass,
                    textTransform: "uppercase", fontWeight: 700,
                    marginBottom: 6 }}>
        Reasoning — dormant
      </div>
      <div style={{ fontSize: 13, color: ink, lineHeight: 1.6 }}>
        {dormantSentence || "The reasoning faculty is not yet in force."}
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 8,
                    fontStyle: "italic", lineHeight: 1.55 }}>
        The five stages above (Frame → Name → Challenge → Weigh → Lock-in)
        are the shape of the walk. Their body lights up when the Solver
        lands — until then, the direction is captured, the objective is
        admitted and frozen, and the ledger records the admission.
      </div>
    </div>
  );
}


function RefusalCard({ reason, row, onRetry }) {
  return (
    <div data-testid="thinklab-refusal-card"
         style={{ marginTop: 20, padding: "22px 24px", background: surface,
                  borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
                  border: `1px solid ${line}` }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
                    textTransform: "uppercase", fontWeight: 700 }}>
        Refused at Admit
      </div>
      <div style={{ fontSize: 13.5, color: ink, lineHeight: 1.6,
                    marginTop: 8, fontFamily: "ui-monospace, Menlo, monospace",
                    background: "#f7ecea", padding: "10px 12px",
                    borderRadius: 4 }}>
        {reason}
      </div>
      <div style={{ fontSize: 11, color: ink3, marginTop: 8 }}>
        Ledger row: {row?.row_id} · stage: {row?.stage} · at {row?.at || ""}
      </div>
      <button onClick={onRetry}
              style={{ marginTop: 14, padding: "8px 14px",
                       background: "transparent", color: blue,
                       border: `1px solid ${blue}`, borderRadius: 5,
                       cursor: "pointer", fontSize: 12, fontWeight: 600 }}>
        Try again
      </button>
    </div>
  );
}
