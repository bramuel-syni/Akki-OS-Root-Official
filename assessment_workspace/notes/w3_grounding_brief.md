# W3 · Chokepoint · Masking · Exit Gate · Residency · Data Shield surface — grounding brief

**Owner Order 2026-08-25 · "W3 go"** (see `STATE/DECISIONS.md` for verbatim). Scope class **L**.

## 1. Register rows targeted by W3

Read directly from `notes/requirements_register_17docs.md` + `notes/canon_addendum_1_requirements.md`:

- **Doc 01 · Custody & Crossing Pt 1 · The Chokepoint** — 19 rows total. W3 addresses the mechanism half of the register (the crossing engine, not the intent-extraction half which is anchored to reasoning in W5).
  Key rows in scope this wave:
  - Doc01-001 · A5.1 · **Single chokepoint** (one function invokes external client; every outbound model call passes through it; enforced by negative-scan build gate).
  - Doc01-002 · A5.2 · **Custody sequence** (de-identify → invoke → re-identify; no path skips).
  - Doc01-003 · A5.3 · **Per-request envelope dies with the call** (token-to-value mapping never persisted).
  - Doc01-004 · A5.4 · **Tenant-scoped entity resolution** (each tenant supplies the entity set the de-identifier consults).
  - Doc01-005 · A5.5 · **Closed outbound network except at crossing** (network-layer allowlist + static-analysis build gate).
  - Doc01-006 · A5.6 · **Structural impossibility, not policed prohibition**.
  - Doc01-007 · A5.7 · **Trust receipt** (per invocation; credential never logged; signed & tenant-bound; one authoritative record).
  - Doc01-008 · A5.8 · **Two custody pathways both receipted** (synthesis + perception).
  - Doc01-009 · A5.9 · **Grounding failure is refusal** (Doc 4; bounds "complete answer" here).
  - Doc01-010 · A6 · **Negative-scan test exists and runs**.
  - Doc01-011 · A6 · **De-identifier + tenant set jointly cover identifiers in-estate**.
  - Doc01-012 · A6 · **Per-request envelope verifiably destroyed**.
  - Doc01-013 · A6 · **Allowlist + build gate both active**.
  - Doc01-014 · A6 · **Credential never varies behaviour**.
  - Doc01-015 · A6 · **Both custody pathways held simultaneously**.

  Deferred beyond W3 (intent-extraction half):
  - Doc01-016..019 · B-part (intent · meaning · objective extraction BEFORE de-identify; Solva + Northena consumers) — belongs to W4 (Northena) / W5 (Solver · Shrinkage · Memory).

- **Doc 02 · Custody & Crossing Pt 2 · Confidentiality Authoring & Dual-File** — 20 rows total (18 canon + CA1-007 + CA1-001).
  Key rows in scope this wave:
  - Doc02-001 · A5.1 · **Confidentiality list extends the tenant entity set** consumed at the crossing.
  - Doc02-002 · A5.2 · Objective-shaping loop produces a testable declaration (Generate/Edit dialogue → mechanically testable declaration).
  - Doc02-003 · A5.3 · Review shows reach against **measured material only** (honesty-about-the-unmeasured).
  - Doc02-004 · A5.4 · Adding/removing asymmetric — **removal runs the governed ceremony** (Doc 14).
  - Doc02-005 · A5.5 · The list is itself a **governed record** (authoring provenance retained).
  - Doc02-011 · B5.1 · **Two items split before assessment** (File 1 = question; File 2 = extracted data pre-redaction).
  - Doc02-012 · B5.2 · **Independent assessment, no cross-consultation**.
  - Doc02-013 · B5.3 · **Re-association seam re-checks** ("mark twice"); refuses if either file fails.
  - Doc02-014 · B5.4 · Two files' custody class **distinct from mapping envelope** (files retained in full; every subsequent read is fully masked).
  - Doc02-015 · B5.5 · **Single-query guarantee** (two items, one query).
  - Doc02-016 · B5.6 · **Joint re-identification check at the seam**.
  - **Doc02-020 · CA1-007 · Dry-run preview** between Review and Adopt. Status **BUILD** (no equivalent surface exists).

- **CA1-N4 · Residency & cross-border transfer control** — 1 row.
  - Enforcement rule on data already tagged per-source-region (Doc 9 already captures region at Connect). Real facts on record: Aurora cluster in `eu-west-1`. akki-vm commissioning record carries NO region field — real gap; W3 renders drawn-not-blank + enforces at the parse boundary.

**W3 row count target: 15 (Doc 01) + 12 (Doc 02) + 1 (CA1-007) + 1 (CA1-N4) = 29 rows.**
Not all 29 will be fully DONE by W3 close — some belong to future waves (perception path W6+, intent-extraction W4/W5, Watch dovetail W6/W8, dual-file custody class W5/W6). W3 opens the CORE of Doc01/Doc02: single chokepoint + custody sequence + tenant entity set + closed egress + trust receipt + honest-about-unmeasured + dry-run + residency enforcement.

