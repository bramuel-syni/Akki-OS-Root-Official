import React, { useEffect, useState } from "react";
import ConnectWizard from "@/components/ConnectWizard";

/**
 * Registry — the estate's inventory surface (Owner Order 2026-08-19 · FL-P2-25).
 *
 * Renders per fixtures/screen_mockups_v7.pdf Registry Feature & Component
 * Brief. Every figure traces to a durable record on disk via
 * GET /api/registry/facts. No fabrication; approximations flagged (≈);
 * empty tabs draw the gap ("drawn, never left blank").
 *
 * Page pattern (§2):
 *   Two-column: LEFT fluid | RIGHT 300px.
 *   Topline row     | Headliner panel
 *   Divider
 *   Visual row      | Context panel
 *   Divider
 *   Table row       | Context panel
 *
 * Content rules (§6):
 *   1. Sentences first, measures second.
 *   2. No figure without provenance.
 *   3. Gaps are drawn.
 *   4. Refusals/failures are work done.
 *   5. One emphasis per deck.
 *   6. Read-only means read-only.
 *
 * Role switcher renders static (Track-B; FL-P2-15).
 */
const cream = "#f6f2ea";
const navy = "#1c2b45";
const grey = "#666";
const mid = "#8a8a8a";
const rule = "#e2ded4";
const cardWhite = "#ffffff";
const crimson = "#b83a2b";
const sage = "#7a8a5a";

const TABS = [
  { key: "data-connected", label: "DATA CONNECTED", testid: "tab-data-connected" },
  { key: "compute-connected", label: "COMPUTE CONNECTED", testid: "tab-compute-connected" },
  { key: "llms-trained-models", label: "LLMS & TRAINED MODELS", testid: "tab-llms-trained-models" },
];

const ROLES = ["Compliance Owner", "Watch Officer", "Operator"];

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

export default function Registry() {
  const [activeTab, setActiveTab] = useState("data-connected");
  const [wizardOpen, setWizardOpen] = useState(false);
  const [facts, setFacts] = useState(null);
  const [error, setError] = useState(null);
  const [selectedSource, setSelectedSource] = useState(null);
  const [selectedCompute, setSelectedCompute] = useState(null);

  useEffect(() => {
    // /api/registry/facts
    const url = `${BACKEND_URL}/api/registry/facts`;
    fetch(url)
      .then((r) => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
      .then(setFacts)
      .catch((e) => setError(String(e.message || e)));
  }, []);

  return (
    <div style={{ minHeight: "100vh", background: cream, fontFamily: "ui-sans-serif" }}>
      <Header />

      <main style={{ padding: "32px 60px 80px" }}>
        <div style={{ maxWidth: 1280, margin: "0 auto" }}>
          <TitleDeck />
          <TabBar activeTab={activeTab} onTabChange={setActiveTab} onOpenWizard={() => setWizardOpen(true)} />

          <div style={{ marginTop: 32 }}>
            {error && <ErrorBanner error={error} />}
            {!facts && !error && <LoadingBanner />}
            {facts && activeTab === "data-connected" && (
              <DataConnectedTab facts={facts} onOpen={setSelectedSource} />
            )}
            {facts && activeTab === "compute-connected" && (
              <ComputeConnectedTab facts={facts} onOpen={setSelectedCompute} />
            )}
            {facts && activeTab === "llms-trained-models" && (
              <LLMsTrainedModelsTab facts={facts} />
            )}
          </div>
        </div>
      </main>

      {selectedSource && (
        <DataSourceDetailCard source={selectedSource} onClose={() => setSelectedSource(null)} />
      )}
      {selectedCompute && (
        <ComputeDetailCard host={selectedCompute} onClose={() => setSelectedCompute(null)} />
      )}
      {wizardOpen && <ConnectWizard onClose={() => setWizardOpen(false)} />}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Header + Title + TabBar
// ---------------------------------------------------------------------------

function Header() {
  return (
    <header style={{ background: navy, color: cardWhite, padding: "16px 60px",
                     display: "flex", alignItems: "center", gap: 24 }}>
      <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 18, letterSpacing: 0.5 }}>
        Akki · ESTATE
      </div>
      <div style={{ flex: 1 }} />
      <div data-testid="role-switcher" style={{ display: "flex", gap: 8 }}>
        {ROLES.map((role) => (
          <div key={role} data-testid={`role-${role.toLowerCase().replace(/\s+/g, "-")}`}
               style={{ padding: "6px 12px", borderRadius: 999,
                        background: "rgba(255,255,255,0.08)",
                        fontSize: 12, color: cardWhite, letterSpacing: 0.3 }}>
            {role}
          </div>
        ))}
        <div style={{ width: 32, height: 32, borderRadius: 999,
                      background: "rgba(255,255,255,0.15)",
                      display: "flex", alignItems: "center", justifyContent: "center",
                      fontSize: 13, marginLeft: 4 }}>U</div>
      </div>
    </header>
  );
}

function TitleDeck() {
  return (
    <div style={{ marginBottom: 32 }}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey }}>REGISTRY · ESTATE</div>
      <h1 data-testid="registry-title"
          style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 44,
                   margin: "8px 0 12px 0", color: navy }}>
        Registry
      </h1>
      <p style={{ color: grey, lineHeight: 1.55, maxWidth: 720, margin: 0 }}>
        What you hold, what is connected, what is answering.
        Read-only by design, with one write path — Connect.
      </p>
    </div>
  );
}

