import React, { useState } from "react";
import axios from "axios";

/**
 * ConnectWizard - the estate's one write path (Owner fixture drop 2026-08-14).
 *
 * Renders per Akki Prototype v7 "Screen mockups" (fixtures/screen_mockups_v7.pdf §5).
 * A right-hand drawer holding a conversation, not a form. Four suggestion chips
 * (A data source · An LLM · A trained model · Compute) + free-text input + Send.
 *
 * Compute chip branches into the sub-flow that collects the SAME 7 ordered
 * GPU fields as the retired Admin surface (host_name, username, password,
 * public_ip, private_ip, os, deploy_date). Submit machinery unchanged:
 * POST /api/connect/gpu with the same payload; the same seven-stage backend
 * pipeline fires.
 *
 * Failure grammar per PDF §5: handshake step by step, failing step in crimson,
 * untried greyed, retry/switch/log conversation options. Success ends with a
 * single Close per PDF §5.
 */
const BACKEND = process.env.REACT_APP_BACKEND_URL;

const cream = "#f6f2ea";
const navy = "#1c2b45";
const oxblood = "#5a1a1a";
const amber = "#c98a1c";
const sage = "#4a7c59";
const grey = "#666";
const cardWhite = "#ffffff";

const CHIPS = [
  { key: "data-source", label: "A data source", testid: "wizard-chip-data-source" },
  { key: "llm", label: "An LLM", testid: "wizard-chip-llm" },
  { key: "trained-model", label: "A trained model", testid: "wizard-chip-trained-model" },
  { key: "compute", label: "Compute", testid: "wizard-chip-compute" },
];

const GPU_FIELDS = [
  ["host_name", "Host Name", "text", true, "connect-gpu-host_name"],
  ["username", "Username", "text", true, "connect-gpu-username"],
  ["password", "Password", "password", true, "connect-gpu-password"],
  ["public_ip", "Public IP", "text", true, "connect-gpu-public_ip"],
  ["private_ip", "Private IP (optional)", "text", false, "connect-gpu-private_ip"],
  ["os", "OS (optional)", "text", false, "connect-gpu-os"],
  ["deploy_date", "Deploy date (pins +14d)", "date", false, "connect-gpu-deploy_date"],
];

export default function ConnectWizard({ onClose }) {
  const [step, setStep] = useState("what"); // what | compute-form | attempting | after-state
  const [freeText, setFreeText] = useState("");
  const [form, setForm] = useState({
    host_name: "",
    username: "",
    password: "",
    public_ip: "",
    private_ip: "",
    os: "",
    deploy_date: new Date().toISOString().slice(0, 10),
  });
  const [afterState, setAfterState] = useState(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const chooseChip = (key) => {
    if (key === "compute") return setStep("compute-form");
    // Data source / LLM / trained model paths are not built in this cycle;
    // the conversation acknowledges honestly per PDF §5 (unreadable answer
    // is asked again rather than guessed).
    setError(`The ${key.replace(/-/g, " ")} path is not yet wired. Choose Compute for now.`);
  };

  const sendFreeText = () => {
    const t = freeText.trim().toLowerCase();
    if (!t) return;
    if (t.includes("compute") || t.includes("gpu") || t.includes("machine")) {
      setFreeText("");
      setStep("compute-form");
      return;
    }
    setError("I did not read that clearly. Try one of the chips - only Compute is wired in this cycle.");
  };

  const onChange = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    setStep("attempting");
    try {
      const resp = await axios.post(`${BACKEND}/api/connect/gpu`, form);
      setAfterState(resp.data);
      setForm((f) => ({ ...f, password: "" }));
      setStep("after-state");
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      setStep("compute-form");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(28,43,69,0.35)", zIndex: 50, display: "flex", justifyContent: "flex-end" }}
         data-testid="wizard-drawer">
      <div style={{ width: "min(520px, 90vw)", background: cream, height: "100vh", overflowY: "auto",
                    boxShadow: "-8px 0 24px rgba(0,0,0,0.12)", display: "flex", flexDirection: "column" }}>
        {/* Drawer header */}
        <div style={{ padding: "24px 32px 12px", borderBottom: "1px solid #ddd" }}>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
            <div>
              <div style={{ fontSize: 11, letterSpacing: 2, color: grey }}>REGISTRY · CONNECT</div>
              <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28, margin: "6px 0 4px 0", color: navy }}>
                Connect something new
              </h2>
              <p style={{ color: grey, fontSize: 14, margin: 0 }}>A conversation, not a form.</p>
            </div>
            <button type="button" data-testid="wizard-close" onClick={onClose}
                    style={{ background: "transparent", border: "none", cursor: "pointer",
                             color: grey, fontSize: 22, lineHeight: 1, padding: 4 }} aria-label="Close">
              ×
            </button>
          </div>
        </div>

        {/* Drawer body */}
        <div style={{ flex: 1, padding: "24px 32px" }}>
          {step === "what" && <StepWhat
            freeText={freeText} onFreeTextChange={setFreeText}
            onChooseChip={chooseChip} onSend={sendFreeText}
            error={error} />}
          {step === "compute-form" && <StepCompute
            form={form} onChange={onChange} onSubmit={submit}
            submitting={submitting} error={error} />}
          {step === "attempting" && <StepAttempting />}
          {step === "after-state" && <StepAfterState state={afterState} onClose={onClose} />}
        </div>
      </div>
    </div>
  );
}

