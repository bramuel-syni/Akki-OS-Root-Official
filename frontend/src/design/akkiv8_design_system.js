// Akki V8 design system — tokens, NAV, TABS, ROLES.
//
// Sourced verbatim from the v8 file-of-record:
//   fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html
//     sha256 e56871d01a99c2f3aa173c9b0a0f09e983c9f0e54ba3e61795ac8cb8575f98f2
//   fixtures/Akki_Platform_v8_Design_Spec.docx
//     sha256 d7cfd3aed244da1b53b7b86ed9572852b8e6e928f2294d6f94083ff775491304
// See notes/prototype_inventory_v8.md §2 (tokens), §4 (nav taxonomy),
// §18 (v8 NAV → pod route mapping).
//
// v4 shell code retained at `frontend/src/design/AkkiV4Shell*` is invisible
// implementation only; v8 is the design authority. Every value in this file
// traces to a byte-range in the v8 artifacts.

// ------------------------------------------------------------------
// §2.1 color tokens · v8-Docx §2.1 lines 23-43 · verbatim
// ------------------------------------------------------------------
export const TOKENS = {
  paper:      '#f5f2ea',
  surface:    '#f0ece1',
  surface2:   '#ede8da',
  line:       '#e4dfd3',
  ink:        '#1b1f27',
  ink2:       '#3d4350',
  ink3:       '#5b6270',
  blue:       '#16274a',
  blue2:      '#0f1b33',
  oxblood:    '#b8395b',
  oxblood2:   '#c64e6e',
  brass:      '#b08d2e',
  sage:       '#1d7a6e',
  accent:     '#4c5fd5',
  accentSoft: 'rgba(76,95,213,.10)',
  accentMid:  'rgba(76,95,213,.22)',
  scrim:      'rgba(15,27,51,.42)',
  shadowPop:    '0 22px 64px rgba(15,27,51,.26)',
  shadowDrawer: '-14px 0 48px rgba(15,27,51,.18)',
  drawerW:      'min(460px,94vw)',
  drawerWide:   'max(480px,50vw)',
  // §2.2 typography — v8-Docx §2.2 lines 57-62 · verbatim
  head: 'Iowan Old Style,Georgia,serif',
  body: 'Söhne,Helvetica Neue,Arial,sans-serif',
  mono: 'ui-monospace,Menlo,Consolas,monospace',
};

// ------------------------------------------------------------------
// §4 navigation taxonomy · verbatim from v8-HTML const NAV literal
// ------------------------------------------------------------------
export const NAV = [
  { key: 'workstudio', label: 'WorkStudio', items: [
      { key: 'chat',       label: 'Chat' },
      { key: 'analyze',    label: 'Data Suite' },
      { key: 'documents',  label: 'Documents' },
      { key: 'tasks',      label: 'Task Manager' },
  ]},
  { key: 'thinklab', label: 'ThinkLab', items: [
      { key: 'clarity',     label: 'Seek Clarity' },
      { key: 'strategy',    label: 'Develop Strategy' },
      { key: 'hypothesis',  label: 'Test Hypothesis' },
      { key: 'perspective', label: 'Get Perspective' },
  ]},
  { key: 'collab', label: 'Collab', items: [
      { key: 'mentions', label: 'Mentions' },
      { key: 'emails',   label: 'Emails' },
      { key: 'projects', label: 'Projects/Tasks' },
      { key: 'hrstuff',  label: 'HR Stuff' },
  ]},
  { key: 'monitor', label: 'Performance Management', items: [
      { key: 'performance', label: 'Exco 360' },
      { key: 'board',       label: 'Board 360' },
  ]},
  { key: 'estate', label: 'Manage Estate', items: [
      { key: 'estate',     label: 'Registry' },
      { key: 'govern',     label: 'Shield' },
      { key: 'greymirror', label: 'Grey Mirror' },
  ]},
  { key: 'approvals', label: 'Approvals', items: [
      { key: 'spendreq',       label: 'Spend Requests' },
      { key: 'rulesupd',       label: 'Rules Updates' },
      { key: 'modeladmission', label: 'Model Admission' },
  ]},
  { key: 'build', label: 'Build Your Resources', items: [
      { key: 'train',      label: 'Train Models' },
      { key: 'agentbuild', label: 'Build Agents' },
      { key: 'extract',    label: 'Extract Data' },
  ]},
  { key: 'buildlib', label: 'Your Resources', divider: true, tabs: true, items: [
      { key: 'youragents', label: 'Agents' },
      { key: 'yourmodels', label: 'Models' },
  ]},
  { key: 'thirdparty', label: '3rd Party Apps', items: [
      { key: 'appsnew',        label: 'New' },
      { key: 'appsfrequent',   label: 'Frequent' },
      { key: 'appsconnected',  label: 'Connected' },
      { key: 'appsrequests',   label: 'Requests' },
  ]},
  // watch group is appended in v8 via NAV.push(...) after the canon-mapping
  // comment · Watch Officer role only. Kept in the same array here; role
  // gating done at render time via ROLES.groups.
  { key: 'watch', label: 'The Watch', items: [
      { key: 'wstate',      label: 'State' },
      { key: 'wrecord',     label: 'Record' },
      { key: 'wunder',      label: 'Under Watch' },
      { key: 'wdecisions',  label: 'Decisions' },
  ]},
];

