import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * SkillFiles.jsx — W11 B · CP4 · Doc 18 A18.7 provenance surface.
 *
 * Doc 18 §A18.7 verbatim (Wave B grounding brief):
 *   "every skill's provenance chain traces back to the training run
 *    that produced its adapter (extends Doc14-016 rights-lineage +
 *    Doc14-017 version-history)."
 *
 * Doc 18 §A18.4 verbatim (grounding brief):
 *   "Below the floor is a refusal, never a degraded answer."
 *
 * Data source: GET /api/skill-files/state.
 * Every rendered row cites its on-disk record identifiers (skill_id,
 * adapter_id, training_run_id, moac_card_id, recipe_version); no raw
 * signing material crosses the response boundary. Empty stores render
 * an honest sentence naming the canon anchor. REFERENCE-NOT-COPY.
 *
 * NO provisioning happens from this surface. Provisioning is a
 * POST /api/skill-files/{skill_id}/provenance triggered by the
 * trainer runner at CP8 close (Doc 18 §A18.5 registry admission).
 * This surface's job is to make the provenance chain legible after
 * the fact, per Doc 18 A18.4 ("refusal, never a degraded answer") —
 * the surface refuses to lie about empty state.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette · matched to Training / Governance / Watch / GreyMirror.
const paper = "#f5f2ea";
const surface = "#ffffff";
const ink = "#1b1f27";
const ink2 = "#3a3f4a";
const ink3 = "#7a7f8a";
const line = "#e4dccf";
const blue = "#16274a";
const sage = "#1d7a6e";
const brass = "#b08d2e";
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
    <p data-testid="skill-files-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
      No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
    </p>
  );
}

function ChainCrumbs({ chain }) {
  const kindLabel = {
    base_model: "base model",
    training_run: "training run",
    moac_admission: "MOAC admission",
    skill_provision: "skill provision",
  };
  return (
    <ol data-testid="skill-file-chain" style={{
      margin: "8px 0 0 0", paddingLeft: 20, color: ink2, fontSize: 13,
    }}>
      {chain.map((step, i) => (
        <li key={step.step_id || i} data-testid={`chain-step-${step.kind}`}
            style={{ marginBottom: 4 }}>
          <span style={{ letterSpacing: 1.2, fontSize: 11, color: sage, textTransform: "uppercase" }}>
            {kindLabel[step.kind] || step.kind}
          </span>
          <span style={{ margin: "0 6px", color: ink3 }}>·</span>
          <span style={{ color: ink }}>{step.label}</span>
          <span style={{ marginLeft: 8, color: ink3, fontSize: 11 }}>
            {step.at}
          </span>
          {step.artifact_ref && (
            <span data-testid="chain-step-artifact"
                  style={{ marginLeft: 8, color: brass, fontSize: 11, fontFamily: "ui-monospace, monospace" }}>
              artifact: {step.artifact_ref}
            </span>
          )}
        </li>
      ))}
    </ol>
  );
}

export default function SkillFiles() {
  const [state, setState] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/skill-files/state`)
      .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
      .then((body) => setState(body))
      .catch((e) => setErr(String(e)));
  }, []);

  return (
    <div data-testid="skill-files-page" style={{
      minHeight: "100vh", background: paper, padding: "48px 40px", fontFamily: "ui-sans-serif",
    }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · SKILL FILES</div>
        <h1 style={{ fontFamily: head, fontSize: 40, margin: "10px 0 6px 0", color: blue }}>
          Provenance chain register
        </h1>
        <p data-testid="skill-files-doc-anchor"
           style={{ color: ink2, maxWidth: 720, lineHeight: 1.55, margin: "0 0 26px 0" }}>
          Doc 18 §A18.7 · every skill's provenance chain traces back to the training run
          that produced its adapter, extending Doc14-016 rights-lineage and Doc14-017
          version-history. Below the floor is a refusal (A18.4), never a degraded answer.
        </p>

        {err && (
          <Panel data-testid="skill-files-error" title="Surface unreachable" anchor="A18.4">
            <p style={{ color: "#8a2a44" }}>Backend refused this request: {err}</p>
          </Panel>
        )}

        <Panel data-testid="skill-files-state-panel"
               title="Skill files on record"
               anchor="Doc 18 §A18.7 · Wave B CP4">
          {!state && !err && (
            <p style={{ color: ink3, fontStyle: "italic" }}>Loading state…</p>
          )}
          {state && state.count === 0 && (
            <>
              <EmptyState anchor="Doc 18 §A18.7" kind="provisioned skills" />
              <p style={{ color: ink3, fontSize: 12, marginTop: 8 }}>
                Ship-state: {state.ship_state}. The seat is empty by design — CP5
                fills the recipe seat via the Muon two-arm optimizer protocol
                (Doc 17 §A17.5–A17.6), and CP8's trainer runner writes the first
                provenance row on close. No pre-population by convention.
              </p>
            </>
          )}
          {state && state.count > 0 && (
            <div data-testid="skill-files-list">
              <p style={{ color: ink3, fontSize: 12, marginBottom: 12 }}>
                {state.count} skill{state.count === 1 ? "" : "s"} on record ·
                ship_state = {state.ship_state}.
              </p>
              {state.skills.map((s) => (
                <article key={s.skill_id}
                         data-testid={`skill-file-row-${s.skill_id}`}
                         style={{
                           borderTop: `1px solid ${line}`, padding: "14px 0",
                         }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                    <h3 style={{ fontFamily: head, fontSize: 16, color: ink, margin: 0 }}>
                      {s.skill_id}
                    </h3>
                    <span style={{ fontSize: 11, color: ink3 }}>
                      provisioned {s.provisioned_at}
                    </span>
                  </div>
                  <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
                    adapter <code data-testid="skill-adapter-id">{s.adapter_id}</code> ·
                    training run <code>{s.training_run_id}</code> ·
                    MOAC card <code>{s.moac_card_id}</code> ·
                    recipe <code data-testid="skill-recipe-version">{s.recipe_version}</code>
                  </div>
                  <ChainCrumbs chain={s.chain} />
                </article>
              ))}
            </div>
          )}
        </Panel>

        <div style={{ marginTop: 32, fontSize: 12, color: ink3 }}>
          <Link to="/" style={{ color: blue }} data-testid="skill-files-back">← Registry</Link>
          <span style={{ margin: "0 10px" }}>·</span>
          <Link to="/training" style={{ color: blue }} data-testid="skill-files-training">Training →</Link>
        </div>
      </div>
    </div>
  );
}
