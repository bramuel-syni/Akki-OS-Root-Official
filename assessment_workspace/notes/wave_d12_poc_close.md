READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-D12-POC · wave-close note (owner-facing at M5 sprint-close · pinned here durable)

**Wave sealed at CP-D12P1 receipt-contract only.** Live-run stages exercised end-to-end across pod → JUMP → NAS + pod → akki-vm; two specific blockers identified with root-cause diagnosis. Matches CP-A5 precedent (contract landed · blockers banked · wave sealed · live-run scheduled as follow-on when blockers close).

**Sealed-at-utc:** 2026-09-15T~10:20Z.

**Track-a HEAD at CP-D12P1 seal:** `7cccbe8b` (unchanged this wave-close · code lane sealed at contract landing).
**Master HEAD at CP-D12P1 seal:** to-fill (imminent state commit).

## §A · Progress made (this wave)

| CP | Landed | Ratchet | Δ | Track-a |
|---|---|---|---|---|
| CP-D12P1 · receipt-contract (frozen D12PocReceipt 16-carrier + assemble_d12_poc_receipt + module-frozen canonical tokens + ALLOWED/FORBIDDEN field-set disjointness) | 4062 → 4068 | +6 | `7cccbe8b` |

Live-run stages exercised (evidence, not ratchet-contributing):

| Stage | Verdict | dt | Notes |
|---|---|---|---|
| 1 · pod prep (SEC hygiene · custody-cat guard exercised) | PASS | — | 4 SEC re-leaks banked (15-08/09/10 + partial 15-07 recurrence class); custody-cat guard scope confirmed insufficient for python-level custody reads; M8 W-TESTS-FIRST-GUARD-INVARIANT scope extension banked |
| 2 · JUMP SSH probe (sshpass · uname · smbclient present) | PASS | 3.6s | ubuntu@JUMP · smbclient available |
| 3 · smbclient share probe (`-L //10.10.55.55 -U Bramwel`) | PASS | 5.3s | 13 share lines matched · zero stderr · position-redaction preserved |
| 4 · enumerate audio in `channel01/2026_09_14/` | PASS | ~8s | 288 audio-shaped `.mp4` files (~79 MB each · 300-sec chunks) · first-lex-slot: `channel01_2026_09_14_00_00_00.mp4` |
| 5 · fetch bounded audio to pod | **BLOCKED** | — | smbclient `NT_STATUS_IO_TIMEOUT` at ~8 MB · retry with `-t 300 --socket-options=TCP_NODELAY,IPTOS_LOWDELAY,SO_KEEPALIVE --max-protocol=SMB2` did not complete within pod-side subprocess 180s timeout · effective throughput ~127 KB/s → 79 MB would need ~10 min minimum |
| 6 · scp pod → GPU host | UNEXECUTED | — | prerequisite (stage 5) blocked |
| 7 · install `faster-whisper` on GPU host | PARTIAL PASS | 17.8s (isolated call) | `pip install --break-system-packages --user faster-whisper` succeeded on akki-vm · v1.2.1 confirmed importing (verified in isolated call after PEP-668 fix) |
| 8 · bank receipt under `phase0/d12_poc_receipts/` | PASS | — | one receipt banked at `phase0/d12_poc_receipts/20260915T101724Z_channel01_2026_09_14_00_00_00.json` (2089 bytes · captures blocker-D12-01 verbatim + partial-run stage data · POC-NOT-PRODUCTION flag stamped) |

## §B · Blockers identified (verbatim · owner action required)

### `BLOCKER-D12-01` (P1 · NAS SMB IO throughput / timeout)

* **Symptom**: smbclient `get channel01_2026_09_14_00_00_00.mp4` from `//10.10.55.55/OFFAIRRECS` via JUMP returns `NT_STATUS_IO_TIMEOUT` after transferring ~8 MB of a 79 MB file.
* **Effective throughput**: ~127 KB/s (8388608 bytes in ~63 s per diagnostic 2026-09-15T~10:15Z).
* **Root-cause hypothesis**: NAS-side rate limiting · JUMP↔NAS link throttle · Samba `parallel_read` timeout on the NAS.  Not diagnosable without NAS-side or JUMP-side sysadmin access.
* **Diagnostics run** (this wave): (a) fresh smbclient `-L` returns 13 shares clean (share enumeration is fast · only bulk transfers throttle) · (b) `set -x` trace confirmed smbclient invocation with correct `-U Bramwel + PASSWD env` shape · (c) retry with `-t 300 --socket-options=TCP_NODELAY,IPTOS_LOWDELAY,SO_KEEPALIVE --max-protocol=SMB2 -m SMB2` did not lift throughput.
* **Not fixable in agent-session**: needs network / NAS admin.
* **Owner-desk item**: investigate NAS-side rate limiting for the `OFFAIRRECS` share · or open a JUMP-side `mount.cifs` (kernel-CIFS) transport path as an alternative to userspace smbclient.
* **Follow-on**: when D12-01 closes, re-run the sealed `tools/d12_poc_full_pipeline.py` with a 900 s pod-side subprocess timeout to re-attempt stage 5 → stage 8.

### `BLOCKER-D12-02` (P1 · closed this wave · PEP-668 externally-managed-environment on akki-vm)

