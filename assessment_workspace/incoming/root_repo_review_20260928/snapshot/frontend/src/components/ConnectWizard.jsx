import React, { useEffect, useState } from "react";
import axios from "axios";

/**
 * ConnectWizard - Single paste-and-connect panel (Owner Simplification 2026-08-14).
 *
 * The 5-step wizard is retired as the primary path. Connect collapses to
 * ONE panel: a large paste area with type chips on the same panel
 * (default: auto-detect), manual fallback fields inline, and a one-tap
 * aside for the provisioning card. Step grammar survives ONLY as the
 * post-submit progress/result view - the handshake walk from the
 * existing seven-stage pipeline (unchanged).
 *
 * Custody rule (owner Q2 addendum):
 *   Pasted text may contain the password; the /api/connect/parse-paste
 *   response NEVER carries it back (server strips + password_captured
 *   signal). This component keeps the raw paste in its own textarea
 *   memory and submits the full credential set once to /api/connect/gpu
 *   (compute) or /api/connect/intent (non-compute).
 */

const BACKEND = process.env.REACT_APP_BACKEND_URL;

const CHIPS = [
  { key: "auto", label: "Auto-detect", testid: "chip-auto-detect" },
  { key: "data-source", label: "A data source", testid: "wizard-chip-data-source" },
  { key: "llm", label: "An LLM", testid: "wizard-chip-llm" },
  { key: "trained-model", label: "A trained model", testid: "wizard-chip-trained-model" },
  { key: "compute", label: "Compute", testid: "wizard-chip-compute" },
];

const COMPUTE_MANUAL_FIELDS = [
  ["host_name", "Host Name", "text", true],
  ["username", "Username", "text", true],
  ["password", "Password", "password", true],
  ["public_ip", "Public IP", "text", true],
  ["private_ip", "Private IP", "text", false],
  ["os", "OS", "text", false],
  ["deploy_date", "Deploy date (pins +14d)", "date", false],
];

const HANDSHAKE_STAGES = [
  { key: "declaration", label: "Declaration" },
  { key: "hardening", label: "Hardening" },
  { key: "acceptance", label: "Acceptance" },
];

// Client-side mirror password extractor (deterministic; same shape as the
// server parser). The parse-paste response never carries the password back
// (custody rule), so the browser plucks it from its own textarea memory
// before POSTing to /api/connect/gpu.
function extractPasswordFromPaste(paste) {
  if (!paste) return "";
  const re = /^\s*(password|pass|pwd)\s*[:=]\s*(.+?)\s*$/im;
  const m = paste.match(re);
  return m ? m[2] : "";
}

// Same mirror pattern for aws_secret_access_key — the parse-paste response
// omits it; we pluck from the raw paste for the /api/connect/data-source POST.
function extractAwsSecretFromPaste(paste) {
  if (!paste) return "";
  const re = /^\s*(aws[_ ]?secret[_ ]?access[_ ]?key|secret[_ ]access[_ ]key|secret[_ ]key)\s*[:=]\s*(.+?)\s*$/im;
  const m = paste.match(re);
  return m ? m[2] : "";
}

// Styles (top-level so component can reference them; palette matches the
// wider estate surface — cream / navy / oxblood / amber / sage).
const cream = "#f6f2ea";
const navy = "#1c2b45";
const oxblood = "#5a1a1a";
const amber = "#c98a1c";
const sage = "#4a7c59";
const grey = "#666";

