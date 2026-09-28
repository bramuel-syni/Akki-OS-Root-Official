import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

/**
 * ModelEcosystem.jsx — W7 CP7 · Docs 13/14 · CA1-004/005/011 surface.
 *
 * Owner Ruling 2026-08-25T23:30Z (W7 GO):
 *   "The Model Admission ceremony renders per the v7 oracle's approvals
 *    fabric — admission is a ceremony with a record, and the LLMS &
 *    TRAINED MODELS tab fills from admission records only."
 *
 * Three tabs (canonical order):
 *   1. LLMs on record        — 7 Emergent Universal purchased LLMs (real facts).
 *   2. Trained adapters      — fills from admission records only.
 *                               Empty state is drawn-not-blank, not fabricated.
 *   3. Admission records     — history of ceremony fires (admit / refuse).
 *
 * Live data:
 *   GET /api/model_registry/models          — inventory (partitioned)
 *   GET /api/model_admission/records        — ceremony history
 *   GET /api/model_recheck/all              — CA1-011 W7-half states
 *   GET /api/baseline_line/records          — CA1-004 baseline lines
 *
 * Design law: REFERENCE-NOT-COPY (v7 oracle carries approvals fabric;
 * this port is structurally faithful, not byte-copy). No emojis in
 * icons — Newsreader/Iowan serif for headers, sans for figures.
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

// v7 palette tokens — must match CostLedger.jsx (audit uniformity).
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
const brass = "#b08d2e";
const head = 'ui-serif, "Iowan Old Style", Georgia, serif';


function Tab({ label, active, onClick, count, testid }) {
  return (
    <button
      onClick={onClick}
      data-testid={testid}
      style={{
        background: active ? blue : "transparent",
        color: active ? paper : ink2,
        border: `1px solid ${active ? blue : line}`,
        padding: "10px 20px",
        fontFamily: head,
        fontSize: 14,
        letterSpacing: 0.4,
        cursor: "pointer",
        marginRight: 8,
      }}
    >
      {label}
      {typeof count === "number" && (
        <span style={{ marginLeft: 10, opacity: 0.7, fontSize: 12 }}>({count})</span>
      )}
    </button>
  );
}


function LLMsTab({ purchased }) {
  if (!purchased) return <div style={{ color: ink3 }}>Loading LLMs on record…</div>;
  return (
    <div data-testid="llms-on-record">
      <div style={{ fontFamily: head, fontSize: 24, color: ink, marginBottom: 6 }}>
        LLMs on record
      </div>
      <div style={{ color: ink3, fontSize: 13, marginBottom: 24, maxWidth: 720 }}>
        {purchased.length} purchased LLM{purchased.length === 1 ? "" : "s"} on this estate.
        All access via the Emergent Universal proxy — no raw keys on record;
        custody markers only (Owner Order 2026-08-25 §4).
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        {purchased.map((m) => (
          <div
            key={m.model_id}
            data-testid={`llm-card-${m.model_id}`}
            style={{
              background: surface,
              border: `1px solid ${line}`,
              padding: "18px 22px",
            }}
          >
            <div style={{ fontFamily: head, fontSize: 18, color: ink }}>
              {m.model_id}
            </div>
            <div style={{ color: ink3, fontSize: 12, marginTop: 4, letterSpacing: 0.4 }}>
              {(m.role || "").replace(/_/g, " ")}
            </div>
            <div style={{ marginTop: 14, fontSize: 13, color: ink2, lineHeight: 1.5 }}>
              <div><b style={{ color: ink }}>Provider:</b> {m.provider}</div>
              <div><b style={{ color: ink }}>Custody:</b> {m.custody_kind}</div>
              <div><b style={{ color: ink }}>Connected:</b> {m.connected_at}</div>
            </div>
            <div style={{
              marginTop: 12, fontSize: 12, color: ink3, borderTop: `1px solid ${line}`,
              paddingTop: 10, lineHeight: 1.5,
            }}>
              {m.license_note}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


function TrainedAdaptersTab({ trained, rechecks }) {
  const seamNote = "services.watch.route_recheck_failure (lands W9)";
  if (!trained) return <div style={{ color: ink3 }}>Loading trained adapters…</div>;
  if (trained.length === 0) {
    return (
      <div data-testid="trained-empty" style={{
        background: surface, border: `1px solid ${line}`, padding: "32px 28px",
      }}>
        <div style={{ fontFamily: head, fontSize: 22, color: ink, marginBottom: 8 }}>
          No trained adapters admitted yet.
        </div>
        <div style={{ color: ink3, fontSize: 14, lineHeight: 1.6, maxWidth: 660 }}>
          Trained adapters fill this list <em>only</em> from admission records
          (Owner Ruling 2026-08-25T23:30Z). No ceremony has fired on this
          estate yet — the honest state on record is empty. This is
          drawn-not-blank per Canon 1 §4.4.
        </div>
        <div style={{ marginTop: 16, fontSize: 12, color: ink3, letterSpacing: 0.4 }}>
          When ceremony fires: MOAC six-criterion card + resolved training
          lineage → adapter registered + re-check-date stamped (90-day
          cadence · CA1-011 W7 half). Watch route (W9) will fire on overdue.
        </div>
      </div>
    );
  }
  const rc = new Map((rechecks || []).map((r) => [r.model_id, r]));
  return (
    <div data-testid="trained-list">
      {trained.map((m) => {
        const s = rc.get(m.model_id) || {};
        return (
          <div key={m.model_id} style={{
            background: surface, border: `1px solid ${line}`, padding: "18px 22px",
            marginBottom: 14,
          }} data-testid={`trained-card-${m.model_id}`}>
            <div style={{ fontFamily: head, fontSize: 18, color: ink }}>
              {m.model_id}
            </div>
            <div style={{ fontSize: 12, color: ink3, letterSpacing: 0.4, marginTop: 4 }}>
              trained adapter · admitted {m.connected_at}
            </div>
            <div style={{ marginTop: 10, fontSize: 13, color: ink2 }}>
              {m.license_note}
            </div>
            <div style={{
              marginTop: 12, fontSize: 12, color: s.state === "overdue" ? oxblood : sage,
              borderTop: `1px solid ${line}`, paddingTop: 10,
            }}>
              <b style={{ letterSpacing: 0.4 }}>CA1-011 re-check:</b>{" "}
              {s.state === "overdue" ? `OVERDUE (due ${s.re_check_due_at})` :
               s.state === "due_later" ? `due ${s.re_check_due_at}` :
               "state on record"}
              <span style={{ color: ink3, marginLeft: 12 }}>
                Watch seam: <code style={{ fontSize: 11 }}>{seamNote}</code>
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}


function AdmissionRecordsTab({ records }) {
  if (!records) return <div style={{ color: ink3 }}>Loading admission history…</div>;
  if (records.length === 0) {
    return (
      <div data-testid="admissions-empty" style={{
        background: surface, border: `1px solid ${line}`, padding: "32px 28px",
      }}>
        <div style={{ fontFamily: head, fontSize: 22, color: ink, marginBottom: 8 }}>
          Admission history is empty.
        </div>
        <div style={{ color: ink3, fontSize: 14, lineHeight: 1.6, maxWidth: 660 }}>
          No Model Admission ceremony has fired on this estate yet. Records
          land under <code>phase0/model_admission_records/</code>. Ceremony
          fires trigger: MOAC validation (§26) → uncurated-evidence check
          (§27) → rights-lineage check (§28) → floor check → register.
        </div>
      </div>
    );
  }
  return (
    <div data-testid="admission-history">
      {records.map((r, i) => (
        <div key={i} data-testid={`admission-row-${i}`} style={{
          background: surface, border: `1px solid ${line}`, padding: "16px 20px",
          marginBottom: 10, borderLeft: `4px solid ${r.outcome === "admitted" ? sage : oxblood}`,
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
            <div>
              <div style={{ fontFamily: head, fontSize: 16, color: ink }}>
                {r.candidate_model_id}
              </div>
              <div style={{ fontSize: 12, color: ink3, marginTop: 3 }}>
                {r.computed_at}
              </div>
            </div>
            <div style={{
              padding: "4px 10px", fontSize: 12, letterSpacing: 0.6,
              background: r.outcome === "admitted" ? sage : oxblood,
              color: paper,
            }}>
              {(r.outcome || "").toUpperCase()}
            </div>
          </div>
          {r.reason && (
            <div style={{ marginTop: 10, fontSize: 13, color: ink2 }}>
              <b>Reason:</b> {r.reason}
            </div>
          )}
          {r.refusal_note && (
            <div style={{ marginTop: 6, fontSize: 13, color: ink3, lineHeight: 1.5 }}>
              {r.refusal_note}
            </div>
          )}
          {r.outcome === "admitted" && (
            <div style={{ marginTop: 10, fontSize: 12, color: sage }}>
              Registry bumped to v{r.registry_version_after}.
              CA1-011 Watch seam: <code style={{ fontSize: 11 }}>{r.ca1_011_watch_seam}</code>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}


export default function ModelEcosystem() {
  const [tab, setTab] = useState("llms");
  const [models, setModels] = useState(null);
  const [rechecks, setRechecks] = useState(null);
  const [admissions, setAdmissions] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [m, r, a] = await Promise.all([
          fetch(`${BACKEND_URL}/api/model_registry/models`).then((x) => x.json()),
          fetch(`${BACKEND_URL}/api/model_recheck/all`).then((x) => x.json()),
          fetch(`${BACKEND_URL}/api/model_admission/records`).then((x) => x.json()),
        ]);
        setModels(m);
        setRechecks(r.statuses || []);
        setAdmissions(a.records || []);
      } catch (e) {
        setError(String(e));
      }
    };
    load();
  }, []);

  return (
    <div style={{ minHeight: "100vh", background: paper, padding: "48px 40px 80px" }}>
      <div style={{ maxWidth: 1080, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>
          AKKI · MODEL ECOSYSTEM
        </div>
        <h1 style={{ fontFamily: head, fontSize: 42, color: ink, margin: "10px 0 8px 0", letterSpacing: -0.5 }}>
          Every model on the estate, on record.
        </h1>
        <div style={{ color: ink3, fontSize: 14, maxWidth: 720, lineHeight: 1.6 }}>
          Docs 13/14 · CA1-004 baseline line · CA1-005 whitepaper (W8 · named gap) ·
          CA1-011 re-check (W7 register + surface · W9 Watch enforcement at named seam).
          Purchased LLMs seed from the Emergent Universal connection (real).
          Trained adapters fill from Model Admission ceremony records only.
        </div>

        <div style={{ marginTop: 32, marginBottom: 20 }}>
          <Tab
            label="LLMs on record" testid="tab-llms"
            active={tab === "llms"} onClick={() => setTab("llms")}
            count={models?.purchased_llms?.length}
          />
          <Tab
            label="Trained adapters" testid="tab-trained"
            active={tab === "trained"} onClick={() => setTab("trained")}
            count={models?.trained_adapters?.length}
          />
          <Tab
            label="Admission records" testid="tab-admissions"
            active={tab === "admissions"} onClick={() => setTab("admissions")}
            count={admissions?.length}
          />
        </div>

        {error && (
          <div style={{ background: surface, border: `1px solid ${oxblood}`,
                        color: oxblood, padding: 16, fontSize: 13 }}>
            {error}
          </div>
        )}

        {tab === "llms" && <LLMsTab purchased={models?.purchased_llms} />}
        {tab === "trained" && (
          <TrainedAdaptersTab
            trained={models?.trained_adapters}
            rechecks={rechecks}
          />
        )}
        {tab === "admissions" && <AdmissionRecordsTab records={admissions} />}

        <div style={{ marginTop: 48, fontSize: 12, color: ink3, borderTop: `1px solid ${line}`, paddingTop: 20 }}>
          <Link to="/" style={{ color: blue, textDecoration: "none" }} data-testid="nav-registry">
            ← Registry
          </Link>
          <span style={{ marginLeft: 20 }}>
            <Link to="/cost-ledger" style={{ color: blue, textDecoration: "none" }} data-testid="nav-cost-ledger">
              Cost Ledger →
            </Link>
          </span>
        </div>
      </div>
    </div>
  );
}
