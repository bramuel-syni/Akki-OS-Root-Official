import React, { useEffect, useState } from "react";
import axios from "axios";

/**
 * ConnectWizard - the estate's ONE write path, per PDF §5.
 *
 * Owner course-correction 2026-08-14: the wizard is generic. All four
 * resource kinds walk the SAME 5 steps:
 *   1 What  -> 2 How  -> 3 Credentials  -> 4 Name  -> 5 Attempt.
 *
 * COMPUTE path:
 *   Step 2 renders the estate's provisioning card (public SSH key +
 *   fingerprint + pod egress IP) BEFORE credentials are keyed - fetched
 *   from GET /api/connect/estate-facts. The owner installs the public key
 *   into VM Access and adds both /32 rows (their IP + pod egress) at
 *   creation. Step 3 collects the 7 ordered GPU fields (unchanged shape).
 *   Step 5 renders the seven-stage handshake walk from POST
 *   /api/connect/gpu (unchanged pipeline).
 *
 * NON-COMPUTE paths (data-source, llm, trained-model):
 *   Steps 1-4 fully wired; Step 5 records an honest ledgered intent via
 *   POST /api/connect/intent. Copy: "Recorded - this connection type
 *   goes live with its wave." Amber grammar, no fake success.
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

// Per-type "how" branches, seeded from PDF §5 Step 2.
const HOW_BY_KIND = {
  "data-source": {
    question: "How does Akki reach it?",
    options: ["Private link", "On-premise mount", "Scheduled batch"],
  },
  "llm": {
    question: "How is it hosted?",
    options: ["In-seam hosted", "On-premise weights", "Sandbox only"],
  },
  "trained-model": {
    question: "Where are the weights?",
    options: ["Registry", "Imported weights"],
  },
  "compute": {
    question: "How does it reach us?",
    // Compute is currently SSH over a public IP, per the AISCA journey +
    // brief §5 Step 2 phrasing. Kept generic in the label so future compute
    // sources can add other transports.
    options: ["SSH over a public IP"],
  },
};

// Free-text routing: known keyword -> kind. Unrecognized -> asks again.
function routeFreeText(t) {
  const s = (t || "").toLowerCase();
  if (!s.trim()) return null;
  if (/(gpu|compute|machine|vm|server|host)/.test(s)) return "compute";
  if (/(data|source|bucket|batch|mount|stream)/.test(s)) return "data-source";
  if (/(llm|model|chat|language)/.test(s) && /(train)/.test(s)) return "trained-model";
  if (/(llm|gpt|claude|gemini|language model|chat)/.test(s)) return "llm";
  if (/(train|weight)/.test(s)) return "trained-model";
  return null;
}

export default function ConnectWizard({ onClose }) {
  const [step, setStep] = useState("what");
  const [kind, setKind] = useState(null);
  const [how, setHow] = useState("");
  const [freeText, setFreeText] = useState("");
  const [error, setError] = useState("");
  const [name, setName] = useState("");
  const [form, setForm] = useState({
    host_name: "", username: "", password: "",
    public_ip: "", private_ip: "", os: "",
    deploy_date: new Date().toISOString().slice(0, 10),
  });
  const [submitting, setSubmitting] = useState(false);
  const [afterState, setAfterState] = useState(null);
  const [intentResult, setIntentResult] = useState(null);

  const chooseChip = (k) => { setKind(k); setError(""); setStep("how"); };
  const sendFreeText = () => {
    const routed = routeFreeText(freeText);
    if (routed) { setKind(routed); setStep("how"); setFreeText(""); setError(""); return; }
    setError("I did not read that clearly. Tap a suggestion, or say 'data source', 'LLM', 'trained model', or 'compute'.");
  };
  const goCredentials = () => {
    // Compute has one transport (seeded); non-compute users may skip explicit How.
    setStep("credentials");
  };
  const goName = () => setStep("name");
  const goAttempt = () => {
    if (!name.trim()) { setError("Give it a name - nothing connects unnamed (§5 Step 4)."); return; }
    setError("");
    setStep("attempt");
  };

  const onChange = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  useEffect(() => {
    // On entering the attempt step, fire the appropriate submit.
    if (step !== "attempt") return;
    if (kind === "compute") submitCompute();
    else submitIntent();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [step]);

  const submitCompute = async () => {
    setSubmitting(true); setError(""); setAfterState(null);
    try {
      const resp = await axios.post(`${BACKEND}/api/connect/gpu`, { ...form });
      setAfterState(resp.data);
      setForm((f) => ({ ...f, password: "" }));
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const submitIntent = async () => {
    setSubmitting(true); setError(""); setIntentResult(null);
    try {
      const resp = await axios.post(`${BACKEND}/api/connect/intent`, {
        kind, name: name.trim(), description: how || "",
      });
      setIntentResult(resp.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(28,43,69,0.35)", zIndex: 50,
                  display: "flex", justifyContent: "flex-end" }} data-testid="wizard-drawer">
      <div style={{ width: "min(560px, 92vw)", background: cream, height: "100vh", overflowY: "auto",
                    boxShadow: "-8px 0 24px rgba(0,0,0,0.12)", display: "flex", flexDirection: "column" }}>
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
                             color: grey, fontSize: 22, lineHeight: 1, padding: 4 }} aria-label="Close">×</button>
          </div>
          <StepTracker step={step} />
        </div>

        <div style={{ flex: 1, padding: "20px 32px" }}>
          {step === "what" && <StepWhat freeText={freeText} onFreeText={setFreeText}
            onChip={chooseChip} onSend={sendFreeText} error={error} />}
          {step === "how" && <StepHow kind={kind} how={how} onHow={setHow}
            onNext={goCredentials} onBack={() => setStep("what")} />}
          {step === "credentials" && <StepCredentials kind={kind} form={form} onChange={onChange}
            onNext={goName} onBack={() => setStep("how")} />}
          {step === "name" && <StepName name={name} onName={setName}
            onNext={goAttempt} onBack={() => setStep("credentials")} error={error} />}
          {step === "attempt" && <StepAttempt kind={kind} name={name}
            submitting={submitting} afterState={afterState} intentResult={intentResult}
            error={error} onClose={onClose} onRetry={() => setStep("credentials")} />}
        </div>
      </div>
    </div>
  );
}

const STEPS = [
  { key: "what", label: "1 What", testid: "wizard-step-what" },
  { key: "how", label: "2 How", testid: "wizard-step-how" },
  { key: "credentials", label: "3 Credentials", testid: "wizard-step-credentials" },
  { key: "name", label: "4 Name", testid: "wizard-step-name" },
  { key: "attempt", label: "5 Attempt", testid: "wizard-step-attempt" },
];

function StepTracker({ step }) {
  return (
    <div style={{ display: "flex", gap: 6, marginTop: 16, flexWrap: "wrap" }}>
      {STEPS.map((s) => {
        const active = s.key === step;
        return (
          <div key={s.key} data-testid={s.testid}
            style={{ padding: "4px 10px", borderRadius: 999,
                     background: active ? navy : cardWhite,
                     color: active ? cardWhite : grey,
                     fontSize: 11, letterSpacing: 1.2,
                     border: active ? "none" : "1px solid #ddd" }}>
            {s.label}
          </div>
        );
      })}
    </div>
  );
}

function StepWhat({ freeText, onFreeText, onChip, onSend, error }) {
  return (
    <>
      <PromptCard>
        What would you like to connect? Tell me in your own words -
        a data source, a model, or compute. Or tap a suggestion below.
        An unreadable answer, I will ask again rather than guess.
      </PromptCard>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 20 }}>
        {CHIPS.map((c) => (
          <button key={c.key} type="button" data-testid={c.testid}
            onClick={() => onChip(c.key)}
            style={chipStyle}>{c.label}</button>
        ))}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input data-testid="wizard-input" type="text" value={freeText}
          onChange={(e) => onFreeText(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") onSend(); }}
          placeholder="Type your answer..." style={inputStyle} />
        <button type="button" data-testid="wizard-send" onClick={onSend}
          style={sendStyle}>Send</button>
      </div>
      {error && <ErrorCard>{error}</ErrorCard>}
    </>
  );
}

function StepHow({ kind, how, onHow, onNext, onBack }) {
  const cfg = HOW_BY_KIND[kind] || { question: "How?", options: [] };
  const [needFacts, setNeedFacts] = useState(kind === "compute");
  const [facts, setFacts] = useState(null);
  const [factsError, setFactsError] = useState("");

  useEffect(() => {
    if (!needFacts) return;
    let cancelled = false;
    (async () => {
      try {
        const r = await axios.get(`${BACKEND}/api/connect/estate-facts`);
        if (!cancelled) setFacts(r.data);
      } catch (e) {
        if (!cancelled) setFactsError(e.response?.data?.detail || e.message);
      }
    })();
    return () => { cancelled = true; };
  }, [needFacts]);

  const seededDefault = cfg.options[0] || "";

  return (
    <>
      <PromptCard>
        {cfg.question} {kind === "compute" ? "Currently one transport: SSH over a public IP." : "Pick the closest, or say more."}
      </PromptCard>
      <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 8, marginBottom: 20 }}>
        {cfg.options.map((opt) => (
          <button key={opt} type="button"
            data-testid={`how-option-${opt.toLowerCase().replace(/\s+/g, "-")}`}
            onClick={() => onHow(opt)}
            style={{ ...chipStyle, textAlign: "left",
                     borderColor: (how || seededDefault) === opt ? navy : "#ddd" }}>
            {opt}
          </button>
        ))}
      </div>
      {kind === "compute" && (
        <ProvisioningCard facts={facts} error={factsError} />
      )}
      <NavRow onBack={onBack} onNext={onNext} nextLabel="Credentials -->" />
    </>
  );
}

function ProvisioningCard({ facts, error }) {
  return (
    <div data-testid="provisioning-card" style={cardBox}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: navy, marginBottom: 10 }}>
        PROVISIONING CARD · from the estate
      </div>
      {!facts && !error && (
        <div style={{ color: grey, fontSize: 13 }}>Fetching the estate's public key and egress IP...</div>
      )}
      {error && (
        <div style={{ color: oxblood, fontSize: 13 }}>{error}</div>
      )}
      {facts && (
        <>
          <FactRow label="Estate public key (paste into VM Access at creation)"
                   value={facts.estate_public_key} testid="provisioning-card-public-key" />
          <FactRow label="Fingerprint (SHA256)"
                   value={facts.estate_public_key_fingerprint} testid="provisioning-card-fingerprint" />
          <FactRow label="Pod egress IP (add as /32 to the VM's SG SSH rules alongside your operator /32)"
                   value={facts.pod_egress_ip} testid="provisioning-card-egress-ip" />
          <div style={{ marginTop: 12, fontSize: 12, color: grey, lineHeight: 1.5 }}>
            {(facts.provenance || []).map((s, i) => (
              <div key={i} style={{ marginBottom: 4 }}>· {s}</div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function FactRow({ label, value, testid }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: 11, letterSpacing: 1.5, color: grey, marginBottom: 4 }}>
        {label.toUpperCase()}
      </div>
      <code data-testid={testid} style={{ display: "block", background: "#f4f0e8",
        padding: "8px 12px", borderRadius: 6, fontSize: 12, wordBreak: "break-all",
        border: "1px solid #ddd" }}>
        {value}
      </code>
    </div>
  );
}

function StepCredentials({ kind, form, onChange, onNext, onBack }) {
  if (kind === "compute") {
    return (
      <>
        <PromptCard>
          Enter the vendor-issued bootstrap credentials once. Once the estate
          verifies its own key works, password auth is disabled, the bootstrap
          is retired, and the password is dropped. It is not stored anywhere
          and cannot be retrieved after send.
        </PromptCard>
        <form data-testid="wizard-compute-form" onSubmit={(e) => { e.preventDefault(); onNext(); }}>
          {GPU_FIELDS.map(([k, label, type, req, testid]) => (
            <div key={k} style={{ marginBottom: 12 }}>
              <label style={{ display: "block", fontSize: 12, color: grey, marginBottom: 4 }}>{label}</label>
              <input data-testid={testid}
                type={k === "password" ? "password" : type}
                value={form[k]} onChange={(e) => onChange(k, e.target.value)}
                required={req}
                autoComplete={k === "password" ? "new-password" : "off"}
                style={inputStyleFull} />
            </div>
          ))}
          <NavRow onBack={onBack} nextTestid="connect-gpu-submit" nextLabel="Name it -->" />
        </form>
      </>
    );
  }
  // Non-compute: brief acknowledgement per §5 Step 3 (credentials issued or minted-and-recorded)
  return (
    <>
      <PromptCard>
        Credentials for {kindLabel(kind)} connections travel through the
        estate's key custody when this connection type goes live with its
        wave. Nothing is entered here today.
      </PromptCard>
      <NavRow onBack={onBack} onNext={onNext} nextLabel="Name it -->" />
    </>
  );
}

function StepName({ name, onName, onNext, onBack, error }) {
  return (
    <>
      <PromptCard>
        Give it a name in the estate's words - nothing connects unnamed.
      </PromptCard>
      <div style={{ marginBottom: 16 }}>
        <input data-testid="wizard-connection-name" type="text"
          value={name} onChange={(e) => onName(e.target.value)}
          placeholder="e.g. AISCA GPU host 01"
          style={inputStyleFull} />
      </div>
      {error && <ErrorCard>{error}</ErrorCard>}
      <NavRow onBack={onBack} onNext={onNext} nextLabel="Attempt -->" />
    </>
  );
}

function StepAttempt({ kind, name, submitting, afterState, intentResult, error, onClose, onRetry }) {
  if (kind === "compute") {
    return <ComputeAttempt submitting={submitting} afterState={afterState}
      error={error} onClose={onClose} onRetry={onRetry} />;
  }
  return <IntentAttempt kind={kind} name={name} submitting={submitting}
    intentResult={intentResult} error={error} onClose={onClose} />;
}

// Compute Step 5: handshake walk (declaration -> hardening -> acceptance)
function ComputeAttempt({ submitting, afterState, error, onClose, onRetry }) {
  const cls = afterState && afterState.after_state && afterState.after_state.state_class;
  const border = cls === "green" ? sage : cls === "failed" ? oxblood : cls === "held" ? amber : grey;

  const stages = deriveHandshakeStages(afterState, submitting);
  return (
    <>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>ATTEMPT · HANDSHAKE</div>
      <div data-testid="handshake-walk" style={cardBox}>
        {stages.map((s, i) => (
          <div key={s.key} data-testid={`handshake-stage-${s.key}`}
            style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 0",
                     borderTop: i === 0 ? "none" : "1px solid #eee",
                     color: s.status === "failed" ? oxblood :
                            s.status === "untried" ? "#bbb" :
                            s.status === "done" ? navy :
                            s.status === "held" ? amber : grey }}>
            <div style={{ width: 20, textAlign: "center" }}>{stageGlyph(s.status)}</div>
            <div style={{ flex: 1, fontSize: 14 }}>
              <div style={{ fontWeight: s.status === "failed" ? 600 : 400 }}>{s.label}</div>
              {s.sentence && <div style={{ fontSize: 12, color: grey }}>{s.sentence}</div>}
            </div>
          </div>
        ))}
      </div>

      {afterState && afterState.after_state && (
        <div data-testid="connect-gpu-after-state"
             style={{ marginTop: 16, borderLeft: `4px solid ${border}`, paddingLeft: 16 }}>
          <FourQuestions a={afterState.after_state} />
        </div>
      )}
      {error && <ErrorCard>{error}</ErrorCard>}

      <div style={{ marginTop: 20, display: "flex", gap: 12 }}>
        {cls === "green" && (
          <button type="button" data-testid="wizard-close-after-success" onClick={onClose}
            style={sendStyle}>Close</button>
        )}
        {cls === "failed" && (
          <button type="button" data-testid="connect-gpu-retry" onClick={onRetry}
            style={sendStyle}>Retry the credentials</button>
        )}
        {cls === "held" && (
          <div data-testid="connect-gpu-held-note" style={{ color: amber, fontSize: 13 }}>
            Held with evidence · escalated to the vendor.
          </div>
        )}
      </div>
    </>
  );
}

// Non-compute Step 5: honest intent record
function IntentAttempt({ kind, name, submitting, intentResult, error, onClose }) {
  return (
    <>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>ATTEMPT · RECORD INTENT</div>
      <div style={cardBox}>
        {submitting && <div style={{ color: grey, fontSize: 13 }}>Writing the intent to the ledger...</div>}
        {intentResult && (
          <div data-testid="intent-recorded" style={{ borderLeft: `4px solid ${amber}`, paddingLeft: 16 }}>
            <div style={{ fontSize: 11, letterSpacing: 1.5, color: amber, marginBottom: 8 }}>
              INTENT RECORDED
            </div>
            <div style={{ color: navy, fontSize: 15, lineHeight: 1.5, marginBottom: 8 }}>
              {kindLabel(kind)} '{name}' captured.
            </div>
            <div style={{ color: grey, fontSize: 14, lineHeight: 1.5 }}>
              Recorded - this connection type goes live with its wave.
              Nothing crossed and nothing was written to the connected estate today.
            </div>
            {intentResult.intent_receipt_path && (
              <div style={{ marginTop: 8, fontSize: 11, color: grey }}>
                Receipt: <code style={{ fontSize: 11 }}>{intentResult.intent_receipt_path}</code>
              </div>
            )}
          </div>
        )}
        {error && <ErrorCard>{error}</ErrorCard>}
      </div>
      {intentResult && (
        <div style={{ marginTop: 20 }}>
          <button type="button" data-testid="wizard-close-after-intent" onClick={onClose}
            style={sendStyle}>Close</button>
        </div>
      )}
    </>
  );
}

// -------- helpers --------

function deriveHandshakeStages(afterState, submitting) {
  // Derive the 3 pipeline stages from the response. If in-flight, mark
  // stages as running/untried per state; if failed, mark the failing
  // stage crimson and later stages 'untried' greyed (brief §5).
  const a = (afterState && afterState.after_state) || null;
  const cls = a && a.state_class;
  const failedStage = a && a.failed_stage;
  const seq = [
    { key: "declaration", label: "Declaration - the actor and task are on record" },
    { key: "hardening", label: "Hardening - key installed, password auth disabled, bootstrap retired" },
    { key: "acceptance", label: "Acceptance - verified against the §6 spec" },
  ];
  return seq.map((s) => {
    if (submitting && !a) return { ...s, status: "running", sentence: "..." };
    if (!a) return { ...s, status: "untried", sentence: "" };
    if (cls === "green") return { ...s, status: "done", sentence: "" };
    if (cls === "held" && s.key === "acceptance") return { ...s, status: "held", sentence: a.how_we_know || "" };
    if (cls === "failed" && failedStage === s.key) return { ...s, status: "failed", sentence: a.how_we_know || "" };
    if (cls === "failed" && !failedStage) {
      // no failed_stage → assume hardening
      if (s.key === "hardening") return { ...s, status: "failed", sentence: a.how_we_know || "" };
      if (s.key === "acceptance") return { ...s, status: "untried", sentence: "" };
      return { ...s, status: "done", sentence: "" };
    }
    if (cls === "failed") {
      const idx = seq.findIndex((x) => x.key === failedStage);
      const myIdx = seq.findIndex((x) => x.key === s.key);
      if (myIdx < idx) return { ...s, status: "done", sentence: "" };
      return { ...s, status: "untried", sentence: "" };
    }
    return { ...s, status: "done", sentence: "" };
  });
}

function stageGlyph(status) {
  switch (status) {
    case "done": return "OK";
    case "failed": return "!";
    case "held": return "…";
    case "running": return "·";
    case "untried": return "-";
    default: return "?";
  }
}

function kindLabel(k) {
  return { "data-source": "Data source", "llm": "LLM", "trained-model": "Trained model", "compute": "Compute" }[k] || k;
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

// -------- styles --------

const chipStyle = { padding: "12px 14px", background: cardWhite, border: "1px solid #ddd",
                    borderRadius: 999, cursor: "pointer", color: navy, fontSize: 14, textAlign: "left" };
const inputStyle = { flex: 1, padding: "12px 14px", borderRadius: 8, border: "1px solid #ddd", fontSize: 14 };
const inputStyleFull = { width: "100%", padding: "10px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14 };
const sendStyle = { padding: "10px 20px", background: navy, color: cardWhite, border: "none",
                    borderRadius: 999, cursor: "pointer", fontSize: 14 };
const backStyle = { padding: "10px 20px", background: "transparent", color: grey, border: "1px solid #ddd",
                    borderRadius: 999, cursor: "pointer", fontSize: 14 };
const cardBox = { background: cardWhite, borderRadius: 10, padding: "16px 20px", marginBottom: 16 };

// -------- small subcomponents --------

function PromptCard({ children }) {
  return (
    <div style={cardBox}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 6 }}>AKKI</div>
      <p style={{ color: navy, fontSize: 15, lineHeight: 1.55, margin: 0 }}>{children}</p>
    </div>
  );
}

function ErrorCard({ children }) {
  return (
    <div data-testid="wizard-error" style={{ marginTop: 12, padding: "10px 14px", background: cardWhite,
      borderRadius: 8, borderLeft: `3px solid ${amber}`, color: navy, fontSize: 13, lineHeight: 1.5 }}>
      {children}
    </div>
  );
}

function NavRow({ onBack, onNext, nextTestid, nextLabel }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", marginTop: 20 }}>
      {onBack ? (
        <button type="button" onClick={onBack} style={backStyle}>Back</button>
      ) : <div />}
      {onNext ? (
        <button type={nextTestid ? "submit" : "button"} onClick={onNext}
          data-testid={nextTestid || undefined} style={sendStyle}>{nextLabel || "Next -->"}</button>
      ) : (
        // In the compute form the submit is triggered by form submit
        nextTestid ? <button type="submit" data-testid={nextTestid} style={sendStyle}>{nextLabel || "Next"}</button> : <div />
      )}
    </div>
  );
}
