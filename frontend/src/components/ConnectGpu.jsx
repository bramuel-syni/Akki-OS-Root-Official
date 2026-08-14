import React, { useEffect, useState } from "react";
import axios from "axios";

const BACKEND = process.env.REACT_APP_BACKEND_URL;

/* --- fixture grammar helpers --- */
const cream = "#f6f2ea";
const navy = "#1c2b45";
const lavender = "#c9c6e5";
const oxblood = "#5a1a1a";
const amber = "#c98a1c";
const grey = "#666";
const cardWhite = "#ffffff";

const GROUPS = [
  {
    label: "TRUST CENTER",
    tiles: [
      { name: "Manage Rules", icon: "◐" },
      { name: "Data Shield", icon: "◇" },
      { name: "Reasoning Shield", icon: "◈" },
      { name: "Access Shield", icon: "◉" },
    ],
  },
  {
    label: "REGISTRY",
    tiles: [
      { name: "Data Estate", icon: "▤" },
      { name: "Models", icon: "☰" },
      { name: "Compute", icon: "⚙" },
      { name: "Connect", icon: "⇌", detail: "connect_gpu" },
    ],
  },
];

export default function ConnectGpu() {
  const [selected, setSelected] = useState("Connect");
  const [token, setToken] = useState(() => localStorage.getItem("owner_token") || "");
  const [enteredToken, setEnteredToken] = useState("");
  const [afterState, setAfterState] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    host_name: "",
    username: "",
    password: "",
    public_ip: "",
    private_ip: "",
    os: "",
    deploy_date: new Date().toISOString().slice(0, 10),
  });

  const saveToken = () => {
    localStorage.setItem("owner_token", enteredToken.trim());
    setToken(enteredToken.trim());
    setEnteredToken("");
  };

  const clearToken = () => {
    localStorage.removeItem("owner_token");
    setToken("");
  };

  const onChange = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    setAfterState(null);
    try {
      const resp = await axios.post(`${BACKEND}/api/connect/gpu`, form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAfterState(resp.data);
      // Password never re-echoed. Clear from form immediately.
      setForm((f) => ({ ...f, password: "" }));
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const retry = () => {
    setAfterState(null);
    setError("");
  };

  // Auth gate
  if (!token) {
    return (
      <div style={{ minHeight: "100vh", background: cream, padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
        <div style={{ maxWidth: 480, margin: "0 auto", background: cardWhite, padding: "40px", borderRadius: 12 }}>
          <div style={{ fontSize: 12, letterSpacing: 2, color: grey }}>OWNER ACCESS</div>
          <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 34, margin: "12px 0 20px 0", color: navy }}>
            Sign in to the estate
          </h1>
          <p style={{ color: grey, marginBottom: 16, lineHeight: 1.5 }}>
            Paste the owner access token issued for this pod. This is an app login, not a console or VM credential.
          </p>
          <input
            type="password"
            data-testid="owner-token-input"
            value={enteredToken}
            onChange={(e) => setEnteredToken(e.target.value)}
            placeholder="owner access token"
            style={{ width: "100%", padding: "12px 14px", borderRadius: 8, border: `1px solid ${grey}`, fontSize: 16 }}
          />
          <button
            type="button"
            data-testid="owner-token-submit"
            onClick={saveToken}
            disabled={!enteredToken.trim()}
            style={{ marginTop: 16, padding: "12px 24px", background: navy, color: cardWhite, border: "none",
                     borderRadius: 999, cursor: "pointer", fontSize: 14, letterSpacing: 0.5 }}
          >
            Enter
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", background: cream, padding: "40px 60px", fontFamily: "ui-sans-serif" }}>
      <div style={{ display: "flex", gap: 40 }}>
        {/* LEFT PANE — tile grid */}
        <div style={{ flex: "0 0 45%" }}>
          <div style={{ display: "flex", gap: 12, marginBottom: 32 }}>
            <div style={{ padding: "6px 14px", background: cardWhite, borderRadius: 999, fontSize: 13, color: grey }}>Work</div>
            <div style={{ padding: "6px 14px", background: cardWhite, borderRadius: 999, fontSize: 13, color: grey }}>Build</div>
            <div style={{ padding: "6px 14px", background: cardWhite, borderRadius: 999, fontSize: 13, color: grey }}>3rd Party Apps</div>
            <div style={{ flex: 1 }} />
            <div style={{ padding: "6px 14px", background: navy, color: cardWhite, borderRadius: 999, fontSize: 13 }} data-testid="admin-pill">Admin</div>
          </div>
          {GROUPS.map((g) => (
            <div key={g.label} style={{ marginBottom: 36 }}>
              <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>{g.label}</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 12 }}>
                {g.tiles.map((t) => {
                  const isSel = t.name === selected;
                  return (
                    <button
                      key={t.name}
                      type="button"
                      data-testid={`tile-${t.name.toLowerCase().replace(/\s+/g, "-")}`}
                      onClick={() => setSelected(t.name)}
                      style={{
                        background: isSel ? cardWhite : cream,
                        border: isSel ? `1px solid ${navy}` : `1px solid #ddd`,
                        borderRadius: 12, padding: "24px 8px", cursor: "pointer",
                        display: "flex", flexDirection: "column", alignItems: "center", gap: 12,
                      }}
                    >
                      <div style={{
                        width: 40, height: 40, borderRadius: isSel ? 10 : 999,
                        background: isSel ? lavender : "#eee",
                        display: "flex", alignItems: "center", justifyContent: "center",
                        color: navy, fontSize: 20,
                      }}>{t.icon}</div>
                      <div style={{ fontSize: 13, color: navy }}>{t.name}</div>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* RIGHT PANE — detail card */}
        <div style={{ flex: "0 0 55%" }}>
          <div style={{ background: cardWhite, borderRadius: 16, padding: "36px 44px" }}>
            <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a5aae", marginBottom: 12 }}>REGISTRY</div>
            <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: 0, color: navy }}>Connect · GPU</h1>

            {selected !== "Connect" && (
              <>
                <p style={{ color: grey, marginTop: 20, lineHeight: 1.5 }}>
                  Select the <strong>Connect</strong> tile to enter GPU credentials.
                </p>
                <p style={{ color: grey, fontSize: 13, marginTop: 12 }}>
                  This surface accepts one connection type. Other tiles are placeholders in this build.
                </p>
              </>
            )}

            {selected === "Connect" && !afterState && (
              <>
                <p style={{ color: grey, marginTop: 20, lineHeight: 1.5 }}>
                  Enter the vendor-issued bootstrap credentials once. On submit the estate installs its key,
                  disables password auth, retires the bootstrap, and runs acceptance against the §6 spec.
                  The password is not stored anywhere and cannot be retrieved after submit.
                </p>
                <hr style={{ margin: "24px 0", border: "none", borderTop: "1px solid #eee" }} />
                <form onSubmit={submit}>
                  {[
                    ["host_name", "Host Name", "text", true],
                    ["username", "Username", "text", true],
                    ["password", "Password", "password", true],
                    ["public_ip", "Public IP", "text", true],
                    ["private_ip", "Private IP (optional)", "text", false],
                    ["os", "OS (optional)", "text", false],
                    ["deploy_date", "Deploy date (pins +14d)", "date", false],
                  ].map(([k, label, type, req]) => (
                    <div key={k} style={{ marginBottom: 14 }}>
                      <label style={{ display: "block", fontSize: 12, color: grey, marginBottom: 6 }}>{label}</label>
                      <input
                        data-testid={`connect-gpu-${k}`}
                        type={type}
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
                  <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
                    <button type="submit" disabled={submitting} data-testid="connect-gpu-submit"
                      style={{ padding: "12px 28px", background: navy, color: cardWhite, border: "none",
                               borderRadius: 999, cursor: "pointer", fontSize: 14, letterSpacing: 0.4 }}>
                      {submitting ? "Working…" : "Submit"}
                    </button>
                    <button type="button" onClick={clearToken} data-testid="connect-gpu-signout"
                      style={{ padding: "12px 20px", background: "transparent", color: navy,
                               border: `1px solid ${navy}`, borderRadius: 999, cursor: "pointer", fontSize: 14 }}>
                      Sign out
                    </button>
                  </div>
                </form>
              </>
            )}

            {selected === "Connect" && afterState && (
              <AfterState state={afterState} onRetry={retry} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function AfterState({ state, onRetry }) {
  const a = state.after_state || {};
  const cls = a.state_class;
  const border =
    cls === "green" ? "#2e7d32" :
    cls === "failed" ? "#5a1a1a" :
    cls === "held" ? "#c98a1c" : "#666";
  return (
    <div data-testid="connect-gpu-after-state" style={{ marginTop: 24 }}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a5aae", marginBottom: 8 }}>AFTER STATE · {cls?.toUpperCase()}</div>
      <div style={{ borderLeft: `4px solid ${border}`, paddingLeft: 20 }}>
        <FourQuestions a={a} />
      </div>
      <hr style={{ margin: "24px 0", border: "none", borderTop: "1px solid #eee" }} />
      <div style={{ fontSize: 12, color: "#666", marginBottom: 6 }}>
        Commissioning record: <code style={{ fontSize: 11 }}>{state.commissioning_record_path}</code>
      </div>
      <div style={{ fontSize: 12, color: "#666" }}>
        Data movement permitted: <strong>{String(state.data_movement_permitted)}</strong>
      </div>
      <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
        {cls === "failed" && (
          <button type="button" onClick={onRetry} data-testid="connect-gpu-retry"
            style={{ padding: "12px 28px", background: "#1c2b45", color: "#fff",
                     border: "none", borderRadius: 999, cursor: "pointer", fontSize: 14 }}>Retry</button>
        )}
        {cls === "held" && (
          <div data-testid="connect-gpu-held-note" style={{ fontSize: 13, color: "#c98a1c" }}>
            Escalated to the vendor · nothing further to click here.
          </div>
        )}
      </div>
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
        <div key={q} style={{ marginBottom: 14 }}>
          <div style={{ fontSize: 11, letterSpacing: 1.5, color: "#888", marginBottom: 4 }}>{q.toUpperCase()}</div>
          <div style={{ fontSize: 15, color: "#1c2b45", lineHeight: 1.5 }} data-testid={`four-q-${q.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
            {ans || "not yet measured"}
          </div>
        </div>
      ))}
    </div>
  );
}
