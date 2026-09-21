# R-98 · G5-v5 Family D · RBM-1..23 + ROC-1..11 · Seal Report

**Wave**: R-98 · CP-G5V5-FAMILY-D-RBM-ROC
**Family**: D · Rules Service
**Sealed at UTC**: 2026-09-21T07:10:00Z (Commit-B state banking)
**Commit-A SHA**: `38eeef6c4844c56e91900a83355c140f76733148` on `programme/track-a`
**Commit-B SHA**: (this-commit · state master)
**COMPLETION SPRINT step**: 2 of 6 (Family D · CLOSED)

---

## Rules registered (34 · byte-verbatim SRR statements)

### RBM Tier A · rulebook_engine_spec_v1 · Rules Service · SRR rows 288..309

| ID | SRR row | Rule statement (byte-verbatim) |
| --- | --- | --- |
| RBM-1 | 288 | Rule authored with full field set — ID, origination, owner, enforcement class, domain, tier, assessment procedure — or authoring refuses to save |
| RBM-2 | 289 | Drafting assistance may propose; only the named human author confirms before a rule enters PROPOSED |
| RBM-3 | 290 | Mnemonic prefix reserved centrally before first use; collision refused at reservation |
| RBM-4 | 291 | Tier declared at authoring: system-TCB, system-ordinary, or customer |
| RBM-5 | 292 | Impact record produced before countersign — every dependent rule, checkpoint, component, profile |
| RBM-6 | 293 | Every adopted or customer rule checked against system rules; refused if it relaxes a STRUCTURAL/MECHANICAL rule |
| RBM-7 | 294 | System-ordinary/customer ceremony: propose, impact record, countersign, cancellable countdown, apply, re-verify |
| **RBM-8** | **295** | **System-TCB ceremony: as RBM-7 plus slowest countdown and external witness with no credentials over the component** ← R-91 CEREMONY ANCHOR |
| RBM-9 | 296 | Either signatory may cancel before countdown expires; cancellation recorded with identity and reason |
| RBM-10 | 297 | Apply is atomic: status, Registry entry, Ledger record, rule-version stamp — all four or none |
| RBM-11 | 298 | Re-verify runs the assessment procedure after apply; failure raises a finding, never a silent rollback |
| RBM-12 | 299 | Amendment is a new version through full ceremony; prior version retained, never overwritten |
| RBM-13 | 300 | Retirement is through ceremony; retired rule keeps status and history; destruction attestation where required |
| RBM-14 | 301 | Library rule book: versioned, cites source clause, every rule in RBM-1's format — uncited rule is not admissible |
| RBM-15 | 302 | Profile: named bundle of rule books per business type, versioned, changed through system-ordinary ceremony |
| RBM-16 | 303 | At onboarding, business type selected and matching profile presented as recommendation, marked as such |
| RBM-17 | 304 | Adoption instantiates rule-book rules as customer rules via customer-tier ceremony, after RBM-6's conflict check |
| RBM-18 | 305 | Registry is the authoritative store — every ROC-10 field, append-only per ROC-11 |
| RBM-19 | 306 | Assessment procedure runnable on demand and on schedule; Statement of Applicability is a Registry view |
| RBM-20 | 307 | Registry queryable by ID, objective, promise, tier, status, enforcement class, domain, rule book, profile, tenant |
| RBM-21 | 308 | Rules Service's own rules are system-TCB tier; no path alters them outside RBM-8's ceremony |
| RBM-22 | 309 | Every Rules Service action writes an audit record with all six AU-3 elements |

### RBM Tier B · watch_learning_v1 · O2 Security & Intent · SRR row 483

| ID | SRR row | Rule statement (byte-verbatim) |
| --- | --- | --- |
| RBM-23 | 483 | Certificate requirements are a named rule class of tier system-TCB — they determine Mkono's inputs. Each is authored with RBM-1's full field set, enters force only through RBM-8's ceremony (the platform's slowest countdown; an external witness holding no credentials over the Watch), and is amended or retired only through RBM-12 and RBM-13. Every requirement carries its provenance — the Ledger references of the incidents it was formed from — and the library is queryable under RBM-20. |

