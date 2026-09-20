import React, { useState, useEffect, useCallback, createContext, useContext } from "react";
import { NavLink, Outlet } from "react-router-dom";
import {
  Database, Shield, FileText, LayoutDashboard, Link2,
  ArrowDownToLine, ChevronRight, LogIn, LogOut, User
} from "lucide-react";
import { login as apiLogin, refreshToken, fetchMe } from "@/lib/apiClient";

/* ── Auth context (shared across all DAP pages) ─────── */
const AuthCtx = createContext({ user: null, loading: false, doLogin: async () => {}, doLogout: () => {} });
export function useAuth() { return useContext(AuthCtx); }

const NAV_GROUPS = [
  {
    label: "Overview",
    items: [
      { to: "/dap", icon: LayoutDashboard, label: "Landing", end: true },
    ],
  },
  {
    label: "Extract",
    items: [
      { to: "/dap/extract/processed", icon: FileText, label: "Get Intelligence" },
      { to: "/dap/extract/finetune", icon: Database, label: "Train a Model" },
      { to: "/dap/extract/skills", icon: FileText, label: "Build a Skill" },
      { to: "/dap/extract/raw", icon: ArrowDownToLine, label: "Download Raw Data" },
    ],
  },
  {
    label: "Available Resources",
    items: [
      { to: "/dap/resources/compute", icon: Database, label: "Compute" },
      { to: "/dap/resources/base-models", icon: Database, label: "Base Models" },
      { to: "/dap/resources/trained-models", icon: Database, label: "Trained Models" },
      { to: "/dap/resources/skills", icon: FileText, label: "Skills" },
    ],
  },
  {
    label: "Data Governance",
    items: [
      { to: "/dap/governance/policies", icon: Shield, label: "Policies & Regulations" },
      { to: "/dap/governance/contract", icon: FileText, label: "Contract & Access Terms" },
      { to: "/dap/governance/collection", icon: Database, label: "Data Collection" },
    ],
  },
  {
    label: "Connect Resources",
    items: [
      { to: "/dap/connect/key", icon: Link2, label: "Workspace API Key" },
      { to: "/dap/connect/agents", icon: Database, label: "Your AI Agent" },
      { to: "/dap/connect/compute", icon: Database, label: "Your Compute" },
      { to: "/dap/connect/models", icon: Database, label: "Your Models & Recipes" },
    ],
  },
  {
    label: "Requests",
    items: [
      { to: "/dap/requests", icon: FileText, label: "Request Lifecycle" },
    ],
  },
];

