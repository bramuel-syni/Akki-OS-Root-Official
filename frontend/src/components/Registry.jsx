import React, { useState } from "react";
import ConnectWizard from "@/components/ConnectWizard";

/**
 * Registry - the estate's inventory surface (Owner fixture drop 2026-08-14).
 *
 * Renders per Akki Prototype v7 "Screen mockups" (fixtures/screen_mockups_v7.pdf,
 * sha256 418ad0e3...). Three-tab shell: DATA CONNECTED · COMPUTE CONNECTED ·
 * LLMS & TRAINED MODELS. "+ Connect" button pushed right on the tab bar
 * opens the ConnectWizard right-hand drawer (see ConnectWizard.jsx).
 *
 * Honest current state only: no fabricated demo-org numbers. Every tab
 * renders "not yet measured" style copy until real measurement lands.
 * The role switcher (Compliance Owner · Watch Officer · Operator) renders
 * as STATIC presentation per FL-P2-15 (auth-role wiring is Track-B).
 */
const cream = "#f6f2ea";
const navy = "#1c2b45";
const grey = "#666";
const cardWhite = "#ffffff";

const TABS = [
  { key: "data-connected", label: "DATA CONNECTED", testid: "tab-data-connected" },
  { key: "compute-connected", label: "COMPUTE CONNECTED", testid: "tab-compute-connected" },
  { key: "llms-trained-models", label: "LLMS & TRAINED MODELS", testid: "tab-llms-trained-models" },
];

const ROLES = ["Compliance Owner", "Watch Officer", "Operator"];

export default function Registry() {
  const [activeTab, setActiveTab] = useState("data-connected");
  const [wizardOpen, setWizardOpen] = useState(false);

  return (
    <div style={{ minHeight: "100vh", background: cream, fontFamily: "ui-sans-serif" }}>
      <Header />

      <main style={{ padding: "32px 60px 80px" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto" }}>
          {/* Title deck */}
          <div style={{ marginBottom: 32 }}>
            <div style={{ fontSize: 11, letterSpacing: 2, color: grey }}>REGISTRY · ESTATE</div>
            <h1 data-testid="registry-title"
                style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 44, margin: "8px 0 12px 0", color: navy }}>
              Registry
            </h1>
            <p style={{ color: grey, lineHeight: 1.55, maxWidth: 720, margin: 0 }}>
              What you hold, what is connected, what is answering.
              Read-only by design, with one write path - Connect.
            </p>
          </div>

          {/* Tab bar with + Connect pushed right */}
          <TabBar activeTab={activeTab} onTabChange={setActiveTab} onOpenWizard={() => setWizardOpen(true)} />

          {/* Tab body - honest empty state per tab */}
          <div style={{ marginTop: 32 }}>
            {activeTab === "data-connected" && <DataConnectedEmpty />}
            {activeTab === "compute-connected" && <ComputeConnectedEmpty />}
            {activeTab === "llms-trained-models" && <LLMsTrainedModelsEmpty />}
          </div>
        </div>
      </main>

      {wizardOpen && <ConnectWizard onClose={() => setWizardOpen(false)} />}
    </div>
  );
}

function Header() {
  return (
    <header style={{ background: navy, color: cardWhite, padding: "16px 60px", display: "flex", alignItems: "center", gap: 24 }}>
      <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 18, letterSpacing: 0.5 }}>
        Akki · ESTATE
      </div>
      <div style={{ flex: 1 }} />
      <div data-testid="role-switcher" style={{ display: "flex", gap: 8 }}>
        {ROLES.map((role) => (
          <div key={role} data-testid={`role-${role.toLowerCase().replace(/\s+/g, "-")}`}
               style={{ padding: "6px 12px", borderRadius: 999, background: "rgba(255,255,255,0.08)",
                        fontSize: 12, color: cardWhite, letterSpacing: 0.3 }}>
            {role}
          </div>
        ))}
        <div style={{ width: 32, height: 32, borderRadius: 999, background: "rgba(255,255,255,0.15)",
                      display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, marginLeft: 4 }}>
          U
        </div>
      </div>
    </header>
  );
}

function TabBar({ activeTab, onTabChange, onOpenWizard }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 32, borderBottom: "1px solid #ddd", paddingBottom: 0 }}>
      {TABS.map((t) => {
        const active = t.key === activeTab;
        return (
          <button
            key={t.key}
            type="button"
            data-testid={t.testid}
            onClick={() => onTabChange(t.key)}
            style={{
              background: "transparent", border: "none", cursor: "pointer",
              padding: "12px 4px", fontSize: 12, letterSpacing: 2,
              color: active ? navy : grey,
              borderBottom: active ? `2px solid ${navy}` : "2px solid transparent",
              marginBottom: -1,
            }}
          >
            {t.label}
          </button>
        );
      })}
      <div style={{ flex: 1 }} />
      <button
        type="button"
        data-testid="open-connect-wizard"
        onClick={onOpenWizard}
        style={{ padding: "10px 20px", background: navy, color: cardWhite, border: "none",
                 borderRadius: 999, cursor: "pointer", fontSize: 13, letterSpacing: 0.3, marginBottom: 8 }}
      >
        + Connect
      </button>
    </div>
  );
}

function EmptyPanel({ eyebrow, headline, sentence }) {
  return (
    <div data-testid="tab-empty-panel" style={{ background: cardWhite, borderRadius: 12, padding: "48px 44px" }}>
      <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>{eyebrow}</div>
      <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28, margin: "0 0 16px 0", color: navy }}>
        {headline}
      </h2>
      <p style={{ color: grey, lineHeight: 1.6, fontSize: 15, maxWidth: 640 }}>
        {sentence}
      </p>
      <p style={{ color: grey, lineHeight: 1.6, fontSize: 13, marginTop: 20, fontStyle: "italic" }}>
        drawn, never left blank
      </p>
    </div>
  );
}

function DataConnectedEmpty() {
  return (
    <EmptyPanel
      eyebrow="WHAT YOU HOLD"
      headline="No data connected yet."
      sentence="Nothing has been admitted into the estate through Connect. When a source lands, it appears here as measurement, never as an estimate - not yet measured until the next census reads it."
    />
  );
}

function ComputeConnectedEmpty() {
  return (
    <EmptyPanel
      eyebrow="WHAT IS CONNECTED"
      headline="One machine pending connection."
      sentence="The AISCA GPU host is provisioned upstream; the estate has not yet received its credential entry through Connect. When it arrives, this tab renders its commissioning record - hardened, accepted, and receipted - not yet measured until Phase-0 completes."
    />
  );
}

function LLMsTrainedModelsEmpty() {
  return (
    <EmptyPanel
      eyebrow="WHAT IS ANSWERING"
      headline="No models connected yet."
      sentence="Bought-in and locally-trained models both land here, on one record. Nothing has been connected through the wizard's LLM or trained-model paths. Not yet measured - drawn, never left blank."
    />
  );
}
