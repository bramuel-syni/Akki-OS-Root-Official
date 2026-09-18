# M12-W1d · DAP-7 custody wire-in · design fork banked pre-open

**Banked:** 2026-09-18T~17:10:00Z · post-CP-M12-W1b seal (`0ccedd35`/`c3416bc5`/`132195be`) · pre-M12-W1d open.

**Owner directive (Run Order 2026-09-18T~15:30Z · Milestone 1):**

> "Custody sequence per DAP-7: the party's query enters, de-identification at the crossing, re-identification only inside; no code path by which estate data leaves under a query."

**Canon anchor (Canon 3 §13.1 · sequence):**

1. Provider selection
2. **De-identify** (inbound payload → placeholder tokens + per-request custody envelope)
3. **Watch input seat** (Document 8 · hostility + provenance scored before invoke)
4. **Invoke with metering**
5. **Re-identify** (output against envelope · unmatched token raises)
6. Grounding gate
7. Class-honesty check
8. Trust receipt

**Owner-noted invariants:**
- Envelope is per-request; does not outlive it (Canon 3 §14).
- Tenant-scoped entity resolution supplies the entities to recognise (never limited to what a general recogniser detects).

---

## The fork

Wiring de-identify + Watch input seat + re-identify into `services.chokepoint.llm.invoke()` is **substantively consequential**:

### Fact 1 · Signature-change surface

`invoke()` current signature (line 269 of `services/chokepoint/llm.py`):

```python
async def invoke(
    *, purpose: str, prompt: str, masking_tier: str, actor: str,
    model: str, provider: str, system_message: Optional[str] = None,
    session_id: Optional[str] = None,
) -> LLMResponse
```

**Missing:** `tenant_id` — required by `deidentify(content, *, tenant_id, purpose)` since tenant-scoped entity resolution is canonical (Canon 3 §14).

### Fact 2 · Nine downstream call-sites

- `services/chat/router.py:50` — 1 call
- `services/solva/reasoning.py` — 6 calls (lines 154, 263, 324, 518, 578, 658)
- `services/wizard/connect_llm_router.py:220` — 1 call (llm.connect_verify)
- `services/synisense/shield/llm_router.py:125` — 1 call (HARVESTED-BUT-DEAD; not on live path)

Live call-sites: 8. Legacy dead-code: 1.

### Fact 3 · Two shape questions

**Q1 · tenant_id source.** Where does the tenant_id come from at each call site?
- chat/router.py — request scope; per-request from HTTP context.
- solva/reasoning.py 6 sites — from the reasoning frame's `tenant_id` field.
- wizard/connect_llm_router.py `llm.connect_verify` — the verifier does NOT act under tenant custody (it verifies a connection against a candidate provider before any tenant data touches it). What tenant_id does the CONNECT_VERIFY carry? Possibly a synthetic `tenant_id="__connection_verify__"` that de-id treats as an empty entity catalogue.

**Q2 · Watch input seat.** Canon 3 §13.1 requires a Watch scoring gate BETWEEN de-identify and invoke. Does the Watch input seat already exist as a callable module?
- `services/watch/` package exists.
- Need to check if there's a `services.watch.input_seat.score(payload)` -> `WatchInputSeatVerdict` or similar.
- If it exists → wire it in. If not → first author it (this is the "Reading C" from M12-W1a fork; owner has this queued).

### Options

**Option A · Minimal wire-in (additive to invoke, fail-closed on missing tenant_id):**

* Add `tenant_id: Optional[str] = None` param with default `None`.
* At function head: `if tenant_id is None: raise ChokepointRefused("tenant_id_required_for_dap7_custody — refused before dispatch. Every crossing must run under a tenant custody envelope; a missing tenant_id is an unverifiable custody path (canon 3 §14).")`
* Wire de-identify + re-identify with the tenant_id.
* Callers: each of the 8 live call-sites gets a compile-time RED if tenant_id is not passed (via mypy) or a runtime RED at first execution.
* Migration: each caller updates its invoke() call to pass tenant_id in a subsequent seal.

**Pros:** Additive to signature (Optional-with-fail-closed). Preserves M12 stop condition #1 (no second path to model client — the de-id step IS the single custody sequence, not a bypass). Callers migrate at their own pace under RED-first per-caller cycles.

**Cons:** Between wire-in landing and last caller migration, invoke() paths without tenant_id fail-closed. Any code path currently reaching invoke() without a tenant_id becomes a hard refusal. This IS the canonical constraint — "no code path by which estate data leaves under a query" — but any latent call-site not updated at once regresses to refusing.

**Option B · Wire-in with explicit `dap7_bypass="reason"` escape hatch:**