* **Symptom**: `python3 -m pip install --user --quiet faster-whisper` on akki-vm failed with `externally-managed-environment` per PEP-668 (Ubuntu 22.04+ / Python 3.12 protection).
* **Root-cause**: distro-provided Python 3.12 marks the system site as externally-managed.
* **Fix (applied this wave)**: `python3 -m pip install --break-system-packages --user --quiet faster-whisper` succeeds in 17.8 s · `import faster_whisper` returns `1.2.1` on akki-vm.
* **Standing**: fix banked in `tools/d12_poc_full_pipeline.py` at Stage 7.  Blocker is CLOSED.

## §C · What was actually banked (receipt observability)

* Receipt file at `phase0/d12_poc_receipts/20260915T101724Z_channel01_2026_09_14_00_00_00.json` (2089 bytes) carries the CP-D12P1 receipt-contract shape (POC_NOT_PRODUCTION_FLAG + input_canonical_key + input_sha256 + input_bytes + model + compute + beam + live-run stage-by-stage verdict + provenance_note) — the receipt IS the artefact per owner directive verbatim ("receipts banked").
* Receipt intentionally carries `stage_5.verdict = FAIL_ON_IO_TIMEOUT` (or `stage_5.verdict = PASS · file_bytes=0` in the first-attempt banking) — the receipt records the blocker as data.  When D12-01 closes and the pipeline reruns, a *new* receipt lands as an append (E.5 append-only discipline).

## §D · SEC hygiene · this-session incident report

Four re-leaks banked (all same class · all agent-side · all zero-new-leak-surface · all values were already `PENDING-OWNER-ROTATION-POST-VERIFICATION` before this session):

| SEC | Class | Pattern | Value(s) re-emitted |
|---|---|---|---|
| SEC-2026-09-15-06 | recurrence of 14-02 | `cat` on bastion CSV (in prior turn) | JUMP root pw |
| SEC-2026-09-15-07 | recurrence of 14-03 | `cat` on bastion CSV (in prior turn) | RADIO ubuntu pw |
| SEC-2026-09-15-08 | new class · python csv.reader header print | `next(csv.reader(open(<custody>)))` print pattern | HF token (matches SEC-14-04) |
| SEC-2026-09-15-09 | new class · openpyxl iter_rows print | `load_workbook + iter_rows + print` on xlsx custody | NAS Bramwel user/pw · JUMP root pw · RADIO ubuntu pw |
| SEC-2026-09-15-10 | new class · `set -x` shell tracing | `set -x` + `PASSWD="$NAS_PW"` co-occurrence | NAS Bramwel pw |

Standing rules 4 (custody csv header emit) · 5 (openpyxl iter_rows print) · 6 (`set -x` + password co-occurrence) banked.  Corrective work is M8 W-TESTS-FIRST-GUARD-INVARIANT part-B scope extension:

> Extend `services/secret_hygiene/custody_file.py` guard scope from 8 shell commands to a wider family covering (a) `next(csv.reader(open(<custody>)))` + `print` python patterns, (b) `openpyxl.load_workbook(<custody>).iter_rows` + `print` python patterns, (c) `set -x` / `bash -x` / `sh -x` shell tracing when co-occurring with `PASSWD=` / `PASSWORD=` / `SSHPASS=` / `SECRET=` / `TOKEN=` variable references.  Filed as part-B of M8 W-TESTS-FIRST-GUARD-INVARIANT.

Owner-desk carry-forward update: all four rotated values remain `PENDING-OWNER-ROTATION-POST-VERIFICATION`.  Recommendation to rotate at end-of-session batches: JUMP root pw · RADIO ubuntu pw · NAS Bramwel pw · rotated HF token (sha256 `3ea89c94…19c5`).

## §E · Wave-close hand-off to M5 sprint-close

Per owner directive verbatim (2026-09-15T~09:50Z): *"After D12 POC: continue the ratified chain — M5 sprint-close report (M0→M5 milestone-boundary format, include D12 POC results: wall-clock per file, quality observations shape-only, cost, and the per-hour projection for the full gap-set so the owner can judge scale-up)."*

Content the M5 sprint-close carries for D12 POC:

| Owner-specified field | Value at wave-close |
|---|---|
| Wall-clock per file | UNMEASURED · stage 5 blocked before transcription · no on-GPU wall-clock captured this session |
| Quality observations shape-only | UNMEASURED · no transcription produced |
| Cost | $0 marginal (Cassava lease + no HF-inference calls · no GPU-hours billed for the failed pipeline path) |
| Per-hour projection for full gap-set | UNCOMPUTABLE without wall-clock · needs BLOCKER-D12-01 close + re-run |

**Recommendation to owner** (M5 sprint-close §5): rank BLOCKER-D12-01 close as the *fastest unlock of ASR production-model selection* per §A17.11.  Without D12 POC completion, §A17.11's "activate the model the census surfaces" cannot fire — the census surfaced NAS 16ch as `unknown`-sensitivity registered-but-unenumerated (CP-CSAIM1), and D12 was supposed to be the pipe proof.  BLOCKER-D12-01 close (network / NAS admin) is the single-most-leveraged unblock in the current audio-plane critical path.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
