import React, { useState } from "react";
import axios from "axios";

/**
 * AdminSurface — the ONE governed surface (Owner stop-order 2026-08-14).
 *
 * Shape (fixture grammar):
 *   root (/) → top tab bar [Work · Build · 3rd Party Apps · … Admin]
 *              (Admin right-aligned, selected by default)
 *   → tile grid: TRUST CENTER (4 tiles) + REGISTRY (4 tiles)
 *   → click Connect tile → GPU form renders in the detail card.
 *
 * Access control lives at the source-IP allowlist middleware. This
 * component carries NO token machinery, NO sign-in card, NO localStorage.
 */
const BACKEND = process.env.REACT_APP_BACKEND_URL;

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
      { name: "Connect", icon: "⇌" },
    ],
  },
];

// Explicit testid mapping — invariants pin literal strings (not
// template-computed) so grep-based gating tests can assert them cleanly.
const TILE_TESTIDS = {
  "Manage Rules": "tile-manage-rules",
  "Data Shield": "tile-data-shield",
  "Reasoning Shield": "tile-reasoning-shield",
  "Access Shield": "tile-access-shield",
  "Data Estate": "tile-data-estate",
  "Models": "tile-models",
  "Compute": "tile-compute",
  "Connect": "tile-connect",
};

export default function AdminSurface() {
  const [selected, setSelected] = useState("Connect");

  return (
    <div style={{ minHeight: "100vh", background: cream, padding: "40px 60px", fontFamily: "ui-sans-serif" }}>
      <div style={{ display: "flex", gap: 40 }}>
        {/* LEFT PANE — top tab bar + tile grid */}
        <div style={{ flex: "0 0 45%" }}>
          <div style={{ display: "flex", gap: 12, marginBottom: 32 }} data-testid="top-tab-bar">
            <div style={{ padding: "6px 14px", background: cardWhite, borderRadius: 999, fontSize: 13, color: grey }}>Work</div>
            <div style={{ padding: "6px 14px", background: cardWhite, borderRadius: 999, fontSize: 13, color: grey }}>Build</div>
            <div style={{ padding: "6px 14px", background: cardWhite, borderRadius: 999, fontSize: 13, color: grey }}>3rd Party Apps</div>
            <div style={{ flex: 1 }} />
            <div style={{ padding: "6px 14px", background: navy, color: cardWhite, borderRadius: 999, fontSize: 13 }} data-testid="admin-pill">Admin</div>
          </div>
          {GROUPS.map((g) => (
            <div key={g.label} style={{ marginBottom: 36 }} data-testid={`tile-group-${g.label.toLowerCase().replace(/\s+/g, "-")}`}>
              <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>{g.label}</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 12 }}>
                {g.tiles.map((t) => (
                  <TileButton
                    key={t.name}
                    tile={t}
                    testid={TILE_TESTIDS[t.name]}
                    isSelected={t.name === selected}
                    onSelect={() => setSelected(t.name)}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* RIGHT PANE — detail card */}
        <div style={{ flex: "0 0 55%" }} data-testid="detail-card">
          <div style={{ background: cardWhite, borderRadius: 16, padding: "36px 44px" }}>
            {selected === "Connect" ? <ConnectGpuDetail /> : <PlaceholderDetail selected={selected} />}
          </div>
        </div>
      </div>
    </div>
  );
}

function TileButton({ tile, testid, isSelected, onSelect }) {
  return (
    <button
      type="button"
      data-testid={testid}
      onClick={onSelect}
      style={{
        background: isSelected ? cardWhite : cream,
        border: isSelected ? `1px solid ${navy}` : `1px solid #ddd`,
        borderRadius: 12, padding: "24px 8px", cursor: "pointer",
        display: "flex", flexDirection: "column", alignItems: "center", gap: 12,
      }}
    >
      <div style={{
        width: 40, height: 40, borderRadius: isSelected ? 10 : 999,
        background: isSelected ? lavender : "#eee",
        display: "flex", alignItems: "center", justifyContent: "center",
        color: navy, fontSize: 20,
      }}>{tile.icon}</div>
      <div style={{ fontSize: 13, color: navy }}>{tile.name}</div>
    </button>
  );
}

function PlaceholderDetail({ selected }) {
  return (
    <>
      <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a5aae", marginBottom: 12 }}>REGISTRY / TRUST CENTER</div>
      <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 36, margin: 0, color: navy }}>{selected}</h1>
      <p style={{ color: grey, marginTop: 20, lineHeight: 1.5 }}>
        This tile is a placeholder in the current build. The Connect tile
        accepts the one wired connection type (GPU).
      </p>
    </>
  );
}

function ConnectGpuDetail() {
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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const onChange = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const retry = () => { setAfterState(null); setError(""); };

  const submit = async (e) => {
    e.preventDefault();
    setSubmitting(true); setError(""); setAfterState(null);
    try {
      const resp = await axios.post(`${BACKEND}/api/connect/gpu`, form);
      setAfterState(resp.data);
      setForm((f) => ({ ...f, password: "" }));
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a5aae", marginBottom: 12 }}>REGISTRY</div>
      <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: 0, color: navy }}>Connect · GPU</h1>
      {!afterState && (
        <>
          <p style={{ color: grey, marginTop: 20, lineHeight: 1.5 }}>
            Enter the vendor-issued bootstrap credentials once. On submit the estate installs its key,
            disables password auth, retires the bootstrap, and runs acceptance against the §6 spec.
            The password is not stored anywhere and cannot be retrieved after submit.
          </p>
          <hr style={{ margin: "24px 0", border: "none", borderTop: "1px solid #eee" }} />
          <form onSubmit={submit} data-testid="connect-gpu-form">
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
            </div>
          </form>
        </>
      )}
      {afterState && <AfterState state={afterState} onRetry={retry} />}
    </>
  );
}

function AfterState({ state, onRetry }) {
  const a = state.after_state || {};
  const cls = a.state_class;
  const border =
    cls === "green" ? "#2e7d32" :
    cls === "failed" ? oxblood :
    cls === "held" ? amber : grey;
  return (
    <div data-testid="connect-gpu-after-state" style={{ marginTop: 24 }}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a5aae", marginBottom: 8 }}>AFTER STATE · {cls?.toUpperCase()}</div>
      <div style={{ borderLeft: `4px solid ${border}`, paddingLeft: 20 }}>
        <FourQuestions a={a} />
      </div>
      <hr style={{ margin: "24px 0", border: "none", borderTop: "1px solid #eee" }} />
      <div style={{ fontSize: 12, color: grey, marginBottom: 6 }}>
        Commissioning record: <code style={{ fontSize: 11 }}>{state.commissioning_record_path}</code>
      </div>
      <div style={{ fontSize: 12, color: grey }}>
        Data movement permitted: <strong>{String(state.data_movement_permitted)}</strong>
      </div>
      <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
        {cls === "failed" && (
          <button type="button" onClick={onRetry} data-testid="connect-gpu-retry"
            style={{ padding: "12px 28px", background: navy, color: cardWhite,
                     border: "none", borderRadius: 999, cursor: "pointer", fontSize: 14 }}>Retry</button>
        )}
        {cls === "held" && (
          <div data-testid="connect-gpu-held-note" style={{ fontSize: 13, color: amber }}>
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
          <div style={{ fontSize: 15, color: navy, lineHeight: 1.5 }} data-testid={`four-q-${q.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
            {ans || "not yet measured"}
          </div>
        </div>
      ))}
    </div>
  );
}