* Same as A, but add `dap7_bypass: Optional[str] = None` for the `llm.connect_verify` purpose that legitimately has no tenant context.
* At function head: `if tenant_id is None and dap7_bypass is None: raise ChokepointRefused(...)`
* If `dap7_bypass` is set, skip de-id AND write a `dap7_bypass=<reason>` field into the crossing receipt.
* Only whitelisted bypass reasons allowed (e.g., `"llm.connect_verify"`).

**Pros:** Handles the legitimate connect-verify case cleanly.
**Cons:** Introduces a bypass surface. Owner may argue that ANY bypass path violates "no code path by which estate data leaves under a query" — but the counter is that connect-verify does NOT carry estate data (it's a canned probe).

**Option C · Full atomic wire with all 8 callers updated in one seal:**

* Modify invoke() signature: `tenant_id` becomes required positional-keyword arg.
* Update all 8 callers in the same commit (atomic).
* Single §3.3 seal covers invoke + all callers.

**Pros:** Clean semantic constraint (tenant_id always known at call). No transitional fail-closed period.
**Cons:** Very large surgical change (invoke + 8 call-sites + tests). Higher risk of breaking downstream tests. Not additive per SO §3.8 (touches multiple non-sealed but load-bearing modules).

### Recommendation (DEFAULT-class · take under modified stop discipline)

**Option B**. Rationale:

1. Preserves M12 stop condition #1 (chokepoint remains single seat; de-id is now IN the seat's sequence).
2. Additive to signature (Optional param + Optional bypass).
3. Handles `llm.connect_verify` cleanly (owner has explicitly named this purpose in W5 ruling; it is the ONLY legitimate no-tenant path).
4. Per-caller migration under separate RED-first cycles keeps blast radius small.
5. If Watch input seat module exists → wire in same seal. If not → add a stub `services.watch.input_seat.score(payload, tenant_id)` that returns `WatchInputSeatVerdict(admit=True, notes=[])` and mark it as M12-W1e for the actual scoring logic (Document 8 anchor).

**Consequential-adjacent element:** the `dap7_bypass="llm.connect_verify"` escape hatch IS an owner-visible design choice — this fork bank formalises it for owner disposition before wire-in.

### What to bank as unwritten backlog

- **M12-W1d** (this wave): wire deidentify + reidentify into `invoke()` per Option B (or A if owner overrides B) · fail-closed on missing tenant_id · Watch input seat stub if module absent · Watch scoring logic in later wave.
- **M12-W1e**: per-caller migration of the 8 live call-sites to pass tenant_id.
- **M12-W1f**: Watch input seat scoring logic (Document 8 hostility + provenance).
- **M12-W1g**: closed outbound network (extend allowlist strictness).
- **M12-W1h**: D-17 inner perimeter + D-16 local-first cascade.
- **M12-W1i**: TCB golden-input byte-identical tests (B.8).

### Estimated ratchet delta (M12-W1d Option B alone)

- 4-6 tests for wire behaviour (de-id called + re-id called + fail-closed on missing tenant_id + bypass honoured for connect_verify + estate data never appears in send_message prompt · unmatched token in response raises).
- ~10-30 tests as byproduct of updating existing chokepoint tests to pass tenant_id.
- Net estimated: +10 to +30 ratchet.

### Why not doing this-session

Context budget consumed by:
- CP-M10-CLOSE (3-commit seal + G5 slice 5).
- Owner rulings bank.
- CP-R19-MIRROR-EQUALITY (3-commit seal).
- CP-M12-W1a-NEG-SCAN-OPEN (3-commit seal + Reading C fork bank).
- CP-M12-W1b-SEC1-INTEGRITY (3-commit seal + ORCH_BOOT housekeeping fix).

Remaining context is insufficient to safely land a signature-change surgical wire across 9 files without risking downstream test breakage that I can't verify with confidence in a full sweep. Doing this poorly is a bigger risk than not doing it this-session.

**Awaiting owner disposition on Option A vs B vs C, and on the Watch input seat module status (Reading C from M12-W1a fork).**

---

## Combined M12 fork disposition table for owner

| Fork | Seal | Recommendation | Awaiting |
|---|---|---|---|
| M12-W1a Reading A/B/C first-RED interpretation | `cff65be3` sealed | Applied A+B (import + call-site levels) | Owner may want Reading C (Watch input seat) as W1a-c |
| M12-W1d wire-in Option A/B/C | not opened | Option B (fail-closed + bypass for connect_verify) | Owner may prefer A or C |
| M12-W1f Watch input seat scoring logic | not opened | Stub in W1d if absent · scoring in later wave | Owner ruling on Document 8 mapping |

Two natural stops for owner:
1. Take the M12-W1d Option B disposition, greenlight, resume next-session.
2. Override with different option/order.
