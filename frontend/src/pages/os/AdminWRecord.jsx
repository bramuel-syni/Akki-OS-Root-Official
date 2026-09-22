/*
 * AdminWRecord.jsx — v2 OS · admin tab · THE WATCH Record leaf.
 * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
 * R-103 amendment: single continuous run to completion.
 * HONEST-GAP · SO §5 honest-gap-never-fake.
 */

import React from "react";

export default function AdminWRecord() {
  return (
    <div
      data-testid="admin-wrecord-surface"
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
          data-testid="admin-wrecord-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          THE WATCH · Record
        </div>
        <h1
          data-testid="admin-wrecord-title"
          style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          Record
        </h1>
      </header>
      <section
        data-testid="admin-wrecord-lead"
        style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
      >
        <p style={{ margin: "0 0 24px 0" }}>
          External witness trail. Every held / refused / admitted decision is written here with source, authority, and timestamp.
        </p>
      </section>
      <section
        data-testid="admin-wrecord-honest-gap"
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
          data-testid="admin-wrecord-honest-gap-label"
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
        <div data-testid="admin-wrecord-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
          Backend for Record not yet wired. This surface reveals the design-of-record
          structure honestly; no fabricated data is shown. Wire lands at PHASE 3
          Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
          + R-103 amendment (single continuous run).
        </div>
        <div
          data-testid="admin-wrecord-honest-gap-see-working"
          style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
        >
          See the working: NAV admin.wrecord at App.js const NAV · surface at
          pages/os/AdminWRecord.jsx.
        </div>
      </section>
    </div>
  );
}
