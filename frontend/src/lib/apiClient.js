/**
 * Centralized API client for the Akki frontend.
 * All calls use REACT_APP_BACKEND_URL from environment.
 * All backend routes are prefixed with /api.
 */

const BASE = process.env.REACT_APP_BACKEND_URL;
if (!BASE) throw new Error("REACT_APP_BACKEND_URL is required.");

async function request(path, options = {}) {
  const url = `${BASE}${path}`;
  const headers = { ...options.headers };

  // Attach JWT if stored
  const token = sessionStorage.getItem("akki_access_token");
  if (token && !headers["Authorization"]) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  return res;
}

export async function get(path) {
  const res = await request(path);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`GET ${path} → ${res.status}: ${body}`);
  }
  return res.json();
}

export async function post(path, body) {
  const res = await request(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`POST ${path} → ${res.status}: ${text}`);
  }
  return res.json();
}

/** Login and store tokens.
 *  Backend uses `email` + `password` (NOT username). */
export async function login(email, password) {
  const res = await request("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Login failed");
  const data = await res.json();
  if (data.access_token) sessionStorage.setItem("akki_access_token", data.access_token);
  if (data.refresh_token) sessionStorage.setItem("akki_refresh_token", data.refresh_token);
  return data;
}

/** Refresh the access token.
 *  Backend reads the refresh token from Authorization header. */
export async function refreshToken() {
  const refresh = sessionStorage.getItem("akki_refresh_token");
  if (!refresh) throw new Error("No refresh token");
  const res = await request("/api/auth/refresh", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${refresh}`,
    },
  });
  if (!res.ok) throw new Error("Refresh failed");
  const data = await res.json();
  if (data.access_token) sessionStorage.setItem("akki_access_token", data.access_token);
  if (data.refresh_token) sessionStorage.setItem("akki_refresh_token", data.refresh_token);
  return data;
}

/** Get current identity */
export const fetchMe = () => get("/api/auth/me");

// Specific API calls matching the contract

export const fetchRegistryFacts = () => get("/api/registry/facts");
export const fetchComputeEstate = () => get("/api/compute/estate");
export const fetchModels = () => get("/api/model_registry/models");
export const fetchFullRecord = () => get("/api/model_registry/full_record");
export const fetchSkillFilesState = () => get("/api/skill-files/state");
export const fetchCensusLatest = () => get("/api/census/latest");
export const fetchGovernanceState = () => get("/api/governance/state");
export const fetchWatchState = () => get("/api/watch/state");
export const fetchGreyMirrorState = () => get("/api/grey_mirror/state");
export const fetchAuditTrailOverview = () => get("/api/audit_trail/overview");
export const fetchGovernEstateRulesRecord = () => get("/api/govern/estate_rules_record");
export const fetchTeamAccessRegister = () => get("/api/team/access_register");
export const fetchTeamConstitutionalSeats = () => get("/api/team/constitutional_seats");
export const fetchComplianceRefusals = () => get("/api/compliance/refusals");
export const fetchGovernTrustCenter = () => get("/api/govern/trust_center_record");
export const fetchShieldReceipts = () => get("/api/shield/receipts?limit=50");
export const fetchShieldAllowlists = () => get("/api/shield/allowlists");
export const fetchCostLedgerSummary = (kind = "") => get(`/api/cost_ledger/summary?kind=${kind}`);
export const fetchCostLedgerEntries = (kind = "", limit = 25) => get(`/api/cost_ledger/entries?kind=${kind}&limit=${limit}`);
export const fetchModelById = (id) => get(`/api/model_registry/${id}/journal`);

// ── Portal write-path (R-100 · JWT-gated) ────────────────────────────────
// tryGet / tryPost return {ok, status, data, error} — never throw on HTTP errors.
// This allows callers to handle 404 (endpoint not mounted) gracefully.

export async function tryGet(path) {
  try {
    const res = await request(path);
    const data = res.ok ? await res.json().catch(() => null) : await res.json().catch(() => null);
    return { ok: res.ok, status: res.status, data, error: res.ok ? null : `${res.status}` };
  } catch (e) {
    return { ok: false, status: 0, data: null, error: e.message };
  }
}

export async function tryPost(path, body) {
  try {
    const res = await request(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body != null ? JSON.stringify(body) : undefined,
    });
    const data = await res.json().catch(() => null);
    return { ok: res.ok, status: res.status, data, error: res.ok ? null : `${res.status}` };
  } catch (e) {
    return { ok: false, status: 0, data: null, error: e.message };
  }
}

// Portal requests
export const fetchPortalRequests = () => tryGet("/api/portal/requests");
export const fetchPortalRequestDetail = (id) => tryGet(`/api/portal/requests/${id}`);
export const submitPortalRequest = (body) => tryPost("/api/portal/requests", body);
export const stopPortalRequest = (id) => tryPost(`/api/portal/requests/${id}/stop`);
export const retryPortalRequest = (id) => tryPost(`/api/portal/requests/${id}/retry`);

// Portal entitlement
export const fetchPortalLicence = () => tryGet("/api/portal/entitlement/licence");
export const fetchPortalCatalog = () => tryGet("/api/portal/entitlement/catalog/listed");
export const fetchPortalAllowance = () => tryGet("/api/portal/entitlement/allowance");
export const fetchPortalBadges = () => tryGet("/api/portal/entitlement/badges");

// Canon rules (R-99 · public, no auth)
export const fetchCanonRulesDap = () => tryGet("/api/canon/rules/dap");
export const fetchCanonRulesRbm = () => tryGet("/api/canon/rules/rbm");
export const fetchCanonRulesRoc = () => tryGet("/api/canon/rules/roc");
export const fetchCanonRbm8Ceremony = () => tryGet("/api/canon/rules/rbm-8-ceremony-mechanic");
