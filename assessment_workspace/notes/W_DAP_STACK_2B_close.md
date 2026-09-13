READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_DAP_STACK_2B_close.md

**Wave.** W-DAP-STACK · Sub-wave 2B · Trust-domain + browse + pull-seam + API keys.
**Canon anchors.** DAP-Spec DAP-5, DAP-6, DAP-7, DAP-8 (partial), DAP-13.
**Owner authorisation.** Verbatim 2026-09-13: *"Gate 1 rescinded, Gate 2 - b, Gate 3 - in-block"*. Role-override rescission preserved from 2A close.
**Ratchet.** 3570 → 3578 (+8).
**Track-a commit.** `4ed29e0`.
**Seal.** `phase0/output_verified_seals/wdap_2b.seal.txt`.

---

## §A · Invariants added (8 new)

| Test | Anchor | What it enforces |
|---|---|---|
| B2-01 · module fabric present | DAP-5/6/7/13 | `services.dap.browse`, `services.dap.api_keys`, `services.dap.trust_boundary` importable; required symbols present |
| B2-02 · DAP-6 browse returns aggregates only | DAP-6 verbatim | Browse response carries only aggregate figures; no row-level records; no raw values leaked |
| B2-03 · DAP-6 browse is not a crossing | DAP-6 | Browse invocation MUST NOT emit a crossing receipt; distinct code path from DAP-Spec §7 crossing composition |
| B2-04 · DAP-5 trust-domain separation refuses cross-domain resolution | DAP-5 | A resolution request that spans two trust domains refuses without terms federation |
| B2-05 · DAP-7 pull-seam source never egresses | DAP-7 verbatim | Pull-seam contract: destination pulls from source under authenticated boundary; source-side never opens outbound connection to destination |
| B2-06 · DAP-13 API-key receipt carries no key material | DAP-13 verbatim | Issue receipt exposes fingerprint, principal_id, revocable flag; key material out-of-band only |
| B2-07 · DAP-13 API keys are per-principal | DAP-13 | Key issued to principal A cannot resolve as principal B; per-principal binding invariant |
| B2-08 · DAP-13 API-key revocation immediate | DAP-13 | Revoke is single-act; post-revoke resolution refuses without a grace window |

## §B · Mechanism landed

- `backend/services/dap/browse.py` (72 lines · DAP-6 aggregate-only browse + DAP-7 pull-seam scaffold).
- `backend/services/dap/api_keys.py` (77 lines · per-principal API-key kernel · revoke-single-act, never-transferable).
- `backend/services/dap/trust_boundary.py` (75 lines · DAP-5 trust-domain boundary primitive).
- `backend/services/dap/admission.py` extended (+93 lines · kwargs-form wrappers preserving 2A obj form; `get_party_principal()` lookup for api_keys; `reset_state` alias).
- `backend/tests/invariants/test_wdap_2b_browse_pull_seam_and_api_keys.py` (230 lines · 8 invariants).

## §C · Markers held (flip-forbidden)

- **R-C1**: `ControlledDeterminationBasis.CUSTODY_CLASS_FALLBACK` — carried forward from 2A. Rules-Service still not built (Doc-0 §8 dependency).
- **R-C2**: `MeteredEvent.au_3b_defensible=False` default — carried forward from 2A. Doc-0 G-8 (reliable time source) still open.

## §D · Discipline receipts

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T152500Z_wdap_2b_RED.log` | `fe79b7942cd5d7013a0159583a9c2304e00ed5aed867ed3b5ea5ff3e4e0909ac` |
| GREEN 1 | `phase0/drill_receipts/20260913T153000Z_wdap_2b_GREEN1.log` | `6816c22d5c33741869d644aaf642d1cc7758fe0a4018db7b5803b937c72ef522` |
| GREEN 2 | `phase0/drill_receipts/20260913T153200Z_wdap_2b_GREEN2.log` | `d9042d2bade9a8a36e185f806f4d84af0d65b00f34470007dd319f9bf3c4a6f9` |
| **Rider 1** pip freeze | `phase0/drill_receipts/20260913T153300Z_wdap_2b_PIPFREEZE.txt` | `7c45a54d1264b9098875fb92f16b01460dc7702bbb6decf03212d996ffd162b8` |
| **Rider 1** collect-only | `phase0/drill_receipts/20260913T153300Z_wdap_2b_COLLECTONLY.txt` | `8d6ce7fb5347315bea9cd7f35156f4e1285ed5f84312f0294b7b613993355381` |
| Seal | `phase0/output_verified_seals/wdap_2b.seal.txt` | — |
| Byte-match | 3578 passed / 1 skipped / 438 warnings — identical modulo wall-time | — |

## §E · Promises discharged

Per `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M1:
- **Full** — DAP-6 (browse aggregate boundary), DAP-7 (pull-seam contract), DAP-13 (per-principal API keys · revoke-single-act).
- **Partial** — DAP-5 (trust-domain primitive at kernel grade; federated resolution deferred), DAP-8 (crossing profile fields — schema wired in 2A, aggregate-egress hardening deferred to 2E metering).

## §F · Guardrails held

- Local commit only (`programme/track-a` HEAD `4ed29e0`). NEVER pushed.
- No egress. Radio T4 held.
- `testing_agent` BANNED. Terminal pytest only.
- Rider-1 discipline banked with the close.
- Rider-2 `ENV-DRIFT-2TESTS-20260913` remains tracked-open (no impact this wave).

## §G · State-side backfill note

This master-side close manifest was authored 2026-09-13 during 2D housekeeping,
after the track-a commit `4ed29e0` had already been made. No content in the
2B commit is altered by this backfill; only the state-side documentation is
now caught up to match the pattern established by W_DAP_STACK_2A_close.md.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
