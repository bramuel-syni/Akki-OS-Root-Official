// Akki V8 Shell — top bar + portal/app modes + NAV lattice.
//
// Sourced verbatim from the v8 file-of-record. See:
//   notes/prototype_inventory_v8.md §3 (top bar, portal/app modes)
//   notes/prototype_inventory_v8.md §4 (nav taxonomy)
//   notes/prototype_inventory_v8.md §18 (v8 → pod route mapping)
//
// v4 shell code at frontend/src/design/AkkiV4Shell* is invisible
// implementation only; v8 is the design authority. This file re-derives
// every visible element from the v8 spec + verbatim NAV/TABS/ROLES.

import React, { useMemo, useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { TOKENS, NAV, TABS, ROLES, V8_TO_POD_ROUTE, POD_ONLY_TILES } from './akkiv8_design_system';

// ------------------------------------------------------------------
// §3.1 top bar · v8-Docx §3.1 lines 83-86 · verbatim structure
//   Fixed 52px height · background var(--blue2) · shield SVG · RMS AI
//   wordmark in --head 16px, letterspacing .02em, color --paper.
//   Right: role/dept text (12px, #c9c2ae) + 27px circular avatar
//   (bg #28345c, 2-letter initials, 11px, #efe9da).
// ------------------------------------------------------------------
function TopBar({ role }) {
  return (
    <div
      data-testid="akki-v8-topbar"
      style={{
        height: 52, flexShrink: 0, background: TOKENS.blue2,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 22px',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 9 }}>
        <svg width="19" height="22" viewBox="0 0 24 28" fill="none" style={{ flexShrink: 0 }}>
          <path
            d="M12 1.5 22 5.2v8.1c0 6.2-4.2 10.9-10 13.2C6.2 24.2 2 19.5 2 13.3V5.2L12 1.5Z"
            fill="rgba(255,255,255,.10)" stroke={TOKENS.paper}
            strokeWidth="1.6" strokeLinejoin="round"
          />
          <path
            d="m7.7 13.6 3 3 5.6-6" stroke={TOKENS.paper}
            strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"
          />
        </svg>
        <div
          data-testid="akki-v8-wordmark"
          style={{
            fontFamily: TOKENS.head, fontSize: 16,
            color: TOKENS.paper, letterSpacing: '.02em',
          }}
        >RMS AI</div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ fontSize: 12, color: '#c9c2ae', whiteSpace: 'nowrap' }}>
          {role.person} · {role.dept}
        </div>
        <div style={{
          width: 27, height: 27, borderRadius: '50%', background: '#28345c',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 11, color: '#efe9da', flexShrink: 0,
        }}>{role.initials}</div>
      </div>
    </div>
  );
}

// ------------------------------------------------------------------
// §3.4 Tabs pill row · v8-Docx §3.4 line 97
//   Work / Build / 3rd Party Apps left-aligned, Admin right-aligned.
//   Pills in an rgba(22,39,74,.1) track; active tab gets solid/tinted fill.
// ------------------------------------------------------------------
function TabPills({ activeTab, onTab }) {
  const leftTabs = TABS.filter(t => !t.right);
  const rightTabs = TABS.filter(t => t.right);
  const render = (tabs) => (
    <div data-testid="akki-v8-tab-pills"
      style={{ display: 'flex', gap: 4, background: 'rgba(22,39,74,.1)', borderRadius: 8, padding: 3 }}>
      {tabs.map(tb => (
        <div key={tb.key}
          data-testid={`akki-v8-tab-${tb.key}`}
          onClick={() => onTab(tb.key)}
          style={{
            padding: '7px 13px', fontSize: 12.5, cursor: 'pointer',
            color: activeTab === tb.key ? '#fff' : TOKENS.ink2,
            fontWeight: activeTab === tb.key ? 700 : 600,
            borderRadius: 6,
            background: activeTab === tb.key ? TOKENS.blue : 'transparent',
            whiteSpace: 'nowrap',
          }}
        >{tb.label}</div>
      ))}
    </div>
  );
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      gap: 22, borderBottom: `1px solid ${TOKENS.line}`,
      marginBottom: 24, paddingBottom: 14,
    }}>
      {render(leftTabs)}
      {render(rightTabs)}
    </div>
  );
}

