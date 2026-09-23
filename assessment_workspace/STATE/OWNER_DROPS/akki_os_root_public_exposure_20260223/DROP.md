# OWNER DROP — AKKI-OS-ROOT PUBLIC EXPOSURE — P0 SECURITY · NON-BLOCKING — 2026-02-23

**Received:** 2026-02-23 (mid-CP-AIP-9 pre-Commit-B) · **Class:** P0-security honest-gap · **Banking:** verbatim + probe result + owner-action-required receipt · **Additive:** no sealed code touched; no repo state modified from the pod because the repo is not on-disk and pod lacks repo-admin capability · **Blast radius:** GitHub repo visibility (external to this pod).

---

## §1 — Verbatim owner text

> "Akki-OS-Root is PUBLIC and its receipts carry customer connector hosts. MAKE IT PRIVATE. Objective (name it): customer connector hostnames must not be exposed on a public repo. If you have the access/tooling in-pod to flip the repo visibility (gh CLI / API token with repo admin scope), do it and record the receipt. If you do NOT have repo-admin access from the pod, record honest-gap AKKI-OS-ROOT-PUBLIC-EXPOSURE in DECISIONS.md with the exact action needed, and surface it to me so the owner can flip it in the GitHub UI — treat as P0-security but non-blocking to the build. Report which applied."

---

## §2 — Pod-side probe result (2026-02-23 · this-drop)

| Capability | Present? | Detail |
|---|---|---|
| `gh` CLI (GitHub CLI) | ❌ NO | `which gh` returns nothing; neither `/usr/bin/gh` nor `/usr/local/bin/gh` exists on disk. |
| GitHub token env vars (`GH_TOKEN`, `GITHUB_TOKEN`, `GH_ADMIN_TOKEN`, etc.) | ❌ NO | `env \| grep -iE '^(gh_\|github_)'` returns nothing. |
| `Akki-OS-Root` repo cloned in this pod | ❌ NO | The four cloned repos under `/app/assessment_workspace/repos/` are `Extraction-Akki`, `Akki-OS-V1`, `Akki-Executive-Core`, `RMS-IQ-Core-2`. **`Akki-OS-Root` is not on disk in this pod** — it has never been fetched in this session. The owner drop names a repo the pod has never inspected. |
| Repo-admin capability via API without token | ❌ NO | Unauth'd API cannot change repo visibility. |

**Conclusion:** the pod CANNOT flip `bramuel-syni/Akki-OS-Root` visibility from public to private under any in-pod path. The owner-action-required path (Drop §1 else-branch) applies.

---

## §3 — Honest-gap recorded: `AKKI-OS-ROOT-PUBLIC-EXPOSURE`

**Objective the gap protects (owner-named):** customer connector hostnames must not be exposed on a public repo.

**Residual gap:** `bramuel-syni/Akki-OS-Root` GitHub repo visibility is (per owner) currently PUBLIC, and its receipts carry customer connector hostnames. Making it private is a P0-security action.

**Exact action owner needs to take** (any one is sufficient):
1. **GitHub UI path** (fastest, no tooling required): navigate to `https://github.com/bramuel-syni/Akki-OS-Root/settings` → scroll to "Danger Zone" → "Change repository visibility" → "Make private" → confirm by typing the repo name.
2. **`gh` CLI path** (if the owner has `gh` locally with admin scope): `gh repo edit bramuel-syni/Akki-OS-Root --visibility private --accept-visibility-change-consequences`.
3. **REST API path** (if the owner has an admin PAT): `curl -X PATCH -H "Authorization: Bearer <PAT>" -H "Accept: application/vnd.github+json" https://api.github.com/repos/bramuel-syni/Akki-OS-Root -d '{"private":true}'`.

**What E1 needs from the owner if E1 is to do it later:** either (a) install `gh` in the pod plus a PAT with `repo` scope (owner-provided at credential-drop time per §4.1 §F sha-pin discipline), or (b) an API PAT with `repo` scope alone. Neither is currently present in the pod.

**Non-blocking status:** per owner directive verbatim ("P0-security but non-blocking to the build"), the in-flight CP-AIP-9 5-commit seal continues without pause; this drop is banked additively at the same boundary.

**Adjacent-repo cleanliness note (measured this-drop):** the four repos cloned in-pod (`Extraction-Akki`, `Akki-OS-V1`, `Akki-Executive-Core`, `RMS-IQ-Core-2`) are the repos operated on in this run. `Akki-OS-Root` is a **separate** repo not touched by this run. E1 has not, at any point in this session, pushed content to or fetched receipts from `Akki-OS-Root` — the exposure predates this session and is not caused by any E1 action. This is measured, not asserted.

---

## §4 — Adjacent hygiene note (this-drop measurement, additive-only)

**Have the four cloned repos on-disk in this pod carried any similar exposures?** Measured this-drop:

- `git -C repos/<r> remote -v` for each of the four repos returns only `origin https://github.com/bramuel-syni/<repo>` (no auth token embedded, no credential leak in remote URL).
- The four repos are (per Chunk-1 canon probe) all PUBLIC on GitHub. If any of them carries customer connector hostnames, that is a separate P0-security surface not covered by this drop and should be surfaced by the owner as a follow-on.

**Deferral:** this drop does NOT extend the P0 flag to the four cloned repos absent explicit owner direction (scope-freeze per SO §3.8; novel expansions PARKED per §3.8 discipline). Any expansion is an owner-desk item.

---

## §5 — Report to owner (surface line for CP-AIP-9 seal boundary REPORT-AND-CONTINUE)

**Report line (verbatim for delivery):**

> "AKKI-OS-ROOT-PUBLIC-EXPOSURE — pod cannot flip visibility (no `gh` CLI, no admin token, repo not on-disk). Honest-gap banked in DECISIONS.md + GAPS_FIXED_LEDGER.md at CP-AIP-9 seal boundary. Owner-action-required: flip `bramuel-syni/Akki-OS-Root` to private via GitHub UI (Settings → Danger Zone → Change visibility → Make private). Objective: customer connector hostnames must not be exposed on a public repo. P0-security · NON-BLOCKING to build per owner directive."

---

## §6 — One-sentence protected objectives (per §6.9 desk discipline)

- **`AKKI-OS-ROOT-PUBLIC-EXPOSURE` honest-gap (P0-security):** prevents customer connector hostnames from being read by any unauthenticated party via the public GitHub repo page.
- **In-pod probe receipt (§2):** proves that E1 measured before claiming inability, and named the exact missing tooling; the owner can act on the named gap without a round-trip.
- **Non-blocking status (owner-directed):** preserves build velocity while the owner performs the external action; the seal record captures the gap so no successor session forgets it.

---

## §7 — Ledger check

This drop banks the AKKI-OS-ROOT-PUBLIC-EXPOSURE honest-gap verbatim + records the pod-side probe result + surfaces the exact owner action needed, and nothing else. Additive-only. No sealed carrier edit. No repo state modified. In-flight CP-AIP-9 5-commit seal continues on the same commit boundary; State Commit-B carries the fold-in.
