/*
 * ThinkLabHypothesis.jsx — v2 OS · work tab · THINKLAB Test Hypothesis leaf.
 * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
 * R-103 amendment: single continuous run to completion.
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 */

import React from "react";

export default function ThinkLabHypothesis() {
  return (
    <div
      data-testid="thinklab-hypothesis-surface"
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
          data-testid="thinklab-hypothesis-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          THINKLAB · Test Hypothesis
        </div>
        <h1
          data-testid="thinklab-hypothesis-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          Test Hypothesis
        </h1>
      </header>
      <section
        data-testid="thinklab-hypothesis-lead"
        style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
      >
        <p style={{ margin: "0 0 24px 0" }}>
          Frame a claim; the system finds what admits it, what refuses it, what stays silent.
        </p>
      </section>
      <section
        data-testid="thinklab-hypothesis-honest-gap"
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
          data-testid="thinklab-hypothesis-honest-gap-label"
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
        <div data-testid="thinklab-hypothesis-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Backend for Test Hypothesis not yet wired. This surface reveals the design-of-record
          structure honestly; no fabricated data is shown. Wire lands at PHASE 3
          Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
          + R-103 amendment (single continuous run).
        </div>
        <div
          data-testid="thinklab-hypothesis-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV work.hypothesis at App.js const NAV · surface at
          pages/os/ThinkLabHypothesis.jsx.
        </div>
      </section>
    </div>
  );
}
