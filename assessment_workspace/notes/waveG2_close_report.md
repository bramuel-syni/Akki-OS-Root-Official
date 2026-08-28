# Wave G2 Close Report · V8 LITERAL Adoption + Live-Data Bridge

**Session close: 2026-08-28T~06:55Z · autonomous under all standing disciplines · STOP-and-report for owner's re-eyeball.**

---

## §1. Scope executed (owner ruling verbatim)

Owner verdict on Wave G (interpretation shell) verbatim: *"What you have build is totally out of touch with the HTML."* Wave G reopened as defect class **REINTERPRETATION-INSTEAD-OF-LITERAL-ADOPTION**.

Owner ruling (verbatim, 2026-08-28T~06:00Z): *"NEW METHOD — LITERAL ADOPTION (the prototype's own code becomes our code): … Extract the v8 embedded app COMPLETELY … The prototype's CSS ships VERBATIM as our stylesheet … MECHANICAL FIDELITY GATES … zero styles authored by us outside the prototype's files."*

Owner amendment (verbatim, 2026-08-28T~06:35Z): *"as you do that can the data be real data, assuming digicow was integrated"* — YES, live-data injection wired via same-origin iframe + `iframe.contentDocument` text-node substitution.

Executed:
- **Extract**: full extraction of the v8 embedded app (HTML template, head-`<style>`, dc-script blocks, 4 bundler payloads); hashes banked.
- **Adopt LITERAL**: prototype ships byte-verbatim as `public/v8_prototype.html` (sha256 unchanged from source).
- **BAN interpretation**: `AkkiV8Shell.jsx` + `akkiv8_design_system.js` deleted from both trees; hand-built React shell abandoned.
- **Wire real data**: pod React app hosts prototype in same-origin iframe, injects DigiCow / audit-trail / GPU-metadata into prototype's own DOM as text-node substitution + labelled live-fact cards.
- **Fidelity gates**: 100 mechanical invariants in `test_wave_g_v8_shell_port.py` (asset presence + BANNED-file absence + byte-identity + design-token / NAV-key / TAB-label / ROLE-person / content-constant / wordmark / canon-citation / agentsList-default-seed).
- **Env-drift fix**: monkey-patched Motor's `get_io_loop` in `conftest.py` to lazily rebind onto the current running loop on every async call (fixed anyio-parametrized `[asyncio]` tests dropped between Wave G close and now).
- **Close**: ratchet floor 2389 → 2463 (+74); double-green identical at new floor; receipts banked.

---

## §2. Files landed (LITERAL adoption artifacts)

**BYTE-IDENTICAL prototype** (Step-0-verified source, unchanged):

| path | sha256 | bytes |
|---|---|---:|
| `pod_shell/frontend/public/v8_prototype.html` | `e56871d01a99c2f3aa173c9b0a0f09e983c9f0e54ba3e61795ac8cb8575f98f2` | 1,264,425 |
| `/app/frontend/public/v8_prototype.html` | same | same |
| `phase0/html_snapshots/wave_g2_portal.html` | same | same |
| source: `fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html` | same | same |

**EXTRACTED artifacts** (recorded with hashes):

| path | sha256 | bytes |
|---|---|---:|
| `notes/wave_g2_extraction/v8_prototype_head_styles.css` | `299e6a48d35f3c81ebd7f4d1f741207d2de8d259325089d38dfbdad1a457fe55` | 388 |
| `notes/wave_g2_extraction/v8_prototype_dc_scripts.js` | `bd3a42b48723b32a12973494b7c5db99cc5bdf3a1a19564edb13b6af1b704b23` | 599,515 |
| `notes/wave_g_step0_v8/v8_template_decoded.html` | `9177c2b910b9caf5b07d6887317b37404443da83f548166da6f6e08f858e3a9a` | 1,111,498 |
| `notes/wave_g_step0_v8/8d5cc57e-*.application_javascript` | `ba61852925c4327a…` (dc-runtime county-map) | 6,289 |
| `notes/wave_g_step0_v8/0f495aa5-*.text_javascript` | `8fe7df74405f3c55…` (dc-runtime main bundle) | 69,150 |
| `notes/wave_g_step0_v8/a27c8ca4-*.text_javascript` | `35f4f974f4b2bcd4…` (react-dom UMD) | 131,835 |
| `notes/wave_g_step0_v8/373c1b27-*.text_javascript` | `d949f1c3687aedad…` (react UMD) | 10,751 |