// ------------------------------------------------------------------
// §3.4 grouped NAV renderer · v8-Docx §3.4 lines 98-99
//   Each nav group renders as label + vertical item list, except a group
//   flagged tabs:true (buildlib), which renders items as an inline
//   horizontal tab row. A group flagged divider:true gets a hairline
//   rule above it.
// ------------------------------------------------------------------
function NavGroups({ tab, role }) {
  // Determine which groups render for the active tab + role.
  const tabDef = TABS.find(t => t.key === tab);
  const visibleGroupKeys = (tabDef ? tabDef.groups : []);
  const groupsToRender = NAV.filter(g => visibleGroupKeys.includes(g.key));

  return (
    <div data-testid="akki-v8-nav-groups">
      {groupsToRender.map((grp, gi) => (
        <React.Fragment key={grp.key}>
          {grp.divider && (
            <div style={{ borderTop: `1px solid ${TOKENS.line}`, margin: '4px 0 18px' }} />
          )}
          <div data-testid={`akki-v8-nav-group-${grp.key}`} style={{ marginBottom: 22 }}>
            <div style={{
              fontFamily: TOKENS.mono, fontSize: 10, letterSpacing: '.1em',
              textTransform: 'uppercase', color: '#8b8371', fontWeight: 700,
              marginBottom: 9,
            }}>{grp.label}</div>
            {grp.tabs ? (
              // inline horizontal tab row (buildlib · "Your Resources")
              <div style={{ display: 'flex', gap: 16 }}>
                {grp.items.map(it => <NavItem key={it.key} item={it} inline />)}
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 8 }}>
                {grp.items.map(it => <NavItem key={it.key} item={it} />)}
              </div>
            )}
          </div>
        </React.Fragment>
      ))}
    </div>
  );
}

function NavItem({ item, inline = false }) {
  const target = V8_TO_POD_ROUTE[item.key] || null;
  const testid = `akki-v8-nav-item-${item.key}`;
  const styleTile = {
    display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8,
    padding: '14px 4px 11px', borderRadius: 12, fontSize: 12, fontWeight: 600,
    cursor: target ? 'pointer' : 'default',
    textAlign: 'center', background: '#fff',
    color: target ? TOKENS.ink : TOKENS.ink3,
    border: `1px solid ${TOKENS.line}`,
    boxShadow: '0 1px 2px rgba(22,39,74,.05)',
    opacity: target ? 1 : 0.55,
    textDecoration: 'none',
  };
  const styleInline = {
    fontSize: 13, fontWeight: 600, cursor: target ? 'pointer' : 'default',
    padding: '1px 0', color: target ? TOKENS.ink2 : TOKENS.ink3,
    borderBottom: `2px solid ${TOKENS.line}`,
    textDecoration: 'none',
  };
  const style = inline ? styleInline : styleTile;
  const inner = inline ? (
    <span>{item.label}</span>
  ) : (
    <>
      <span style={{
        width: 34, height: 34, borderRadius: '50%',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: target ? TOKENS.blue : TOKENS.ink3,
        background: target ? TOKENS.accentSoft : TOKENS.surface2,
        flexShrink: 0, fontFamily: TOKENS.mono, fontSize: 12,
      }}>{item.key.slice(0, 2).toUpperCase()}</span>
      <span style={{ whiteSpace: 'pre-line' }}>{item.label}</span>
      {!target && (
        <span style={{
          fontSize: 9, color: TOKENS.ink3, fontFamily: TOKENS.mono,
          letterSpacing: '.06em', textTransform: 'uppercase',
        }}>not yet mounted</span>
      )}
    </>
  );
  if (target) {
    return (
      <Link to={target} data-testid={testid} style={style}>{inner}</Link>
    );
  }
  return <div data-testid={testid} style={style} title="Surface on v8 spec — pod mount pending">{inner}</div>;
}