export default function DAPLayout() {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(false);
  const [loginOpen, setLoginOpen] = useState(false);
  const [loginError, setLoginError] = useState(null);

  // Try refreshing on mount (if a token is in storage)
  useEffect(() => {
    const token = sessionStorage.getItem("akki_access_token");
    if (token) {
      setAuthLoading(true);
      fetchMe()
        .then(setUser)
        .catch(() => {
          sessionStorage.removeItem("akki_access_token");
          sessionStorage.removeItem("akki_refresh_token");
        })
        .finally(() => setAuthLoading(false));
    }
  }, []);

  const doLogin = useCallback(async (email, password) => {
    setAuthLoading(true);
    setLoginError(null);
    try {
      await apiLogin(email, password);
      const me = await fetchMe();
      setUser(me);
      setLoginOpen(false);
    } catch (e) {
      setLoginError(e.message);
    } finally {
      setAuthLoading(false);
    }
  }, []);

  const doLogout = useCallback(() => {
    sessionStorage.removeItem("akki_access_token");
    sessionStorage.removeItem("akki_refresh_token");
    setUser(null);
  }, []);

  return (
    <AuthCtx.Provider value={{ user, loading: authLoading, doLogin, doLogout }}>
    <div
      data-testid="dap-layout"
      className="min-h-screen flex"
      style={{ background: "var(--paper, #f5f2ea)", fontFamily: "var(--body, Söhne, Helvetica Neue, Arial, sans-serif)" }}
    >
      {/* Sidebar */}
      <aside
        data-testid="dap-sidebar"
        className="w-64 flex-shrink-0 border-r overflow-y-auto"
        style={{ borderColor: "var(--line, #e4dfd3)", background: "var(--surface, #f0ece1)" }}
      >
        <div className="px-5 py-6">
          <h1
            data-testid="dap-logo"
            className="text-sm font-semibold tracking-wide uppercase mb-6"
            style={{ color: "var(--blue, #16274a)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
          >
            RMS · Data Access Portal
          </h1>

          <nav>
            {NAV_GROUPS.map((group) => (
              <div key={group.label} className="mb-5">
                <p
                  className="text-[10px] uppercase tracking-widest font-medium mb-2 px-2"
                  style={{ color: "var(--ink3, #5b6270)" }}
                >
                  {group.label}
                </p>
                <ul className="space-y-0.5">
                  {group.items.map((item) => (
                    <li key={item.to}>
                      <NavLink
                        to={item.to}
                        end={item.end}
                        data-testid={`dap-nav-${item.label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
                        className={({ isActive }) =>
                          `flex items-center gap-2 px-2 py-1.5 rounded text-sm transition-colors ${
                            isActive
                              ? "font-medium"
                              : "hover:bg-black/[.04]"
                          }`
                        }
                        style={({ isActive }) => ({
                          color: isActive ? "var(--blue, #16274a)" : "var(--ink2, #3d4350)",
                          background: isActive ? "rgba(22,39,74,.08)" : undefined,
                        })}
                      >
                        <item.icon size={14} />
                        <span>{item.label}</span>
                        {item.end ? null : <ChevronRight size={12} className="ml-auto opacity-30" />}
                      </NavLink>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </nav>
        </div>

        {/* Auth controls */}
        <div className="px-5 py-3 border-t" style={{ borderColor: "var(--line, #e4dfd3)" }}>
          {user ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <User size={12} style={{ color: "var(--sage)" }} />
                <span data-testid="dap-user-email" className="text-[10px] truncate max-w-[140px]" style={{ color: "var(--ink2)" }}>
                  {user.email || user.identity || "Logged in"}
                </span>
              </div>
              <button
                data-testid="dap-logout-btn"
                onClick={doLogout}
                className="p-1 rounded hover:bg-black/5 transition-colors"
                title="Logout"
              >
                <LogOut size={12} style={{ color: "var(--ink3)" }} />
              </button>
            </div>
          ) : (
            <>
              <button
                data-testid="dap-login-toggle"
                onClick={() => setLoginOpen(!loginOpen)}
                className="flex items-center gap-2 text-xs hover:underline"
                style={{ color: "var(--ink3)" }}
              >
                <LogIn size={12} /> Sign in for full access
              </button>
              {loginOpen && (
                <form
                  data-testid="dap-login-form"
                  className="mt-2 space-y-2"
                  onSubmit={(e) => {
                    e.preventDefault();
                    const fd = new FormData(e.target);
                    doLogin(fd.get("email"), fd.get("password"));
                  }}
                >
                  <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    data-testid="dap-login-email"
                    className="w-full text-xs px-2 py-1.5 rounded border"
                    style={{ borderColor: "var(--hair)", background: "white" }}
                    defaultValue="demo.master_admin@demo.rms.example.com"
                    required
                  />
                  <input
                    name="password"
                    type="password"
                    placeholder="Password"
                    data-testid="dap-login-password"
                    className="w-full text-xs px-2 py-1.5 rounded border"
                    style={{ borderColor: "var(--hair)", background: "white" }}
                    defaultValue="demo-master-admin-pw"
                    required
                  />
                  <button
                    type="submit"
                    data-testid="dap-login-submit"
                    disabled={authLoading}
                    className="w-full text-xs px-2 py-1.5 rounded font-medium transition-colors"
                    style={{ background: "var(--blue)", color: "white" }}
                  >
                    {authLoading ? "Signing in\u2026" : "Sign in"}
                  </button>
                  {loginError && (
                    <p data-testid="dap-login-error" className="text-[10px]" style={{ color: "var(--oxblood)" }}>
                      {loginError}
                    </p>
                  )}
                </form>
              )}
            </>
          )}
        </div>

        {/* Switch to OS link */}
        <div className="px-5 py-4 border-t mt-auto" style={{ borderColor: "var(--line, #e4dfd3)" }}>
          <NavLink
            to="/"
            data-testid="dap-nav-os-prototype"
            className="text-xs hover:underline"
            style={{ color: "var(--ink3, #5b6270)" }}
          >
            ← Akki OS Prototype
          </NavLink>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto min-h-screen">
        <Outlet />
      </main>
    </div>
    </AuthCtx.Provider>
  );
}