**BANNED interpretation files** (deleted):
- `pod_shell/frontend/src/design/AkkiV8Shell.jsx` — deleted
- `pod_shell/frontend/src/design/akkiv8_design_system.js` — deleted
- `/app/frontend/src/design/AkkiV8Shell.jsx` — deleted (runtime mirror)
- `/app/frontend/src/design/akkiv8_design_system.js` — deleted (runtime mirror)

**MODIFIED** (byte-identical mirror between pod_shell and /app/frontend):

| path | sha256 | note |
|---|---|---|
| `pod_shell/frontend/src/App.js` | `364415486d602367542833faab6e3ce4cef24683e7d90f21c76038ca2b1abe16` | Root `/` renders `<PortalIframe/>` → iframe of `/v8_prototype.html` + post-load live-data injection via `iframe.contentDocument`. |
| `/app/frontend/src/App.js` | same | runtime mirror |

**Conftest env-drift fix** (targeted, non-invasive):

| path | change |
|---|---|
| `backend/tests/invariants/conftest.py` | Added `_install_motor_loop_autorebind()` at module load — monkey-patches `AgnosticCollection.get_io_loop` + `AgnosticDatabase.get_io_loop` to return `asyncio.get_running_loop()` when there is one. Idempotent. |

---

## §3. Right-reason RED banked pre-implementation

`phase0/drill_receipts/20260828T060500Z_wave_g2_literal_adoption_right_reason_fail.log`:

```
FAILED test_pod_shell_interpretation_authored_shell_is_banned[src/design/AkkiV8Shell.jsx]
FAILED test_pod_shell_interpretation_authored_shell_is_banned[src/design/akkiv8_design_system.js]
FAILED test_app_frontend_interpretation_authored_shell_is_banned[src/design/AkkiV8Shell.jsx]
FAILED test_app_frontend_interpretation_authored_shell_is_banned[src/design/akkiv8_design_system.js]
FAILED test_v8_prototype_html_present_in_pod_shell_public
FAILED test_v8_prototype_html_present_in_runtime_public
FAILED test_pod_shell_app_js_redirects_root_to_v8_prototype
FAILED test_pod_shell_app_js_does_not_import_banned_shell
FAILED test_runtime_app_js_does_not_import_banned_shell
FAILED test_no_authored_v8_css_module_in_design_folder
FAILED test_decisions_md_records_interpretation_ban
======================== 11 failed, 2 passed, 2 skipped in 0.67s ========================
```

Right-reason: BANNED files present (should be absent), byte-identity file not yet present, App.js still references banned shell.

---

## §4. Mechanical fidelity gates (100 invariants · `test_wave_g_v8_shell_port.py`)

| gate | count | discipline enforced |
|---:|---:|---|
| BANNED interpretation-file absence (pod_shell + runtime) | 4 | interpretation shell may never re-appear |
| Byte-identity of served prototype vs Step-0 source | 3 | `sha256(v8_prototype.html) == e56871d0…` in pod + runtime + snapshot |
| Extracted head-`<style>` hash | 1 | `sha256(v8_prototype_head_styles.css) == 299e6a48…` |
| App.js wires shell + doesn't import banned | 3 | 1 wiring + 2 negative-import gates |
| No authored v8 CSS/module in design/ folder | 1 | zero self-authored styles |
| Every declared pod route deep-link-accessible | 1 | pod components stay URL-accessible |
| DECISIONS.md records interpretation BAN | 1 | ruling permanence gate |
| Portal snapshot byte-identical to source | 1 | phase0/html_snapshots/wave_g2_portal.html |
| Served prototype contains each of 33 v8 NAV item keys | 33 | per-surface presence gate |
| Served prototype contains each of 10 v8 NAV group labels | 10 | verbatim labels |
| Served prototype contains each of 4 v8 TAB labels | 4 | Work/Build/3rd Party Apps/Admin |
| Served prototype contains each of 3 v8 ROLES (person + label) | 3 | M.Chen/A.Njeri/J.Otieno |
| Served prototype contains each of 17 v8 design token values | 17 | colors + font stacks |
| Served prototype contains `RMS AI` wordmark | 1 | Step 0 identity marker |
| Served prototype contains canon-citation comment | 1 | v8's self-declared canon mapping |
| Served prototype seeds Vendor Risk Monitor + Payroll Variance Checker | 1 | Step 0 verdict marker |
| Served prototype declares each of 14 content constants | 14 | GOV/GM/TRUST/RB_CATS/EST_GROUPS/APPROVALS/RULES_IN_FORCE/RAILS/CEREMONIES/CEREMONY_STAGES/ACTORS/WALKS/BRIEF/PATTERNS |
| agentsList default seed excludes Farma IQ | 1 | v8 removed FarmaIQ from default |
| **Total** | **100** | |