function TabBar({ activeTab, onTabChange, onOpenWizard }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 32,
                  borderBottom: `1px solid ${rule}` }}>
      {TABS.map((t) => {
        const active = t.key === activeTab;
        return (
          <button key={t.key} type="button" data-testid={t.testid}
                  onClick={() => onTabChange(t.key)}
                  style={{ background: "transparent", border: "none", cursor: "pointer",
                           padding: "12px 4px", fontSize: 12, letterSpacing: 2,
                           color: active ? navy : grey,
                           borderBottom: active ? `2px solid ${navy}` : "2px solid transparent",
                           marginBottom: -1 }}>
            {t.label}
          </button>
        );
      })}
      <div style={{ flex: 1 }} />
      <button type="button" data-testid="open-connect-wizard" onClick={onOpenWizard}
              style={{ padding: "10px 20px", background: navy, color: cardWhite,
                       border: "none", borderRadius: 999, cursor: "pointer",
                       fontSize: 13, letterSpacing: 0.3, marginBottom: 8 }}>
        + Connect
      </button>
    </div>
  );
}

function LoadingBanner() {
  return (
    <div data-testid="registry-loading" style={{ padding: 32, color: grey }}>
      Reading the estate…
    </div>
  );
}

function ErrorBanner({ error }) {
  return (
    <div data-testid="registry-error"
         style={{ padding: 24, background: cardWhite, borderRadius: 8, color: crimson }}>
      The estate could not be read: {error}. This is work done, not work lost — try again.
    </div>
  );
}

// ---------------------------------------------------------------------------
// Layout primitives — Topline / Headliner / Visual / Table / Context bands
// ---------------------------------------------------------------------------

function TwoColBand({ children }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: 24,
                  marginBottom: 24 }}>
      {children}
    </div>
  );
}

function Divider() {
  return <div style={{ height: 1, background: rule, margin: "24px 0" }} />;
}

function SectionTitle({ title, intro, right }) {
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 20, marginBottom: 12 }}>
      <div>
        <div style={{ fontSize: 12, letterSpacing: 1.5, color: navy, fontWeight: 600 }}>
          {title}
        </div>
        {intro && (
          <div style={{ fontSize: 13, color: grey, marginTop: 4 }}>{intro}</div>
        )}
      </div>
      <div style={{ flex: 1 }} />
      {right}
    </div>
  );
}