const overlayStyle = {
  position: "fixed", inset: 0, background: "rgba(28,43,69,0.6)", zIndex: 1000,
  display: "flex", alignItems: "flex-start", justifyContent: "center",
  overflowY: "auto", padding: "32px 16px",
};
const panelStyle = {
  background: "#ffffff", padding: 24, borderRadius: 8,
  width: "min(720px, 95vw)", maxHeight: "88vh", overflowY: "auto",
  fontFamily: "system-ui, -apple-system, sans-serif",
};
const headerRow = { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 };
const h1Style = { fontSize: 22, fontWeight: 600, color: navy };
const closeBtn = { border: "none", background: "transparent", fontSize: 24, cursor: "pointer", color: grey };
const chipRow = { display: "flex", flexWrap: "wrap", gap: 8, margin: "12px 0" };
const pasteStyle = { width: "100%", minHeight: 140, fontFamily: "monospace", fontSize: 13, padding: 10, border: "1px solid #ccc", borderRadius: 4, boxSizing: "border-box" };
const buttonRow = { display: "flex", gap: 12, margin: "12px 0", alignItems: "center", flexWrap: "wrap" };
const btnPrimary = { background: navy, color: "#fff", padding: "10px 18px", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 14 };
const btnAmber = { background: amber, color: "#fff", padding: "8px 14px", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 13 };
const btnLink = { background: "transparent", border: "none", color: amber, textDecoration: "underline", cursor: "pointer", fontSize: 13, padding: 0 };
const confirmStyle = { marginTop: 12, background: cream, padding: 12, border: "1px solid #ddd", borderRadius: 4 };
const warningStyle = { marginTop: 8, padding: 10, background: "#fef4e5", color: oxblood, border: `1px solid ${amber}`, borderRadius: 4, fontSize: 13 };
const fieldGrid = { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 8, marginTop: 8 };
const fieldLabel = { display: "flex", flexDirection: "column", gap: 4 };
const inputStyle = { padding: "6px 8px", border: "1px solid #ccc", borderRadius: 4, fontSize: 13 };

function chipStyle(selected) {
  return {
    padding: "6px 12px", border: `1px solid ${selected ? navy : "#ccc"}`,
    background: selected ? navy : "#fff", color: selected ? "#fff" : navy,
    borderRadius: 20, cursor: "pointer", fontSize: 13,
  };
}

