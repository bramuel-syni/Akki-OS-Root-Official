/*
 * WorkChat.jsx — v2 OS Prototype · Work tab · WORKSTUDIO group · chat leaf.
 *
 * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
 * Owner FE brief §0 verbatim: "The prototype is the design of record ... prototype wins."
 * Owner directive verbatim 2026-09-22T~06:10Z: "UI/UX architecture and experience
 * flow needs to be exact as the HTML I shared."
 *
 * Sub-slice 4d owner ruling verbatim 2026-09-22T~08:15Z: "Work tab (chat LIVE +
 * analyze/documents/tasks/team/performance/board honest-gap)".
 *
 * HONEST-GAP DISCLOSURE (SO §5 honest-gap-never-fake · this-slice specific):
 * No `/api/chat` or equivalent chat surface currently exists in the
 * Extraction-Akki backend (grep verified 2026-09-22T08:20Z zero hits on
 * backend/routers/ for chat routes). The design-of-record "chat LIVE"
 * capability is a PHASE 4 feature (owner R-102 MASTER DIRECTIVE
 * "productized and functional or gaps surfaced"). This surface reveals the
 * gap honestly rather than fabricating a fake chat pipeline. Live-wire
 * lands at CP-CHAT-LIVE-WIRE (queued to DQ-14/15/16 fork if desk cannot
 * fold into PHASE 4 (h) Model Registry lane).
 *
 * FOURQ discipline (Rule zero · every block leads with a sentence; measures
 * live behind "see the working"): each section header is a plain-English
 * lead sentence; details/measures collapse below.
 */

import React from "react";

export default function WorkChat() {
  return (
    <div
      data-testid="work-chat-surface"
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
          data-testid="work-chat-breadcrumb"
        >
          WORKSTUDIO · Chat
        </div>
        <h1
          style={{
            fontSize: 40,
            fontWeight: 300,
            margin: 0,
            letterSpacing: "-0.02em",
          }}
          data-testid="work-chat-title"
        >
          Chat
        </h1>
      </header>

      <section
        data-testid="work-chat-lead"
        style={{
          maxWidth: 720,
          fontSize: 17,
          lineHeight: 1.6,
          color: "var(--ink, #12121a)",
        }}
      >
        <p style={{ margin: "0 0 24px 0" }}>
          Ask a question; the shield stays on. Every answer traces to a source
          or says plainly why it can't. Branch a reply to compare two directions
          without losing the original.
        </p>
      </section>

      <section
        data-testid="work-chat-honest-gap"
        style={{
          marginTop: 40,
          padding: "24px 28px",
          background: "rgba(184,57,91,.06)",
          border: "1px solid var(--oxblood, #b8395b)",
          borderRadius: 4,
          maxWidth: 720,
        }}
      >
        <div
          style={{
            fontSize: 11,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--oxblood, #b8395b)",
            marginBottom: 8,
            fontWeight: 600,
          }}
          data-testid="work-chat-honest-gap-label"
        >
          Honest gap · backend wire pending
        </div>
        <div
          style={{ fontSize: 15, lineHeight: 1.5, color: "var(--ink, #12121a)" }}
          data-testid="work-chat-honest-gap-body"
        >
          The chat backend is not yet wired. This surface reveals the gap
          honestly. Live wire lands at CP-CHAT-LIVE-WIRE under the PHASE 4
          feature build-out per R-102 MASTER DIRECTIVE. Until then this page
          shows the design-of-record shape without fabricating a fake pipeline.
        </div>
        <div
          style={{
            marginTop: 16,
            fontSize: 13,
            color: "var(--ink3, #6b6b78)",
          }}
          data-testid="work-chat-honest-gap-see-working"
        >
          See the working: shell constants at /app/frontend/src/App.js
          const NAV → workstudio.chat · this surface at pages/os/WorkChat.jsx.
        </div>
      </section>
    </div>
  );
}