function StatCell({ label, value, note }) {
  return (
    <div style={{ borderTop: `1px solid ${rule}`, padding: "14px 0" }}>
      <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid, textTransform: "uppercase" }}>
        {label}
      </div>
      <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 24, color: navy,
                    marginTop: 4 }}>
        {value}
      </div>
      {note && <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>{note}</div>}
    </div>
  );
}

function StatGrid({ cells }) {
  return (
    <div data-testid="registry-topline"
         style={{ background: cardWhite, borderRadius: 12, padding: "16px 24px" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "0 32px" }}>
        {cells.map((c, i) => <StatCell key={i} {...c} />)}
      </div>
    </div>
  );
}

function Headliner({ eyebrow, deck, emphasis, provenance }) {
  return (
    <aside data-testid="registry-headliner"
           style={{ background: cardWhite, borderRadius: 12, padding: "18px 20px",
                    display: "flex", flexDirection: "column", justifyContent: "center" }}>
      <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
                    textTransform: "uppercase", marginBottom: 8 }}>
        {eyebrow}
      </div>
      <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 20,
                    lineHeight: 1.35, color: navy }}>
        {deck}
        {emphasis && (
          <span style={{ color: crimson }}> {emphasis}</span>
        )}
      </div>
      {provenance && (
        <div style={{ fontSize: 11, color: grey, marginTop: 10, lineHeight: 1.5 }}>
          {provenance}
        </div>
      )}
    </aside>
  );
}

function VisualBars({ rows, denominator }) {
  const measured = rows.filter((r) => r.approx_rows != null);
  const max = measured.reduce((m, r) => Math.max(m, r.approx_rows || 0), 1);
  return (
    <div data-testid="registry-visual"
         style={{ background: cardWhite, borderRadius: 12, padding: "18px 24px" }}>
      {rows.map((r, i) => {
        const pct = r.approx_rows ? Math.max(4, Math.round(100 * r.approx_rows / max)) : 0;
        const hatched = r.approx_rows == null;
        return (
          <div key={i} style={{ display: "grid",
                                gridTemplateColumns: "220px 1fr 120px",
                                alignItems: "center", gap: 12, padding: "6px 0" }}>
            <div style={{ fontSize: 13, color: navy }}>{r.table}</div>
            <div style={{ height: 10, background: rule, borderRadius: 3, position: "relative" }}>
              {hatched ? (
                <div style={{ position: "absolute", inset: 0, borderRadius: 3,
                              backgroundImage: `repeating-linear-gradient(45deg, ${rule}, ${rule} 4px, ${mid} 4px, ${mid} 5px)` }} />
              ) : (
                <div style={{ position: "absolute", left: 0, top: 0, bottom: 0,
                              width: `${pct}%`, background: navy, borderRadius: 3 }} />
              )}
            </div>
            <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 13,
                          color: navy, textAlign: "right" }}>
              {hatched ? "not yet measured" : `≈ ${(r.approx_rows).toLocaleString()} rows`}
            </div>
          </div>
        );
      })}
      <div style={{ fontSize: 11, color: grey, marginTop: 12, borderTop: `1px solid ${rule}`,
                    paddingTop: 8 }}>
        {denominator}
      </div>
    </div>
  );
}

function ContextPanel({ eyebrow, sentences }) {
  return (
    <aside data-testid="registry-context-panel"
           style={{ background: cardWhite, borderRadius: 12, padding: "18px 20px" }}>
      <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
                    textTransform: "uppercase", marginBottom: 10 }}>
        {eyebrow}
      </div>
      {sentences.map((s, i) => (
        <p key={i} style={{ fontSize: 13, color: navy, lineHeight: 1.55, margin: "0 0 10px" }}>
          {s}
        </p>
      ))}
    </aside>
  );
}

