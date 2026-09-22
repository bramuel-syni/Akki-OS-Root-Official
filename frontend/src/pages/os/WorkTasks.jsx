/*
 * WorkTasks.jsx — v2 OS · Work tab · WORKSTUDIO · tasks leaf ("My Work" label).
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 *
 * Cures V8-render drift where current runtime showed label "Task Manager"
 * instead of design-of-record "My Work" (landmark 01 evidence).
 */

import React from "react";

export default function WorkTasks() {
  return (
    <div
      data-testid="work-tasks-surface"
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
          data-testid="work-tasks-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          WORKSTUDIO · My Work
        </div>
        <h1
          data-testid="work-tasks-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          My Work
        </h1>
      </header>
      <section data-testid="work-tasks-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
        <p style={{ margin: "0 0 24px 0" }}>
          Your open work in one place: what's yours, what's waiting on evidence,
          what's held. Every card leads with a sentence; measures live behind
          "see the working".
        </p>
      </section>
      <section
        data-testid="work-tasks-honest-gap"
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
          data-testid="work-tasks-honest-gap-label"
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
        <div data-testid="work-tasks-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Task/request backlog service exists partially in dap_lifecycle but
          the "My Work" aggregation view is not yet wired to it. This surface
          presents the design-of-record structure; no fabricated tasks are
          shown. Wire lands at PHASE 4 (b) Connect + Commission wizard live
          feature build.
        </div>
        <div
          data-testid="work-tasks-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV workstudio.tasks label="My Work" at App.js ·
          surface at pages/os/WorkTasks.jsx. Cures V8-render drift showing
          "Task Manager".
        </div>
      </section>
    </div>
  );
}
