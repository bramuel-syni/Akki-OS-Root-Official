/*
 * MonitorSignals.jsx — v2 OS · Work tab · MONITOR · signals leaf.
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 */

import React from "react";

export default function MonitorSignals() {
  return (
    <div
      data-testid="monitor-signals-surface"
      style={{
        minHeight: "100vh",
        background: "var(--surface, #f7f5ef)",
        color: "var(--ink, #12121a)",
        padding: "48px 64px",
        fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
      }}
    >
      <header style={{ marginBottom: 32 }}>
        <div
          data-testid="monitor-signals-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          MONITOR · Signals
        </div>
        <h1
          data-testid="monitor-signals-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          Signals
        </h1>
      </header>
      <section data-testid="monitor-signals-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
        <p style={{ margin: "0 0 24px 0" }}>
          The system speaks up when something wobbles: shield refusals, entitlement
          expiries, source drift, unexplained silences. Every signal traces back
          to what triggered it.
        </p>
      </section>
      <section
        data-testid="monitor-signals-honest-gap"
        style={{
          marginTop: 40,
          padding: "24px 28px",
          background: "rgba(176,141,46,.07)",
          border: "1px solid var(--brass, #b08d2e)",
          borderRadius: 4,
          maxWidth: 720,
        }}
      >
        <div
          data-testid="monitor-signals-honest-gap-label"
          style={{
            fontSize: 11,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--brass, #b08d2e)",
            fontWeight: 600,
            marginBottom: 8,
          }}
        >
          Honest gap · surface only
        </div>
        <div data-testid="monitor-signals-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Signal aggregation not yet wired. Real signals will pull from shield
          refusal logs, entitlement-service allowance events, and Census
          drift-detection. Wire lands at PHASE 4 (g) Watch external-witness
          trail feature build.
        </div>
        <div
          data-testid="monitor-signals-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV monitor.signals at App.js · surface at
          pages/os/MonitorSignals.jsx.
        </div>
      </section>
    </div>
  );
}
