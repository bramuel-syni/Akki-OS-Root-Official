# CP-AIP-P2-VOICE-IDENTITY-AND-MUSIC-REGISTER · objective card (parked) · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §7 + §7.5 · Build Sequence P2.

**Status:** 🔒 **PARKED (Phase 2 · non-foreclosure only)** · never opened without explicit owner authorisation.

## Rationale for position (spec §15 verbatim)

> *"P2 · Voice identity rendering; music register — Phase 2. Non-foreclosure is guaranteed by item 1 and §7.5."*

## Non-foreclosure scope (this is what P2 REQUIRES NOW · not a build)

**§7.5 verbatim:**

> *"Rendering requires a synthesis stack, which is a separate build from recognition. What this specification requires now is non-foreclosure: the identity specification (attribute schema, distance method, certificate format) is defined, and §4.4's ingestion capture ensures the substrate exists when rendering is built."*

Non-foreclosure has THREE components, all of which land structurally as part of CP-AIP-1..10 without any P2 code:

1. **Identity attribute schema defined** — §7.4 verbatim four-component identity table (acoustic identity, speech character, interaction character, versioning). Contract `contracts/voice_identity_v0.py` can land at CP-AIP-3 or CP-AIP-5 additively — schema-only, no synthesis code.
2. **Distance method defined** — §7.2 verbatim distance-from-every-corpus-speaker gate + threshold + verification method recording. Function shape `speaker_distance_gate(constructed_id, corpus) -> {distance, method, threshold}` — schema-only, no rendering.
3. **Certificate format defined** — §7.3 verbatim certificate carrier (method, threshold, corpus_version, "provably derived from no individual"). Contract `contracts/voice_identity_certificate_v0.py` — schema-only, first-class sellable artifact shape.
4. **Substrate capture at §4.4** — pitch statistics, energy contours, duration patterns per segment · lands at CP-AIP-1 (§4.4).

## What P2 will build LATER (never in this-run · never without owner authorisation)

- Synthesis stack (rendering).
- Actual voice-identity construction (§7.1 inherit-learned + synthesize-organic).
- Live distance-gate scoring against every corpus speaker.
- Music register (Phase 2 · undefined scope at v1.0).

## Ceremony change (§7.4 versioning)

> *"Changing one is a ceremony with the standard waiting period, because audience recognition accrues to the voice and recognition is the asset. Identities never drift."*

When P2 opens, changing an identity is a ceremony — waiting period, countersignature, owner-approved. Identity versioning contract lands at CP-AIP-3 or CP-AIP-5 (whichever admits the register write path).

## Ledger check

**P2 is PARKED.** No seal-time ledger check line applies until owner authorises P2 open.

**Non-foreclosure guaranteed by:**

- CP-AIP-1 §4.4 substrate capture.
- CP-AIP-3 §6 register write-path custody boundary (identity attribute schema).
- CP-AIP-5 §5.3 clustering (identity components inherit from clusters).

**Additive-only §3.8 · parked-with-substrate-guarantee.**