## 2. Real crossings today — inventory

Owner cautionary line held: **no invented crossing volumes**. The estate's actual outbound paths on disk RIGHT NOW:

- **(x1) AWS RDS Data API** — HTTPS out via boto3. Path: `services.connect.rds_data_submit.submit()`. Region: `eu-west-1`. Verb set: SELECT (structure-only reads via `information_schema` today; no PII-bearing rows crossed the seam yet, tests-first grounded). No frontier LLM upstream.
- **(x2) Compute seam SSH** — SSH to `akki-vm`. Path: `services.compute_seam.seam.execute()`. Location: not on record in commissioning record (real gap). Verb set: attested command list only. No LLM traffic.
- **(x0) LLM crossing** — DOES NOT EXIST YET. There is no `synisense.chokepoint` in this estate; no external model client is imported anywhere in `backend/`. The chokepoint mechanism must be built such that when the LLM path lands, it lands INSIDE the discipline; not after.

**W3 chokepoint scope decision (per owner):** the chokepoint must cover the real outbound paths as they exist today (Data API + SSH), bringing them under ledgered + receipted discipline, BEFORE any LLM path lands. Where full masking of SQL results is premature (structure-only reads so far), enforce and test the gate at the boundary that exists and name the deferred part.

- Full row-value masking on the Data API path: **deferred to a future wave that carries the first row-bearing query.**
- Trust receipt + residency check + governance mark on the crossing itself: **in scope for W3.**

## 3. Six mechanisms in scope (a–f)

### (a) Single outbound chokepoint

**Reuse pulls cited** (per `notes/reuse_map_v7.md`):
- **LIFT** `Akki-Executive-Core/backend/services/privacy_wall.py` → adaptable one-function wrapper pattern (private-network only) — read here as a shape reference only.
- **ADAPT** `RMS-IQ-Core-2/backend/services/synisense/shield/egress_firewall.py` (137 LOC) → the runtime egress firewall + AST gate pattern. `EgressFirewallDenied` exception class. httpx transport wrapper. Rewrite for boto3+SSH crossings we actually run.
- **ADAPT** `RMS-IQ-Core-2/backend/services/synisense/shield/exceptions.py` → `ShieldFailure` grammar.
- Destination: **new** `backend/services/chokepoint/` module in Extraction-Akki (this repo).

**W3 shape**: one Python function `register_crossing(kind, endpoint, verb, payload_shape, actor)` that every outbound service must call at the boundary. Chokepoint returns a `CrossingReceipt` (see (f)) or raises `ChokepointRefused` on residency / masking-tier violation. Boto3 clients and SSH executor call `register_crossing()` at the last line before the network. Static test proves no path in `backend/` reaches `boto3`, `paramiko`, or `httpx` without transiting the chokepoint.

### (b) Masking tiers

**Reuse pulls cited**:
- **ADAPT** `RMS-IQ-Core-2/backend/services/synisense/shield/masking_tier.py` (69 LOC) → positive allowlist reader pattern with `MaskingTierRefused` refusal grammar and per-env admissibility.
- Destination: `backend/services/chokepoint/masking_tier.py` (new).
- Config file: `backend/services/chokepoint/masking_tier_allowlist.v0.json` (new) — governed positive list.

**Doc 02 §A3 canonical tiers**: three-level specificity (exact / pattern / category). Our W3 admissible tiers land as:
- `structure_only` — Data API reads limited to `information_schema` metadata + counts. NO row content crosses.
- `attested_command` — SSH seam allows only the attested command list from `hardening.json`; no shell.
- `receipt_only` — for governance/audit reads (registry facts, commissioning records) that touch no external system.

Row-bearing tiers (`t1_full_mask`, `t2_partial`, `t3_category`) are declared in the allowlist but marked `admissible_under_env: []` — **not yet admissible in any env** — pending row-bearing queries and DPO declaration authoring (Doc 02 §A5.2 / CA1-007 lands the authoring surface separately in this wave).

### (c) Exit gate

**Reuse pull cited**:
- **ADAPT** `RMS-IQ-Core-2/backend/services/synisense/shield/egress_firewall.py` static-AST + runtime pattern.
- Destination: `backend/tests/invariants/test_chokepoint_single_exit.py` + `backend/services/chokepoint/exit_gate.py`.

**W3 shape**: two enforcement layers per Doc 01 §A5.5 (allowlist + build gate).
- **Static**: AST test that fails if any module in `backend/` other than `chokepoint/` imports `boto3` or `paramiko` (the SSH lib we actually use) OR calls `httpx.*`. Existing seam adapters (`services.connect.rds_data_submit`, `services.compute_seam.seam`) get moved onto chokepoint's `register_crossing()` call FIRST; then the AST rule tightens.
- **Runtime**: `enforce_exit(request)` refuses on: (i) unknown masking tier; (ii) tier not admissible under current `AKKI_ENV`; (iii) residency mismatch.