export default function ConnectWizard({ isOpen = true, onClose, initialKind }) {
  const [paste, setPaste] = useState("");
  const [chipKind, setChipKind] = useState(initialKind || "auto");
  const [parseResult, setParseResult] = useState(null);
  const [parseErr, setParseErr] = useState("");
  const [manual, setManual] = useState({});
  const [showProvCard, setShowProvCard] = useState(false);
  const [estateFacts, setEstateFacts] = useState(null);
  const [connectionName, setConnectionName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [handshake, setHandshake] = useState(null);
  const [intentRecorded, setIntentRecorded] = useState(null);
  const [dataSourceResult, setDataSourceResult] = useState(null);
  const [submitErr, setSubmitErr] = useState("");

  useEffect(() => {
    if (!isOpen) return;
    axios.get(`${BACKEND}/api/connect/estate-facts`)
      .then((r) => setEstateFacts(r.data))
      .catch(() => setEstateFacts(null));
  }, [isOpen]);

  if (!isOpen) return null;

  const effectiveKind = parseResult?.kind || (chipKind === "auto" ? "compute" : chipKind);

  const doParse = async () => {
    setParseErr("");
    setHandshake(null);
    setIntentRecorded(null);
    if (!paste.trim()) {
      setParseErr("I did not read anything to parse. Paste the details, or fill the manual fields below.");
      setParseResult(null);
      return;
    }
    try {
      const body = { paste, hint_kind: chipKind === "auto" ? null : chipKind };
      const r = await axios.post(`${BACKEND}/api/connect/parse-paste`, body);
      setParseResult(r.data);
      // Seed manual fields from parsed non-secret values (owner can edit)
      setManual((m) => ({ ...m, ...r.data.fields }));
    } catch (e) {
      const detail = e?.response?.data?.detail || e.message;
      setParseErr(`I couldn't read that. ${detail}. Try again, or fill the manual fields.`);
      setParseResult(null);
    }
  };

  const doSubmit = async () => {
    setSubmitErr("");
    setSubmitting(true);
    try {
      if (effectiveKind === "compute") {
        const pwFromPaste = extractPasswordFromPaste(paste);
        const payload = {
          host_name: manual.host_name || parseResult?.fields?.host_name || "",
          username: manual.username || parseResult?.fields?.username || "",
          password: manual.password || pwFromPaste,
          public_ip: manual.public_ip || parseResult?.fields?.public_ip || "",
          private_ip: manual.private_ip || parseResult?.fields?.private_ip || "",
          os: manual.os || parseResult?.fields?.os || "",
          deploy_date: manual.deploy_date || parseResult?.fields?.deploy_date || "",
        };
        const r = await axios.post(`${BACKEND}/api/connect/gpu`, payload);
        setHandshake(r.data);
      } else if (effectiveKind === "data-source") {
        // Client-side mirror pluck for aws_secret_access_key (custody:
        // /api/connect/parse-paste never carries it back, so we pull it
        // from the raw paste same as we do for the compute password).
        const awsSecretFromPaste = extractAwsSecretFromPaste(paste);
        const payload = {
          aws_access_key_id: manual.aws_access_key_id || parseResult?.fields?.aws_access_key_id || undefined,
          aws_secret_access_key: manual.aws_secret_access_key || awsSecretFromPaste || undefined,
          region: manual.region || parseResult?.fields?.region || "",
          cluster_arn: manual.cluster_arn || parseResult?.fields?.cluster_arn || "",
          secret_arn: manual.secret_arn || parseResult?.fields?.secret_arn || "",
          database: manual.database || parseResult?.fields?.database || undefined,
        };
        const r = await axios.post(`${BACKEND}/api/connect/data-source`, payload);
        setDataSourceResult(r.data);
      } else {
        const payload = {
          kind: effectiveKind,
          name: connectionName || `unnamed-${effectiveKind}`,
          description: (paste || "").slice(0, 200),
        };
        const r = await axios.post(`${BACKEND}/api/connect/intent`, payload);
        setIntentRecorded(r.data);
      }
    } catch (e) {
      const detail = e?.response?.data?.detail || e.message;
      setSubmitErr(`The estate could not accept that: ${detail}`);
    } finally {
      setSubmitting(false);
    }
  };

  // -------- Post-submit result views ----------------------------------------

  if (handshake) {
    return (
      <div style={overlayStyle}>
        <div style={panelStyle}>
          <div style={headerRow}>
            <div style={h1Style}>Handshake walk</div>
            <button data-testid="wizard-close" onClick={() => { setHandshake(null); onClose && onClose(); }} style={closeBtn}>×</button>
          </div>
          <HandshakeWalk data={handshake} />
        </div>
      </div>
    );
  }
  if (dataSourceResult) {
    return (
      <div style={overlayStyle}>
        <div style={panelStyle}>
          <div style={headerRow}>
            <div style={h1Style}>Data connection</div>
            <button data-testid="wizard-close" onClick={() => { setDataSourceResult(null); onClose && onClose(); }} style={closeBtn}>×</button>
          </div>
          <DataSourceResult result={dataSourceResult} />
        </div>
      </div>
    );
  }
  if (intentRecorded) {
    return (
      <div style={overlayStyle}>
        <div style={panelStyle}>
          <div style={headerRow}>
            <div style={h1Style}>Intent recorded</div>
            <button data-testid="wizard-close" onClick={() => { setIntentRecorded(null); onClose && onClose(); }} style={closeBtn}>×</button>
          </div>
          <div data-testid="intent-recorded" style={{ color: sage, padding: 12, background: cream, borderRadius: 4 }}>
            Recorded — this connection type goes live with its wave.
            <div style={{ color: grey, marginTop: 12, fontSize: 13 }}>Name: {intentRecorded.name}</div>
          </div>
        </div>
      </div>
    );
  }

  // -------- Main single-panel form -----------------------------------------

  return (
    <div style={overlayStyle}>
      <div data-testid="connect-panel" style={panelStyle}>
        <div style={headerRow}>
          <div>
            <div style={h1Style}>Connect something new</div>
            <div style={{ color: grey, fontSize: 13, marginTop: 4 }}>
              A conversation, not a form. Paste the connection details exactly as you received them — I will read them.
            </div>
          </div>
          <button data-testid="wizard-close" onClick={onClose} style={closeBtn}>×</button>
        </div>

        <div style={chipRow}>
          {CHIPS.map((c) => (
            <button
              key={c.key}
              data-testid={c.testid}
              onClick={() => { setChipKind(c.key); setParseResult(null); }}
              style={chipStyle(chipKind === c.key)}
            >
              {c.label}
            </button>
          ))}
        </div>

        <textarea
          data-testid="connect-paste-input"
          value={paste}
          onChange={(e) => setPaste(e.target.value)}
          placeholder={"Host Name: aisca-gpu-01\nUsername: ubuntu\nPassword: ...\nPublic IP: 203.0.113.5\nOS: ubuntu24.04"}
          style={pasteStyle}
        />

        <div style={buttonRow}>
          <button data-testid="connect-parse" onClick={doParse} style={btnAmber}>Parse & confirm</button>
          <button
            data-testid="provisioning-card-toggle"
            onClick={() => setShowProvCard(!showProvCard)}
            style={btnLink}
          >
            {showProvCard ? "Hide provisioning card" : "Provisioning a new machine? What to paste on the AISCA side"}
          </button>
        </div>

        {parseErr && (
          <div data-testid="parse-error" style={warningStyle}>{parseErr}</div>
        )}

        {parseResult && <ConfirmView result={parseResult} />}

        {showProvCard && <ProvisioningCard facts={estateFacts} />}

        <details style={{ marginTop: 16, borderTop: `1px solid ${grey}30`, paddingTop: 12 }}>
          <summary style={{ cursor: "pointer", color: grey, fontSize: 13 }}>
            Manual fallback fields (edit what I read, or fill from scratch)
          </summary>
          {effectiveKind === "compute" && (
            <div style={fieldGrid}>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Host Name *</span>
                <input data-testid="manual-field-host_name" type="text" autoComplete="off"
                  value={manual.host_name || ""}
                  onChange={(e) => setManual({ ...manual, host_name: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Username *</span>
                <input data-testid="manual-field-username" type="text" autoComplete="off"
                  value={manual.username || ""}
                  onChange={(e) => setManual({ ...manual, username: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Password *</span>
                <input data-testid="manual-field-password" type="password" autoComplete="new-password"
                  value={manual.password || ""}
                  onChange={(e) => setManual({ ...manual, password: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Public IP *</span>
                <input data-testid="manual-field-public_ip" type="text" autoComplete="off"
                  value={manual.public_ip || ""}
                  onChange={(e) => setManual({ ...manual, public_ip: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Private IP</span>
                <input data-testid="manual-field-private_ip" type="text" autoComplete="off"
                  value={manual.private_ip || ""}
                  onChange={(e) => setManual({ ...manual, private_ip: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>OS</span>
                <input data-testid="manual-field-os" type="text" autoComplete="off"
                  value={manual.os || ""}
                  onChange={(e) => setManual({ ...manual, os: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Deploy date (pins +14d)</span>
                <input data-testid="manual-field-deploy_date" type="date" autoComplete="off"
                  value={manual.deploy_date || ""}
                  onChange={(e) => setManual({ ...manual, deploy_date: e.target.value })}
                  style={inputStyle} />
              </label>
            </div>
          )}
          {effectiveKind === "data-source" && (
            <div style={fieldGrid}>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>AWS Access Key ID</span>
                <input data-testid="manual-field-aws_access_key_id" type="text" autoComplete="off"
                  value={manual.aws_access_key_id || ""}
                  onChange={(e) => setManual({ ...manual, aws_access_key_id: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>AWS Secret Access Key</span>
                <input data-testid="manual-field-aws_secret_access_key" type="password" autoComplete="new-password"
                  value={manual.aws_secret_access_key || ""}
                  onChange={(e) => setManual({ ...manual, aws_secret_access_key: e.target.value })}
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Region *</span>
                <input data-testid="manual-field-region" type="text" autoComplete="off"
                  value={manual.region || ""}
                  onChange={(e) => setManual({ ...manual, region: e.target.value })}
                  placeholder="us-east-1"
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Cluster ARN *</span>
                <input data-testid="manual-field-cluster_arn" type="text" autoComplete="off"
                  value={manual.cluster_arn || ""}
                  onChange={(e) => setManual({ ...manual, cluster_arn: e.target.value })}
                  placeholder="arn:aws:rds:us-east-1:…:cluster:…"
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Secret ARN *</span>
                <input data-testid="manual-field-secret_arn" type="text" autoComplete="off"
                  value={manual.secret_arn || ""}
                  onChange={(e) => setManual({ ...manual, secret_arn: e.target.value })}
                  placeholder="arn:aws:secretsmanager:us-east-1:…:secret:…"
                  style={inputStyle} />
              </label>
              <label style={fieldLabel}>
                <span style={{ color: navy, fontSize: 12 }}>Database</span>
                <input data-testid="manual-field-database" type="text" autoComplete="off"
                  value={manual.database || ""}
                  onChange={(e) => setManual({ ...manual, database: e.target.value })}
                  style={inputStyle} />
              </label>
            </div>
          )}
          {effectiveKind !== "compute" && (
            <div style={{ marginTop: 8, color: grey, fontSize: 13 }}>
              This kind ({effectiveKind}) is intent-only right now — it records
              via /api/connect/intent. The paste and name are enough.
            </div>
          )}
        </details>

        {effectiveKind !== "compute" && effectiveKind !== "data-source" && (
          <input
            data-testid="wizard-connection-name"
            placeholder="Name it in the estate's words (nothing connects unnamed)"
            value={connectionName}
            onChange={(e) => setConnectionName(e.target.value)}
            style={{ ...inputStyle, marginTop: 12, width: "100%", boxSizing: "border-box" }}
          />
        )}

        <button
          data-testid="connect-submit"
          onClick={doSubmit}
          disabled={submitting}
          style={{ ...btnPrimary, marginTop: 16 }}
        >
          {submitting ? "Connecting…"
            : effectiveKind === "compute" ? "Connect"
            : effectiveKind === "data-source" ? "Test connection"
            : "Record intent"}
        </button>

        {submitErr && <div style={warningStyle}>{submitErr}</div>}
      </div>
    </div>
  );
}

function ConfirmView({ result }) {
  if (result.missing && result.missing.length > 0) {
    return (
      <div style={confirmStyle}>
        <div style={{ color: amber, marginBottom: 8 }}>
          I read this as a <b>{result.kind}</b> paste, but I did not find:
        </div>
        <ul data-testid="parse-missing-fields" style={{ margin: 0, paddingLeft: 20 }}>
          {result.missing.map((f) => <li key={f} style={{ color: oxblood }}>{f}</li>)}
        </ul>
        <div style={{ color: grey, fontSize: 12, marginTop: 8 }}>
          Fill the manual fields below, or paste again with the missing labels.
          Ask again is the estate's default when it cannot read.
        </div>
      </div>
    );
  }
  return (
    <div style={confirmStyle}>
      <div style={{ color: sage, marginBottom: 8 }}>
        I read this as a <b>{result.kind}</b> paste. Confirm:
      </div>
      <table style={{ width: "100%", fontSize: 13, borderCollapse: "collapse" }}>
        <tbody>
          {Object.entries(result.fields).map(([k, v]) => (
            <tr key={k}>
              <td style={{ color: grey, paddingRight: 8, verticalAlign: "top" }}>{k}</td>
              <td style={{ fontFamily: "monospace" }}>{String(v)}</td>
            </tr>
          ))}
          {result.password_captured && (
            <tr>
              <td style={{ color: grey, paddingRight: 8 }}>password</td>
              <td data-testid="parsed-password-captured" style={{ fontFamily: "monospace" }}>•••• captured</td>
            </tr>
          )}
          {result.aws_secret_captured && (
            <tr>
              <td style={{ color: grey, paddingRight: 8 }}>aws_secret_access_key</td>
              <td data-testid="parsed-aws-secret-captured" style={{ fontFamily: "monospace" }}>•••• captured</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function DataSourceResult({ result }) {
  const ok = result.link_working && result.ready;
  const border = ok ? sage : oxblood;
  return (
    <div style={{ padding: 12, borderLeft: `4px solid ${border}`, background: cream, borderRadius: 4 }}>
      <div style={{ marginBottom: 8, color: navy, fontSize: 14, fontWeight: 600 }}>
        {ok ? `Connected to ${result.source_id || "the data source"}.` : "The data connection didn't come up."}
      </div>
      <table style={{ width: "100%", fontSize: 13, borderCollapse: "collapse" }}>
        <tbody>
          <tr>
            <td style={{ color: grey, paddingRight: 8, width: 180 }}>Is the link working?</td>
            <td data-testid="data-link-working" style={{ color: result.link_working ? sage : oxblood }}>
              {result.link_working ? "yes — SELECT 1 returned over the Data API" : "no"}
            </td>
          </tr>
          <tr>
            <td style={{ color: grey, paddingRight: 8, verticalAlign: "top" }}>What did we find?</td>
            <td data-testid="data-source-found" style={{ verticalAlign: "top" }}>
              {result.link_working ? renderFound(result.found) : "—"}
            </td>
          </tr>
          <tr>
            <td style={{ color: grey, paddingRight: 8 }}>Is it ready?</td>
            <td data-testid="data-source-ready" style={{ color: result.ready ? sage : oxblood }}>
              {result.ready ? "yes" : "no"}
            </td>
          </tr>
          <tr>
            <td style={{ color: grey, paddingRight: 8, verticalAlign: "top" }}>Any failure to name?</td>
            <td data-testid="data-source-failure" style={{ verticalAlign: "top" }}>
              {result.failure
                ? <div><b>{result.failure}</b> — {result.failure_sentence}</div>
                : "no"}
            </td>
          </tr>
        </tbody>
      </table>
      <div style={{ color: grey, fontSize: 12, marginTop: 10 }}>
        Engine: {result.engine} · Channel: {result.channel} · Standing creds stored key-custody-locally at {result.creds_path}
      </div>
    </div>
  );
}

function renderFound(found) {
  if (!found || Object.keys(found).length === 0) return "—";
  const schemas = found.schemas || [];
  const tables = found.tables || [];
  return (
    <div>
      <div>
        <b>{schemas.length}</b> schema{schemas.length === 1 ? "" : "s"}:{" "}
        {schemas.slice(0, 6).join(", ")}{schemas.length > 6 ? "…" : ""}
      </div>
      <div>
        <b>{tables.length}</b> table{tables.length === 1 ? "" : "s"} sampled (cap {found.inventory_cap})
        {tables.length > 0 && (
          <ul style={{ margin: "6px 0 0 0", paddingLeft: 20 }}>
            {tables.slice(0, 8).map((t, i) => (
              <li key={i} style={{ fontFamily: "monospace", fontSize: 12 }}>
                {t.schema}.{t.table} <span style={{ color: grey }}>≈ {t.approx_row_count} rows</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}


function HandshakeWalk({ data }) {
  return (
    <div data-testid="handshake-walk">
      {HANDSHAKE_STAGES.map((s) => {
        const stage = (data.stages || {})[s.key] || {};
        const status = stage.status || "untried";
        const border = status === "pass" ? sage : status === "fail" ? oxblood : "#999";
        return (
          <div
            key={s.key}
            data-testid={`handshake-stage-${s.key}`}
            style={{ padding: 8, borderLeft: `4px solid ${border}`, margin: "6px 0", background: cream }}
          >
            <b>{s.label}</b> <span style={{ color: grey }}>· {status}</span>
            {stage.detail && <div style={{ fontSize: 12, color: "#333" }}>{stage.detail}</div>}
          </div>
        );
      })}
      <div style={{ fontSize: 12, color: grey, marginTop: 10 }}>
        Handshake walk from POST /api/connect/gpu — declaration → hardening → acceptance.
      </div>
    </div>
  );
}

function ProvisioningCard({ facts }) {
  if (!facts) {
    return (
      <div data-testid="provisioning-card" style={{ marginTop: 12, color: grey, padding: 12, background: cream, borderRadius: 4 }}>
        Loading provisioning card from /api/connect/estate-facts…
      </div>
    );
  }
  return (
    <div data-testid="provisioning-card" style={{ marginTop: 12, background: cream, padding: 12, border: "1px solid #ccc", borderRadius: 4 }}>
      <div style={{ fontSize: 12, color: grey, marginBottom: 6 }}>What to paste on the AISCA side (VM creation form):</div>
      <div style={{ marginBottom: 4, wordBreak: "break-all" }}>
        <b>Public key:</b>{" "}
        <code data-testid="provisioning-card-public-key" style={{ fontSize: 12 }}>{facts.estate_public_key}</code>
      </div>
      <div style={{ marginBottom: 4 }}>
        <b>Pod egress IP:</b>{" "}
        <code data-testid="provisioning-card-egress-ip" style={{ fontSize: 12 }}>{facts.pod_egress_ip}</code>
      </div>
      <div>
        <b>Fingerprint:</b>{" "}
        <code data-testid="provisioning-card-fingerprint" style={{ fontSize: 12 }}>{facts.estate_public_key_fingerprint}</code>
      </div>
    </div>
  );
}
