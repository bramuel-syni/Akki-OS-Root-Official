# RULING_LEDGER.md — owner rulings ledger (STEP 3 close, owner directive 2026-09-08T~06:15Z)

**Created:** 2026-09-09
**Owner directives banked:** 2026-09-08T~06:15Z (STEP 3) · 2026-09-09T~11:40Z (proceed straight through)
**Ratchet floor at creation:** 3017

## Purpose

Every owner ruling banked verbatim in `STATE/DECISIONS.md` gets its human-readable
status row here. This ledger is the source of truth for "what's ratified, what's
default, what's coupled, what's still owner-open" — mirrored from the DECISIONS
verbatim bank without paraphrasing the ruling itself.

Categories:
- **RATIFIED** — owner explicitly approved the proposed value; binding immediately.
- **DEFAULT** — owner set a working value with `DEFAULT-class · revisable on evidence` posture; wired now, may change on later ruling.
- **COUPLED** — must be ruled together with a named companion; solo ruling forbidden.
- **OPEN** — genuinely awaiting owner input; **not** an ambiguity reflected back — a concrete decision the owner has said he wants to make himself.

---

## RATIFIED (5)

| # | Ruling | Owner text (verbatim from DECISIONS.md 2026-09-08T~06:15Z) |
|--:|---|---|
| 1 | Rules-Service **R-4** taxonomy | Ratified as proposed. |
| 2 | DAP **R-1** controlled-unit definition | Ratified as proposed. |
| 3 | Agent-Containment **R-1** capability-ceiling list | Ratified as proposed (the four ceilings: no self-replication, no unauthorised resource acquisition, no unauthorised credential escalation, no self-access to oversight). |
| 4 | Rules-Service **R-3** witness | Same witness the Watch already uses (C3). |
| 5 | Agent-Containment **R-2** scope-ratifying authority | Syni.ai for early deployments. |

## DEFAULT (9 — DEFAULT-class, revisable-on-evidence)

| # | Ruling | Value (verbatim) | Wired at |
|--:|---|---|---|
| 1 | Rules-Service **R-1** countdown | 48h system-ordinary / 7 days system-TCB | `backend/services/rulings/default_class_constants.py` `RULES_SERVICE_COUNTDOWN_SYSTEM_ORDINARY_HOURS`, `_SYSTEM_TCB_DAYS` |
| 2 | DAP **R-4** API-key lifetime | 90-day rotation | `backend/services/rulings/default_class_constants.py` `DAP_API_KEY_LIFETIME_DAYS` |
| 3 | DAP **R-5** AI labs taxonomy | AI labs get their own external-party taxonomy entry | Taxonomy allowlist (existing) |
| 4 | Security **R-10** recommendation window | 24h | `backend/services/rulings/default_class_constants.py` `SECURITY_RECOMMENDATION_WINDOW_HOURS` |
| 5 | Security **R-8** | Baseline-period approach | `backend/services/rulings/default_class_constants.py` `SECURITY_R8_APPROACH = "baseline_period"` |
| 6 | Security **R-9** | Baseline-period approach | `backend/services/rulings/default_class_constants.py` `SECURITY_R9_APPROACH = "baseline_period"` |
| 7 | Security **R-11** | Baseline-period approach | `backend/services/rulings/default_class_constants.py` `SECURITY_R11_APPROACH = "baseline_period"` |
| 8 | Agent-Containment **R-3** sample rate / observation window | Baseline-period approach | `backend/services/rulings/default_class_constants.py` `AC_R3_APPROACH = "baseline_period"` |
| 9 | Pruning **R-12** | Re-derivation is default; recall requires explicit case-by-case owner sign-off | `backend/services/rulings/default_class_constants.py` `PRUNING_R12_DEFAULT = "re_derivation"` |

## COUPLED (1)

| # | Ruling | Coupling clause (verbatim) |
|--:|---|---|
| 1 | DAP **R-3** per-party ceilings | MUST NOT be ruled alone — allocation against Security **R-7** estate release budget; rule together. |

## OPEN (4 — genuine owner decisions)

| # | Ruling | What owner has explicitly reserved for himself |
|--:|---|---|
| 1 | Security **R-7** | Estate release budget number |
| 2 | DAP **R-6** | Pricing model |
| 3 | WPW **R-2** | External-release signatory |
| 4 | DAP named approving authority | Person/role identity |

---

## Rollup

| Class | Count |
|---|--:|
| RATIFIED | 5 |
| DEFAULT (wired tests-first) | 9 |
| COUPLED (blocked until companion) | 1 |
| OPEN (owner-reserved) | 4 |
| **Total tracked** | **19** |

## Rule (banked)

DEFAULT-class values are **wired into `backend/services/rulings/default_class_constants.py`
tests-first**: every value in that module is frozen by an invariant test that
docstring-quotes the owner ruling verbatim. If the owner overrides a DEFAULT
later, the invariant is amended in the same commit that flips the value. A
DEFAULT value is never silently changed.

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
