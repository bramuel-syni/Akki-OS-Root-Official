/*
 * WorkCommission.jsx — v2 OS · Work tab · workstudio · commission leaf.
 * PHASE 4 (a) · CP-COMMISSION-WIZARD-LIVE · Commit-A · 2026-09-22T22:25:00Z
 *
 * Owner banked order verbatim (2026-09-22T~21:21Z):
 *   "PHASE 4 (banked order): entitlements backend → Connect + Commission
 *    wizards live → CP-SKILLS-LAYER → ..."
 *
 * This page wraps the pre-existing sealed Canon-5-§14 Shaping-Wizard
 * <CommissionWizard /> (byte-identical across pod_shell/frontend/src ↔
 * /app/frontend/src twins per wave_g mirror invariant + Ship-Manifest DoD)
 * into a routable surface at `/os/work/commission`.
 *
 * Sealed carriers UNCHANGED per SO §3.8:
 *   - CommissionWizard.jsx (Canon 5 §14 Shaping Wizard · Phase 7 Stage B-1
 *     operator variant) is consumed by identity import ONLY.
 *   - Backend `/api/wizard/operator/*` endpoints are consumed by the wizard
 *     component; this page adds no backend consumption of its own.
 *
 * Honest-gap-narrowing (SO §5.7 · additive) — WorkTasks.jsx honest-gap body
 * cites "Wire lands at PHASE 4 (b) Connect + Commission wizard live feature
 * build". This page IS that wire for the Commission half. The WorkTasks
 * honest-gap remains banked because the Task/request backlog aggregation
 * view is a SEPARATE surface that is NOT resolved by this-slice; owner
 * gets a truthful narrowing without a paraphrase drift.
 */

import React from "react";
import CommissionWizard from "@/components/CommissionWizard";

export default function WorkCommission() {
  return (
    <div
      data-testid="work-commission-surface"
      style={{
        minHeight: "100vh",
        background: "var(--surface, #f7f5ef)",
        color: "var(--ink, #12121a)",
        padding: "24px 32px",
        fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
      }}
    >
      <header
        data-testid="work-commission-header"
        style={{ marginBottom: 16, maxWidth: 1080 }}
      >
        <div
          data-testid="work-commission-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          WORKSTUDIO · Commission
        </div>
        <h1
          data-testid="work-commission-title"
          style={{ fontSize: 32, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
        >
          Commission an objective
        </h1>
        <p
          data-testid="work-commission-lead"
          style={{ fontSize: 15, lineHeight: 1.55, color: "var(--ink2, #444)", marginTop: 12, maxWidth: 720 }}
        >
          Define the objective, authorised sources, delivery and budget.
        </p>
      </header>
      <section data-testid="work-commission-wizard-mount">
        <CommissionWizard />
      </section>
    </div>
  );
}