### ROC Tier A · rule_criteria_spec_v1 · Rules Service · SRR rows 277..287

| ID | SRR row | Rule statement (byte-verbatim) |
| --- | --- | --- |
| ROC-1 | 277 | Definition of a rule — addressable, a requirement not an explanation, falsifiable |
| ROC-2 | 280 | Rule proliferation forbidden — cite, never reissue, an already-ratified rule |
| ROC-3 | 281 | POSITIONAL ID scheme — [Part][Section].[Sequence] |
| ROC-4 | 282 | MNEMONIC ID scheme — [prefix]-[Sequence], for named sub-mechanisms only |
| ROC-5 | 283 | Scheme exclusivity — one ID scheme per rule population |
| ROC-6 | 284 | Mnemonic prefixes reserved in the Registry before first use |
| ROC-7 | 285 | Status axis — CANON · RULED · DEFAULT · PROPOSED · OPEN, exactly five |
| ROC-8 | 286 | Enforcement-class axis — STRUCTURAL · MECHANICAL · MEASURED · CEREMONIAL · ADVISORY |
| ROC-9 | 287 | Domain axis — six engines, four outside-the-six categories, Cross-Cutting |
| ROC-10 | 278 | A single standing Rule Registry with the required fields per rule |
| ROC-11 | 279 | Registry is append-only on the Ledger's custody discipline |

---

## RBM-8 · R-91 ceremony-mechanic anchor (owner directive this-session)

Owner directive 2026-09-21T~06:35Z verbatim: **"when you author RBM-8, its invariant should reflect exactly that: ceremony windows are rigid, no shortening path exists in code, and the R-91 window you are currently honoring is the live evidence receipt."**

Owner NO-EXPEDITE ruling 2026-09-21T~06:15Z verbatim: **"The countdown that cannot be shortened is the ceremony (RBM-8; SER C.5 I-4), and it's a Tier A check in the audit standard about to be applied to this repository — §6.6, 'a countdown cut short' is what FAIL looks like."**

### Encoded invariants (Final[...] · load-bearing)

```
RBM_8_IS_R91_CEREMONY_ANCHOR: Final[bool] = True
RBM_8_CEREMONY_WINDOW_IS_RIGID: Final[bool] = True
RBM_8_NO_SHORTENING_PATH_IN_CODE: Final[bool] = True
RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC: Final[str] = "2026-09-23T03:23:15Z"
RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT: Final[bool] = True
```

### Grep-negative scanner (5-pattern watch)

`scan_for_ceremony_shortening_path(code: str) -> tuple[str, ...]` — emits any of these that appear in `code`:

- `shorten_ceremony_countdown`
- `expedite_ceremony_apply`
- `waive_ceremony_countdown`
- `bypass_ceremony_horizon`
- `fast_forward_ceremony`

**Tested**: clean-input-empty + each-pattern-hits (5/5 byte-verbatim).

**SER C.5 I-4** noted as live audit-standard cross-reference but out-of-scope for Family D (Rules Service) code deliverable · belongs to `release_gate/audit_standards` module scope.

---

## Test surface (40 tests)

- **4 registry-shape/metadata**: RBM_RULE_IDS closed 23-tuple + RBM Tier A split 1..22 + RBM Tier B split 23 + ROC_RULE_IDS closed 11-tuple.
- **22 RBM Tier A property**: RBM-1..RBM-22 · each with SO §2.5 verbatim-docstring quoting SRR statement.
- **1 RBM Tier B property**: RBM-23 (asserts "Certificate requirements are a named rule class of tier system-TCB" prefix + "RBM-8's ceremony" citation + "RBM-20" citation).
- **11 ROC Tier A property**: ROC-1..ROC-11 · ROC-7 status axis + ROC-8 enforcement-class axis carry closed-vocab Final tuple assertions.
- **1 extended RBM-8 ceremony-mechanic** (asserts all 5 sub-invariants).
- **2 RBM-8 grep-negative scanner** (clean-input-empty + each-pattern-hits).

