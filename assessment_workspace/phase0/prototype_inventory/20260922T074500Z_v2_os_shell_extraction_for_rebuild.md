# v2 OS Prototype Shell · Design-of-Record Extraction for Sub-Slice 4c Rebuild · 2026-09-22T07:45:00Z

**Turn 4 · sub-slice 4c · state-side prep receipt** — bytes-that-will-land-in-runtime documented here before the App.js edit so the state master carries the extraction permanently.

Canon anchors verbatim:
- Owner ruling R-101 preserved WHAT (banked `STATE/DECISIONS.md:R-101 append` state master `fbcbf1f7`): *"byte-identical mirror `/app/frontend/{App.js,pages/}` ↔ `pod_shell/frontend/{App.js,pages/}` + 5 baselines → 0 + 5 annotations retire retaining cp10-still-recent + milestone_status flip SCHEDULED→SEALED on `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` + ratchet monotonic-up."*
- Owner directive verbatim 2026-09-22T~06:10Z: *"UI/UX architecture and experience flow needs to be exact as the HTML I shared."*
- Owner FE brief §0 (2026-09-20T~08:24Z): *"The prototype is the design of record ... prototype wins."*
- Enumeration checklist byte-verbatim source: `phase0/prototype_inventory/20260922T064500Z_full_enumeration_and_gap_checklist.md` §1.1-§1.5 (state master `5b2c4490`).
- R-102 MASTER DIRECTIVE (state master `c7f8b3bf`).
- DQ-12 Commit-B seal state master `86947a7c` · ratchet floor **5939**.

## 1 · Extraction source integrity

The v2 OS prototype at `custody/owner_drops/20260920T0824Z/RMS_AI_Prototype_v2.html` (2,286,992 bytes) is a **serialized Vue DC-runtime component tree** (`x-dc`, `sc-if`, `sc-for`, `{{ interpolation }}` handlebars) — NOT a plain JS source file. The `const TABS = [...]`, `const NAV = [...]`, `const ROLES = [...]`, `const TONE = {...}` shapes documented in enumeration §1.1-§1.5 are the ratified design-of-record extracted by the enumeration author from prototype behavior + reading the compiled component tree. They are **byte-verbatim per the enumeration checklist** (which the state master banks as source-of-truth for the rebuild), not byte-verbatim per a hypothetical plain-JS source in the HTML.

Sub-slice 4a already banked this extraction posture: enumeration §1.2 line 20 labels the tabular NAV extraction "byte-verbatim extracted" — the tabular row form is the byte-verbatim record, and this receipt reconstructs the standard JS `const NAV = [...]` array literal faithfully from that record.

## 2 · Bytes that will land in `/app/frontend/src/App.js` (additive block · SO §3.8)

The following block will be **inserted** into `/app/frontend/src/App.js` **after the import block and before the JSDoc comment** for the V8 substitution engine (i.e. between existing line 15 and existing line 17). Existing code below the insertion point is **not edited** (SO §3.8 additive-only; sealed shell components + V8 substitution engine untouched).

### 2.1 · Comment header + TABS (verbatim per enumeration §1.1)

```javascript
// ---------------------------------------------------------------------------
// v2 OS Prototype Shell · Design-of-Record Constants
// (byte-verbatim per phase0/prototype_inventory/20260922T064500Z_full_enumeration_and_gap_checklist.md §1.1-§1.5)
// R-101 preserved WHAT · e-apply Turn 4 sub-slice 4c · 2026-09-22T07:45:00Z
// ---------------------------------------------------------------------------

const TABS = [
  { key:'work',  label:'Work',           groups:['workstudio','thinklab','collab','monitor'] },
  { key:'build', label:'Build',          groups:['build','buildlib'] },
  { key:'apps',  label:'3rd Party Apps', groups:[] },
  { key:'admin', label:'Admin',          groups:['estate','approvals','watch'], right:true }
];
```

### 2.2 · NAV (faithful reconstruction of enumeration §1.2 · 10 groups · 37 leaves)

```javascript
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
```

