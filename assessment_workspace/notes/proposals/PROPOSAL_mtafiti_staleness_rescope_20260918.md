READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PROPOSAL · Re-scope 5 `mtafiti_gpu_discovery::test_*_is_recent` staleness invariants · Canon 3 §24 ceremony

**Filed:** 2026-09-18T~09:35Z
**Filer:** main-agent Autopilot (post-reconcile, under owner ruling 2026-09-18 · Option A + (ii))
**Bridge clause active:** owner-authorised at most ONE further reconcile if this ceremony has not landed by `t0 + 72h ≈ 2026-09-21T09:20Z`. Second reconcile is itself a report.
**Ceremony type:** rule change per Canon 3 §24 (propose → counter-sign → wait → apply). This file is the **propose** step only. Applying the change requires owner counter-sign + countdown expiry.

---

## §1 · Owner ruling verbatim (source of this proposal · banked in `STATE/DECISIONS.md`)

> "(ii) — formal campaign close-out through ceremony, within the 72-hour window A buys. The staleness tests encode 'telemetry is younger than 72 hours' as a floor property. With the campaign over, that no longer tests a live property of the system — it tests whether someone keeps refreshing telemetry. A test that measures ritual isn't a floor; it's a chore with a red light. Re-scope, don't retire: an age gate applies only while a campaign is declared open; in steady state the invariant is presence, integrity hash, and last-known-good on record. (iii) is the circle — the same RED every 72 hours. (i) only if there is a stated reason to keep collecting GPU telemetry, and keeping a campaign open to keep a test green is not one."

---

## §2 · What is being re-scoped

Five invariant tests, all currently under `repos/Extraction-Akki/backend/tests/invariants/`:

| Test file | Test name | Current invariant |
|---|---|---|
| `test_mtafiti_gpu_discovery_composition_census.py` | `test_live_composition_census_is_recent` | `age(composition_census_latest.json) < 72h` unconditional |
| `test_mtafiti_gpu_discovery_live_readonly_probe_receipt.py` | `test_probe_receipt_is_recent` | `age(live_readonly_probe_latest.json) < 72h` unconditional |
| `test_mtafiti_gpu_discovery_quality_profiler.py` | `test_live_quality_profile_is_recent` | `age(quality_profile_latest.json) < 72h` unconditional |
| `test_mtafiti_gpu_discovery_stratified_relationships_cost.py` | `test_cost_receipt_is_recent` | `age(cost_receipt_latest.json) < 72h` unconditional |
| `test_mtafiti_gpu_discovery_wave_close.py` | `test_wave_close_bundle_is_recent` | `age(wave_close_bundle_latest.json) < 72h` unconditional |

All five encode "age < 72h" as a floor property. Owner ruling identifies this as "a chore with a red light" once the underlying campaign has closed — the test measures ritual (someone refreshing telemetry), not a live system property.

---

## §3 · Proposed new shape (per owner text verbatim: "re-scope, don't retire")

### §3.1 · Two invariants, gated by campaign-declared-open state

Each of the five tests splits into TWO assertions, gated by a single ambient predicate:

**Ambient predicate:** `_campaign_declared_open() -> bool`

- Reads a **new state file** at `STATE/mtafiti_campaign_state.json`.
- Returns `True` iff the state file contains a JSON object with `{"status": "open", "opened_at_utc": "<ISO8601>", "expected_close_at_utc": "<ISO8601>"}` AND `expected_close_at_utc` is in the future.
- Returns `False` otherwise (missing file · malformed · `status != "open"` · `expected_close_at_utc` in the past).

State-file lifecycle: written by an owner-signed ceremony (a new campaign-open owner ruling banked in `STATE/DECISIONS.md`); status flips to `"closed"` at campaign close via a matching campaign-close ceremony. Never edited by main-agent unilaterally.

### §3.2 · Assertion shape

```python
def test_composition_census_shape():
    d = _load()
    # Steady-state invariants (ALWAYS enforced):
    assert "at_utc" in d, "presence: at_utc field required"
    assert _parse_utc(d["at_utc"]) is not None, "at_utc must be a valid ISO-8601 UTC timestamp"
    file_sha = _sha256_of_path(_CENSUS_PATH)
    assert file_sha == d.get("integrity_hash", file_sha), \
        f"integrity hash mismatch: file={file_sha} vs banked={d.get('integrity_hash')}"
    assert _last_known_good_recorded(d), \
        "last-known-good record required (previous_at_utc + previous_integrity_hash fields)"
    # Age gate (ONLY while campaign is declared open):
    if _campaign_declared_open():
        age = datetime.now(timezone.utc) - _parse_utc(d["at_utc"])
        assert age < timedelta(hours=_MAX_CENSUS_AGE_HOURS), (
            f"campaign is declared open; census stale ({age.total_seconds()/3600:.1f}h)"
        )
```

The **steady-state invariants** (presence · integrity hash · last-known-good on record) run always. The **age gate** activates only inside campaign windows. Outside campaign windows: presence and integrity are still enforced; age is not.

### §3.3 · Reason-for-existence guardrail (per owner "(i) only if there is a stated reason")