---

## Ratchet · sweep · byte-identity

- Prior floor: 5782
- New floor: **5822** (delta +40 measured · targeted equalled measured · no CCS2 correction needed)
- Prior baseline_failures.json sha256: `a2a28fcf153170e80035e038f642cc7559ccd9fc0f2ec280442ce64bb3f88a78`
- New baseline_failures.json sha256: `df3325f7bc82f49060ed097ce0755bb4c3ed3aa46147ea799a14e293a96674cd`
- New ORCH_BOOT.md sha256 (pre-Commit-A regen): `15982ed837224c3688b3b5a71bb669f09b11f435ced938fa046112f47c083b4f` (notes + POD audit mirror byte-identical)
- Deterministic double-green byte-identical stripped-sha256: `33d59d5acf5757b9a6493d3371c7e01239bf097d9be7746a487698fbe7443192` (both runs under `PYTHONHASHSEED=0 BASELINE_GUARD=1`)

### Drill receipts (banked at Commit-A)

- `backend/phase0/drill_receipts/20260921T064000Z_r98_family_d_rbm_roc_RED_pre.log` — RED first (3 fails right-reason AttributeError on incremental owner-directive symbols)
- `backend/phase0/drill_receipts/20260921T064500Z_r98_family_d_rbm_roc_GREEN_post.log` — GREEN (40/40 pass in 0.78s)
- `backend/phase0/drill_receipts/20260921T070000Z_r98_family_d_BASELINE_GUARD1_run1.log` — 5822 passed / 3 baseline-fail / 1 skip / 438 warnings · 184.28s
- `backend/phase0/drill_receipts/20260921T070500Z_r98_family_d_BASELINE_GUARD1_run2.log` — byte-identical to run1

---

## Canon anchors (verbatim)

- Owner COMPLETION SPRINT directive 2026-09-21T~06:10Z (six-step)
- Owner R-91 NO-EXPEDITE ruling 2026-09-21T~06:15Z (RBM-8/SER C.5 I-4 citations)
- Owner this-session RBM-8 ceremony directive 2026-09-21T~06:35Z ("ceremony windows are rigid, no shortening path exists in code, R-91 window is the live evidence receipt")
- Owner G5-v5 sequencing directive 2026-09-21T~01:00Z at `a30db4f7`
- Owner Ruling 5 (SRR-as-authority · v5 workbook sha `00072c58...`)
- Owner Ruling 3 erratum (class column HINT · rule text governs)
- R-97 seal `c98fe5c`/`d233975d`/`971e3dad` (immediately-precedes · Family C fully closed)
- R-96 seal `65da970`/`8cbe5cfe`/`100d0b1f` (Family C Tier A)
- R-91 CEREMONY-OPEN `a30db4f7` (APPLY 2026-09-23T03:23:15Z NO EXPEDITE)
- SO §2.5/§3/§3.3/§3.8/§3.10-α/§6/§6.4/§6.6/§6.7
- M16-W3 corrected order
- CCS2 lesson (with hash-seed determinism · `PYTHONHASHSEED=0` required)

---

## R-91 horizon (unchanged at this seal)

- Horizon: `2026-09-23T03:23:15Z` (frozen at ceremony-open `a30db4f7`)
- Current UTC at Commit-B: `2026-09-21T~07:10Z`
- Delta: ~44.2h out
- **R-91 stays PARKED** · R-98 completes cleanly inside window with zero ceremony-apply operations opened.

---

## Autopilot next per COMPLETION SPRINT sequence

Step 3 · **OPEN-CARD SWEEP** across `STATE/OBJECTIVES/` → step 4 · **LIFECYCLE/ENTITLEMENT HTTP SURFACE** additive routers → step 5 · **R-91 ε-APPLY** at horizon → step 6 · **FINAL CLOSURE REPORT**.

Standing bounds unchanged: zero push · zero remote configured · terminal pytest only · **no `testing_agent`** (STRICTLY BANNED per SO §6) · additive-only §3.8 · three-repo discipline · ratchet monotonic-up floor **5822** · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged.
