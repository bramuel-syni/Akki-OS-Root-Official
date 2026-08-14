# Phase-0 Commissioning Record · <UTC timestamp>

**Fill in and save under `phase0/commissioning_records/<utc>.md` — this is the ledgered record of Phase-0 acceptance.**

---

## Provisioning event

- **VM_HOST:** _(fill in)_
- **VM_USER:** _(fill in)_
- **Provisioning day (UTC):** _(YYYY-MM-DD)_
- **Two-week checkpoint deadline (UTC):** _(auto: provisioning day + 14 days)_
- **AISCA Rafay console operator:** _(name / handle)_
- **Estate operator (this pod egress):** `34.16.56.64/32`

## VM declaration (Actor.Declaration)

```json
{
  "actor_id": "infrastructure.vm.<host>",
  "actor_kind": "infrastructure",
  "objective": "Archive processing and speech-model training.",
  "capabilities": ["compute", "hss_storage", "gpu_training"],
  "risks": ["bulk_data_custody", "external_location"],
  "scope": ["archive.ingestion", "training.speech_kenyan"],
  "lawful_basis": "build_order_01_2026-08-14",
  "declared_at": "<UTC ts>",
  "expires_at": null
}
```

- **Ledgered as `Actor.Declaration` row id:** _(fill in from run_acceptance_via_seam.py output)_

## Acceptance checklist (Build Order 01 §6 verbatim)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | HSS mounted at ~30 TB | _(pass/fail)_ | (paste `df -B1G /mnt/hss` output) |
| 2 | HSS writable | _(pass/fail)_ | (test file path + first-write ts) |
| 3 | HSS write-test survives one deliberate restart | _(pass/fail)_ | (post-restart ls -la path) |
| 4 | `nvidia-smi` shows 4× H200 | _(pass/fail)_ | (paste nvidia-smi query output) |
| 5 | NVLink active | _(pass/fail)_ | (paste `nvidia-smi nvlink --status` head) |
| 6 | Ephemeral present, scratch-only marker | _(pass/fail)_ | (paste `df -B1G` of ephemeral) |
| 7 | Password auth confirmed dead via external probe | _(pass/fail)_ | (paste probe output showing `Permission denied (publickey)`) |

## Compute-seam commissioning

- **Preflight** (`ssh_preflight.py`): _(exit code + verdict)_
- **Acceptance run** (`run_acceptance_via_seam.py`): _(each of 6 commands with exit + ledger row id + failure_kind)_
- **All ledger rows referenced above are in the append-only chain:** _(link/hash)_

## Escalate-and-stop triggers hit? (Y/N)

- HSS absent or undersized: _N_
- NVLink absent: _N_
- Password auth still live: _N_
- Ephemeral persistence contradicted by restart test: _N_

**If any Y: stop; escalate to owner via secure channel; do not adapt.**

## Deliverable status

- [ ] All 7 acceptance checks green.
- [ ] VM_HOST allowlisted only for `34.16.56.64/32`.
- [ ] Private key at `SSH_PRIVATE_KEY_PATH` under named custody (chain-of-custody record: _fill in_).
- [ ] Two-week checkpoint pinned in `STATE/PINS.md`.
- [ ] This record signed off by owner (name / date).

## Signed off

- **Owner:** _(name)_ · _(UTC date)_
- **Ledger row for the commissioning event itself:** _(fill in)_