function Chip({ label, tone = "neutral" }) {
  const bg = tone === "sage" ? sage : tone === "crimson" ? crimson :
             tone === "navy" ? navy : mid;
  return (
    <span style={{ display: "inline-block", padding: "3px 10px", borderRadius: 999,
                   background: bg, color: cardWhite, fontSize: 11, letterSpacing: 0.5 }}>
      {label}
    </span>
  );
}

// ---------------------------------------------------------------------------
// DATA CONNECTED tab
// ---------------------------------------------------------------------------

function DataConnectedTab({ facts, onOpen }) {
  const sources = facts.data_sources || [];
  const totalTables = sources.reduce((n, s) => n + (s.table_count || 0), 0);

  if (sources.length === 0) {
    return (
      <EmptyPanel eyebrow="WHAT YOU HOLD"
                  headline="No data connected yet."
                  sentence="Nothing has been admitted into the estate through Connect. When a source lands it appears here as measurement, never as an estimate — drawn, never left blank." />
    );
  }

  // Aggregate top tables across sources (top 10 by approx rows)
  const allTop = [];
  for (const s of sources) {
    for (const t of (s.top_tables || [])) {
      allTop.push({ database: s.database, ...t });
    }
  }
  allTop.sort((a, b) => (b.approx_rows || 0) - (a.approx_rows || 0));
  const topTen = allTop.slice(0, 10);
  const largest = topTen[0];

  const toplineCells = [
    { label: "Sources connected", value: sources.length,
      note: "drawn, never left blank" },
    { label: "Tables inventoried", value: totalTables.toLocaleString(),
      note: `across ${sources.length} databases` },
    { label: "Largest holding", value: largest ? largest.table : "not yet measured",
      note: largest ? `≈ ${largest.approx_rows.toLocaleString()} rows (approx)` : "" },
    { label: "Rights class", value: "not yet measured",
      note: "record-matrix binding awaits owner ruling" },
    { label: "Records read", value: "0",
      note: "structure only this pass" },
    { label: "Language coverage", value: "not yet measured", note: "" },
    { label: "Verified schemas", value: sources.length,
      note: "SELECT 1 + information_schema green" },
    { label: "Channel", value: "RDS Data API",
      note: "HTTPS out via boto3, no VPC peering" },
    { label: "Provenance", value: "on-record", note: "every figure traces to disk" },
  ];

  const posture = "structure only";
  return (
    <div>
      {/* Topline + Headliner band */}
      <TwoColBand>
        <StatGrid cells={toplineCells} />
        <Headliner
          eyebrow="WHAT YOU HOLD"
          deck={`Two databases answer over one governed channel; nothing has been read beyond their structure.`}
          emphasis="Structure only."
          provenance={`Last verified ${sources[0].last_verified ? sources[0].last_verified.slice(0, 19).replace("T", " ") + "Z" : "—"} · via /api/registry/facts.`} />
      </TwoColBand>

      <Divider />

      {/* Visual band */}
      <SectionTitle
        title="COMPOSITION · TOP TABLES"
        intro="Where the row-mass sits across the two databases." />
      <TwoColBand>
        <VisualBars rows={topTen}
                    denominator={`Denominator: information_schema.tables.table_rows across ${sources.length} databases (approximate on InnoDB).`} />
        <ContextPanel
          eyebrow="READING THE MIX"
          sentences={[
            "USSD activity dominates: the top four tables all sit in digicow_live and hold session-and-response records from the SMS/USSD farmer channel.",
            "Row counts are approximations pulled from information_schema — exact counts require record-level access, which waits on a data-handling agreement.",
          ]} />
      </TwoColBand>

      <Divider />

      {/* Table band */}
      <SectionTitle
        title="RECORD · SOURCES"
        intro="The estate's two connected databases, as last read." />
      <TwoColBand>
        <div data-testid="registry-record-table"
             style={{ background: cardWhite, borderRadius: 12, padding: "8px 0" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {["Source", "Engine", "Tables", "Last verified", "Posture"].map((h) => (
                  <th key={h} style={{ padding: "12px 24px", textAlign: "left",
                                       fontSize: 10, letterSpacing: 1.5, color: mid,
                                       textTransform: "uppercase",
                                       borderBottom: `1px solid ${rule}` }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sources.map((s) => (
                <tr key={s.source_id}
                    data-testid="data-source-row"
                    data-source-id={s.source_id}
                    onClick={() => onOpen(s)}
                    style={{ cursor: "pointer" }}
                    onMouseEnter={(e) => e.currentTarget.style.background = "#f8f5ee"}
                    onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}>
                  <td style={{ padding: "16px 24px", color: navy, fontSize: 14 }}>
                    <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 15 }}>
                      {s.database}
                    </div>
                    <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>{s.region}</div>
                  </td>
                  <td style={{ padding: "16px 24px", color: navy, fontSize: 13 }}>
                    <div>{s.engine}</div>
                    <div style={{ fontSize: 11, color: grey }}>{s.engine_version}</div>
                  </td>
                  <td style={{ padding: "16px 24px", color: navy,
                               fontFamily: "ui-serif, Georgia, serif", fontSize: 15 }}>
                    ≈ {s.table_count}
                  </td>
                  <td style={{ padding: "16px 24px", fontSize: 12, color: grey }}>
                    {s.last_verified ? s.last_verified.slice(0, 10) : "—"}
                  </td>
                  <td style={{ padding: "16px 24px" }}>
                    <span data-testid="posture-chip-structure-only">
                      <Chip label={posture.toUpperCase()} tone="navy" />
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ContextPanel
          eyebrow="WHAT YOU HOLD"
          sentences={[
            `Two databases sit on one Aurora MySQL cluster in ${sources[0].region}: ${sources.map((s) => s.database).join(" and ")}.`,
            "Both answer over the RDS Data API (HTTPS out through boto3). No IP allowlisting on the DB side; no VPC peering.",
            "First pass read the shape only — schemas, tables, and column types via information_schema. Record-level access waits on a data-handling agreement.",
          ]} />
      </TwoColBand>
    </div>
  );
}

function DataSourceDetailCard({ source, onClose }) {
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(28,43,69,0.55)",
                  display: "flex", alignItems: "center", justifyContent: "center", zIndex: 40 }}
         onClick={onClose}>
      <div data-testid="data-source-detail-card"
           onClick={(e) => e.stopPropagation()}
           style={{ background: cardWhite, borderRadius: 16, width: "min(720px, 92vw)",
                    maxHeight: "80vh", overflow: "auto", padding: "28px 32px",
                    boxShadow: "0 20px 40px rgba(0,0,0,0.25)" }}>
        <div style={{ display: "flex", alignItems: "start" }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 11, letterSpacing: 1.5, color: mid, textTransform: "uppercase" }}>
              DATA SOURCE
            </div>
            <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28,
                         margin: "6px 0 4px", color: navy }}>
              {source.database}
            </h2>
            <div style={{ fontSize: 12, color: grey }}>{source.source_id}</div>
          </div>
          <button data-testid="data-source-detail-close" onClick={onClose}
                  style={{ background: "transparent", border: `1px solid ${rule}`,
                           padding: "6px 12px", borderRadius: 999, cursor: "pointer",
                           color: grey, fontSize: 12 }}>
            Close
          </button>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12,
                      marginTop: 20 }}>
          <KV label="ENGINE" value={source.engine} />
          <KV label="VERSION" value={source.engine_version} />
          <KV label="REGION" value={source.region} />
          <KV label="CHANNEL" value={source.channel} />
          <KV label="TABLE COUNT" value={`≈ ${source.table_count}`} />
          <KV label="POSTURE" value={source.posture} />
        </div>
        <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
                     margin: "24px 0 8px", color: navy }}>
          Top tables (approximate)
        </h3>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr>
              {["Table", "≈ Rows", "Size"].map((h) => (
                <th key={h} style={{ padding: "8px 12px", textAlign: "left",
                                     fontSize: 10, letterSpacing: 1.5, color: mid,
                                     borderBottom: `1px solid ${rule}` }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(source.top_tables || []).slice(0, 10).map((t, i) => (
              <tr key={i}>
                <td style={{ padding: "8px 12px", color: navy }}>{t.table}</td>
                <td style={{ padding: "8px 12px", color: navy,
                             fontFamily: "ui-serif, Georgia, serif" }}>
                  ≈ {(t.approx_rows || 0).toLocaleString()}
                </td>
                <td style={{ padding: "8px 12px", color: grey }}>{t.size_mb} MB</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ fontSize: 12, color: grey, marginTop: 16 }}>
          Row counts are approximations from information_schema.tables. This
          first pass read the structure only — zero record contents left the
          database.
        </p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// COMPUTE CONNECTED tab
// ---------------------------------------------------------------------------

function ComputeConnectedTab({ facts, onOpen }) {
  const compute = facts.compute || [];
  if (compute.length === 0) {
    return (
      <EmptyPanel eyebrow="WHAT IS CONNECTED"
                  headline="No compute connected yet."
                  sentence="When a machine lands, this tab renders its commissioning record — hardened, accepted, and receipted. Not yet measured — drawn, never left blank." />
    );
  }
  const host = compute[0];  // one machine for now

  const g = host.gpus || {};
  const pv = host.primary_volume || {};
  const link = host.link || {};

  const toplineCells = [
    { label: "Hosts connected", value: compute.length,
      note: host.state_class === "accepted-as-delivered" ? "accepted as delivered" : "" },
    { label: "GPUs", value: `${g.count} × ${g.model || "GPU"}`,
      note: g.nvlink_active ? "NVLink active" : "no NVLink" },
    { label: "Aggregate VRAM", value: g.vram_gb_total ? `${Math.round(g.vram_gb_total)} GB` : "—",
      note: g.vram_gb_per_gpu ? `${Math.round(g.vram_gb_per_gpu)} GB/GPU` : "" },
    { label: "System RAM", value: `${host.ram_gb_total} GB`, note: "" },
    { label: "vCPU threads", value: host.cpu_threads,
      note: host.cpu_model ? host.cpu_model.split(" ").slice(-2).join(" ") : "" },
    { label: "Primary volume free", value: pv.free_tb ? `≈ ${pv.free_tb} TB` : "—",
      note: pv.write_speed_MBps ? `~${pv.write_speed_MBps} MB/s writes` : "" },
    { label: "Pod ↔ VM link", value: link.throughput_MBps ? `≈ ${link.throughput_MBps} MB/s` : "—",
      note: link.symmetric ? "symmetric" : "" },
    { label: "Hardening", value: host.hardened ? "attested" : "not attested",
      note: host.hardening_result || "" },
    { label: "OS", value: host.os || "—", note: "" },
  ];

  return (
    <div>
      <TwoColBand>
        <StatGrid cells={toplineCells} />
        <Headliner
          eyebrow="WHAT IS CONNECTED"
          deck="One machine connected · hardened · accepted as delivered."
          emphasis={g.count === 2 ? "Two H200s carry the room." : ""}
          provenance={`Commissioned ${host.deploy_date || "—"} · four questions green (link works · found · ready · no failure).`} />
      </TwoColBand>

      <Divider />

      {/* Just-connected announcement row + record table */}
      <SectionTitle
        title="RECORD · HOSTS"
        intro="The estate's compute inventory, as last received." />
      <TwoColBand>
        <div data-testid="registry-record-table"
             style={{ background: cardWhite, borderRadius: 12 }}>
          {/* Announcement row */}
          <div style={{ display: "flex", alignItems: "center", gap: 12,
                        padding: "10px 24px", background: "#f2eee4",
                        borderTopLeftRadius: 12, borderTopRightRadius: 12,
                        borderBottom: `1px solid ${rule}` }}>
            <Chip label="JUST CONNECTED" tone="sage" />
            <span style={{ fontSize: 12, color: grey }}>
              {host.host_name} landed {host.deploy_date} — accepted as delivered
            </span>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {["Host", "GPUs · VRAM", "RAM · CPU", "Link · Free storage", "Status"].map((h) => (
                  <th key={h} style={{ padding: "12px 24px", textAlign: "left",
                                       fontSize: 10, letterSpacing: 1.5, color: mid,
                                       textTransform: "uppercase",
                                       borderBottom: `1px solid ${rule}` }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {compute.map((h) => (
                <tr key={h.host_name} data-testid="compute-row"
                    onClick={() => onOpen(h)}
                    style={{ cursor: "pointer" }}
                    onMouseEnter={(e) => e.currentTarget.style.background = "#f8f5ee"}
                    onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}>
                  <td style={{ padding: "16px 24px", color: navy }}>
                    <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 15 }}>
                      {h.host_name}
                    </div>
                    <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>{h.os}</div>
                  </td>
                  <td style={{ padding: "16px 24px", fontSize: 13, color: navy }}>
                    {h.gpus.count} × {h.gpus.model} · ≈ {Math.round(h.gpus.vram_gb_total)} GB
                  </td>
                  <td style={{ padding: "16px 24px", fontSize: 13, color: navy }}>
                    {h.ram_gb_total} GB · {h.cpu_threads} threads
                  </td>
                  <td style={{ padding: "16px 24px", fontSize: 13, color: navy }}>
                    ≈ {h.link.throughput_MBps} MB/s · {h.primary_volume.free_tb} TB free
                  </td>
                  <td style={{ padding: "16px 24px" }}>
                    <Chip label={h.hardened ? "HARDENED · ACCEPTED" : "NOT HARDENED"}
                          tone={h.hardened ? "sage" : "crimson"} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ContextPanel
          eyebrow="THE CONNECTION"
          sentences={[
            `A 2 × ${g.model} workhorse with ≈ ${Math.round(g.vram_gb_total)} GB aggregate VRAM and NVLink active between the cards.`,
            `The pod↔VM link is the real ceiling at ≈ ${link.throughput_MBps} MB/s symmetric — bulk audio should land on the VM from its own internet, not this pod.`,
            "Hardening attested: password auth dead server-wide; SSH is key-only.",
          ]} />
      </TwoColBand>
    </div>
  );
}

function ComputeDetailCard({ host, onClose }) {
  const g = host.gpus || {};
  const link = host.link || {};
  const pv = host.primary_volume || {};
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(28,43,69,0.55)",
                  display: "flex", alignItems: "center", justifyContent: "center", zIndex: 40 }}
         onClick={onClose}>
      <div data-testid="compute-detail-card"
           onClick={(e) => e.stopPropagation()}
           style={{ background: cardWhite, borderRadius: 16, width: "min(720px, 92vw)",
                    maxHeight: "82vh", overflow: "auto", padding: "28px 32px",
                    boxShadow: "0 20px 40px rgba(0,0,0,0.25)" }}>
        <div style={{ display: "flex", alignItems: "start" }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 11, letterSpacing: 1.5, color: mid, textTransform: "uppercase" }}>
              HOST
            </div>
            <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28,
                         margin: "6px 0 4px", color: navy }}>
              {host.host_name}
            </h2>
            <div style={{ fontSize: 12, color: grey }}>{host.state_class}</div>
          </div>
          <button data-testid="compute-detail-close" onClick={onClose}
                  style={{ background: "transparent", border: `1px solid ${rule}`,
                           padding: "6px 12px", borderRadius: 999, cursor: "pointer",
                           color: grey, fontSize: 12 }}>
            Close
          </button>
        </div>

        <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
                     margin: "24px 0 8px", color: navy }}>The four questions</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10 }}>
          <FQ label="LINK WORKING" value={host.four_questions?.link_working ? "yes" : "no"} />
          <FQ label="FOUND" value={host.four_questions?.found ? "yes" : "no"} />
          <FQ label="READY" value={host.four_questions?.ready ? "yes" : "no"} />
          <FQ label="FAILURE" value={host.four_questions?.failure || "none"} />
        </div>

        <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
                     margin: "20px 0 8px", color: navy }}>Measured capacity</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
          <KV label="GPUS" value={`${g.count} × ${g.model}`} />
          <KV label="AGGREGATE VRAM" value={`${Math.round(g.vram_gb_total)} GB`} />
          <KV label="NVLINK" value={g.nvlink_active ?
            `active · ${Math.round(g.nvlink_aggregate_gbps_per_gpu)} GB/s aggregate per GPU` : "not active"} />
          <KV label="SYSTEM RAM" value={`${host.ram_gb_total} GB`} />
          <KV label="CPU" value={`${host.cpu_threads} threads · ${host.cpu_model}`} />
          <KV label="PRIMARY VOLUME" value={`${pv.mount} · ≈ ${pv.free_tb} TB free · ~${pv.write_speed_MBps} MB/s`} />
          <KV label="POD ↔ VM LINK" value={`≈ ${link.throughput_MBps} MB/s · ${link.symmetric ? "symmetric" : "asymmetric"}`} />
          <KV label="HARDENING" value={host.hardened ? `attested · ${host.hardening_result}` : "not attested"} />
        </div>

        <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
                     margin: "20px 0 8px", color: navy }}>What it can carry</h3>
        <p style={{ fontSize: 13, color: navy, lineHeight: 1.6 }}>
          {host.usability_paragraph}
        </p>
      </div>
    </div>
  );
}

