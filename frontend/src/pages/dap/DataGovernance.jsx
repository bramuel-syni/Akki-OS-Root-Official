import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import LoadingState from "@/components/shared/LoadingState";
import TransportError from "@/components/shared/TransportError";
import HonestEmpty from "@/components/shared/HonestEmpty";
import BackendPending from "@/components/shared/BackendPending";
import { get, fetchGovernEstateRulesRecord, fetchTeamAccessRegister, fetchGovernTrustCenter } from "@/lib/apiClient";
import { useAuth } from "@/pages/dap/DAPLayout";

/**
 * Data Governance — DAP §4.5
 * 3 views: Policies & Regulations, Contract & Access Terms, Data Collection
 */

function PoliciesView() {
  const { user } = useAuth();
  const [govState, setGovState] = useState(null);
  const [estateRules, setEstateRules] = useState(null);
  const [trustCenter, setTrustCenter] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const promises = [
      get("/api/governance/state").then(setGovState).catch(() => {}),
    ];
    if (user) {
      promises.push(
        fetchGovernEstateRulesRecord().then(setEstateRules).catch(() => {}),
        fetchGovernTrustCenter().then(setTrustCenter).catch(() => {}),
      );
    }
    Promise.all(promises)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [user]);

  if (loading) return <LoadingState message="Reading the governance state\u2026" />;
  if (error) return <TransportError error={error} />;

  const sRails = estateRules?.S_rails || [];
  const oRules = estateRules?.O_rules || [];
  const refusals = trustCenter?.refusals?.rows || [];

  return (
    <div data-testid="governance-policies">
      {/* Governance overview cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>Approvals</p>
          <p data-testid="gov-approvals-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>
            {govState?.approvals?.count ?? 0}
          </p>
        </div>
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--accent)" }}>Rules Updates</p>
          <p data-testid="gov-rules-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>
            {govState?.rules_updates?.count ?? 0}
          </p>
        </div>
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--gate)" }}>Reserved Decisions</p>
          <p data-testid="gov-reserved-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>
            {govState?.reserved_decisions?.count ?? 0}
          </p>
        </div>
      </div>

      {govState?.reference_note && (
        <div
          data-testid="gov-reference-note"
          className="rounded-lg p-4 mb-6 text-xs"
          style={{ background: "var(--surface)", color: "var(--ink3)", fontFamily: "var(--mono, monospace)" }}
        >
          {govState.reference_note}
        </div>
      )}

      {/* Estate Rules — auth-gated */}
      {estateRules ? (
        <div className="mb-6">
          <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
            Estate Rules ({sRails.length + oRules.length} rules)
          </h3>
          {sRails.length > 0 && (
            <div className="mb-4">
              <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>S-Rails (structural)</p>
              <div className="space-y-1">
                {sRails.map((r, i) => (
                  <div key={i} data-testid={`estate-rule-s-${i}`} className="flex items-center justify-between rounded border p-3" style={{ borderColor: "var(--line)", background: "white" }}>
                    <div>
                      <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{r.name}</p>
                      <p className="text-xs" style={{ color: "var(--ink3)" }}>{r.value}</p>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ color: "var(--sage)", background: "rgba(29,122,110,.12)" }}>
                      {r.enforcement_class}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {oRules.length > 0 && (
            <div>
              <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>O-Rules (operational)</p>
              <div className="space-y-1">
                {oRules.map((r, i) => (
                  <div key={i} data-testid={`estate-rule-o-${i}`} className="flex items-center justify-between rounded border p-3" style={{ borderColor: "var(--line)", background: "white" }}>
                    <div>
                      <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{r.name}</p>
                      <p className="text-xs" style={{ color: "var(--ink3)" }}>{r.value}</p>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ color: "var(--brass)", background: "rgba(176,141,46,.12)" }}>
                      {r.enforcement_class}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : !user ? (
        <div className="mb-6 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
          <p className="text-xs" style={{ color: "var(--brass)" }}>
            Sign in to view estate rules. The /api/govern/estate_rules_record endpoint requires authentication.
          </p>
        </div>
      ) : null}

      {/* Trust Center / Refusals — auth-gated */}
      {refusals.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
            Refusals ({trustCenter?.refusals?.absolute + trustCenter?.refusals?.escalatable + trustCenter?.refusals?.held_for_check} total)
          </h3>
          <div className="space-y-2">
            {refusals.map((r, i) => (
              <div key={i} data-testid={`refusal-${i}`} className="rounded-lg border-l-4 p-3" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ color: "var(--oxblood)", background: "rgba(184,57,91,.12)" }}>
                    {r.class_hint}
                  </span>
                  <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{r.reason_code}</span>
                </div>
                <p className="text-sm" style={{ color: "var(--ink2)" }}>{r.criterion_verbatim}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ContractView() {
  const { user } = useAuth();
  const [register, setRegister] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }
    fetchTeamAccessRegister()
      .then(setRegister)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) return (
    <div data-testid="governance-contract">
      <div className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
        <p className="text-xs" style={{ color: "var(--brass)" }}>
          Sign in to view the access register. The /api/team/access_register endpoint requires authentication.
        </p>
      </div>
    </div>
  );

  if (loading) return <LoadingState message="Reading the access register\u2026" />;
  if (error) return <TransportError error={error} />;

  const rows = register?.rows || [];

  return (
    <div data-testid="governance-contract">
      {register?.canon_ref && (
        <p className="text-xs font-mono mb-4" style={{ color: "var(--ink3)" }}>{register.canon_ref}</p>
      )}
      {rows.length === 0 ? (
        <HonestEmpty message="No access grants on record. This list populates as grants are created and managed." />
      ) : (
        <div className="space-y-2">
          {rows.map((r, i) => (
            <div key={i} data-testid={`access-grant-${i}`} className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{r.grant_id}</span>
                <span
                  className="text-[10px] px-2 py-0.5 rounded-full font-medium"
                  style={{
                    color: r.state === "active" ? "var(--sage)" : "var(--ink3)",
                    background: r.state === "active" ? "rgba(29,122,110,.12)" : "rgba(27,31,39,.06)",
                  }}
                >
                  {r.state}
                </span>
              </div>
              <p className="text-sm" style={{ color: "var(--ink)" }}>{r.who_grantee_email}</p>
              <p className="text-xs mt-1" style={{ color: "var(--ink3)" }}>{r.what_scope}</p>
              <div className="flex gap-4 text-[10px] mt-2" style={{ color: "var(--ink3)" }}>
                <span>Created: {r.when_created_iso?.slice(0, 10)}</span>
                <span>By: {r.by_whom_grantor_email}</span>
                {r.propagation_state_plain && <span>{r.propagation_state_plain}</span>}
              </div>
              {r.is_sample && (
                <span className="text-[9px] mt-1 inline-block px-1.5 py-0.5 rounded bg-yellow-50" style={{ color: "var(--brass)" }}>sample data</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function CollectionView() {
  return (
    <div data-testid="governance-collection">
      <div className="rounded-lg border p-6" style={{ borderColor: "var(--line)", background: "white" }}>
        <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--ink)" }}>How data is collected</h3>
        <div className="space-y-3 text-sm" style={{ color: "var(--ink2)" }}>
          <p>
            All data in the estate is collected from Digicow&apos;s own systems — customer service lines,
            written complaints archive, core banking records, platform logs, and email archive.
          </p>
          <p>
            Data is read from source systems through governed connections. Each connection is receipted,
            and every record carries its provenance chain from source to the estate.
          </p>
          <p>
            Personal details are handled according to the rights Digicow holds over each data class.
            Some sets are cleared for outside use; others require per-request sign-off; some are
            internal-only and never available.
          </p>
        </div>
      </div>
    </div>
  );
}

const VIEW_MAP = {
  policies: { title: "Policies & Regulations", Component: PoliciesView },
  contract: { title: "Contract & Access Terms", Component: ContractView },
  collection: { title: "Data Collection", Component: CollectionView },
};

export default function DataGovernance() {
  const { tab } = useParams();
  const current = VIEW_MAP[tab] || VIEW_MAP["policies"];
  const Component = current.Component;

  return (
    <div data-testid="data-governance" className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="data-governance-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
      >
        Data Governance
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        {current.title}
      </p>
      <Component />
    </div>
  );
}