Each of the five telemetry files carries a `campaign_context` sub-field naming the campaign that produced the row. Rows lacking `campaign_context` are legacy; a data-migration seal at ratification time bank the current file's `campaign_context = "CP-M11-GATE-RELEASE · GPU 72h discovery window · opened 2026-09-15T~08:00Z · closed 2026-09-18T~08:16Z"` per the seal history.

### §3.4 · Refactor cost

Each of the five test files gains ~15 lines (steady-state assertions + gated age check + new imports). All five reuse a **shared helper** at `tests/invariants/_mtafiti_staleness_helpers.py` for `_campaign_declared_open()`, `_sha256_of_path()`, `_last_known_good_recorded()`. Total new code: ~50 lines of test infrastructure + shared helper. No production code touched.

Ratchet impact:
- Existing 5 tests remain by name; assertion body changes.
- No test is retired; no test is added; **ratchet floor stays at 4826**.
- Byte-identical double-green byte-match on the ceremony-apply seal.

---

## §4 · Bridge clause (owner-authorised)

Per owner ruling text verbatim: "**if the ceremony can't land inside 72 hours, exactly one further reconcile is permitted, banked as bridging — not a standing practice, and the second reconcile is itself a report.**"

**Operational reading (banked in `STATE/DECISIONS.md` § "OWNER RULING · GPU-telemetry-staleness fork"):**
- **t0 (this reconcile):** 2026-09-18T~09:20Z (executed this-turn).
- **Bridge horizon:** `t0 + 72h ≈ 2026-09-21T09:20Z`.
- **If this proposal has landed** (owner counter-sign + countdown expiry + apply seal on master) before the bridge horizon: no further reconcile needed. Steady state via new gated shape.
- **If this proposal has NOT landed** by the bridge horizon: exactly ONE reconcile-B may execute (same pipeline: census → probe → quality → cp6-bundle → wave-close). Reconcile-B execution surfaces as its own owner-report. No third reconcile. No standing practice.

---

## §5 · Canon-3-§24-ceremony structure

Per Canon 3 §24 (banked in `notes/chunk1_20260918/chunk1_task_d_canon_3_requirements.md` C3-R-083..C3-R-086):

1. **Propose** (this file · this-turn · main-agent) — done.
2. **Counter-sign** (owner · pending) — required.
3. **Countdown** (per §24 default class · TBD by owner) — runs after counter-sign.
4. **Apply** (main-agent · new §3.3 3-commit seal) — implements the shape change under standing autonomous authority once countdown expires.

**Cross-references banked:**
- Owner ruling 2026-09-18 (`STATE/DECISIONS.md`).
- Canon 3 §24 five-step rule-change ceremony (C3-R-083..C3-R-086).
- Canon 8 W8 the-floor-never-learns (C8-R-051..C8-R-054) — the floor moves only by ceremony, ceremony is itself a monitored tripwire. This proposal is filed in the open, on record, monitored.
- SO §3.3 seal-chain integrity R-1..R-6.

---

## §6 · What this proposal is deliberately not

- **Not a retirement.** The tests remain by name; their assertion shape re-scopes.
- **Not a threshold-loosening.** Bumping `_MAX_*_AGE_HOURS` from 72 to some larger value was explicitly rejected by the owner (Option B in the prior stop-and-report) and is not this proposal.
- **Not a rewrite of the mtafiti tools.** The five `tools/mtafiti_*.py` continue writing the same JSON shapes; they gain a `campaign_context` field per §3.3.
- **Not an amendment to canon.** This proposal reshapes tests, not canon. Any tension with canon halts the ceremony per Item-5 stop-and-report.
- **Not applicable to other invariants.** The re-scope pattern (steady-state presence+hash+LKG · age gate only while campaign open) is proposed for these FIVE tests only. Broader adoption is a separate proposal if surfaced.

---

## §7 · Landing path if owner counter-signs

1. Owner counter-sign (owner ruling banked in `STATE/DECISIONS.md`).
2. Countdown per §24 default class runs.
3. Main-agent authors:
   - `STATE/mtafiti_campaign_state.json` (initial content: `{"status": "closed", "closed_at_utc": "2026-09-18T~08:16Z", "prior_campaign": "CP-M11-GATE-RELEASE · GPU 72h discovery window"}`)
   - `tests/invariants/_mtafiti_staleness_helpers.py` (shared helper)
   - Amended 5 test files per §3.2 shape
4. Full `BASELINE_GUARD=1` sweep pre-seal (per new pre-seal standard folded into ORCH_BOOT §2).
5. §3.3 3-commit seal (Commit-A code on track-a for the test edits + helper module · Commit-B state on master · Commit-C fixup on master).
6. Byte-identical double-green byte-match banked; ratchet stays at 4826.

---

## §8 · If owner rejects or ignores past bridge horizon

If the ceremony has not landed and no bridge-B ruling comes by `2026-09-21T09:20Z`, main-agent surfaces a stop-and-report per SO §3 Item 5 (a bridge horizon passed without a decision is a rule-vs-rule tension of the T-a/T-b kind).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
