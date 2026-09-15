READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# SEC INCIDENT · JUMP root credential leak to transcript · 2026-09-15T22:29:35Z

**Banked at UTC:** 2026-09-15T22:29:35Z.
**Receipt:** `phase0/security_incidents/sec_incident_jump_cred_leak_20260915T222935Z.json`.
**Severity:** HIGH.
**Category:** credential_leak_to_stdout.

---

## §A · What happened

While preparing to fire Boundary Probe #54 at the CP-M6-6-3 seal, I attempted to view the JUMP-server CSV to confirm the target endpoint coordinates. My redaction filter was flawed:

```
head -5 /app/backend/estate_keys/bastion/jump_server_radio_system.csv \
  | sed 's/,.*/,<REDACTED>/'
```

The CSV file's schema places the sensitive values in column-0 (left of the first comma) — this matches `tools/step3_reachability_probe.py::load_jump()` which reads `rows[i][0]` to extract the IP, user, and password. My sed pattern masked only substrings *right* of the first comma. The cleartext JUMP `root` password rendered in the agent-tool STDOUT of that bash call.

## §B · What did NOT happen

- The cleartext value was not written to any receipt file on disk.
- The cleartext value was not written to any commit message.
- The cleartext value was not written to any log file under `/var/log/`, `phase0/drill_receipts/`, or `phase0/*_receipts/`.
- No downstream service consumed the value; no probe was actually fired against JUMP with the leaked value.

The leak is bounded to the agent-tool STDOUT captured in the current session's transcript.

## §C · Root cause

Position-redaction hard-lock exists in the guard-module layer of the production code, but does NOT apply to ad-hoc bash-shell reads of the credential storage file from within the agent's tool surface. The redaction responsibility for such reads sits with the operator writing the command. I authored a bad redaction pattern for a column-0 CSV.

## §D · Immediate containment (already done this turn)

1. Halted the probe #54 firing sequence at the point of leak.
2. Halted the CP-M6-6-4 walk that was queued next.
3. Banked this note + the JSON receipt on disk.
4. Committed the incident to `master` state repo (see commit that lands with this note).
5. Refused any further command in this session that would re-read column-0 of the JUMP CSV before rotation.

## §E · Owner-desk actions requested

1. **Rotate the JUMP root password** at `159.138.173.250` via the same admin desk that opened the CD/visitors SGs on 2026-09-15. Re-issue the new value under `/app/backend/estate_keys/bastion/jump_server_radio_system.csv` at mode `0600`.
2. **Ratify this incident** in `STATE/DECISIONS.md` at your next turn.
3. **Decide** whether to strengthen the redaction discipline. Two candidate hardening options:
   - **Option 1** (procedural): Add a §E clause to `STANDING_ORDERS.md` requiring that all direct reads of credential-carrying CSV/JSON files go through a helper (`tools/read_credential_metadata.py`) that yields only path + sha256 + size + non-secret metadata, never column-0 values.
   - **Option 2** (mechanical): Move column-0 values into an encrypted-at-rest store (e.g., an age-encrypted file with the key living in a separate protected mode-0400 file). Requires ops work outside the current thin-kernel discipline.

## §F · Relation to prior SEC ledger

- `SEC-2026-09-15-05` (rotation already OWNER-DESK per `ADMIN_BINDS_20260915.md` §D #6) was already outstanding for a different reason. This incident is a *distinct event* — it increases urgency but is not a duplicate.
- No prior credential leak has been banked in `phase0/security_incidents/` during this session's shift; this is the first entry there.

## §G · Guardrail state after incident

| Item | Status |
|---|---|
| CP-M6-6-3 seal | **COMPLETE** · Commit A track-a `75447ac` · Commit B master `ea823aa3` · Commit C master `c1ed5bc6` · ratchet 4274 |
| Boundary probe #54 | **NOT FIRED** · halted pending owner ratification of this incident |
| CP-M6-6-4 walk | **NOT STARTED** · halted pending owner ratification of this incident |
| Ratchet floor | 4274 (unchanged) |
| Position-redaction hard-lock (production code) | Unchanged (this leak was operator-side, not guard-module-side) |

## §H · What I will do next in the same session

Nothing that touches credentials or fires the probe.  Awaiting owner ratification + rotation.  Meanwhile:

- I will **not** attempt any inline probe firing.
- I will **not** open the JUMP CSV again via any command that would print column-0.
- If the owner directs me to proceed with CP-M6-6-4 as agnostic of probe #54 (the CP does not depend on the probe result), I will resume the M6 §15 walk with a NOTE-SKIPPED entry for probe #54 that references this receipt.
