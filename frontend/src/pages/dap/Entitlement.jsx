import React, { useState, useEffect } from "react";
import BackendPending from "@/components/shared/BackendPending";
import LoadingState from "@/components/shared/LoadingState";
import { useAuth } from "@/pages/dap/DAPLayout";
import { tryGet } from "@/lib/apiClient";
import {
  ENT_23_COST_NOT_MEASURED,
  ENT_26_FRONTIER_EXHAUSTION,
  ENT_34_FRONTIER_UNAVAILABLE,
  ENT_43_BADGE_INCLUDED_LOCAL,
  ENT_43_BADGE_CREDITS_FRONTIER,
  ENT_43_BADGE_YOUR_KEY,
  ENT_43_BADGE_AUTO,
} from "@/strings/entitlementStrings";
import { Award, CreditCard, Package, Tag, Shield, AlertCircle } from "lucide-react";

/**
 * Entitlement — DAP Portal entitlement surfaces.
 *
 * Wired to:
 *   GET /api/portal/entitlement/licence         — principal-scoped licence read
 *   GET /api/portal/entitlement/catalog/listed   — CatalogRow status=listed
 *   GET /api/portal/entitlement/allowance        — derived allowance (ENT-22)
 *   GET /api/portal/entitlement/badges           — picker badges filtered via dial-admit
 *
 * BINDING constraints:
 *   - Allowance figure displayed as-is (never compute/cache client-side) (ENT-22)
 *   - Badges show ONLY rows the licence's dials admit (ENT-3/ENT-43)
 *   - Excluded catalog rows ABSENT, not greyed/disabled
 *   - NO remaining-budget reason lines (DAP-35)
 *   - ENT-43 badge strings from entitlementStrings.js
 */

const BADGE_COLORS = {
  [ENT_43_BADGE_INCLUDED_LOCAL]: { bg: "rgba(29,122,110,.10)", color: "var(--sage)" },
  [ENT_43_BADGE_CREDITS_FRONTIER]: { bg: "rgba(22,39,74,.10)", color: "var(--blue)" },
  [ENT_43_BADGE_YOUR_KEY]: { bg: "rgba(176,141,46,.10)", color: "var(--brass)" },
  [ENT_43_BADGE_AUTO]: { bg: "rgba(27,31,39,.06)", color: "var(--ink2)" },
};