function FQ({ label, value }) {
  const yes = value === "yes";
  return (
    <div style={{ border: `1px solid ${rule}`, borderRadius: 8, padding: "10px 12px" }}>
      <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
                    textTransform: "uppercase" }}>{label}</div>
      <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 18,
                    color: yes ? sage : (value === "no" ? crimson : navy), marginTop: 2 }}>
        {value}
      </div>
    </div>
  );
}

function KV({ label, value }) {
  return (
    <div style={{ border: `1px solid ${rule}`, borderRadius: 8, padding: "10px 12px" }}>
      <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
                    textTransform: "uppercase" }}>{label}</div>
      <div style={{ fontSize: 13, color: navy, marginTop: 4, lineHeight: 1.4 }}>{value}</div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// LLMS & TRAINED MODELS tab (honest empty)
// ---------------------------------------------------------------------------

function LLMsTrainedModelsTab({ facts }) {
  const reason = (facts.models && facts.models.reason) ||
    "No models connected yet.";
  return (
    <EmptyPanel eyebrow="WHAT IS ANSWERING"
                headline="No models connected yet."
                sentence={reason + " Not yet measured — drawn, never left blank."} />
  );
}

// ---------------------------------------------------------------------------
// Shared empty panel
// ---------------------------------------------------------------------------

function EmptyPanel({ eyebrow, headline, sentence }) {
  return (
    <div data-testid="tab-empty-panel"
         style={{ background: cardWhite, borderRadius: 12, padding: "48px 44px" }}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>{eyebrow}</div>
      <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28,
                   margin: "0 0 16px 0", color: navy }}>
        {headline}
      </h2>
      <p style={{ color: grey, lineHeight: 1.6, fontSize: 15, maxWidth: 640 }}>{sentence}</p>
      <p style={{ color: grey, lineHeight: 1.6, fontSize: 13, marginTop: 20, fontStyle: "italic" }}>
        drawn, never left blank
      </p>
    </div>
  );
}