// ------------------------------------------------------------------
// §18 pod-only extras tile row — every currently-declared pod route
// must be click-reachable from `/`.
// ------------------------------------------------------------------
function PodOnlyTiles() {
  return (
    <div data-testid="akki-v8-pod-only-tiles" style={{ marginTop: 8 }}>
      <div style={{ borderTop: `1px solid ${TOKENS.line}`, margin: '4px 0 18px' }} />
      <div style={{
        fontFamily: TOKENS.mono, fontSize: 10, letterSpacing: '.1em',
        textTransform: 'uppercase', color: '#8b8371', fontWeight: 700,
        marginBottom: 9,
      }}>Extras · pod-only surfaces (deep-linked from v8 spec)</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 8 }}>
        {POD_ONLY_TILES.map(t => (
          <Link key={t.key} to={t.route}
            data-testid={`akki-v8-pod-tile-${t.key}`}
            style={{
              display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8,
              padding: '14px 4px 11px', borderRadius: 12, fontSize: 12, fontWeight: 600,
              cursor: 'pointer', textAlign: 'center', background: '#fff',
              color: TOKENS.ink, border: `1px solid ${TOKENS.line}`,
              boxShadow: '0 1px 2px rgba(22,39,74,.05)',
              textDecoration: 'none',
            }}>
            <span style={{
              width: 34, height: 34, borderRadius: 10,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontFamily: TOKENS.mono, fontSize: 11.5, fontWeight: 700,
              letterSpacing: '.02em', color: TOKENS.blue,
              background: 'rgba(22,39,74,.08)', flexShrink: 0,
            }}>{t.label.split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase()}</span>
            <span style={{ whiteSpace: 'pre-line', lineHeight: 1.25 }}>{t.label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}

// ------------------------------------------------------------------
// §3.2 portal mode landing card · right pane, 55% width, max 600px
// ------------------------------------------------------------------
function PortalLanding({ role }) {
  return (
    <div style={{
      flex: '1 1 55%', padding: '32px 40px',
      background: TOKENS.paper, minHeight: 0, overflowY: 'auto',
    }}>
      <div
        data-testid="akki-v8-portal-landing"
        style={{
          background: '#fff', maxWidth: 600, borderRadius: 16,
          border: `1px solid ${TOKENS.line}`,
          padding: '32px 34px', boxShadow: '0 1px 2px rgba(22,39,74,.05)',
        }}
      >
        <div style={{
          fontFamily: TOKENS.mono, fontSize: 10, letterSpacing: '.12em',
          textTransform: 'uppercase', color: '#8b8371', fontWeight: 700,
          marginBottom: 10,
        }}>Akki OS · {role.label}</div>
        <div style={{
          fontFamily: TOKENS.head, fontSize: 28, lineHeight: 1.15,
          color: TOKENS.ink, marginBottom: 12,
        }}>{role.person}, everything you asked to be kept is kept.</div>
        <div style={{
          fontSize: 14, color: TOKENS.ink2, lineHeight: 1.55, marginBottom: 22,
        }}>
          Pick a surface on the left. The tab pills group by mode of work
          (Work · Build · 3rd Party Apps · Admin); each group opens the
          surfaces v8 names. Surfaces that aren't yet mounted in the pod
          are shown greyed and marked — no fabricated data.
        </div>
        <div style={{
          fontFamily: TOKENS.mono, fontSize: 10, letterSpacing: '.06em',
          color: TOKENS.ink3, borderTop: `1px solid ${TOKENS.line}`, paddingTop: 12,
        }}>
          Design source: v8 (Akki_Platform_v8_Design_Spec.docx · sha256 d7cfd3ae…) ·
          Prototype: RMS_AI_Akki_Prototype_v8_Standalone.html · sha256 e56871d0…
        </div>
      </div>
    </div>
  );
}

// ------------------------------------------------------------------
// §3.2 portal mode composition · left 45% · right 55%
// ------------------------------------------------------------------
function PortalMode({ role, activeTab, onTab }) {
  return (
    <div data-testid="akki-v8-portal-mode" style={{ flex: 1, display: 'flex', minHeight: 0 }}>
      <div style={{
        flex: '0 0 45%', minWidth: 0, background: TOKENS.surface,
        borderRight: `1px solid ${TOKENS.line}`,
        padding: '24px 34px 50px', overflowY: 'auto',
      }}>
        <TabPills activeTab={activeTab} onTab={onTab} />
        <NavGroups tab={activeTab} role={role} />
        <PodOnlyTiles />
      </div>
      <PortalLanding role={role} />
    </div>
  );
}

// ------------------------------------------------------------------
// §3.3 app mode · slim header + <Outlet/>
// ------------------------------------------------------------------
function AppMode({ location }) {
  // Trim leading slash + guess mono-breadcrumb from path
  const path = location.pathname;
  const crumb = path === '/' ? 'AKKI' : path.replace(/^\/+/, '').replace(/\//g, ' · ');
  return (
    <div data-testid="akki-v8-app-mode" style={{
      flex: 1, display: 'flex', flexDirection: 'column',
      background: TOKENS.paper, minHeight: 0,
    }}>
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '10px 28px', borderBottom: `1px solid ${TOKENS.line}`,
        background: '#fff',
      }}>
        <div style={{
          fontFamily: TOKENS.mono, fontSize: 10.5, letterSpacing: '.14em',
          textTransform: 'uppercase', color: TOKENS.ink3, fontWeight: 700,
        }} data-testid="akki-v8-app-breadcrumb">{crumb}</div>
        <Link to="/" data-testid="akki-v8-exit-to-portal" style={{
          fontFamily: TOKENS.mono, fontSize: 11, letterSpacing: '.08em',
          textTransform: 'uppercase', color: TOKENS.blue, fontWeight: 700,
          textDecoration: 'none',
        }}>← Exit to portal</Link>
      </div>
      <div style={{ flex: 1, overflow: 'auto' }}>
        <Outlet />
      </div>
    </div>
  );
}

// ------------------------------------------------------------------
// Layout root · used as element on the parent Route in App.js
// ------------------------------------------------------------------
export function AkkiV8ShellLayout() {
  const location = useLocation();
  const isPortal = location.pathname === '/';
  const [activeTab, setActiveTab] = useState('work');
  // Default role — v8-HTML seeds Compliance Owner (M. Chen · MC) as the
  // starting role; keep that here.
  const role = useMemo(() => ROLES[0], []);
  return (
    <div data-testid="akki-v8-shell" style={{
      minHeight: '100vh', background: TOKENS.paper,
      display: 'flex', flexDirection: 'column',
      fontFamily: TOKENS.body, color: TOKENS.ink,
    }}>
      <TopBar role={role} />
      {isPortal
        ? <PortalMode role={role} activeTab={activeTab} onTab={setActiveTab} />
        : <AppMode location={location} />}
    </div>
  );
}

export default AkkiV8ShellLayout;
