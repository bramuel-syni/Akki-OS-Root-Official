/*
 * WorkTeam.jsx — v2 OS · Work tab · WORKSTUDIO · team leaf ("My Team" label).
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 */

import React from "react";

export default function WorkTeam() {
  return (
    <div
      data-testid="work-team-surface"
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
          data-testid="work-team-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          WORKSTUDIO · My Team
        </div>
        <h1
          data-testid="work-team-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          My Team
        </h1>
      </header>
      <section data-testid="work-team-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
        <p style={{ margin: "0 0 24px 0" }}>
          Your people in one place: who's on watch, whose entitlements need
          renewal, who's holding what.
        </p>
      </section>
      <section
        data-testid="work-team-honest-gap"
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
          data-testid="work-team-honest-gap-label"
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
        <div data-testid="work-team-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Team roster + entitlement rollup service not yet wired. Principal
          Model v1 exists at backend/services/request_context/context.py but
          the team-level aggregation view is queued for CP-TENANT-SEPARATION
          (PHASE 2) where per-tenant roster views become meaningful.
        </div>
        <div
          data-testid="work-team-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV workstudio.team label="My Team" at App.js ·
          surface at pages/os/WorkTeam.jsx.
        </div>
      </section>
    </div>
  );
}
