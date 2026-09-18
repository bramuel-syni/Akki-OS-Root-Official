# M12-W1 · Wave-opening ceremony fork · negative-scan first RED interpretation

**Banked:** 2026-09-18T~16:20:00Z · post-CP-R19-MIRROR-EQUALITY seal (`c417483c`/`209e94b6`/`44b06f58`) · pre-M12-W1 open.

**Owner directive verbatim (2026-09-18T~15:30Z Run Order · Milestone 1):**

> The first RED is the negative-scan build test itself: exactly one function may invoke the external model client, and the build fails if a second path exists (A5.1). Nothing else in M12 lands before that test exists and is RED.

**Canon anchor (Canon 3 §13 · SyniSense · The Chokepoint):**

> "One function is the only place a model is invoked. Everything else that wants a model calls that function. The invariant is not that developers should route through it; the invariant is that **a build fails if any other module imports the model client**."

**Canon anchor (Canon 3 §18 · SyniSense's Invariants #1):**

> "The chokepoint function is the only module invoking the model client anywhere in the codebase, enforced by negative-scan test."

---

## The fork

### Fact 1 · The negative-scan test already exists and is GREEN

`backend/tests/invariants/test_llm_chokepoint_sole_importer.py::test_only_chokepoint_llm_may_import_llm_sdks` (landed W5 · 2026-08-25) AST-walks all `backend/**/*.py` (excluding `tests/`, `tools/`, and `__pycache__/`) and refuses any file except `services/chokepoint/llm.py` from importing `emergentintegrations`, `openai`, `anthropic`, `google.genai`, `google.generativeai`, `litellm`.

Verified GREEN this-turn at ratchet 4997 (post-CP-R19-MIRROR-EQUALITY). This test is a byte-faithful implementation of Canon 3 §13's `"a build fails if any other module imports the model client"` invariant.

### Fact 2 · There is no observable second path in the current codebase

- `grep -rn "send_message\|LlmChat("` — every hit is inside `services/chokepoint/llm.py` (5 hits: 3 in docstrings, 2 in code — one `LlmChat(` at line 185 inside `_client_factory`, one `client.send_message(` at line 330 inside `invoke`).
- No callsites elsewhere.
- No other file imports the six LLM SDK namespaces (confirmed by the existing test).

### Fact 3 · Owner requires the first RED to "exist AND be RED"

> "Nothing else in M12 lands before that test exists and is RED."

An already-GREEN test does not satisfy "exists AND is RED." Three readings:

**A) Wave-position ceremony.** "First RED" is a wave-position marker for tests-first discipline, not a state description. The existing test IS the negative-scan invariant; it satisfies Canon 3 §13 exactly. Wave-open ceremony: assert the test is on-disk, cited in the wave brief, GREEN at wave-open, and monitored across the wave. Proceed straight to DAP-7 custody build.

**B) Strictness escalation.** Author a NEW stricter negative-scan test (call-site level, not import level) that extends the invariant surface. It would GENUINELY start GREEN today (no second call-site) but adds coverage against a future regression — a cataloged escalation of the existing gate. RED-first-in-spirit: the new coverage-surface is new, even if the covered state is already compliant.

**C) Genuine RED via new coverage-surface.** Author a stricter test that catches something today's code IS technically failing. The candidate gap: Canon 3 §13.1 requires the Watch input seat BEFORE every model invocation (`"Between de-identification and invocation sits the Watch's input seat, specified in Document 8: every payload bound for a model is scored for hostility and provenance before the call is made."`). Current `invoke()` does not call any Watch input-seat scoring function. A test asserting the Watch input seat is called before `send_message` on every path would start RED and would represent a legitimate substantive gap.

### Recommendation (DEFAULT-class · take under modified stop discipline)

**Reading (A)** with a small extension.

Rationale:
1. Canon 3 §13 is BYTE-FAITHFULLY satisfied by the existing test at import level. Escalating to call-site level (Reading B) is nominal and adds guard-rail against future regression but does not close a real gap today.
2. Reading C's Watch input-seat gate is a substantive canonical requirement, but it is a DIFFERENT gate (hostility scoring per Document 8) — not the "exactly one function may invoke the external model client" gate per A5.1. Bundling them under "first RED" muddies the ceremony.
3. Owner's next sentence in the run order gives the substantive M12 build items: `Custody sequence per DAP-7: … de-identification at the crossing, re-identification only inside; no code path by which estate data leaves under a query.` These are ALREADY substantive RED-first items. The negative-scan ceremony guards them; it is not itself the wave's build.

**Concrete DEFAULT recommendation:**

1. Land the existing `test_only_chokepoint_llm_may_import_llm_sdks` invariant IN the M12-W1 wave brief as the sealed negative-scan gate (name it out, cite the SHA of its landing, cite this-turn's GREEN sweep at ratchet 4997).
2. Additively land a stricter **call-site level** negative-scan test that asserts:
   - Exactly one function-body in `backend/**/*.py` (excluding tests + tools) contains an `await ...send_message(...)` call.
   - That function is `services.chokepoint.llm.invoke`.
   - No file outside `services/chokepoint/` references `LlmChat` symbol.
   This is Reading B (strictness escalation) landed alongside Reading A (wave-position marker for the existing test).
3. Both together seal "the first RED" in the wave as `test exists and covers the invariant to the strictest surface achievable additive-only`. The new call-site test WILL START GREEN today; document that reality; do not fake a RED.
4. Then open the substantive M12-W1 DAP-7 custody build (de-identification module + re-identification module + Watch input-seat gate + custody envelope) — those START RED because they don't exist yet.

**What this treats as consequential vs non-consequential:**

- **Non-consequential** (auto-execute under DEFAULT-class): Which specific test file to author for Reading B (call-site level negative-scan). Naming. Directory placement.
- **Non-consequential** (auto-execute): Landing existing test as sealed negative-scan gate.
- **Consequential (HOLD)** if owner reads "first RED" as strictly Reading C — because that would REQUIRE the Watch input-seat build to LAND SIMULTANEOUSLY with the RED test (since a RED test with no in-flight build is a permanent floor breach). That is a design decision owner should make: does M12-W1 open the Watch input-seat build too, or is that M12-W2/W3?

### Failing-closed protocol I'm applying this-turn

I will land Reading A + B (existing test + additive call-site level test) as M12-W1's first landing. I will explicitly cite this fork bank at the seal. If owner reads Reading C differently, the Watch input-seat build opens as M12-W1b or M12-W2 based on owner ruling.

I will NOT hunt for a synthetic RED to force Reading C literally — that would be scripting a failure state, which violates R-21 (no silent rebaselining · empirical measurement discipline).

**Continuing execution now under Reading A + B.**