// ------------------------------------------------------------------
// §4 TABS · verbatim from v8-HTML const TABS literal at pos≈514470
// ------------------------------------------------------------------
export const TABS = [
  { key: 'work',  label: 'Work',           groups: ['workstudio','thinklab','collab','monitor'] },
  { key: 'build', label: 'Build',          groups: ['build','buildlib'] },
  { key: 'apps',  label: '3rd Party Apps', groups: ['thirdparty'] },
  { key: 'admin', label: 'Admin',          groups: ['estate','approvals','watch'], right: true },
];

// ------------------------------------------------------------------
// §4 ROLES · verbatim from v8-HTML const ROLES literal at pos≈514800
// ------------------------------------------------------------------
export const ROLES = [
  { key: 'compliance', label: 'Compliance Owner', person: 'M. Chen',   dept: 'Compliance', initials: 'MC', groups: ['estate','approvals'] },
  { key: 'watch',      label: 'Watch Officer',    person: 'A. Njeri',  dept: 'The Watch',  initials: 'AN', groups: ['watch'] },
  { key: 'operator',   label: 'Operator',         person: 'J. Otieno', dept: 'Operations', initials: 'JO', groups: ['estate'] },
];

// ------------------------------------------------------------------
// V8 NAV item → pod route mapping · notes/prototype_inventory_v8.md §18
// Keys that don't yet have a pod destination map to null and render an
// honest-empty landing card ("this surface is on the v8 spec but not yet
// mounted in the pod").
// ------------------------------------------------------------------
export const V8_TO_POD_ROUTE = {
  // WorkStudio (§6)
  chat:            '/chat',
  analyze:         null,
  documents:       null,
  tasks:           null,
  // ThinkLab (§7)
  clarity:         '/thinklab/clarity',
  strategy:        '/thinklab/strategy',
  hypothesis:      '/thinklab/hypothesis',
  perspective:     '/thinklab/perspective',
  // Collab (§8)
  mentions:        null,
  emails:          null,
  projects:        null,
  hrstuff:         null,
  // Performance Management (§9)
  performance:     null,
  board:           null,
  // Manage Estate (§12)
  estate:          '/registry',
  govern:          '/shield',
  greymirror:      '/grey-mirror',
  // Approvals (§13)
  spendreq:        '/governance',
  rulesupd:        '/governance',
  modeladmission:  '/governance',
  // Build Your Resources (§10)
  train:           '/training',
  agentbuild:      null,
  extract:         null,
  // Your Resources (§10)
  youragents:      null,
  yourmodels:      '/models',
  // 3rd Party Apps (§11)
  appsnew:         null,
  appsfrequent:    null,
  appsconnected:   null,
  appsrequests:    null,
  // The Watch (§14)
  wstate:          '/watch',
  wrecord:         '/watch',
  wunder:          '/watch',
  wdecisions:      '/watch',
};

// ------------------------------------------------------------------
// Pod surfaces NOT in v8 NAV — rendered inside the portal as an
// additional "Extras (pod-only)" tile row so every existing pod route
// is click-reachable from `/`. See notes/prototype_inventory_v8.md §18.
// ------------------------------------------------------------------
export const POD_ONLY_TILES = [
  { key: 'audit-trail',       label: 'Audit Trail',        route: '/audit-trail',        note: 'Wave F Cleanup CP · CA1-001/002/003 · Governance Surface overview lens' },
  { key: 'skill-files',       label: 'Skill Files',        route: '/skill-files',        note: 'Doc 18 A18.7 · callable-file mount seam' },
  { key: 'evidence-register', label: 'Evidence Register',  route: '/evidence-register',  note: 'Doc 19B §19B.4-6 · Walk-this deep-linked' },
  { key: 'commission',        label: 'Commission',         route: '/commission',         note: 'Canon 5 §14 · Instance › Ceremonies mount' },
  { key: 'cost-ledger',       label: 'Cost Ledger',        route: '/cost-ledger',        note: 'Registry › LLM · spend cadence view' },
];
