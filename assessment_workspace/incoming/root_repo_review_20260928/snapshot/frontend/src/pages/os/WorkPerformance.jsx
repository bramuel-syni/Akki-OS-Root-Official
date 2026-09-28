/*
 * WorkPerformance.jsx — v2 OS · Work tab · WORKSTUDIO · performance leaf
 * ("Company Goals" label per enumeration §1.2).
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 *
 * Cures V8-render drift where current runtime showed separate "Performance
 * Management" section with "Exco 360" tile (landmark 01 evidence).
 */

import React from "react";

export default function WorkPerformance() {
  return (
    <div
      data-testid="work-performance-surface"
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
          data-testid="work-performance-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          WORKSTUDIO · Company Goals
        </div>
        <h1
          data-testid="work-performance-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          Company Goals
        </h1>
      </header>
      <section data-testid="work-performance-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
        <p style={{ margin: "0 0 24px 0" }}>
          The measures that matter to the board are the measures on this page.
          Every card leads with a sentence; every number carries its source.
        </p>
      </section>
      <section
        data-testid="work-performance-honest-gap"
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
          data-testid="work-performance-honest-gap-label"
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
        <div data-testid="work-performance-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Company Goals aggregation not yet wired. Real board-level measures
          require a full Census + Registry pipeline pulling from admitted
          sources — that lands at PHASE 3 Census Productization + PHASE 4
          (h) Model Registry.
        </div>
        <div
          data-testid="work-performance-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV workstudio.performance label="Company Goals" at
          App.js · surface at pages/os/WorkPerformance.jsx. Cures V8-render
          drift showing "Exco 360" tile in separate "Performance Management"
          section.
        </div>
      </section>
    </div>
  );
}