Every gate is a byte-search or hash comparison against a verified constant. No "we think it matches" logic anywhere.

---

## §5. Per-surface LIVE-DATA vs PROTOTYPE-SAMPLE table (owner amendment)

Per the owner amendment: *"the close report's per-surface table must show LIVE-DATA vs PROTOTYPE-SAMPLE per panel so the owner sees exactly which is which."*

The pod React app at `/` hosts the prototype in a same-origin iframe and (post-load, 400ms after `load` event to allow dc-runtime hydration) injects real data as:
1. **Text-node substitutions** inside prototype's own containers (regex-matched sample values swap for live values).
2. **Live-fact cards** appended to `document.body` with `data-fidelity="live-data"` + `data-live-source="<panel-id>"` attributes; positioned top-left, styled with prototype's own tokens (`Söhne` body / `ui-monospace` mono / `#1d7a6e` sage accent border).
3. **Untouched panels** get `data-fidelity="prototype-sample"` at their outer container.

| v8 surface | container(s) touched | data source (live) | fidelity | notes |
|---|---|---|---|---|
| **Registry / Data Estate** | `#registry-digicow-live-card` (appended) + text-node subs where regex matches sample values | `GET /api/registry/facts` | **LIVE-DATA** | Real DigiCow: `aws.rds.db-restore-603-cluster.digicow_live` · aurora-mysql 8.0.42 · region `eu-west-1` · 125 tables · ussd_users 2,285,264 · ussd_question_response 903,293 · sms_log 255,867 · aggregates only · PII BANNED per CP-E7 sanitizer. |
| **Audit Trail (CA1-001/002/003)** | `#audit-trail-live-card` (appended) | `GET /api/audit_trail/overview` | **LIVE-DATA** | Live multi_unit_answers count · evidence_completeness count · record_carriers count · partial_closure flag. |
| **Compute · akki-vm** | `#compute-akkivm-live-card` (appended) | non-secret metadata literal | **LIVE-METADATA** | Name `akki-vm` · OS `Ubuntu 22.04` · GPU specs pending SSH key drop (interrupt-priority sequence recorded) · auth key-pair · CUDA verify-only per amendment. Credentials never render. |
| Chat (WorkStudio · §6.1) | prototype seed conversations rendered by dc-runtime | none wired | **PROTOTYPE-SAMPLE** | `seedConversations()` renders; live chat backend is at `/chat` (deep-link) for full function. |
| Data Suite / Analyze (§6.2) | prototype seed | none wired | **PROTOTYPE-SAMPLE** | Not yet mounted in pod. |
| Documents (§6.3) | prototype seed | none wired | **PROTOTYPE-SAMPLE** | Not yet mounted in pod. |
| Task Manager (§6.4) | prototype seed (TASK_SEED × 3) | none wired | **PROTOTYPE-SAMPLE** | Not yet mounted in pod. |
| ThinkLab · Clarity / Strategy / Hypothesis / Perspective (§7) | prototype seed (TL_FLOW × 4 modes) | none wired at portal (deep-link `/thinklab/:mode` still works) | **PROTOTYPE-SAMPLE** | Full ThinkLab live at `/thinklab` deep-link. |
| Collab · Mentions / Emails / Projects / HR (§8) | prototype seed | none wired | **PROTOTYPE-SAMPLE** | No pod backend. |
| Exco 360 · Board 360 (§9) | prototype seed | none wired | **PROTOTYPE-SAMPLE** | No pod backend (Executive-Core donor material exists per reuse audit). |
| Manage Estate · Registry (§12.1) | shared with Registry surface above | `GET /api/registry/facts` | **LIVE-DATA** (via card) | Same DigiCow live-fact card serves this surface. |
| Manage Estate · Shield (§12.2) | prototype seed (GOV) | none wired | **PROTOTYPE-SAMPLE** | Live at `/shield` deep-link. |
| Manage Estate · Grey Mirror (§12.3) | prototype seed (GM) | none wired | **PROTOTYPE-SAMPLE** | Live at `/grey-mirror` deep-link. |
| Approvals · Spend / Rules / Model Admission (§13) | prototype seed (APPROVALS) | none wired | **PROTOTYPE-SAMPLE** | Live at `/governance` deep-link. |
| Build Your Resources · Train / Agent Build / Extract (§10) | prototype seed | none wired | **PROTOTYPE-SAMPLE** | Live at `/training` deep-link (Doc 17 Wave R4.1). |
| Your Resources · Agents / Models | prototype seed (Vendor Risk Monitor + Payroll Variance Checker) | none wired | **PROTOTYPE-SAMPLE** | Live at `/models` deep-link. |
| 3rd Party Apps · New / Frequent / Connected / Requests (§11) | prototype seed | none wired | **PROTOTYPE-SAMPLE** | No pod backend. |
| The Watch · State / Record / Under Watch / Decisions (§14) | prototype seed (RECORD_ROWS · PATTERNS · DECISIONS) | none wired | **PROTOTYPE-SAMPLE** | Live at `/watch` deep-link. |
| Instance · People & Declarations · Ceremonies (§15) | prototype seed (ACTORS · CEREMONIES) | none wired | **PROTOTYPE-SAMPLE** | Live at `/commission` deep-link. |

