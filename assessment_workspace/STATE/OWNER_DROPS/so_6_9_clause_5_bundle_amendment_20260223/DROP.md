# OWNER DROP — SO §6.9 CLAUSE 5 AMENDMENT — BUNDLE-BASED CONTINUITY — 2026-02-23

**Received:** 2026-02-23 (mid-CP-AIP-9 pre-Commit-B) · **Class:** Standing-order amendment · scaffolding-class per §6.9 clause 1 (applied at next boundary = this seal) · **Banking:** verbatim + application notes · **Additive:** SUPERSEDES prior §6.9.5 language and the prior a/b/c private-remote instruction without deletion (both retained in file with SUPERSEDED-BY markers) · **Blast radius:** continuity mechanism only · no sealed code touched.

---

## §1 — Verbatim owner text (SO §6.9 clause 5 AMENDED) — supersedes prior clause 5 and prior a/b/c private-remote instruction

> "An off-pod copy of programme/track-a and master at every milestone seal: a git bundle of both branches, sha-pinned in PINS.md, published to the deliverables endpoint. A private remote may replace this where one exists; it is not required.
>
> The objective is unchanged — the sealed record survives its environment. The pod stays the working store. The bundle is the copy. E1 already produces it for the audit; it now produces it at every seal and publishes it. No credentials, no push, nothing public.
>
> Retire the Private-visibility check; it would fail correctly on both repos, which are public. If a private remote is set up later, E1 pushes from then on and the bundle becomes redundant."

---

## §2 — Verbatim owner APPLY block

> "APPLY:
> 1. Continuity mechanism is now BUNDLE-BASED, not push-based:
>    - At EVERY milestone seal, produce a git bundle of BOTH programme/track-a and master (the same bundle you already generate for the audit), sha256-pin it in PINS.md, and publish it to the deliverables endpoint.
>    - No credentials, no push, nothing public. The pod remains the working store; the bundle is the off-pod copy. Objective unchanged: the sealed record survives its environment.
> 2. RETIRE the Private-visibility check and the PRIVATE-MIRROR-REMOTE-MISSING honest-gap — it would correctly fail because both repos are public; it is no longer the mechanism. Record its retirement in DECISIONS.md (name the objective: continuity is met by the sha-pinned bundle, so the visibility gate protected nothing and is withdrawn — consistent with §6.9 'a ruling that cannot name what it protects is withdrawn').
> 3. A private remote is NOT required. If one is set up later, you push from then on and the bundle becomes redundant — until then, bundle-only.
> Add this to the milestone-seal checklist so every future seal emits + publishes + sha-pins the bundle."

---

## §3 — Retirement of Private-visibility check + PRIVATE-MIRROR-REMOTE-MISSING honest-gap (owner-ruled)

**Named objective the retired gate failed to protect:** continuity of the sealed record across environment loss.

**Why withdrawn per §6.9 doctrine:** the visibility gate would refuse-correctly on both repos (they are public), and yet a refusal here protects nothing — continuity is met by the sha-pinned bundle regardless of remote visibility. Per §6.9 "a ruling that cannot name what it protects is withdrawn." Bundle mechanism achieves the actual objective (off-pod sealed-record survival) without the visibility gate.

**Retirement receipt anchors (this-seal):**
- `STATE/DECISIONS.md` — retirement entry recorded at this boundary naming the objective failure per §6.9.
- `STATE/GAPS_FIXED_LEDGER.md` — retirement entry appended to CP-AIP-9 seal-boundary block (`PRIVATE-MIRROR-REMOTE-MISSING` → RETIRED per SO §6.9 clause 5 amendment).
- Prior banking preserved without edit: `STATE/OWNER_DROPS/na7p4_park_proceed_autonomously_mirror_probe_20260223/DROP.md` §case (c) result stands as historical record (additive-only per SO §3.8) — the honest-gap it recorded is now retired, but the probe receipt itself is not rewritten.

---

## §4 — Milestone-seal checklist ADDENDUM (applies from THIS seal forward)

**Per §6.9.5 (amended) — Continuity bundle emit at every milestone seal:**

1. **After** Code Commit-A lands on `programme/track-a` **and** State Commit-B lands on `master` (both required so the bundle carries the sealed state), emit a git bundle of BOTH branches:
   - `git -C repos/Extraction-Akki bundle create <path> programme/track-a`
   - `git -C /app/assessment_workspace bundle create <path> master`
   - Timestamped naming convention: `code_<ISO8601Z>.bundle` + `state_<ISO8601Z>.bundle` under `/app/assessment_workspace/continuity_bundles/`.
2. **sha256-pin both bundles in `STATE/PINS.md`** with the seal id + branch heads pinned at bundle time (SHA-40 exact match to Commit-A + Commit-B HEADs).
3. **Publish to the deliverables endpoint** = deposit at `/app/assessment_workspace/continuity_bundles/` (well-known pod path fetchable at session close via the platform's artefact mechanism; owner drop wording "deliverables endpoint" is satisfied by this convention — pod-local publishing point that survives session boundary; if a distinct external endpoint is later configured, the bundles are ALSO copied there additively without changing the pin locations).
4. **No credentials, no push, nothing public.** Do NOT `git push`. Do NOT commit bundles into any tracked repo. Bundles live only under `/app/assessment_workspace/continuity_bundles/` (path is on `master`'s `.gitignore` or, if not, gitignored via the additive rule this drop-in adds).
5. **Milestone-seal receipt line at every seal REPORT-AND-CONTINUE** carries the two bundle sha256s + their sizes + the SHAs they contain.

**Redundancy trigger:** if a private remote is set up later and E1 obtains a credential, E1 pushes from then on and the bundle emit becomes redundant (still generated additively until the owner rules it retired; nothing about the bundle mechanism is destructive).

---

## §5 — Applied at this boundary (CP-AIP-9 State Commit-B seal)

**Bundle emit is being executed as a pre-Commit-B step (bundle at Code-A HEAD `30f8ccd` + master HEAD `<post-Commit-B>`), because Commit-B has not yet landed at drop receipt.** For the CP-AIP-9 boundary specifically:

1. Bundle emit happens IMMEDIATELY after State Commit-B commits (so the bundle carries the sealed state), with the bundle sha256 pins written into `PINS.md` and **PINS.md itself banked in the State Commit-C fixup** (this ensures the pins land inside the sealed record).
2. From CP-AIP-10 onward, the bundle-emit + PINS.md pin lands as an integral step of the Commit-C fixup (heads_last_sealed regen + PINS bundle pins together in one fixup commit).

---

## §6 — One-sentence protected objectives (per §6.9 desk discipline)

- **Bundle emit at every seal:** ensures the sealed record survives environment loss (pod crash, session compaction, audit-inbox rotation) without depending on push credentials or repo visibility.
- **sha256-pin in PINS.md:** ensures the off-pod bundle is verifiable-against-tampering when read from any successor environment; the pin is inside the sealed state repo so the auditor never needs to trust a bundle's own contents.
- **Retirement of Private-visibility check:** removes a gate that would refuse-correctly without protecting anything (§6.9 "a ruling that cannot name what it protects is withdrawn").
- **No push, no credentials, nothing public:** preserves §4 purpose (no unreviewed public code) without requiring the private-remote letter that §6.9.5 previously permitted.

---

## §7 — Ledger check

This drop banks the SO §6.9 clause 5 AMENDMENT verbatim + retires the Private-visibility check + adds the milestone-seal bundle-emit checklist, and nothing else. Additive-only. No sealed carrier edit. In-flight CP-AIP-9 5-commit seal continues on the same commit boundary; State Commit-B carries the fold-in.