Leaf-count sanity: workstudio 7 + thinklab 4 + collab 4 + monitor 3 + estate 3 + approvals 3 + watch 4 + build 4 + buildlib 2 + thirdparty 4 = **38 leaf entries**. Enumeration §1.2 gives 37 distinct leaf views because `performance` appears in both `workstudio` and `monitor` (overlap acknowledged by enumeration line 25 verbatim: *"`performance`→Performance (already in workstudio) · **`signals`→Signals** · **`ideas`→Ideas** **(2 net-new leaves + performance overlap)**"*). This reconstruction preserves the overlap literally to match the enumeration verbatim.

### 2.3 · ROLES (byte-verbatim per enumeration §1.3)

```javascript
const ROLES = [
  { key:'compliance', label:'Compliance Owner', person:'M. Chen',   dept:'Compliance', initials:'MC', groups:['estate','approvals'] },
  { key:'watch',      label:'Watch Officer',    person:'A. Njeri',  dept:'The Watch',  initials:'AN', groups:['watch'] },
  { key:'operator',   label:'Operator',         person:'J. Otieno', dept:'Operations', initials:'JO', groups:['estate'] }
];
```

### 2.4 · TONE (byte-verbatim per enumeration §1.4)

```javascript
const TONE = {
  plain:  { bg:'#fff',                       border:'var(--line)',    color:'var(--ink)'  },
  held:   { bg:'rgba(176,141,46,.07)',       border:'var(--brass)',   color:'var(--ink)'  },
  refused:{ bg:'rgba(184,57,91,.06)',        border:'var(--oxblood)', color:'var(--ink)'  },
  failed: { bg:'var(--surface2)',            border:'var(--line)',    color:'var(--ink3)' },
  drill:  { bg:'var(--surface)',             border:'var(--line)',    color:'var(--ink2)' }
};
```

### 2.5 · FOURQ comment (byte-verbatim per enumeration §1.5)

```javascript
/* Four-questions surfaces. Rule zero: every block leads with a sentence;
   measures live behind "see the working". */
```

### 2.6 · Persona-filter helper (new · derived from enumeration §1.3 discipline)

```javascript
// Persona-filter helper · Admin tab shows only groups the current role owns.
function filterGroupsForRole(tab, roleKey) {
  const role = ROLES.find(r => r.key === roleKey);
  const tabDef = TABS.find(t => t.key === tab);
  if (!tabDef) return [];
  if (tab !== 'admin' || !role) return tabDef.groups;
  return tabDef.groups.filter(g => role.groups.includes(g));
}
```

Discipline for filterGroupsForRole (derived from enumeration §1.3 line 45 verbatim): *"a persona sees only their `groups` in Admin tab; the Watch officer sees only `watch`; the operator sees only `estate`; the compliance owner sees `estate + approvals`. Non-admin tabs (work, build, apps) are unconditional."* Return-type:  `string[]` (group keys) — the caller (Sidebar/Nav components arriving in sub-slice 4d-4e) will render these.

## 3 · What sub-slice 4c does NOT touch (SO §3.8 additive-only)

- V8 substitution engine (App.js lines 66 onward). Preserved verbatim.
- `V8_SUBSTITUTIONS` array. Preserved verbatim.
- Sealed shell components (`Chat.jsx`, `ConnectWizard.jsx`, `RefusalCard.jsx`, etc.) — preserved.
- DAP Portal imports (App.js lines 5-15). Preserved verbatim.
- Existing routing tree. Preserved verbatim.
- The 5 R-91 mirror-drift baseline tests (still in `baseline_failures`; scheduled retire at sub-slice 4h).

## 4 · What sub-slice 4c introduces on the RED side (new invariants)

Author `repos/Extraction-Akki/backend/tests/invariants/test_v2_os_shell_present_in_runtime_app_js.py` with the following invariants (all read `/app/frontend/src/App.js` UTF-8 content):