### (d) CA1-007 · Dry-run preview

**Reuse citation**: no existing surface for this — CA1 explicitly says "no equivalent surface exists". So this is **BUILD**.

**W3 shape** (per Addendum): given a candidate declaration + a bounded sample of recent traffic, return what it WOULD have caught and what it WOULD NOT — WITHOUT adopting it. REFERENCE-NOT-COPY: the sample is drawn by identity from records already on disk; the preview references them, never copies them into a standalone artifact.

- Endpoint: `POST /api/shield/dry-run` — payload `{candidate_declaration, sample_scope}`; returns `{would_catch:[…identity refs], would_miss:[…identity refs], provenance}`.
- Since the estate has NOT yet run row-bearing queries, the "bounded sample of recent traffic" today is the crossing-receipt log (see (f)) — the dry-run walks those receipts and reports which crossings would have matched the candidate. That's honest: no fabricated traffic.

### (e) CA1-N4 · Residency

**Real facts on record**:
- `data_source_digicow_live_20260819T152513Z_FINAL.json` · `resource.region = "eu-west-1"`.
- `data_source_ndume_20260819T152513Z_FINAL.json` · `resource.region = "eu-west-1"`.
- `commissioning_akki-vm_20260818T195751Z_ACCEPTED.json` · **NO region field** — real gap.

**W3 shape**:
- Governed allowlist file at `backend/services/chokepoint/residency_allowlist.v0.json` naming the regions admissible for the estate today (`eu-west-1` only, based on the real facts on record).
- Chokepoint refuses `register_crossing()` when `endpoint.region` is not on the allowlist.
- Data Shield surface renders per-crossing region as a chip; renders akki-vm's region as **drawn-not-blank**: "region: not on record — commissioning record does not carry a region field. Log it before this host handles data outside its build phase."

### (f) Data Shield surface (v7 oracle EXACT per T1)

**Reuse pulls cited**:
- **ADAPT** `Akki-Executive-Core/frontend/src/components/synisense/` (existing surface; must be re-tabbed to v7's grammar).
- **ADAPT** `RMS-IQ-Core-2/backend/services/synisense/shield/trust_receipt.py` for receipt shape.
- Destination: `pod_shell/frontend/src/components/DataShield.jsx` (new).

**v7 fabric extracted verbatim** (from `prototype/prototype.html` at offset 334300–337500):
- Header: "Every governed model call is shielded and receipted. The per-message pattern lives inline in Chat, on each answer — open the shielding & provenance expander there to see it live."
- Session-timeline card shape: per-purpose block with countLabel (e.g., "×3 calls"), provider label, exposure %, dilution %.
- Session headline: "N governed calls this session · zero raw content crossed the seam." (real facts render this literally against our crossing log)
- `datashield` icon: `svgI(P(SHIELD))` where `SHIELD` is the standard shield path.
- Nav placement: **Trust Center group → Data Shield** (per `estate: [{key:'estate',label:'Data Estate'},...]` and `trust: [{key:'rules'…{key:'datashield'…}]` in v7).
- Landing greeting (in v7 CONTEXT map): "Six governed calls this session, none of them carrying raw content." — we render the honest count from our own record.

W3 renders the ACTUAL crossings on disk (Data API + SSH), NOT the v7 sample vocabulary. Zero fabricated crossing volumes.

## 4. Scope class L discipline

`notes/status_and_wave_plan.md` §W3 row: L ≈ 2000 LOC · 1 surface · 4 mechanisms · 4 register rows headline.

W3 accounts (estimate — will be measured at close):
- Backend: chokepoint core (~200) + masking_tier (~120) + exit_gate (~150) + dry_run (~180) + residency (~120) + router (~130) = ~900 LOC.
- Frontend: DataShield.jsx (~500 LOC).
- Tests: ~30 invariants across the six mechanisms + AST negative-scan.
- Config: masking_tier_allowlist + residency_allowlist + shield_egress_exemptions = ~90 LOC JSON.
- **Estimate total: ~1500–1800 LOC** — inside L (≤2000). If it grows past 2000 during build, STOP and report per owner cap.

## 5. Checkpoint commit plan

Section A · Grounding brief + ruling logged (this file + `STATE/DECISIONS.md` edit) → checkpoint 1.
Section B · Chokepoint core + masking tier + exit gate + AST negative-scan + tests-first receipts → checkpoint 2.
Section C · Residency allowlist + parse-time enforcement + tests → checkpoint 3.
Section D · CA1-007 dry-run preview endpoint + tests → checkpoint 4.
Section E · Data Shield surface (frontend) + screenshots → checkpoint 5.
Section F · Wave close: STATE + status + green receipt + close notes → checkpoint 6.

**No checkpoint ends with uncommitted green code** (owner rule).
