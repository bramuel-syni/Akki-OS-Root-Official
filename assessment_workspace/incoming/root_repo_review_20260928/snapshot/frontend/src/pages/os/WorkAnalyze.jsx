/*
 * WorkAnalyze.jsx — v2 OS Prototype · Work tab · WORKSTUDIO group · analyze leaf.
 * (label per enumeration §1.2: "Data Suite")
 *
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * Owner FE brief §0 verbatim: "The prototype is the design of record ... prototype wins."
 *
 * HONEST-GAP: no analytics backend exists this-slice. Surface shows the
 * design-of-record shape + honest deferral to PHASE 4 Data Suite build.
 * SO §5 honest-gap-never-fake.
 */

import React from "react";

export default function WorkAnalyze() {
  return (
    <div
      data-testid="work-analyze-surface"
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
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
          data-testid="work-analyze-breadcrumb"
        >
          WORKSTUDIO · Data Suite
        </div>
        <h1
          style={{
            fontSize: 40,
            fontWeight: 300,
            margin: 0,
            letterSpacing: "-0.02em",
          }}
          data-testid="work-analyze-title"
        >
          Data Suite
        </h1>
      </header>

      <section
        data-testid="work-analyze-lead"
        style={{
          maxWidth: 720,
          fontSize: 17,
          lineHeight: 1.6,
        }}
      >
        <p style={{ margin: "0 0 24px 0" }}>
          Analyse what the estate holds without moving it. Every measure carries
          its source; every filter reveals the working.
        </p>
      </section>

      <section
        data-testid="work-analyze-honest-gap"
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
          style={{
            fontSize: 11,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--brass, #b08d2e)",
            fontWeight: 600,
            marginBottom: 8,
          }}
          data-testid="work-analyze-honest-gap-label"
        >
          Honest gap · surface only
        </div>
        <div
          style={{ fontSize: 15, lineHeight: 1.5 }}
          data-testid="work-analyze-honest-gap-body"
        >
          Data Suite analytics backend not yet built. This surface presents the
          design-of-record structure; no fabricated data is shown. Analytics
          engine lands at PHASE 4 Data-Suite feature build.
        </div>
        <div
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
          data-testid="work-analyze-honest-gap-see-working"
        >
          See the working: NAV workstudio.analyze at App.js · surface at
          pages/os/WorkAnalyze.jsx.
        </div>
      </section>
    </div>
  );
}