**Legend:**
- **LIVE-DATA** = the prototype's sample text is replaced (or supplemented by an appended card) with real numbers pulled from a pod API.
- **LIVE-METADATA** = non-secret facts (host name, OS, auth method) inserted from a literal that's factual today; not fabricated.
- **PROTOTYPE-SAMPLE** = the prototype's own seed data renders unchanged; the outer container gets `data-fidelity="prototype-sample"`.

**PII discipline preserved**: no farmer names, no phone numbers, no raw ussd_users rows. Only aggregates (counts, table names, region, engine version) and metadata (source_id, cluster_arn, link_working flag). CP-E7 DigiCow PII sanitizer boundary rule holds.

**16 EXTENSION-PENDING-OWNER-EYEBALL items** from Wave G re-mapped: after live-eyeball, the owner may authorize wiring more surfaces to live data (all of them route through existing pod backends where those backends exist; Executive-Core donor material catalogued in `notes/reuse_audit/PARKED_AT_CAT6_BOUNDARY.md` gives the LIFT/ADAPT/BUILD split for surfaces not yet in the pod).

---

## §6. Env-drift fix (touched conftest.py to unblock the close)

Between Wave G close (2026-08-28T~04:52Z · 2389/0/0) and Wave G2 (~06:20Z) an environmental change caused 31 anyio-parametrized `[asyncio]` tests in `test_phase_8_seam_3_sub_stage_3.py` to fail with `RuntimeError: got Future attached to a different loop`. Confirmed pre-existing to Wave G2 diff (verified by `git stash` at `de3b776`; failure persisted).

Root cause: `_motor_rebound_to_loop` (an `@pytest_asyncio.fixture(autouse=True)`) does not fire for tests marked `@pytest.mark.anyio`. Plain `@pytest.fixture(autouse=True)` async-gen sibling also did not fire. Motor's client stayed bound to a closed loop for those tests.

Fix (single hunk in `backend/tests/invariants/conftest.py`): monkey-patch `motor.core.AgnosticCollection.get_io_loop` and `AgnosticDatabase.get_io_loop` to return `asyncio.get_running_loop()` on every call. Idempotent; installed once at conftest module load. Restores 2389 anyio-passing baseline PLUS the 74-test net delta of the Wave G2 rewrite. New floor **2463**.