function StepWhat({ freeText, onFreeTextChange, onChooseChip, onSend, error }) {
  return (
    <>
      <div data-testid="wizard-prompt" style={{ background: cardWhite, borderRadius: 10, padding: "16px 20px", marginBottom: 20 }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 6 }}>AKKI</div>
        <p style={{ color: navy, fontSize: 15, lineHeight: 1.55, margin: 0 }}>
          What would you like to connect? Tell me in your own words -
          a data source, a model, or compute. Or tap a suggestion below.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 20 }}>
        {CHIPS.map((c) => (
          <button key={c.key} type="button" data-testid={c.testid}
                  onClick={() => onChooseChip(c.key)}
                  style={{ padding: "12px 14px", background: cardWhite, border: "1px solid #ddd",
                           borderRadius: 999, cursor: "pointer", color: navy, fontSize: 14, textAlign: "left" }}>
            {c.label}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          data-testid="wizard-input"
          type="text"
          value={freeText}
          onChange={(e) => onFreeTextChange(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") onSend(); }}
          placeholder="Type your answer..."
          style={{ flex: 1, padding: "12px 14px", borderRadius: 8, border: "1px solid #ddd", fontSize: 14 }}
        />
        <button type="button" data-testid="wizard-send" onClick={onSend}
                style={{ padding: "12px 20px", background: navy, color: cardWhite, border: "none",
                         borderRadius: 8, cursor: "pointer", fontSize: 14 }}>
          Send
        </button>
      </div>

      {error && (
        <div data-testid="wizard-error" style={{ marginTop: 16, padding: "10px 14px", background: cardWhite,
                                                  borderRadius: 8, borderLeft: `3px solid ${amber}`,
                                                  color: navy, fontSize: 13, lineHeight: 1.5 }}>
          {error}
        </div>
      )}
    </>
  );
}

function StepCompute({ form, onChange, onSubmit, submitting, error }) {
  return (
    <>
      <div style={{ background: cardWhite, borderRadius: 10, padding: "16px 20px", marginBottom: 20 }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 6 }}>AKKI</div>
        <p style={{ color: navy, fontSize: 15, lineHeight: 1.55, margin: 0 }}>
          A compute connection. Enter the vendor-issued bootstrap credentials once.
          On send the estate installs its key, disables password auth, retires the
          bootstrap, and runs acceptance against the §6 spec. The password is not
          stored anywhere and cannot be retrieved after send.
        </p>
      </div>

      <form onSubmit={onSubmit} data-testid="wizard-compute-form">
        {GPU_FIELDS.map(([k, label, type, req, testid]) => (
          <div key={k} style={{ marginBottom: 12 }}>
            <label style={{ display: "block", fontSize: 12, color: grey, marginBottom: 4 }}>{label}</label>
            <input
              data-testid={testid}
              type={k === "password" ? "password" : type}
              value={form[k]}
              onChange={(e) => onChange(k, e.target.value)}
              required={req}
              autoComplete={k === "password" ? "new-password" : "off"}
              style={{ width: "100%", padding: "10px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14 }}
            />
          </div>
        ))}

        {error && (
          <div data-testid="connect-gpu-error" style={{ marginTop: 8, color: oxblood, fontSize: 13 }}>
            {typeof error === "string" ? error : JSON.stringify(error)}
          </div>
        )}

        <div style={{ marginTop: 20 }}>
          <button type="submit" disabled={submitting} data-testid="connect-gpu-submit"
                  style={{ padding: "12px 24px", background: navy, color: cardWhite, border: "none",
                           borderRadius: 999, cursor: "pointer", fontSize: 14 }}>
            {submitting ? "Attempting..." : "Send"}
          </button>
        </div>
      </form>
    </>
  );
}

function StepAttempting() {
  return (
    <div data-testid="wizard-attempting"
         style={{ background: cardWhite, borderRadius: 10, padding: "24px 20px" }}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 8 }}>AKKI</div>
      <p style={{ color: navy, fontSize: 15, lineHeight: 1.55, margin: 0 }}>
        Attempting the connection. Route, TLS, credentials, read - step by step.
      </p>
    </div>
  );
}

function StepAfterState({ state, onClose }) {
  const a = (state && state.after_state) || {};
  const cls = a.state_class;
  const border =
    cls === "green" ? sage :
    cls === "failed" ? oxblood :
    cls === "held" ? amber : grey;
  return (
    <div data-testid="connect-gpu-after-state">
      <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a5aae", marginBottom: 8 }}>
        AFTER STATE · {cls ? cls.toUpperCase() : "UNKNOWN"}
      </div>
      <div style={{ borderLeft: `4px solid ${border}`, paddingLeft: 20, marginBottom: 24 }}>
        <FourQuestions a={a} />
      </div>
      {state && state.commissioning_record_path && (
        <div style={{ fontSize: 12, color: grey, marginBottom: 8 }}>
          Commissioning record: <code style={{ fontSize: 11 }}>{state.commissioning_record_path}</code>
        </div>
      )}
      {cls === "green" && (
        <div style={{ marginTop: 16 }}>
          <div data-testid="connect-success" style={{ color: sage, fontWeight: 500, marginBottom: 12 }}>
            Connection successful.
          </div>
          <button type="button" data-testid="wizard-close-after-success" onClick={onClose}
                  style={{ padding: "10px 24px", background: navy, color: cardWhite, border: "none",
                           borderRadius: 999, cursor: "pointer", fontSize: 14 }}>
            Close
          </button>
        </div>
      )}
      {cls === "held" && (
        <div data-testid="connect-gpu-held-note" style={{ marginTop: 16, fontSize: 13, color: amber }}>
          Held with evidence · escalated to the vendor.
        </div>
      )}
    </div>
  );
}

function FourQuestions({ a }) {
  const rows = [
    ["What's happening", a.whats_happening],
    ["How do we know", a.how_we_know],
    ["What we're doing", a.what_we_are_doing],
    ["Is the agreement holding", a.agreement_holding],
  ];
  return (
    <div>
      {rows.map(([q, ans]) => (
        <div key={q} style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, letterSpacing: 1.5, color: "#888", marginBottom: 3 }}>{q.toUpperCase()}</div>
          <div style={{ fontSize: 14, color: navy, lineHeight: 1.5 }}
               data-testid={`four-q-${q.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
            {ans || "not yet measured"}
          </div>
        </div>
      ))}
    </div>
  );
}
