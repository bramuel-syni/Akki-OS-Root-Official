READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# CP-P3-CP1 · M9 · Platform-layer estate_entity · seal note · 2026-09-17T~05:20Z

**Track-a HEAD:** `1fcc34bf67bb74c070c626ea95a96535a56bcaa2`. **Ratchet:** 4516 → **4525** (+9). **First CP of P3.**

## Anchor
§10 verbatim: `estate (id, tenant_id, name, tier, location_summary, estate_contact, agent_id, sandbox_safe)`. §5.1 tier vocabulary: `connected` OR `hosted`. §4.4 M-H-8: *"Sandbox attaches only to sandbox_safe=true connectors + sandbox allocation."*

## Mechanism
`services/platform_control_plane/estate_entity.py` · `EstateEntity` frozen 8-carrier (7 str + 1 bool `sandbox_safe`) · `ESTATE_ENTITY_FIELDS` tuple · `ESTATE_TIER_VALUES = ("connected", "hosted")` OPEN str · preventive-charter `assert_estate_tier_valid(*, estate)` refuses `UnknownEstateTierRefused` when tier not in the 2-set (case-sensitive) · 2 refusal classes · COUNTS-only messages · sandbox_safe rule: bool shape frozen at carrier; runtime rule composed by downstream sandbox-attach CP.

## Invariants (9)
1. Module fabric + `__all__`.
2. `EstateEntity` frozen 8-field exact-order (7 str + 1 bool).
3. `ESTATE_ENTITY_FIELDS` matches dataclass.
4. `ESTATE_TIER_VALUES == ("connected", "hosted")`.
5. Refusal hierarchy.
6. Refuses on unknown tier (incl. empty + case-mismatch).
7. Admits both verbatim tier values.
8. `sandbox_safe` bool shape carrier rule.
9. Verbatim anchor + 21-token grep-negative + import-negative.

## Double-green under `BASELINE_GUARD=1`
GREEN 1 `4525 / 1 / 0 in 125.23s` + GREEN 2 `4525 / 1 / 0 in 125.27s`.

## §3.3
- A `1fcc34bf67bb74c070c626ea95a96535a56bcaa2` ✅.
- B `d27d2a2289c6e925880864c506a3e3e21e22984e` ✅.
- C this-turn (fixup).

## GPU util
Elapsed **25.47 h** · remaining **46.53 h**.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
