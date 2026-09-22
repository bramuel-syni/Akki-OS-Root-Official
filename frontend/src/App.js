import "@/App.css";
import { useEffect, useRef, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

/* ── DAP Portal (Track 1) ─────────────────────────────── */
import DAPLayout from "@/pages/dap/DAPLayout";
import DAPLanding from "@/pages/dap/DAPLanding";
import AvailableResources from "@/pages/dap/AvailableResources";
import DataGovernance from "@/pages/dap/DataGovernance";
import RequestLifecycle from "@/pages/dap/RequestLifecycle";
import DataEstates from "@/pages/dap/DataEstates";
import ExtractModes from "@/pages/dap/ExtractModes";
import ConnectResources from "@/pages/dap/ConnectResources";
import Entitlement from "@/pages/dap/Entitlement";
import CanonCountdown from "@/pages/dap/CanonCountdown";

// v2 OS Prototype · Turn 4 sub-slice 4d GREEN · Frontend rebuild slice 2 ·
// Work tab surfaces (7) + Monitor sub-view surfaces (2). Each surface is a
// native React implementation of the design-of-record shape with honest-gap
// disclosure where backend wiring is pending PHASE 3/4. SO §3.8 additive-only.
import WorkChat from "@/pages/os/WorkChat";
import WorkAnalyze from "@/pages/os/WorkAnalyze";
import WorkDocuments from "@/pages/os/WorkDocuments";
import WorkTasks from "@/pages/os/WorkTasks";
import WorkTeam from "@/pages/os/WorkTeam";
import WorkPerformance from "@/pages/os/WorkPerformance";
import WorkBoard from "@/pages/os/WorkBoard";
import MonitorSignals from "@/pages/os/MonitorSignals";
import MonitorIdeas from "@/pages/os/MonitorIdeas";

// v2 OS Prototype · Turn 4 sub-slice 4e GREEN · Frontend rebuild slice 3 ·
// ThinkLab (4 honest-gap · Work tab) + Admin tab (10 honest-gap: estate 3 +
// approvals 3 + watch 4) via 4c-banked filterGroupsForRole persona helper.
// R-103 amendment: single continuous run to completion.
import ThinkLabClarity from "@/pages/os/ThinkLabClarity";
import ThinkLabStrategy from "@/pages/os/ThinkLabStrategy";
import ThinkLabHypothesis from "@/pages/os/ThinkLabHypothesis";
import ThinkLabPerspective from "@/pages/os/ThinkLabPerspective";
import AdminEstate from "@/pages/os/AdminEstate";
import AdminGovern from "@/pages/os/AdminGovern";
import AdminGreyMirror from "@/pages/os/AdminGreyMirror";
import AdminSpendReq from "@/pages/os/AdminSpendReq";
import AdminRulesUpd from "@/pages/os/AdminRulesUpd";
import AdminModelAdmission from "@/pages/os/AdminModelAdmission";
import AdminWState from "@/pages/os/AdminWState";
import AdminWRecord from "@/pages/os/AdminWRecord";
import AdminWUnder from "@/pages/os/AdminWUnder";
import AdminWDecisions from "@/pages/os/AdminWDecisions";

// v2 OS Prototype · Turn 4 sub-slice 4f GREEN · Frontend rebuild slice 4 ·
// Build 4 + Buildlib 2 + Collab 4 + 3rdParty 4 = 14 honest-gap surfaces ·
// completes 37 of 37 OS leaves. R-103 amendment.
import BuildTrain from "@/pages/os/BuildTrain";
import BuildAgent from "@/pages/os/BuildAgent";
import BuildSkill from "@/pages/os/BuildSkill";
import BuildExtract from "@/pages/os/BuildExtract";
import BuildlibAgents from "@/pages/os/BuildlibAgents";
import BuildlibModels from "@/pages/os/BuildlibModels";
import CollabMentions from "@/pages/os/CollabMentions";
import CollabEmails from "@/pages/os/CollabEmails";
import CollabProjects from "@/pages/os/CollabProjects";
import CollabHrStuff from "@/pages/os/CollabHrStuff";
import AppsNew from "@/pages/os/AppsNew";
import AppsFrequent from "@/pages/os/AppsFrequent";
import AppsConnected from "@/pages/os/AppsConnected";
import AppsRequests from "@/pages/os/AppsRequests";

// ---------------------------------------------------------------------------
// v2 OS Prototype Shell · Design-of-Record Constants
// (byte-verbatim per phase0/prototype_inventory/20260922T064500Z_full_enumeration_and_gap_checklist.md §1.1-§1.5)
// R-101 preserved WHAT · e-apply Turn 4 sub-slice 4c · 2026-09-22T07:45:00Z
//
// Owner FE brief §0 verbatim (2026-09-20T~08:24Z):
//   "The prototype is the design of record ... prototype wins."
//
// Owner directive verbatim 2026-09-22T~06:10Z:
//   "UI/UX architecture and experience flow needs to be exact as the HTML I shared."
//
// This block is ADDITIVE (SO §3.8): the V8 substitution engine below is
// preserved verbatim. The shell constants are consumed by sub-slices 4d-4g
// as the OS surface + DAP LATEST rebuild lands over the V8 iframe path.
// ---------------------------------------------------------------------------

const TABS = [
  { key:'work',  label:'Work',           groups:['workstudio','thinklab','collab','monitor'] },
  { key:'build', label:'Build',          groups:['build','buildlib'] },
  { key:'apps',  label:'3rd Party Apps', groups:[] },
  { key:'admin', label:'Admin',          groups:['estate','approvals','watch'], right:true }
];

const NAV = [
  { key:'workstudio', label:'WorkStudio', tab:'work', items:[
      { key:'chat',        label:'Chat' },
      { key:'analyze',     label:'Data Suite' },
      { key:'documents',   label:'Documents' },
      { key:'tasks',       label:'My Work' },
      { key:'team',        label:'My Team' },
      { key:'performance', label:'Company Goals' },
      { key:'board',       label:'Board' }
  ]},
  { key:'thinklab', label:'ThinkLab', tab:'work', items:[
      { key:'clarity',     label:'Seek Clarity' },
      { key:'strategy',    label:'Develop Strategy' },
      { key:'hypothesis',  label:'Test Hypothesis' },
      { key:'perspective', label:'Get Perspective' }
  ]},
  { key:'collab', label:'Collab', tab:'work', items:[
      { key:'mentions', label:'Mentions' },
      { key:'emails',   label:'Emails' },
      { key:'projects', label:'Projects/Tasks' },
      { key:'hrstuff',  label:'HR Stuff' }
  ]},
  { key:'monitor', label:'Monitor', tab:'work', items:[
      { key:'performance', label:'Performance' },
      { key:'signals',     label:'Signals' },
      { key:'ideas',       label:'Ideas' }
  ]},
  { key:'estate', label:'Manage Estate', tab:'admin', items:[
      { key:'estate',     label:'Registry' },
      { key:'govern',     label:'Shield' },
      { key:'greymirror', label:'Grey Mirror' }
  ]},
  { key:'approvals', label:'Approvals', tab:'admin', items:[
      { key:'spendreq',       label:'Spend Requests' },
      { key:'rulesupd',       label:'Rules Updates' },
      { key:'modeladmission', label:'Model Approval' }
  ]},
  { key:'watch', label:'The Watch', tab:'admin', items:[
      { key:'wstate',     label:'State' },
      { key:'wrecord',    label:'Record' },
      { key:'wunder',     label:'Under Watch' },
      { key:'wdecisions', label:'Decisions' }
  ]},
  { key:'build', label:'Build Your Resources', tab:'build', items:[
      { key:'train',      label:'Train Models' },
      { key:'agentbuild', label:'Build Agents' },
      { key:'buildskill', label:'Build Skill' },
      { key:'extract',    label:'Extract Data' }
  ]},
  { key:'buildlib', label:'Your Resources', tab:'build', divider:true, items:[
      { key:'youragents', label:'Agents' },
      { key:'yourmodels', label:'Models' }
  ]},
  { key:'thirdparty', label:'3rd Party Apps', tab:'apps', items:[
      { key:'appsnew',       label:'New' },
      { key:'appsfrequent',  label:'Frequent' },
      { key:'appsconnected', label:'Connected' },
      { key:'appsrequests',  label:'Requests' }
  ]}
];

const ROLES = [
  { key:'compliance', label:'Compliance Owner', person:'M. Chen',   dept:'Compliance', initials:'MC', groups:['estate','approvals'] },
  { key:'watch',      label:'Watch Officer',    person:'A. Njeri',  dept:'The Watch',  initials:'AN', groups:['watch'] },
  { key:'operator',   label:'Operator',         person:'J. Otieno', dept:'Operations', initials:'JO', groups:['estate'] }
];

const TONE = {
  plain:  { bg:'#fff',                       border:'var(--line)',    color:'var(--ink)'  },
  held:   { bg:'rgba(176,141,46,.07)',       border:'var(--brass)',   color:'var(--ink)'  },
  refused:{ bg:'rgba(184,57,91,.06)',        border:'var(--oxblood)', color:'var(--ink)'  },
  failed: { bg:'var(--surface2)',            border:'var(--line)',    color:'var(--ink3)' },
  drill:  { bg:'var(--surface)',             border:'var(--line)',    color:'var(--ink2)' }
};

/* Four-questions surfaces. Rule zero: every block leads with a sentence;
   measures live behind "see the working". */

// Persona-filter helper · Admin tab shows only groups the current role owns.
// Enumeration §1.3 line 45 verbatim: "a persona sees only their `groups` in
// Admin tab; the Watch officer sees only `watch`; the operator sees only
// `estate`; the compliance owner sees `estate + approvals`. Non-admin tabs
// (work, build, apps) are unconditional."
function filterGroupsForRole(tab, roleKey) {
  const role = ROLES.find(r => r.key === roleKey);
  const tabDef = TABS.find(t => t.key === tab);
  if (!tabDef) return [];
  if (tab !== 'admin' || !role) return tabDef.groups;
  return tabDef.groups.filter(g => role.groups.includes(g));
}

// Export the shell constants so upcoming rebuild slices (4d-4g) can consume
// them without touching the V8 substitution engine below.
export { TABS, NAV, ROLES, TONE, filterGroupsForRole };

/**
 * App.js — Wave G4 · V8 LITERAL adoption · owner Wave G3 REJECT corrections.
 *
 * Owner verdict verbatim (2026-08-28T~11:45Z, banked in DECISIONS.md):
 *   A. Dummy data still the same - see screen shot.
 *   B. Legacy screens should be retired as all components built should
 *      naturally fit this front end without dumping old screens that
 *      create confusion. On the topline statistics, i need practical
 *      data points that speak to everyday users using the system.
 *
 * Three corrections applied here:
 *
 *   Correction 1 — Slot #1 root-cause: the "RMS AI holds ..." sentence is
 *                  fragmented across five nested inline <span> elements
 *                  (border-bottom underlines on "86.4 TB", "12 sources",
 *                  "78% measured", "6 opportunities"). A per-text-node
 *                  regex cannot span multiple text nodes. The fix uses
 *                  ELEMENT-ANCHOR substitution: find the element whose
 *                  full textContent equals the sentence, then assign
 *                  textContent (whole-element replacement). Plus
 *                  MutationObserver re-application (idempotent) so the
 *                  substitution survives portal → Registry → back →
 *                  Registry navigation.
 *
 *   Correction 2 — EVERY topline statistic tile on the Registry surface
 *                  (10 tiles: Held in total, Sources connected, Share
 *                  measured, Data types present, Languages observed,
 *                  Share already verified, Share carrying PII, Licensed
 *                  for external use, Not yet measured, Reduced to reusable
 *                  memory) gets substituted in place. Values are practical
 *                  data points from live data or HONEST-EMPTY
 *                  ("Not yet measured"). Layout untouched.
 *
 *   Correction 3 — Legacy pod component routes retired from routing. The
 *                  V8 front end (PortalIframe) is now the ONLY user-facing
 *                  surface. Any non-root hit lands on the portal.
 *                  Component source files at pod_shell/frontend/src/
 *                  components/*.jsx are RETAINED on disk (donor material
 *                  for wiring real data into V8 surfaces in later waves),
 *                  but are no longer imported here — tree-shaking drops
 *                  them from the shipped bundle.
 *
 * Visual-proof marker: the iframe host <div> in the OUTER document
 * carries a `data-substitution-applied` attribute (monotonic counter of
 * substitutions applied across the session lifetime). This is INVISIBLE
 * bookkeeping on the outer document — not inside the prototype's DOM —
 * so it does not violate the no-engineering-vocab-on-surface rule.
 */

// ---------------------------------------------------------------------------
// Substitution engine
// ---------------------------------------------------------------------------

function _sourcesPhrase(sources) {
  if (sources == null || sources === 0) return "no sources connected yet";
  if (sources === 1) return "1 connected source";
  return `${sources} connected sources`;
}

function _tablesPhrase(tables) {
  if (tables == null || tables === 0) return "no tables read yet";
  if (tables === 1) return "with 1 table read";
  return `with ${tables.toLocaleString()} tables read`;
}

/**
 * V8_SUBSTITUTIONS — the explicit slot substitution map.
 *
 * Rule shapes:
 *   kind='element-anchor' — find the element whose textContent equals
 *                           `dummyContent`. Replace its textContent with
 *                           render(vals). Handles fragmented-span slots.
 *
 *   kind='text-node' — find the text node whose value matches the
 *                      regex `signature`. Replace its nodeValue with
 *                      render(vals). For single-node slots.
 *
 *   kind='tile-value' — find the text node whose trimmed value equals
 *                       `dummy`, verify one ancestor contains `label`
 *                       (to disambiguate value collisions), and replace
 *                       its nodeValue with render(vals). Preserves the
 *                       tile's card layout (label + note stay).
 *
 * Every rule is idempotent: if the target already carries the desired
 * text, the engine skips the mutation. This is required because
 * setting textContent/nodeValue triggers a MutationObserver event
 * which re-invokes applySubstitutions.
 */
const V8_SUBSTITUTIONS = [
  {
    kind: "styled-element-anchor",
    name: "registry-aside-hero-sentence",
    // Slot #1 · Registry header greeting sentence.
    // Wave-H · INTERRUPT 3 (2026-08-28T~13:25Z) + harness finding
    // (2026-08-28T~14:12Z, banked in DECISIONS.md next entry):
    //   dc-runtime renders the plain interpolated string from JS
    //   `estate.greeting` at data-dc-tpl="343" as a single
    //   <span class="sc-interp"> — NOT the multi-span styled variant
    //   that exists elsewhere in the prototype's static HTML. Our job
    //   is to REPLACE the plain-string render with the styled variant
    //   (3 underlined figure phrases + 1 oxblood phrase) that owner
    //   INTERRUPT 3 called out as "by design".
    //
    // dummyContent matches what dc-runtime ACTUALLY renders on the
    // Registry surface (verified via real-Chromium probe 2026-08-28).
    dummyContent:
      "86.4 TB across 12 sources \u2014 78% measured, with 6 opportunities standing ready.",
    // renderFragments returns an ordered list of {kind, value} where kind is:
    //   "text"      -> plain text node (no styling)
    //   "underline" -> span with border-bottom:1px solid rgba(27,31,39,.25)
    //   "oxblood"   -> span with color:var(--oxblood)
    // The prototype's typographic treatment is preserved byte-for-byte on
    // both live-values and honest-empty variants.
    renderFragments: (v) => {
      const hasLive = v.estateSources != null || v.estateTables != null;
      if (!hasLive) {
        // Honest-empty variant · typographic treatment consistent with
        // prototype design language (3 underlined phrases + 1 oxblood).
        return [
          { kind: "text", value: "RMS AI is reading " },
          { kind: "underline", value: "no sources yet" },
          { kind: "text", value: ", " },
          { kind: "underline", value: "no size yet" },
          { kind: "text", value: " \u2014 " },
          { kind: "underline", value: "no measurement" },
          { kind: "text", value: ", " },
          { kind: "oxblood", value: "awaiting first census" },
          { kind: "text", value: "." },
        ];
      }
      // Live-values variant · real figures in underline spans, closing
      // phrase in oxblood.
      const sourcesPhrase = _sourcesPhrase(v.estateSources);
      const tablesPhrase = _tablesPhrase(v.estateTables);
      return [
        { kind: "text", value: "RMS AI is reading " },
        { kind: "underline", value: sourcesPhrase },
        { kind: "text", value: ", holding " },
        { kind: "underline", value: tablesPhrase },
        { kind: "text", value: " \u2014 " },
        { kind: "underline", value: "size and completeness not yet measured" },
        { kind: "text", value: ", " },
        { kind: "oxblood", value: "awaiting first census" },
        { kind: "text", value: "." },
      ];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "registry-census-header",
    // Slot #2a · census "Last activity" header line.
    // Wave-G5b · owner ruling (B) 2026-08-28T~14:30Z: migrate slot #2 to
    // styled-element-anchor with signature matching the ACTUAL render
    // ("Census #4 read the estate at the seam"), not the dead
    // "Every figure on this page traces to..." prefix.
    dummyContent: "Census #4 read the estate at the seam",
    anchorAncestorText: "Last activity",
    renderFragments: (v) => {
      if (v.lastCensus == null) {
        return [{ kind: "text", value: "No census has been run yet" }];
      }
      return [
        { kind: "text",
          value: `Census #${v.lastCensus.number} read the estate at the seam` },
      ];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "registry-census-byline",
    // Slot #2b · census byline (author + date + un-measured %).
    dummyContent: "Run Jul 21, 2026 by J. Mwangi \u00b7 22% still not yet measured",
    anchorAncestorText: "Last activity",
    renderFragments: (v) => {
      if (v.lastCensus == null) {
        return [{ kind: "text", value: "First census pending" }];
      }
      const c = v.lastCensus;
      return [{
        kind: "text",
        value: `Run ${c.date} by ${c.author} \u00b7 ${c.notMeasuredPct}% still not yet measured`,
      }];
    },
  },
  // Wave-G5b · 3 rendered stat tiles (owner ruling A · migrated from the
  // dead measureCards-bound rules). Bound to estate.stats[] labels that
  // dc-runtime ACTUALLY renders. Each tile has two rules (value + label)
  // so live-values enrichment can flow through the label too.
  {
    kind: "styled-element-anchor",
    name: "tile-total-held-value",
    dummyContent: "86.4 TB",
    anchorAncestorText: "held across 12 sources",
    renderFragments: (v) => [
      { kind: "text", value: v.totalVolume != null ? String(v.totalVolume) : "Not yet measured" },
    ],
  },
  {
    kind: "styled-element-anchor",
    name: "tile-total-held-label",
    dummyContent: "held across 12 sources",
    anchorAncestorText: "86.4 TB",
    anchorAncestorSlot: "tile-total-held-value",
    renderFragments: (v) => {
      if (v.estateSources == null) {
        return [{ kind: "text", value: "no sources yet" }];
      }
      const s = v.estateSources;
      return [{ kind: "text", value: `held across ${s} source${s === 1 ? "" : "s"}` }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "tile-share-measured-value",
    dummyContent: "78%",
    anchorAncestorText: "measured at last census",
    renderFragments: (v) => [
      { kind: "text", value: v.shareMeasured != null ? String(v.shareMeasured) : "Not yet measured" },
    ],
  },
  {
    kind: "styled-element-anchor",
    name: "tile-share-measured-label",
    dummyContent: "measured at last census",
    anchorAncestorText: "78%",
    anchorAncestorSlot: "tile-share-measured-value",
    renderFragments: (v) => {
      if (v.lastCensus == null) {
        return [{ kind: "text", value: "awaiting first census" }];
      }
      return [{ kind: "text", value: "measured at last census" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "tile-opportunities-value",
    dummyContent: "6",
    anchorAncestorText: "opportunities standing ready",
    renderFragments: (v) => [
      { kind: "text", value: v.opportunities != null ? String(v.opportunities) : "0" },
    ],
  },
  {
    kind: "styled-element-anchor",
    name: "tile-opportunities-label",
    dummyContent: "opportunities standing ready",
    anchorAncestorText: "opportunities",
    anchorAncestorSlot: "tile-opportunities-value",
    renderFragments: (v) => {
      if (v.opportunities == null) {
        return [{ kind: "text", value: "no opportunities yet" }];
      }
      return [{ kind: "text", value: "opportunities standing ready" }];
    },
  },
  // -------------------------------------------------------------------
  // Wave-G5c-COMPUTE-FRONTEND · RETIRED (2026-08-31 · harness probe).
  //
  // The 6 tile-compute-* rules originally authored in Wave-G5c targeted
  // the prototype's `computeCards` JS variable dummies:
  //   { '840 vCPU-h/day' · 'Total capacity' }
  //   { '62%'            · 'Allocated to Build' }
  //   { '3 queued'       · 'Queue depth' }
  //
  // Real-Chromium harness probe (tools/compute_where_probe.py ·
  // 2026-08-31) established that these dummies are NEVER rendered as
  // visible DOM on ANY prototype surface (portal, Admin, Registry
  // aside, Registry tab, Compute Connected sub-tab). Only "62%" appears
  // in the DOM (once, as a sibling within a different tile section)
  // and its anchor ancestor text "Allocated to Build" is also
  // script-only.
  //
  // Retirement precedent: DECISIONS.md documents that the composite
  // dummy "RMS AI holds 86.4 TB across 12 sources ..." was retired
  // in Wave-G5b for the same reason — dc-runtime never rendered it.
  //
  // The prototype's ACTUAL rendered compute surface (Compute Connected
  // sub-tab of RegistryTab) shows a percentage-driven layout:
  //   "43% of the month" · "43%" / "100%" / "43% committed" ·
  //   "645 hrs · 52%" / "298 hrs · 24%" / "174 hrs · 14%" / "99 hrs · 8%"
  //   / "24 hrs · 2%" · GPU workflows narrative
  //
  // W-G5c-close leaves these compute-tile rules retired. A follow-up
  // wave (W-G5c-COMPUTE-v2 in SPRINT_PLAN.md) will author new rules
  // against the actually-rendered percentage-driven surface, folding
  // akki-vm + akki-vm-ii facts into it per owner Ruling F.
  // -------------------------------------------------------------------

  // -------------------------------------------------------------------
  // Wave-G5c-COMPUTE-v2 · authored 2026-08-31 · owner ruling 8.
  // Rules bind to the ACTUALLY-rendered Compute Connected sub-tab of
  // RegistryTab. Every dummy below was verified as visible DOM text by
  // tools/compute_v2_dom_enum.py (probe artefact:
  // tools/compute_v2_dom_map.json).
  //
  // Discipline banked by ruling 8:
  //   - Rules authored only against harness-verified rendered DOM.
  //   - rule-must-match-rendered-DOM invariant enforced by test file
  //     tests/invariants/test_compute_v2_frontend.py.
  //   - Live values from /api/compute/estate only.
  //   - Honest-empty for anything the estate cannot measure.
  //   - Product language + prototype styling preserved.
  //
  // 4 LIVE + 6 HONEST-EMPTY + 1 LIVE-TAUTOLOGY = 11 rules.
  // -------------------------------------------------------------------

  // LIVE (4) — bind /api/compute/estate facts to compute tiles.

  {
    kind: "styled-element-anchor",
    name: "compute-v2-clusters-value",
    dummyContent: "1",
    anchorAncestorText: "Clusters attached",
    renderFragments: (v) => {
      const c = v.compute;
      if (!c || !Array.isArray(c.hosts) || c.hosts.length === 0) {
        return [{ kind: "text", value: "not measured" }];
      }
      return [{ kind: "text", value: String(c.hosts.length) }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-clusters-byline",
    // Owner Ruling F: fold akki-vm + akki-vm-ii into the compute surface.
    // Byline is DERIVED from v.compute.hosts[].name (never hardcoded).
    dummyContent: "on-premise \u00b7 RMS AI DC, Nairobi",
    anchorAncestorText: "Clusters attached",
    renderFragments: (v) => {
      const c = v.compute;
      if (!c || !Array.isArray(c.hosts) || c.hosts.length === 0) {
        return [{ kind: "text", value: "no hosts attached" }];
      }
      const names = c.hosts.map((h) => h.name).join(" + ");
      return [{ kind: "text", value: `on-premise \u00b7 ${names}` }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-gpus-value",
    dummyContent: "4",
    anchorAncestorText: "GPUs",
    renderFragments: (v) => {
      const c = v.compute;
      if (!c || !c.rollup || typeof c.rollup.gpu_count_total !== "number") {
        return [{ kind: "text", value: "not measured" }];
      }
      return [{ kind: "text", value: String(c.rollup.gpu_count_total) }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-gpus-byline",
    // Derived from gpu_model + gpu_memory_gb_per_gpu + host_count via
    // renderFragments below.
    dummyContent: "A100 80GB \u00b7 single node",
    anchorAncestorText: "GPUs",
    renderFragments: (v) => {
      const c = v.compute;
      if (!c || !Array.isArray(c.hosts) || c.hosts.length === 0) {
        return [{ kind: "text", value: "hardware not enumerated" }];
      }
      // Assume homogeneous fleet (verified for tonight's estate); if
      // heterogeneous, degrade to "mixed hardware · N nodes".
      const models = Array.from(new Set(c.hosts.map((h) => h.gpu_model)));
      const memGb = c.hosts[0].gpu_memory_gb_per_gpu;
      const hostCount = c.hosts.length;
      if (models.length !== 1 || typeof memGb !== "number") {
        return [{ kind: "text", value: `mixed hardware \u00b7 ${hostCount} nodes` }];
      }
      const modelShort = models[0].replace(/^NVIDIA\s+/i, "");
      const memRounded = Math.round(memGb);
      const nodeWord = hostCount === 1 ? "single node" : `${hostCount} nodes`;
      return [{ kind: "text", value: `${modelShort} ${memRounded} GiB \u00b7 ${nodeWord}` }];
    },
  },

  // HONEST-EMPTY (6) — estate has no mechanism to measure these yet;
  // rules render "not measured" instead of echoing prototype numbers.

  {
    kind: "styled-element-anchor",
    name: "compute-v2-capacity-value",
    dummyContent: "2,880 hrs",
    anchorAncestorText: "Capacity this month",
    renderFragments: (v) => {
      // No mechanism: monthly wall-clock capacity ledger doesn't exist yet.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-committed-value",
    dummyContent: "1,240 hrs",
    anchorAncestorText: "Committed to work",
    renderFragments: (v) => {
      // No mechanism: no allocation-hours ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-free-value",
    dummyContent: "1,640 hrs",
    anchorAncestorText: "Free to allocate",
    renderFragments: (v) => {
      // Derives from capacity - committed; both honest-empty.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-jobs-waiting-value",
    dummyContent: "2",
    anchorAncestorText: "Jobs waiting",
    renderFragments: (v) => {
      // No mechanism: no live queue-depth service on the seam.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-workflows-month-value",
    dummyContent: "18",
    anchorAncestorText: "Workflows this month",
    renderFragments: (v) => {
      // Training-run records exist (phase0/training_runner/runs/*.json)
      // but "workflows" is a broader product concept that isn't ledgered
      // separately yet; render honest-empty rather than conflate.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-v2-utilisation-value",
    dummyContent: "43%",
    anchorAncestorText: "Utilisation",
    renderFragments: (v) => {
      // Would need capacity-and-committed both live; both honest-empty.
      return [{ kind: "text", value: "not measured" }];
    },
  },

  // LIVE-TAUTOLOGY (1) — governance guarantees this by construction.

  {
    kind: "styled-element-anchor",
    name: "compute-v2-runs-receipted-value",
    dummyContent: "100%",
    anchorAncestorText: "Runs receipted",
    renderFragments: (v) => {
      // Every governed run (burn, txttrain, and future waves) crosses
      // through services.training_runner.ssh_seam.execute_remote_command
      // which persists a redacted receipt per call. Governance guarantees
      // 100% by construction — honest to assert.
      return [{ kind: "text", value: "100%" }];
    },
  },

  // -------------------------------------------------------------------
  // Wave-G5c-COMPUTE-RESIDUALS · authored 2026-09-06 · owner ruling
  // (verbatim in DECISIONS.md 2026-09-06T~12:XX). Completes the Compute
  // Connected sub-tab visual surface with 14 r1 chart-caption/per-bar
  // rules + 3 r2 tile-note rules = 17 all-honest-empty/honest-phrasing
  // additions (compute-estate has no hours ledger / no queue-depth /
  // no workflow-completion mechanism — 0 LIVE facts land this wave).
  //
  // Discipline (verbatim from owner ruling):
  //   - Rules authored ONLY against harness-verified rendered DOM
  //     (probe artefact: tools/compute_residuals_dom_map.json covering
  //     all 3 chart states door/week/state).
  //   - Live values from /api/compute/estate where a real fact exists
  //     (0 this wave — see grounding brief §B).
  //   - Honest-empty/honest-phrasing where no mechanism exists.
  //   - Styling preserved.
  //   - Grounding brief:
  //     /app/assessment_workspace/notes/wave_g5c_compute_residuals_grounding_brief.md
  //
  // Invariants: tests/invariants/test_compute_residuals_frontend.py
  // (11 tests · rule-must-match-rendered-DOM + full-iteration guards).
  // -------------------------------------------------------------------

  // r1 CHART CAPTIONS (3) — chartCaption slot for each of door/week/state.

  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-chart-caption-door",
    dummyContent: "1,240 hrs committed",
    anchorAncestorText: "Committed hours by door",
    renderFragments: (v) => {
      // No mechanism: no hours-committed-by-door ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-chart-caption-week",
    dummyContent: "of 2,880 hrs available",
    anchorAncestorText: "Hours run by week",
    renderFragments: (v) => {
      // No mechanism: no wall-clock-capacity or hours-run-by-week ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-chart-caption-state",
    dummyContent: "2,880 hrs this month",
    anchorAncestorText: "Hours by state",
    renderFragments: (v) => {
      // No mechanism: no monthly wall-clock capacity ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },

  // r1 PER-BAR LABELS · door state (5) — per-row `size` label
  // (e.g. "645 hrs \u00b7 52%"). Anchor is the row's own label text
  // (Train/Extract/Export/Measure/Prove) which is a unique text node in
  // the same grid row as the size label.

  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-door-train",
    dummyContent: "645 hrs \u00b7 52%",
    anchorAncestorText: "Train",
    renderFragments: (v) => {
      // No mechanism: no per-door hours-committed ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-door-extract",
    dummyContent: "298 hrs \u00b7 24%",
    anchorAncestorText: "Extract",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-door-export",
    dummyContent: "174 hrs \u00b7 14%",
    anchorAncestorText: "Export",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-door-measure",
    dummyContent: "99 hrs \u00b7 8%",
    anchorAncestorText: "Measure",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-door-prove",
    dummyContent: "24 hrs \u00b7 2%",
    anchorAncestorText: "Prove",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },

  // r1 PER-BAR LABELS · week state (4) — row anchor uses the verbatim
  // week-range label text (contains U+2013 EN DASH).

  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-week-1",
    dummyContent: "274 hrs \u00b7 38%",
    anchorAncestorText: "Aug 1\u20137",
    renderFragments: (v) => {
      // No mechanism: no hours-run-by-week ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-week-2",
    dummyContent: "339 hrs \u00b7 47%",
    anchorAncestorText: "Aug 8\u201314",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-week-3",
    dummyContent: "65 hrs \u00b7 9%",
    anchorAncestorText: "Aug 15\u201321",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-week-4",
    dummyContent: "43 hrs \u00b7 6%",
    anchorAncestorText: "Not yet run",
    renderFragments: (v) => {
      return [{ kind: "text", value: "not measured" }];
    },
  },

  // r1 PER-BAR LABELS · state state (2).

  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-state-committed",
    dummyContent: "1,240 hrs \u00b7 43%",
    anchorAncestorText: "Committed",
    renderFragments: (v) => {
      // No mechanism: no committed-hours-share ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r1-bar-state-free",
    dummyContent: "1,640 hrs \u00b7 57%",
    anchorAncestorText: "Free to allocate",
    renderFragments: (v) => {
      // No mechanism: no free-hours-share ledger.
      return [{ kind: "text", value: "not measured" }];
    },
  },

  // r2 TILE NOTES (3) — owner-named tile-note substitutions.
  // Grounding brief §B honest-phrasing mapping:
  //   - capacity  : "wall-clock ledger not measured" (names missing mechanism)
  //   - committed : "share-of-month not measured"   (names missing mechanism)
  //   - free      : "quoted against, not reserved"  (VERBATIM prototype
  //                                                  text preserved as
  //                                                  honest product-language —
  //                                                  not a numeric measurement,
  //                                                  analogous to compute-v2
  //                                                  runs-receipted LIVE-TAUTOLOGY)

  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r2-note-capacity",
    dummyContent: "wall-clock across 4 GPUs",
    anchorAncestorText: "Capacity this month",
    renderFragments: (v) => {
      // No mechanism: no monthly wall-clock capacity ledger.
      return [{ kind: "text", value: "wall-clock ledger not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r2-note-committed",
    dummyContent: "43% of the month",
    anchorAncestorText: "Committed to work",
    renderFragments: (v) => {
      // No mechanism: no share-of-month allocation ledger.
      return [{ kind: "text", value: "share-of-month not measured" }];
    },
  },
  {
    kind: "styled-element-anchor",
    name: "compute-residuals-r2-note-free",
    dummyContent: "quoted against, not reserved",
    anchorAncestorText: "Free to allocate",
    renderFragments: (v) => {
      // HONEST-PHRASING preserving verbatim prototype product-language.
      // The prototype text is a governance statement about allocation
      // policy (not a numeric measurement) — no allocation lock exists
      // in the system by construction; quoting-against-not-reserving is
      // guaranteed by the current absence of a compute-reservation seam.
      // Analogous to compute-v2-runs-receipted-value LIVE-TAUTOLOGY.
      return [{ kind: "text", value: "quoted against, not reserved" }];
    },
  },
];

// Wave-G5b · expose the dummies (never the render output) to window so
// the real-Chromium harness can introspect all rules and check every
// dummyContent is present in the rendered DOM. This is the mechanical
// underpinning of owner's "rule-must-match-rendered-DOM" invariant
// (DECISIONS.md 2026-08-28T~14:30Z · ruling A).
if (typeof window !== "undefined") {
  window.V8_SUBSTITUTIONS_DUMMIES = V8_SUBSTITUTIONS.map((r) => ({
    name: r.name,
    kind: r.kind,
    dummyContent: r.dummyContent || null,
    anchorAncestorText: r.anchorAncestorText || null,
  }));
}

function _findAncestorContainingText(node, label, root) {
  let anc = node.parentNode;
  while (anc && anc !== root) {
    const tc = anc.textContent || "";
    if (tc.includes(label)) return anc;
    anc = anc.parentNode;
  }
  return null;
}

/**
 * _findAncestorWithSlot — Wave-G5c pair-anchor recovery.
 *
 * When two rules pair as (value, label) with each other's dummy as the
 * anchor, the rule that fires FIRST destroys the OTHER's anchor text
 * (replacing the paired element's textContent). On subsequent applyAll
 * calls (MutationObserver re-fire), the second rule's anchor-text
 * check fails and it stays un-substituted forever.
 *
 * This helper lets the SECOND rule accept "paired rule's slot marker
 * exists in a shared ancestor" as valid anchor evidence — i.e. once
 * the value has been substituted (data-substituted-slot=<paired>), the
 * label rule can still bind because the pair is still structurally
 * co-located.
 */
function _findAncestorWithSlot(node, slotName, root) {
  let anc = node.parentNode;
  while (anc && anc !== root) {
    if (anc.querySelector && anc.querySelector(`[data-substituted-slot="${slotName}"]`)) {
      return anc;
    }
    anc = anc.parentNode;
  }
  return null;
}

function applySubstitutions(doc, vals) {
  if (!doc || !doc.body) return 0;
  let count = 0;

  for (const rule of V8_SUBSTITUTIONS) {

    // Wave-H INTERRUPT 3 · styled-element-anchor · rebuild container's
    // children preserving prototype inline span structure (underline +
    // oxblood). Owner directive verbatim (DECISIONS.md 2026-08-28T~13:25Z):
    //   "reusing the prototype's own inline markup IS the literal-adoption
    //    standard ... post-substitution DOM must contain the expected
    //    styled span/link elements (assert style signature presence, not
    //    just text)."
    if (rule.kind === "styled-element-anchor") {
      const fragments = rule.renderFragments(vals);
      if (!fragments || fragments.length === 0) continue;
      const desiredFullText = fragments.map((f) => f.value).join("");
      const dummyTrim = rule.dummyContent.trim();
      const markerAttr = "data-substituted-slot";
      const markerVal = rule.name;
      // Priority 1: element already marked → check if desired changed.
      const marked = doc.querySelector(`[${markerAttr}="${markerVal}"]`);
      let target = marked;
      if (!target) {
        // Priority 2: walk all element matches, apply anchorAncestorText
        // filter if set, then pick the DEEPEST (last in doc order) so
        // leaf spans win over containers that happen to share text.
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
        const matches = [];
        let candidate;
        while ((candidate = walker.nextNode())) {
          const tc = (candidate.textContent || "").trim();
          if (tc !== dummyTrim) continue;
          if (rule.anchorAncestorText || rule.anchorAncestorSlot) {
            // Pair-anchor recovery: accept EITHER raw-text ancestor
            // OR paired-slot-marker ancestor (see _findAncestorWithSlot
            // doc). This lets label rules bind after their value pair
            // has already fired.
            const textAnc = rule.anchorAncestorText
              ? _findAncestorContainingText(candidate, rule.anchorAncestorText, doc.body)
              : null;
            const slotAnc = rule.anchorAncestorSlot
              ? _findAncestorWithSlot(candidate, rule.anchorAncestorSlot, doc.body)
              : null;
            if (!textAnc && !slotAnc) continue;
          }
          matches.push(candidate);
        }
        if (matches.length === 0) continue;
        target = matches[matches.length - 1]; // deepest
      }
      if (!target) continue;
      // Skip if already at desired · but always ensure the marker is set
      // so audits reflect the rule bound to the DOM. Without this, a
      // rule whose live-value render happens to match the prototype's
      // dummy character-for-character (e.g., tile-share-measured-label
      // whose live render is literally "measured at last census") would
      // never get its data-substituted-slot marker, leaving the audit
      // showing the dummy as "still present" and the harness scoring RED.
      if ((target.textContent || "").trim() === desiredFullText.trim()) {
        if (!target.getAttribute(markerAttr)) {
          target.setAttribute(markerAttr, markerVal);
        }
        continue;
      }
      const newChildren = fragments.map((f) => {
        if (f.kind === "text") return doc.createTextNode(f.value);
        const span = doc.createElement("span");
        if (f.kind === "underline") {
          span.setAttribute(
            "style",
            "border-bottom:1px solid rgba(27,31,39,.25);"
          );
        } else if (f.kind === "oxblood") {
          span.setAttribute("style", "color:var(--oxblood);");
        }
        span.textContent = f.value;
        return span;
      });
      target.replaceChildren(...newChildren);
      target.setAttribute(markerAttr, markerVal);
      count++;
      continue;
    }

    const desired = rule.render(vals);
    if (desired == null) continue;

    if (rule.kind === "element-anchor") {
      // Whole-element textContent replacement — handles fragmented spans.
      // Idempotency emerges from state: after mutation, textContent equals
      // desired ≠ dummyContent, so subsequent walks find no match.
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
      let el;
      const dummyTrim = rule.dummyContent.trim();
      while ((el = walker.nextNode())) {
        const tc = (el.textContent || "").trim();
        if (tc !== dummyTrim) continue;
        if (el.textContent !== desired) {
          el.textContent = desired;
          count++;
        }
        break;
      }
      continue;
    }

    if (rule.kind === "text-node") {
      // Idempotency emerges from state: after mutation, node.nodeValue no
      // longer matches rule.signature.
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        const text = node.nodeValue;
        if (!text || text.length < 4) continue;
        if (rule.signature.test(text)) {
          if (node.nodeValue !== desired) {
            node.nodeValue = desired;
            count++;
          }
          break;
        }
      }
      continue;
    }

    if (rule.kind === "tile-value") {
      // Match ONLY on trimmed === rule.dummy (not desired). This avoids a
      // collision where an unrelated tile whose LABEL text happens to
      // equal `desired` (e.g., the "Not yet measured" tile's label
      // colliding with the HONEST-EMPTY rendering of every other tile)
      // is mistaken for the target. Idempotency emerges from state:
      // after mutation, nodeValue equals desired ≠ dummy.
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        const trimmed = (node.nodeValue || "").trim();
        if (trimmed !== rule.dummy) continue;
        const anc = _findAncestorContainingText(node, rule.label, doc.body);
        if (!anc) continue;
        if (node.nodeValue !== desired) {
          node.nodeValue = desired;
          count++;
        }
        break;
      }
      continue;
    }
  }

  return count;
}

// ---------------------------------------------------------------------------
// PortalIframe — the single user-facing surface (Wave G4 CORRECTION 3).
// ---------------------------------------------------------------------------

function PortalIframe() {
  const iframeRef = useRef(null);
  // Monotonic counter of successful substitutions this session — surfaced
  // as data-substitution-applied on the outer iframe host div so external
  // harnesses can prove substitutions actually ran without reading into
  // the prototype's DOM.
  const [substitutionsApplied, setSubstitutionsApplied] = useState(0);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    let observer = null;
    let scheduled = false;
    const liveValues = {
      estateSources: null,
      estateTables: null,
      lastCensus: null,
      totalVolume: null,
      shareMeasured: null,
      opportunities: null,
      compute: null,
    };

    const applyAll = () => {
      if (scheduled) return; // Debounce burst mutations from dc-runtime.
      scheduled = true;
      const run = () => {
        scheduled = false;
        const doc = iframe.contentDocument;
        if (!doc || !doc.body) return;
        const count = applySubstitutions(doc, liveValues);
        // Wave-H · harness instrumentation: emit a console line each time
        // applyAll runs so the real-Chromium harness can see the engine's
        // liveness independently of React state.
        try {
          console.log(
            `wave_g5_substitutions applyAll_run count=${count} bodyLen=${(doc.body.textContent || "").length}`
          );
        } catch (_) {
          /* no-op */
        }
        if (count > 0) {
          setSubstitutionsApplied((prev) => prev + count);
        }
      };
      if (typeof window !== "undefined" && window.requestAnimationFrame) {
        window.requestAnimationFrame(run);
      } else {
        setTimeout(run, 0);
      }
    };

    const onLoad = async () => {
      // Pull live values (silent — HONEST-EMPTY fallback fires when null).
      const backend = process.env.REACT_APP_BACKEND_URL || "";

      // (1) Registry facts — connected sources + table count.
      try {
        const res = await fetch(`${backend}/api/registry/facts`);
        if (res.ok) {
          const facts = await res.json();
          if (facts && Array.isArray(facts.data_sources)) {
            liveValues.estateSources = facts.data_sources.length;
            let tables = 0;
            for (const s of facts.data_sources) {
              if (typeof s.table_count === "number") tables += s.table_count;
            }
            liveValues.estateTables = tables;
          }
        }
      } catch (_) {
        /* silent */
      }

      // (2) Wave-G5c · census status line + estate scale from live
      // census output (owner Stage 3 wiring: Registry reads from
      // /api/census/latest wherever the census provides the truer
      // figure). Census manifest fields land as:
      //   lastCensus.number    ← census_id
      //   lastCensus.date      ← finished_at_utc (formatted)
      //   lastCensus.author    ← initiator
      //   lastCensus.notMeasuredPct  ← honest-empty (census walks
      //     aggregates, not size-in-bytes)
      // estateTables also updates from rollup.table_count (census is
      // authoritative once it has run — walks EVERY table, not the
      // truncated top-25 in the connection record).
      try {
        const res = await fetch(`${backend}/api/census/latest`);
        if (res.ok) {
          const body = await res.json();
          const c = body && body.census;
          if (c && c.census_id != null) {
            const finished = (c.finished_at_utc || "").slice(0, 10);
            liveValues.lastCensus = {
              number: c.census_id,
              date: finished || "recent",
              author: c.initiator || "owner",
              notMeasuredPct: "size",
            };
            if (c.rollup && typeof c.rollup.table_count === "number") {
              liveValues.estateTables = c.rollup.table_count;
            }
            if (c.rollup && typeof c.rollup.database_count === "number") {
              // Census "sees" databases as sources when the connection
              // record hasn't been widened yet.
              if (liveValues.estateSources == null
                  || liveValues.estateSources < c.rollup.database_count) {
                liveValues.estateSources = c.rollup.database_count;
              }
            }
          }
        }
      } catch (_) {
        /* silent */
      }

      // (3) Wave-G5c-COMPUTE-BACKEND · compute descriptor.
      try {
        const res = await fetch(`${backend}/api/compute/estate`);
        if (res.ok) {
          const body = await res.json();
          if (body && Array.isArray(body.hosts)) {
            liveValues.compute = body;
          }
        }
      } catch (_) {
        /* silent */
      }

      // Give dc-runtime time for the first render pass.
      await new Promise((r) => setTimeout(r, 400));
      applyAll();

      // Re-apply on every subsequent dc-runtime re-render (tab switch,
      // Registry mount, drawer open, etc.). Idempotent → safe.
      try {
        const doc = iframe.contentDocument;
        if (doc && doc.body) {
          observer = new MutationObserver(applyAll);
          observer.observe(doc.body, {
            childList: true,
            characterData: true,
            subtree: true,
          });
        }
      } catch (_) {
        /* no-op */
      }
    };

    iframe.addEventListener("load", onLoad);
    return () => {
      iframe.removeEventListener("load", onLoad);
      if (observer) observer.disconnect();
    };
  }, []);

  return (
    <div
      data-testid="v8-portal-iframe-host"
      data-substitution-applied={substitutionsApplied}
      style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, overflow: "hidden" }}
    >
      <iframe
        ref={iframeRef}
        data-testid="v8-prototype-iframe"
        src="/v8_prototype.html"
        title="Akki OS \u00b7 RMS AI"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// App — single-surface routing (Wave G4 CORRECTION 3).
// All paths (root + wildcard) render <PortalIframe/>. The 15 legacy
// deep-link routes are retired. Component source files retained.
// ---------------------------------------------------------------------------

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* Track 1 — DAP Portal */}
          <Route path="/dap" element={<DAPLayout />}>
            <Route index element={<DAPLanding />} />
            <Route path="extract/:mode" element={<ExtractModes />} />
            <Route path="resources/:tab" element={<AvailableResources />} />
            <Route path="governance/:tab" element={<DataGovernance />} />
            <Route path="connect/:tab" element={<ConnectResources />} />
            <Route path="requests" element={<RequestLifecycle />} />
            <Route path="entitlement" element={<Entitlement />} />
            <Route path="countdown" element={<CanonCountdown />} />
            <Route path="estates/:estateId" element={<DataEstates />} />
            <Route path="*" element={<Navigate to="/dap" replace />} />
          </Route>

          {/* Track 3 — OS Native React surfaces · Turn 4 sub-slice 4d · Work tab + Monitor sub-view.
             Routes are additive (SO §3.8) and land BEFORE the PortalIframe wildcard fallback so
             a tester can reach each native surface at ${REACT_APP_BACKEND_URL}/os/work/<leaf> or
             /os/monitor/<leaf>. Un-implemented leaves continue to fall through to the V8/PortalIframe
             render at "/" and "/*" until subsequent sub-slices (4e-4g) land more native surfaces. */}
          <Route path="/os/work/chat" element={<WorkChat />} />
          <Route path="/os/work/analyze" element={<WorkAnalyze />} />
          <Route path="/os/work/documents" element={<WorkDocuments />} />
          <Route path="/os/work/tasks" element={<WorkTasks />} />
          <Route path="/os/work/team" element={<WorkTeam />} />
          <Route path="/os/work/performance" element={<WorkPerformance />} />
          <Route path="/os/work/board" element={<WorkBoard />} />
          <Route path="/os/monitor/signals" element={<MonitorSignals />} />
          <Route path="/os/monitor/ideas" element={<MonitorIdeas />} />

          {/* Sub-slice 4e · ThinkLab (Work tab) + Admin tab groups (estate/approvals/watch) */}
          <Route path="/os/work/clarity" element={<ThinkLabClarity />} />
          <Route path="/os/work/strategy" element={<ThinkLabStrategy />} />
          <Route path="/os/work/hypothesis" element={<ThinkLabHypothesis />} />
          <Route path="/os/work/perspective" element={<ThinkLabPerspective />} />
          <Route path="/os/admin/estate" element={<AdminEstate />} />
          <Route path="/os/admin/govern" element={<AdminGovern />} />
          <Route path="/os/admin/greymirror" element={<AdminGreyMirror />} />
          <Route path="/os/admin/spendreq" element={<AdminSpendReq />} />
          <Route path="/os/admin/rulesupd" element={<AdminRulesUpd />} />
          <Route path="/os/admin/modeladmission" element={<AdminModelAdmission />} />
          <Route path="/os/admin/wstate" element={<AdminWState />} />
          <Route path="/os/admin/wrecord" element={<AdminWRecord />} />
          <Route path="/os/admin/wunder" element={<AdminWUnder />} />
          <Route path="/os/admin/wdecisions" element={<AdminWDecisions />} />

          {/* Sub-slice 4f · Build/Buildlib (build tab) + Collab (work tab) + 3rdParty (apps tab) */}
          <Route path="/os/build/train" element={<BuildTrain />} />
          <Route path="/os/build/agentbuild" element={<BuildAgent />} />
          <Route path="/os/build/buildskill" element={<BuildSkill />} />
          <Route path="/os/build/extract" element={<BuildExtract />} />
          <Route path="/os/build/youragents" element={<BuildlibAgents />} />
          <Route path="/os/build/yourmodels" element={<BuildlibModels />} />
          <Route path="/os/work/mentions" element={<CollabMentions />} />
          <Route path="/os/work/emails" element={<CollabEmails />} />
          <Route path="/os/work/projects" element={<CollabProjects />} />
          <Route path="/os/work/hrstuff" element={<CollabHrStuff />} />
          <Route path="/os/apps/new" element={<AppsNew />} />
          <Route path="/os/apps/frequent" element={<AppsFrequent />} />
          <Route path="/os/apps/connected" element={<AppsConnected />} />
          <Route path="/os/apps/requests" element={<AppsRequests />} />

          {/* Track 2 — OS Prototype v2 (V8 PortalIframe) */}
          <Route path="/" element={<PortalIframe />} />
          <Route path="*" element={<PortalIframe />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export { PortalIframe };
export default App;