---

## §7. Permanent close

- **Ratchet floor**: 2389 → **2463** (+74 net; 100 new fidelity gates minus 26 old shell-presence tests).
- **Full-suite double-green identical:**
  - Run 1: `phase0/drill_receipts/20260828T065200Z_wave_g2_close_run1.log` · `passed=2463 / baseline-failures-remaining=0 / quarantined=0` · 88.08s.
  - Run 2: `phase0/drill_receipts/20260828T065400Z_wave_g2_close_run2.log` · `passed=2463 / baseline-failures-remaining=0 / quarantined=0` · 88.36s.
  - Byte-identical receipt lines.
- **`baseline_failures.json`** updated: `counts_at_baseline.passed = 2463` · `invariants_enforced_when_baseline_guard_1.passed_floor = 2463` · `ratchet_history` entry appended at 20260828T065000Z.

---

## §8. Standing arrivals unchanged

- **SSH interrupt priority** unchanged (interrupts Wave G2 if key drops mid-close; sequence: chmod 600 → `AKKI_GPU_SSH_PRIVATE_KEY_PATH` → `GPU_CONNECT_MODE=real` → hardware fact sheet → CUDA verify-only → EP-4 precondition guard → first governed run on sealed DigiCow set → real MOAC → whitepaper → stop-and-report).
- **Reuse audit** parked at Cat 6 boundary (partial findings at `notes/reuse_audit/PARKED_AT_CAT6_BOUNDARY.md` — Cats 1–5 complete + Cat 6 in-progress: Documents/TaskManager/DataSuite/WorkStudio/Exco-Board donor stacks catalogued with LOC and lift verdicts). Resumes after owner accepts or corrects Wave G2 eyeball.
- **Owner one-liners still open**: CA1-N5 RTO seconds · DigiCow occupation-boolean PII call · Doc 10 evidence-record backfill decision · A17.10 base-model census.
- **Decks/Documents build** remains BUILD-SCHEDULED-POST-PLAN (reuse audit findings shift the recommendation toward LIFT-clean from Executive-Core; ~8000 LOC of donor deck code catalogued).

---

## §9. STOP for owner re-eyeball

**Gate order per ruling**: automated first, then owner eyeball. Automated: 4/4 mechanical gates GREEN (byte-identity + 100 fidelity + double-green + 2463/0/0). Owner eyeball is the final gate — HIS verdict closes the wave, not our tests.

**What the owner will see at `/`:**
1. The full v8 prototype loads byte-verbatim in an iframe filling the viewport.
2. Post-hydration (~400ms after iframe `load`), three live-fact cards appear top-left:
   - `Registry · aws.rds.db-restore-603-cluster.digicow_live` — real DigiCow facts.
   - `Audit Trail · live (CA1-001/002/003)` — real counts.
   - `Compute · akki-vm (owner-signed EC2)` — real non-secret metadata + GPU-pending-SSH note.
3. Every panel in the prototype (whether text-substituted or untouched) carries `data-fidelity="live-data"` or `data-fidelity="prototype-sample"` for DOM inspection.
4. The prototype's URL bar shows `/` (React route); the iframe internally references `/v8_prototype.html` (byte-identical to source).

**What the owner can verify externally:**
- Open `phase0/html_snapshots/wave_g2_portal.html` directly — byte-identical to source `fixtures/RMS_AI_Akki_Prototype_v8_Standalone.html`.
- Diff `public/v8_prototype.html` bytes vs source — must be zero-diff.
- Read `test_wave_g_v8_shell_port.py` — 100 mechanical gates, no "we think it matches" logic.
- Run `BASELINE_GUARD=1 python -m pytest tests/invariants/` — must report `passed=2463 / baseline-failures-remaining=0 / quarantined=0` (or higher `passed` count if new tests have landed since).

**HEADs**: Extraction-Akki `programme/track-a` = PENDING (this commit); master workspace = PENDING (STATE mirror commit).

---

**End of Wave G2 close report. Position: HOLD for owner re-eyeball.**
