import React, { useState } from "react";
import StatusBadge from "@/components/dap/StatusBadge";
import { ChevronDown, ChevronUp, RotateCcw, Plus, AlertTriangle, Clock, CheckCircle } from "lucide-react";
import { ENT_23_COST_NOT_MEASURED } from "@/strings/entitlementStrings";

/**
 * Request Lifecycle — DAP §4.2
 * The spine of the DAP. Shows the complete state machine.
 * 
 * Owner-ratified lifecycle rules (BINDING):
 * a. Interrupted (platform fault) — visible, bounded auto-retry max 3, attempt counter shown
 * b. Expired (14-day, working-day roll-forward) — ONE recourse: "Submit again as a new request"
 * c. Spend-ceiling breach folds into In Approval with reason line
 * d. Escrow semantics on suspension
 * e. Suspension notices visible only to org admin + affected submitters
 * 
 * HARD OMISSIONS:
 * - NO partial-release UI
 * - NO "Waited N days" turnaround copy
 */

const MODE_VERB = {
  processed: "Open report", finetune: "Download model",
  skills: "Download skill", raw: "Download data"
};

const BLOCK_KIND_META = {
  request: { kindLine: "About the request; resubmitting unchanged will be blocked again", showCopy: true },
  check: { kindLine: "Not about your request; a platform check couldn't complete", showCopy: true },
  estate: {
    kindLine: "About an estate-level limit, not your request or agreement",
    fixedReason: "The platform refused this release. No detail is available.",
    showCopy: false
  },
};

// Sample requests showing the full state machine (from DAP reference HTML).
// In production these would come from a real endpoint (backend pending).
const SAMPLE_REQUESTS = [
  {
    id: "ftn-2026-0118", objective: "Train on the cleared complaint files to route by urgency.",
    status: "Executing", pct: 41, eta: "~6h to completion", mode: "finetune",
    agreement: "Agreement MER-007", submitted: "submitted 5 Sep 2026", submittedBy: "R. Adeyemi",
    scope: "Audio", signoffRequired: true, approvedDate: "12 Sep 2026", approvedByRole: "records authority",
  },
  {
    id: "prc-2026-0109", objective: "Find out which branches drive repeat complaints, this quarter.",
    status: "Executing", stageIndex: 2, stageCount: 4, stageLabel: "Analyzing", eta: "~40 min",
    mode: "processed", agreement: "Agreement MER-002", submitted: "submitted 16 Sep 2026", submittedBy: "T. Mwangi",
    scope: "Audio", signoffRequired: false,
  },
  {
    id: "ftn-2026-0119", objective: "Train on IVR prompts to flag automated-menu drop-off.",
    status: "In Approval", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 13 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    submittedAtISO: "2026-09-13", windowEndsAtISO: "2026-09-28",
    spendCeilingBreach: false,
  },
  {
    id: "ftn-2026-0121", objective: "Train on branch chat logs to flag escalation risk.",
    status: "In Approval", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 5 Sep 2026", submittedBy: "A. Osei", scope: "Audio",
    submittedAtISO: "2026-09-05", windowEndsAtISO: "2026-09-19",
    spendCeilingBreach: true,
    spendCeilingReason: "Organisation ceiling reached for this period. Spend-ceiling breach folds into In Approval.",
  },
  {
    id: "int-2026-0001", objective: "Extract quality metrics from the call recordings.",
    status: "Interrupted (platform fault)", mode: "processed",
    agreement: "Agreement MER-002", submitted: "submitted 17 Sep 2026", submittedBy: "R. Adeyemi",
    scope: "Audio", retryAttempts: 2, maxRetries: 3,
    interruptReason: "Upstream compute node unreachable. Bounded auto-retry in progress.",
  },
  {
    id: "ftn-2026-0120", objective: "Train on radio segments to detect ad breaks.",
    status: "Ready", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 10 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    modelId: "MDL-2026-0120", baseModel: "meridian-audio-base-v3",
    targetsSet: "88%", targetsAchieved: "91%", weightsHash: "sha256:7be2a0\u2026d914",
    signoffRequired: true, approvedByRole: "records authority", approvedDate: "14 Sep 2026",
  },
  {
    id: "prc-2026-0111", objective: "Find out which time-of-day produces the most complaint escalations.",
    status: "Retrieved", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 13 Sep 2026", submittedBy: "R. Adeyemi", scope: "Text",
    retrievedAt: "18 Sep 2026",
  },
  {
    id: "ftn-2026-0117", objective: "Train on the call recordings to classify caller intent at 88% accuracy or better.",
    status: "Refused", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 2 Sep 2026", submittedBy: "A. Osei", scope: "Audio",
    refusalReason: "The call recordings contain spoken account details, and Digicow would not release a model trained on them under this agreement. That reason is recorded rather than left implicit.",
  },
  {
    id: "prc-2026-0104", objective: "Find out complaint volume by branch, last quarter.",
    status: "Expired", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 19 Aug 2026", submittedBy: "R. Adeyemi",
    submittedAtISO: "2026-08-18", expiredAtISO: "2026-09-02", expiredAtDisplay: "2 Sep 2026",
  },
  {
    id: "skl-2026-0047", objective: "Build a skill to summarise complaint threads by branch.",
    status: "Blocked", mode: "skills", agreement: "Agreement MER-007",
    submitted: "submitted 5 Sep 2026", submittedBy: "T. Mwangi", scope: "Text",
    blockedAt: "14 Sep 2026, 03:12", blockKind: "estate",
    blockReason: "The platform refused this release. No detail is available.",
    blockRef: "SKL-2026-0047-B1", dataOwner: "the data governance office at Digicow",
  },
  {
    id: "prc-2026-0102", objective: "Find out average time-to-close by branch, last quarter.",
    status: "Blocked", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 12 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    blockedAt: "13 Sep 2026, 17:40", blockKind: "request",
    blockReason: "There isn't enough time-to-close data recorded for last quarter to answer this by branch.",
    blockRef: "PRC-2026-0102-B1",
  },
];