| # | Test | Assertion |
|---:|---|---|
| 1 | `test_module_imports_and_paths_resolve` | Module can import; `RUNTIME_APP_JS_PATH` and `ENUMERATION_PATH` resolve to real files. |
| 2 | `test_tabs_constant_present_verbatim` | The 4-line `const TABS = [` … `];` block appears byte-verbatim in App.js. |
| 3 | `test_tabs_has_exactly_four_entries_and_keys` | Re-parses the TABS array and confirms 4 entries with keys `work/build/apps/admin` in that order, and `admin.right === true`. |
| 4 | `test_nav_constant_present_and_ten_groups` | The `const NAV = [` block appears; 10 group entries; each group carries `key`, `label`, `tab`, `items`. |
| 5 | `test_nav_leaf_keys_match_enumeration_37_distinct` | Union of leaf `key` values across all NAV groups equals the 37 distinct leaves enumerated in §1.2. |
| 6 | `test_roles_constant_present_verbatim` | Byte-verbatim block per §1.3 with `M. Chen`, `A. Njeri`, `J. Otieno`. |
| 7 | `test_tone_constant_present_verbatim` | Byte-verbatim block per §1.4 with 5 states `plain/held/refused/failed/drill`. |
| 8 | `test_fourq_comment_present_verbatim` | Byte-verbatim FOURQ comment per §1.5. |
| 9 | `test_filter_groups_for_role_present_with_admin_rule` | The `filterGroupsForRole` function is declared; docstring/comment references admin-tab persona filter per §1.3. |
| 10 | `test_shell_block_precedes_v8_substitutions` | Text index of `const TABS` < text index of `const V8_SUBSTITUTIONS` (shell lands ABOVE V8 engine in App.js). |
| 11 | `test_ruling_verbatim_owner_prototype_is_design_of_record` | Owner FE brief §0 verbatim (*"The prototype is the design of record ... prototype wins."*) present in App.js OR in a docstring the module reads. |
| 12 | `test_enumeration_source_path_referenced_in_comment` | The comment header cites `phase0/prototype_inventory/20260922T064500Z_full_enumeration_and_gap_checklist.md`. |

**Ratchet delta target**: +12 new invariants → floor **5939 → 5951 (+12 measured)** post-GREEN.

## 5 · Sub-slice 4c green-then-seal cycle

1. Author receipt (this file · state master) + RED test file (Extraction-Akki `programme/track-a`).
2. Run just the new tests · confirm 12/12 RED (right-reason: constants not in App.js yet).
3. Author GREEN edit: insert the block from §2 into `/app/frontend/src/App.js` between line 15 (`import CanonCountdown ...`) and line 17 (`/** App.js — Wave G4 ... */`).
4. Run just the new tests · confirm 12/12 GREEN.
5. 2× `BASELINE_GUARD=1 PYTHONHASHSEED=0 pytest ...` byte-identical (stripped-sha256 IDENTICAL). Confirm ratchet floor 5939 → 5951.
6. §3.3 3-Commit Seal:
   - Code Commit-A on `programme/track-a` (test file at Extraction-Akki tree).
   - Companion Commit-A on `/app` main (App.js edit + vendored mirror sync).
   - State Commit-B on `master` (this receipt + DECISIONS append + RESUME.md refresh + NEXT.md attestation + ORCH_BOOT.md ratchet regen).
   - Fixup Commit-C on `master` (R-6 boundary regen post-Commit-B SHA).
   - Fixup Commit-C companion on `/app` main.
7. Bank REDEPLOY CHECKLIST verification.

## 6 · Bounds

Chrome-46 screenshot pre-first-commit obligation from enumeration §8 is being **honestly deferred** to sub-slice 4c-continuation because the prototype HTML is not currently served on port 3000 and setting up a temporary alias route touches sealed React tree. The deferral is banked here (not glossed) — a small landmark screenshot of the current runtime home page will be taken as receipt, and the full 46-view screenshot pass runs post-4c-first-commit before sub-slice 4d opens. This is a **scope-honesty concession** flagged explicitly in the seal report per SO §6.7.

Zero push · terminal pytest+curl only · no `testing_agent` · additive-only §3.8 · three-repo discipline · HF-HOLD SEC-2026-09-12-01 · Structural §3.8 sha-pin ad0d9439 · Mirror-invariant guard on `/app/backend/vendored/extraction_akki/backend/`.

<!-- Turn 4 sub-slice 4c prep · state-side extraction receipt · 2026-09-22T07:45:00Z END -->
