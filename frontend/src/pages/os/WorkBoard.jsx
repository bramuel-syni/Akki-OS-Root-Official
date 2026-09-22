/*
 * WorkBoard.jsx — v2 OS · Work tab · WORKSTUDIO · board leaf.
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 *
 * Cures V8-render drift where current runtime showed "Board 360" in a
 * separate "Performance Management" section.
 */

import React from "react";

export default function WorkBoard() {
  return (
    <div
      data-testid="work-board-surface"
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
          data-testid="work-board-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          WORKSTUDIO · Board
        </div>
        <h1
          data-testid="work-board-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          Board
        </h1>
      </header>
      <section data-testid="work-board-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
        <p style={{ margin: "0 0 24px 0" }}>
          Board-facing view: what the board will see, phrased in board language,
          traceable back to source data with a single click.
        </p>
      </section>
      <section
        data-testid="work-board-honest-gap"
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
          data-testid="work-board-honest-gap-label"
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
        <div data-testid="work-board-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Board rollup not yet wired. Depends on Company Goals aggregation
          (upstream) which depends on PHASE 3 Census Productization.
        </div>
        <div
          data-testid="work-board-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV workstudio.board at App.js · surface at
          pages/os/WorkBoard.jsx.
        </div>
      </section>
    </div>
  );
}