const ALL_STATES = [
  "In Approval", "Executing", "Ready", "Retrieved", "Refused", "Blocked",
  "Expired", "Interrupted (platform fault)", "Blocked \u00b7 check"
];

const RAIL_ROW = [
  ["Total", "Total"], ["In Approval", "In Approval"], ["Executing", "Executing"],
  ["Ready", "Ready"], ["Retrieved", "Retrieved"], ["Refused", "Refused"],
  ["Blocked", "Blocked"], ["Expired", "Expired"], ["Interrupted (platform fault)", "Interrupted"],
];

function RequestCard({ req }) {
  const [expanded, setExpanded] = useState(false);
  const blockMeta = req.blockKind ? BLOCK_KIND_META[req.blockKind] : null;

  return (
    <div
      data-testid={`request-card-${req.id}`}
      className="rounded-lg border overflow-hidden transition-shadow hover:shadow-sm"
      style={{ borderColor: "var(--line)", background: "white" }}
    >
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{req.id}</span>
              <StatusBadge status={req.status} />
            </div>
            <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{req.objective}</p>
          </div>
          <button
            data-testid={`request-expand-${req.id}`}
            onClick={() => setExpanded(!expanded)}
            className="p-1 rounded hover:bg-black/5 transition-colors"
          >
            {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
        </div>

        <div className="flex flex-wrap gap-3 text-xs" style={{ color: "var(--ink3)" }}>
          <span>{req.mode && MODE_VERB[req.mode] ? MODE_VERB[req.mode] : req.mode}</span>
          <span>·</span>
          <span>{req.agreement}</span>
          <span>·</span>
          <span>{req.submitted}</span>
        </div>

        {/* Spend-ceiling breach folded into In Approval with reason */}
        {req.status === "In Approval" && req.spendCeilingBreach && (
          <div className="mt-2 text-xs p-2 rounded" style={{ background: "rgba(176,141,46,.08)", color: "var(--brass)" }}>
            <AlertTriangle size={12} className="inline mr-1" />
            {req.spendCeilingReason}
          </div>
        )}

        {/* Interrupted state with retry counter */}
        {req.status === "Interrupted (platform fault)" && (
          <div className="mt-2 flex items-center gap-2 text-xs p-2 rounded" style={{ background: "rgba(184,57,91,.06)", color: "var(--oxblood)" }}>
            <RotateCcw size={12} />
            <span>
              Auto-retry attempt {req.retryAttempts || 0} of {req.maxRetries || 3}
              {req.retryAttempts >= (req.maxRetries || 3) && " — exhausted, resolves to Blocked · check"}
            </span>
          </div>
        )}

        {/* Executing progress */}
        {req.status === "Executing" && req.pct != null && (
          <div className="mt-2">
            <div className="flex items-center justify-between text-xs mb-1" style={{ color: "var(--ink3)" }}>
              <span>{req.stageLabel || "Processing"}</span>
              <span>{req.eta}</span>
            </div>
            <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
              <div className="h-full rounded-full transition-all" style={{ width: `${req.pct}%`, background: "var(--accent)" }} />
            </div>
          </div>
        )}

        {/* Ready state */}
        {req.status === "Ready" && req.modelId && (
          <div className="mt-2 text-xs" style={{ color: "var(--ink3)" }}>
            <span>Model: {req.modelId} · Base: {req.baseModel}</span>
            {req.weightsHash && <span className="ml-2 font-mono">{req.weightsHash}</span>}
          </div>
        )}
      </div>

      {/* Expanded details */}
      {expanded && (
        <div className="border-t px-4 py-3 text-sm" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
          {req.submittedBy && <p style={{ color: "var(--ink2)" }}>Submitted by {req.submittedBy}</p>}
          {req.scope && <p style={{ color: "var(--ink3)" }}>Scope: {req.scope}</p>}

          {/* Blocked state details */}
          {req.status === "Blocked" && blockMeta && (
            <div className="mt-2 border-l-4 p-3 rounded" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
              <p className="text-xs font-medium mb-1" style={{ color: "var(--oxblood)" }}>
                {blockMeta.kindLine}
              </p>
              <p className="text-sm" style={{ color: "var(--ink2)" }}>
                {req.blockKind === "estate" ? blockMeta.fixedReason : req.blockReason}
              </p>
              {req.blockRef && (
                <p className="text-xs font-mono mt-1" style={{ color: "var(--ink3)" }}>{req.blockRef}</p>
              )}
              {req.blockKind === "estate" && req.dataOwner && (
                <p className="text-xs mt-1" style={{ color: "var(--ink3)" }}>
                  Contact {req.dataOwner} before submitting again.
                </p>
              )}
              {/* estate block: copy button hidden per spec */}
            </div>
          )}

          {/* Expired: exactly ONE recourse */}
          {req.status === "Expired" && (
            <div className="mt-2 p-3 rounded" style={{ background: "rgba(27,31,39,.04)" }}>
              <p className="text-xs mb-1" style={{ color: "var(--ink3)" }}>
                Expired {req.expiredAtDisplay || ""}. The 14-day approval window closed.
              </p>
              <button
                data-testid={`request-resubmit-${req.id}`}
                className="mt-2 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white"
                style={{ borderColor: "var(--hair)", color: "var(--ink)" }}
              >
                Submit again as a new request
              </button>
            </div>
          )}

          {/* Refused */}
          {req.status === "Refused" && req.refusalReason && (
            <div className="mt-2 border-l-4 p-3 rounded" style={{ borderColor: "var(--ink)", background: "rgba(27,31,39,.03)" }}>
              <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.refusalReason}</p>
            </div>
          )}

          {/* Retrieved */}
          {req.status === "Retrieved" && req.retrievedAt && (
            <p className="mt-1" style={{ color: "var(--sage)" }}>
              <CheckCircle size={12} className="inline mr-1" />
              Retrieved {req.retrievedAt}
            </p>
          )}

          {/* Approval info — no "Waited N days" per hard omission */}
          {req.approvedByRole && (
            <p className="mt-1" style={{ color: "var(--ink3)" }}>
              Approved by {req.approvedByRole} on {req.approvedDate}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default function RequestLifecycle() {
  const [filter, setFilter] = useState("Total");
  const counts = {};
  for (const r of SAMPLE_REQUESTS) {
    counts[r.status] = (counts[r.status] || 0) + 1;
  }
  counts["Total"] = SAMPLE_REQUESTS.length;

  const filtered = filter === "Total"
    ? SAMPLE_REQUESTS
    : SAMPLE_REQUESTS.filter((r) => r.status === filter);

  return (
    <div data-testid="request-lifecycle" className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="request-lifecycle-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
      >
        Request Lifecycle
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        Every request passes through a state machine. This view shows the full lifecycle.
      </p>

      {/* State machine legend */}
      <div data-testid="state-machine-legend" className="mb-6">
        <h2 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>State Legend</h2>
        <div className="flex flex-wrap gap-2">
          {ALL_STATES.map((s) => (
            <StatusBadge key={s} status={s} />
          ))}
        </div>
      </div>

      {/* Rail counts */}
      <div data-testid="request-rail" className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
        <div className="grid grid-cols-9 text-center">
          {RAIL_ROW.map(([key, label]) => (
            <button
              key={key}
              data-testid={`rail-${key.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
              onClick={() => setFilter(key)}
              className={`py-3 text-xs transition-colors border-b-2 ${
                filter === key ? "font-semibold" : "hover:bg-black/[.02]"
              }`}
              style={{
                borderBottomColor: filter === key ? "var(--blue)" : "transparent",
                color: filter === key ? "var(--ink)" : "var(--ink3)",
              }}
            >
              <span className="block text-lg font-semibold">{counts[key] || 0}</span>
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Request cards */}
      <div className="space-y-3" data-testid="request-list">
        {filtered.map((req) => (
          <RequestCard key={req.id} req={req} />
        ))}
        {filtered.length === 0 && (
          <div className="text-center py-8">
            <p className="text-sm" style={{ color: "var(--ink3)" }}>No requests in this state.</p>
          </div>
        )}
      </div>

      {/* Backend pending notice */}
      <div className="mt-8 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
        <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>Backend pending</p>
        <p className="text-xs" style={{ color: "var(--ink3)" }}>
          The request lifecycle endpoints (submit, list, poll, retrieve, approve) are not yet built in the backend.
          The requests shown above are the reference state machine rendered from the DAP design specification.
          Once the backend endpoints are available, this view will display real request data.
        </p>
      </div>
    </div>
  );
}