function BadgeChip({ badge }) {
  const colors = BADGE_COLORS[badge] || BADGE_COLORS[ENT_43_BADGE_AUTO];
  return (
    <span
      data-testid={`badge-${badge.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
      className="inline-flex items-center text-[11px] font-medium px-2 py-0.5 rounded-full"
      style={{ background: colors.bg, color: colors.color }}
    >
      <Tag size={10} className="mr-1" />
      {badge}
    </span>
  );
}

function BindingStringsReference() {
  return (
    <div data-testid="ent-binding-strings" className="rounded-lg border p-4 mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
      <h3 className="text-xs font-medium mb-3" style={{ color: "var(--ink)" }}>Binding copy (entitlement strings)</h3>
      <div className="space-y-2 text-xs" style={{ color: "var(--ink2)" }}>
        <div data-testid="ent-string-23">
          <span className="font-mono text-[10px]" style={{ color: "var(--ink3)" }}>ENT-23:</span>
          <span className="ml-2">{ENT_23_COST_NOT_MEASURED}</span>
        </div>
        <div data-testid="ent-string-26">
          <span className="font-mono text-[10px]" style={{ color: "var(--ink3)" }}>ENT-26:</span>
          <span className="ml-2">{ENT_26_FRONTIER_EXHAUSTION}</span>
        </div>
        <div data-testid="ent-string-34">
          <span className="font-mono text-[10px]" style={{ color: "var(--ink3)" }}>ENT-34:</span>
          <span className="ml-2">{ENT_34_FRONTIER_UNAVAILABLE}</span>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 mt-3">
        <BadgeChip badge={ENT_43_BADGE_AUTO} />
        <BadgeChip badge={ENT_43_BADGE_INCLUDED_LOCAL} />
        <BadgeChip badge={ENT_43_BADGE_CREDITS_FRONTIER} />
        <BadgeChip badge={ENT_43_BADGE_YOUR_KEY} />
      </div>
    </div>
  );
}

function LicenceCard({ data, loading, error }) {
  if (loading) return <LoadingState message="Reading licence\u2026" />;
  if (error === 404) return (
    <div data-testid="licence-pending" className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
      <p className="text-xs" style={{ color: "var(--brass)" }}>
        <AlertCircle size={12} className="inline mr-1" />
        Endpoint not yet mounted (GET /api/portal/entitlement/licence returns 404).
      </p>
    </div>
  );

  return (
    <div data-testid="licence-card" className="rounded-lg border p-5" style={{ borderColor: "var(--line)", background: "white" }}>
      <div className="flex items-center gap-2 mb-3">
        <Award size={16} style={{ color: "var(--sage)" }} />
        <h3 className="text-sm font-medium" style={{ color: "var(--ink)" }}>Licence</h3>
      </div>
      {data?.licence ? (
        <div className="space-y-2 text-sm" style={{ color: "var(--ink2)" }}>
          <p>Terms ID: <span className="font-mono text-xs">{data.licence.terms_id || data.licence.licence_terms_id || "N/A"}</span></p>
          {data.licence.compute_dial != null && <p>Compute dial: {JSON.stringify(data.licence.compute_dial)}</p>}
          {data.licence.frontier_dial != null && <p>Frontier dial: {JSON.stringify(data.licence.frontier_dial)}</p>}
        </div>
      ) : (
        <p className="text-sm" style={{ color: "var(--ink3)" }}>No licence on record for this principal.</p>
      )}
      {data?.authority && <p className="text-[10px] mt-3 font-mono" style={{ color: "var(--ink3)" }}>{data.authority}</p>}
    </div>
  );
}

function AllowanceCard({ data, loading, error }) {
  if (loading) return <LoadingState message="Deriving allowance\u2026" />;
  if (error === 404) return (
    <div data-testid="allowance-pending" className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
      <p className="text-xs" style={{ color: "var(--brass)" }}>
        <AlertCircle size={12} className="inline mr-1" />
        Endpoint not yet mounted (GET /api/portal/entitlement/allowance returns 404).
      </p>
    </div>
  );

  const state = data?.allowance_state;
  return (
    <div data-testid="allowance-card" className="rounded-lg border p-5" style={{ borderColor: "var(--line)", background: "white" }}>
      <div className="flex items-center gap-2 mb-3">
        <CreditCard size={16} style={{ color: "var(--blue)" }} />
        <h3 className="text-sm font-medium" style={{ color: "var(--ink)" }}>Allowance</h3>
      </div>
      {state ? (
        <div className="space-y-2 text-sm" style={{ color: "var(--ink2)" }}>
          <p>Period: <span className="font-medium">{state.period_iso}</span></p>
          <p>Credits allowance: <span className="font-semibold">{state.credits_allowance}</span></p>
          <p>Credits debited: <span className="font-semibold">{state.credits_debited}</span></p>
          {/* DAP-35: NEVER display "remaining budget" — allowance is a derived figure only */}
        </div>
      ) : (
        <p className="text-sm" style={{ color: "var(--ink3)" }}>No allowance state available.</p>
      )}
      {data?.authority && <p className="text-[10px] mt-3 font-mono" style={{ color: "var(--ink3)" }}>{data.authority}</p>}
    </div>
  );
}

function CatalogPicker({ catalogData, badgesData, loading, error }) {
  if (loading) return <LoadingState message="Reading catalog\u2026" />;
  if (error === 404) return (
    <div data-testid="catalog-pending" className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
      <p className="text-xs" style={{ color: "var(--brass)" }}>
        <AlertCircle size={12} className="inline mr-1" />
        Endpoint not yet mounted (GET /api/portal/entitlement/catalog/listed returns 404).
      </p>
    </div>
  );

  const rows = catalogData?.rows || [];
  const badges = badgesData?.badges || [];

  return (
    <div data-testid="catalog-picker" className="rounded-lg border p-5" style={{ borderColor: "var(--line)", background: "white" }}>
      <div className="flex items-center gap-2 mb-3">
        <Package size={16} style={{ color: "var(--brass)" }} />
        <h3 className="text-sm font-medium" style={{ color: "var(--ink)" }}>
          Catalog ({rows.length} listed)
        </h3>
      </div>

      {/* Badges — ONLY what the endpoint returns (ENT-3/ENT-43) */}
      {badges.length > 0 ? (
        <div data-testid="catalog-badges" className="mb-4">
          <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>Picker badges</p>
          <div className="flex flex-wrap gap-2">
            {badges.map((b, i) => (
              <BadgeChip key={i} badge={b.badge || b.name || b} />
            ))}
          </div>
        </div>
      ) : (
        <p className="text-xs mb-4" style={{ color: "var(--ink3)" }}>
          No badges returned. Excluded rows are absent from the response.
        </p>
      )}

      {/* Catalog rows — excluded rows are ABSENT, not greyed/disabled */}
      {rows.length > 0 ? (
        <div className="space-y-2">
          {rows.map((row, i) => (
            <div key={i} data-testid={`catalog-row-${i}`} className="flex items-center justify-between rounded border p-3" style={{ borderColor: "var(--line)" }}>
              <div>
                <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{row.name || row.row_id || `Row ${i + 1}`}</p>
                {row.description && <p className="text-xs" style={{ color: "var(--ink3)" }}>{row.description}</p>}
              </div>
              {row.badge && <BadgeChip badge={row.badge} />}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm" style={{ color: "var(--ink3)" }}>No catalog rows listed for this principal.</p>
      )}

      {catalogData?.authority && <p className="text-[10px] mt-3 font-mono" style={{ color: "var(--ink3)" }}>{catalogData.authority}</p>}
    </div>
  );
}

export default function Entitlement() {
  const { user } = useAuth();
  const [licence, setLicence] = useState({ data: null, loading: false, error: null });
  const [allowance, setAllowance] = useState({ data: null, loading: false, error: null });
  const [catalog, setCatalog] = useState({ data: null, loading: false, error: null });
  const [badges, setBadges] = useState({ data: null, loading: false, error: null });

  useEffect(() => {
    if (!user) return;

    // Licence
    setLicence((s) => ({ ...s, loading: true }));
    tryGet("/api/portal/entitlement/licence").then((res) => {
      setLicence({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
    });

    // Allowance
    setAllowance((s) => ({ ...s, loading: true }));
    tryGet("/api/portal/entitlement/allowance").then((res) => {
      setAllowance({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
    });

    // Catalog
    setCatalog((s) => ({ ...s, loading: true }));
    tryGet("/api/portal/entitlement/catalog/listed").then((res) => {
      setCatalog({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
    });

    // Badges
    setBadges((s) => ({ ...s, loading: true }));
    tryGet("/api/portal/entitlement/badges").then((res) => {
      setBadges({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
    });
  }, [user]);

  if (!user) {
    return (
      <div data-testid="entitlement-page" className="max-w-5xl mx-auto px-8 py-10">
        <h1 className="text-xl font-semibold mb-4" style={{ color: "var(--ink)", fontFamily: "var(--head)" }}>Entitlement</h1>
        <BindingStringsReference />
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
          <p className="text-xs" style={{ color: "var(--brass)" }}>Sign in to view entitlement surfaces. All endpoints require JWT authentication.</p>
        </div>
      </div>
    );
  }

  return (
    <div data-testid="entitlement-page" className="max-w-5xl mx-auto px-8 py-10">
      <h1 className="text-xl font-semibold mb-1" style={{ color: "var(--ink)", fontFamily: "var(--head)" }}>
        <Shield size={20} className="inline mr-2" />
        Entitlement
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        Licence terms, catalog access, and allowance for your principal.
      </p>

      <BindingStringsReference />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <LicenceCard {...licence} />
        <AllowanceCard {...allowance} />
      </div>

      <CatalogPicker catalogData={catalog.data} badgesData={badges.data} loading={catalog.loading} error={catalog.error} />
    </div>
  );
}
