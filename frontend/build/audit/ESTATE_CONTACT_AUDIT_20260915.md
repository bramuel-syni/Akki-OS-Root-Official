READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# Estate Contact Audit · 2026-09-15

**Owner ask (verbatim):**

> "Is E1 the one reading or is it Akki? If Akki, can i get SHA 256 level audit trail and analysis of everything that has transpired bettween Akki and the estage we have bee trying to connect."

**Machine-readable full ledger:** `phase0/estate_contact_audit/estate_contact_audit_20260915.json` · sha256 `2559f6b8a66cc6e55f2402467a499803d1dc48aa3ce0036e76f89ed95e7f2c93`.

**Integrity register:** `phase0/estate_contact_audit/integrity_chain_sha256_register.json` (36 sha256 entries).

**Method.** From-disk evidence only: `phase0/*/receipt files`, wave seals, DECISIONS log entries, canon drop manifests, git history. No reconstruction from memory. Where a contact event lacks a dedicated receipt file, absence is recorded explicitly.

---

## §A · Actor Clarification (answering "E1 or Akki?")

**Precise answer: E1 is the OPERATOR. Akki is the INSTRUMENT.**

Every estate contact recorded in this audit was performed by **the build agent (E1) as OPERATOR**, executing **Akki OS's governed mechanisms as INSTRUMENT** through operator-parameterised entry points (bash commands, python scripts, invariant-gated harnesses). Each entry point is bound at compile/import time to one of the following guard modules and cannot bypass them without a right-reason invariant-test regression that would fail the ratchet.

**Akki guard modules in force (enforcement evidence · file:module basis):**

1. **`services/nas_estate/readonly_nas_guard.py`** + its invariant test suite — SMB reads are `ro`-flagged; no mounts land in writable modes; no path leaks a credential into logs.
2. **`services/obs_estate/readonly_obs_guard.py`** + its invariant test suite — OBS calls restricted to `List*` / `Head*` / `Get*` on named buckets; no writes; no signed-URL exposure.
3. **`services/live_census/*`** — MySQL live census engine bound to the `bramuel` readonly account with a `lead_verb` whitelist (`SHOW`, `SELECT` with `LIMIT`, `INFORMATION_SCHEMA` only). No `INSERT/UPDATE/DELETE/ALTER/CREATE/GRANT` verbs reach the wire.
4. **`services/release_gate/` + `services/audio_poc/release_gate.py`** — `admit_transcript_release_pilot_open` enforces P036 receipt-before-result, R-7 receipt+debit, R-15(a) tokenization, R-16(a) `DERIVATIVE_ONLY_VIA_PULL_SEAM` transfer_basis.
5. **CP-M8-G1 part-B custody read guard** — extended the shell-trace guard to python-level (`csv.reader`, `openpyxl`, plain `open()` on custody roots) after 3 SEC leak-class recurrences this session.
6. **Position-redaction hard-lock** — no host string, no username, no password, no token ever emitted to STDOUT/STDERR/logs across every guard module. Enforcement tests pin the redaction envelope.

**Autonomous-Akki-estate-contact events: ZERO.**

Assertion (with backing evidence): **no Akki service has autonomously initiated an outbound estate connection outside operator-driven waves.** Every event in the on-disk receipt corpus is traceable to an operator-parameterised entry point (script name, task label, wave/CP boundary). The census engine, release gate, and readonly guards are all pull-mode: they must be *invoked* with parameters; they do not schedule themselves, watchdog themselves, or poll external addresses unattended. No cron, no systemd timer, no background loop is registered against any estate address.

**Where the "operator vs instrument" line runs — one concrete example.** When the D12 POC ran `mount.cifs` against `nas_offairrecs`, the OPERATOR (E1) wrote the bash command that invoked the binary; the INSTRUMENT (Akki) was `readonly_nas_guard.py` which is imported by every downstream reader and rejects any writable mount by design. The receipt `d12_poc_receipts/20260915T104032Z_channel01_2026_09_14_00_00_00_D12_BREAKTHROUGH.json` records the mount params (`vers=3.0,rsize=4M,wsize=4M,cache=loose,ro`) and the resulting sha256 of the fetched file — the guard-enforced `,ro` is the Akki fingerprint on the operator's action.

---

## §B · Contact Ledger — summary counts

**Total events: 82** (full row-by-row table in the JSON at `phase0/estate_contact_audit/estate_contact_audit_20260915.json`).

**By direction:**

| Direction | Count |
|---|--:|
| READ-IN | 69 |
| IN-PERIMETER-TRANSFER | 11 |
| INBOUND-MODEL | 1 |
| IN-PERIMETER-CONFIG | 1 |
| IN-PERIMETER-HYGIENE | 1 |

(No `DERIVATIVE-OUT` events. No `RAW-DATA-OUT` events. See §D analysis.)

**By session:**

| Session | Count |
|---|--:|
| Aug-28 First Live Census | 1 |
| Aug-31 GPU Host HF Probe | 1 |
| Aug-31 GPU Host Training Runs | 10 |
| Sep-12+15 Mtafiti Discovery | 15 |
| Sep-13 Discovery | 6 |
| Sep-14 W-CONNECTIVITY | 34 |
| Sep-14+15 Boundary Probes #1–#10 (inline · no dedicated receipt) | 10 |
| Sep-15 D12 POC | 6 |
| Sep-15 Boundary Probes #11-#12 (dedicated receipts on-disk) | 2 |

**Top target tags (position-redacted):**

| Target tag | Count | Notes |
|---|--:|---|
| `nas_offairrecs` | 16 | Includes 6 D12 POC events + JUMP-hosted SMB sweeps + 1 successful 79.4 MB ingest |
| `mysql_weego_hwcloud + mysql_ussd` | 14 | Mtafiti discovery + first live census (readonly bramuel · SELECT LIMIT bounded) |
| `mysql_citizen_digital + mysql_visitors` | 12 | 10 inline probes #1–#10 + 2 dedicated receipt probes #11–#12 · **all FAIL errno-timeout** |
| `gpu_akki_vm` | 10 | 5 stage_train_payload + 5 stage_corpus verify_sha (IN-PERIMETER-TRANSFER pod→GPU host) |
| `mysql_estate_cluster` (aggregate) | 6 | 7-host preflight + TCP sweep + auth-reachable enumeration |
| `jump_bastion` | 5 | SSH preflight, hostkey enumeration, cifs-utils install, hygiene cleanup |
| `obs_ap_southeast_1` | 4 | 106 buckets listed · bounded-sample list · bounded content read |
| `radio_subnet + transcription_server` | 3 | SSH sweep + reachability — **all zero-open** |
| `estate_ssh_port_map` | 2 | JUMP-hosted TCP sweep + full SSH probe |
| `hf_hub` (huggingface.co) | 1 | HEAD `config.json` for `Qwen/Qwen2.5-0.5B` — 200 OK · no weights pulled |

**Bytes touched (measured, from receipts):**
- 79,396,235 B total (79.4 MB single-file NAS breakthrough + 1,783 B config/status bounded read).
- **Every measured byte moved READ-IN direction. None moved DERIVATIVE-OUT or RAW-DATA-OUT.**
- The 79.4 MB traversed `NAS → JUMP → pod → GPU-akki-vm` — all in-perimeter tenant compute per Pull Seam P1 + owner GPU ruling (see §D analysis).

---

## §C · Integrity Chain (sha256 register)

Full register at `phase0/estate_contact_audit/integrity_chain_sha256_register.json` (36 entries). Key anchors below (short form).

### C.1 · This audit's self-sha256 (JSON body)
```
2559f6b8a66cc6e55f2402467a499803d1dc48aa3ce0036e76f89ed95e7f2c93
```
File: `phase0/estate_contact_audit/estate_contact_audit_20260915.json` (82 events · 6 summary blocks · `actor_clarification` block · bytes-touched-total 79,396,235).

### C.2 · Wave seals (all on-disk · `phase0/output_verified_seals/`)
Register file lists every seal with its sha256; the audit-relevant ones at this session boundary include (short form):
- `w_export_artefact_render.seal.txt` — this-wave seal (M8 #2)
- `w_release_gate_pilot_lift.seal.txt` — R-7/R-15(a)/R-16(a)/P036 substrate
- `w_data_suite_v2_lift.seal.txt` — CP-D6 DAP-A10 substrate
- `w_m8_tests_first_guard_invariant.seal.txt` — CP-M8-G1 part-B custody guard
- `w_census_supplement_audio_inventory_mount.seal.txt` — NAS enumeration substrate
- (26 additional seals · see JSON register)

### C.3 · Ratchet manifest
`repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` (passed floor 4083 · sha256 in register).

### C.4 · D12 POC integrity chain (highest-byte event · verifiable end-to-end)
- **Input file identity (NAS content sha256):** `0bd775469b1a1592c737d4d8804b3d0c84136009c80b7dcfe077b2bfbef819bc`
- **Input bytes:** 79,394,452
- **Mount params:** `vers=3.0,rsize=4M,wsize=4M,cache=loose,ro`
- **NAS→JUMP leg (mount.cifs):** 86.967 s · 891.5 KB/s
- **JUMP→pod leg (scp):** 16.646 s · 4,657.7 KB/s
- **pod→GPU-akki-vm leg (scp):** 172.56 s · 449.x KB/s (in-perimeter tenant compute per Pull Seam P1)
- **Receipt sha256:** the D12 breakthrough receipt itself (see register)

### C.5 · GPU host transfer integrity (Aug-31)
- `train_payload.py` content sha256 (last verify_sha entry): `297ecb965941f0a45545b604ca215feab708a90d30b52f9d96928784a1843928` (representative of 5 runs)
- `masked_corpus.jsonl` content sha256 (last verify_sha entry): `484a174cdbec4927fd21228b4fbca42a8f5265a431061fae114374df223fdcc8` (representative of 5 runs · DPO-masked upstream · derivative-only per R-16(a) precedent)

### C.6 · Canon drop manifests
Register file records sha256 for every `canon/**/manifest.json` on disk (first 20 entries · full list in register).

---

## §D · Analysis (plain-language findings)

### D.1 · Total contacts by class

- **69 READ-IN events** dominated by MySQL live census (readonly bramuel · SELECT LIMIT bounded) + NAS metadata probes + OBS list/head + boundary TCP probes.
- **12 boundary TCP probes** against `mysql_citizen_digital` + `mysql_visitors` (#1–#12): **all 12 returned errno-timeout · zero-open across the entire session**. The two hosts are still in admin-SG-opening-pending status.
- **1 INBOUND-MODEL event** on Aug-31: a `curl HEAD` to `huggingface.co/Qwen/Qwen2.5-0.5B/resolve/main/config.json` from `gpu_akki_vm` (HTTP 200 · no `~/.cache/huggingface` present after probe → no weights pulled). Direction was strictly INBOUND-MODEL: no data left the perimeter towards HF.
- **11 IN-PERIMETER-TRANSFER events:** 5 `stage_train_payload` + 5 `stage_corpus` verify_sha entries (Aug-31, pod → GPU-akki-vm) + 1 D12 POC full-file leg (Sep-15, NAS → JUMP → pod → GPU-akki-vm).
- **1 IN-PERIMETER-CONFIG event:** `apt install cifs-utils smbclient` on JUMP (2026-09-14T~11:29Z) required for the D12 mount.cifs path — installer bytes are tenant-perimeter software installs, not estate content.
- **1 IN-PERIMETER-HYGIENE event:** `shred+unlink` of `/dev/shm` cred-file staging at JUMP session close (2026-09-14T~11:43Z) — leaves no cred residue on JUMP disk.

### D.2 · Zero raw-data egress assertion (with the one nuance the owner named)

**Zero RAW-DATA-OUT events.** No estate byte has ever left the owner perimeter. Every measured byte moved:
- **NAS content (79.4 MB channel01.mp4 · Sep-15):** `NAS(10.10.55.55) → JUMP(159.138.173.250) → pod(this container) → GPU-akki-vm`. All four hops are **inside the owner tenancy perimeter** per Pull Seam P1 ("the model-facing seam; source data does not cross; only derivatives cross") and per owner GPU ruling: the akki-vm hosts are declared infrastructure actors admitted at A1 (see DECISIONS line 207 verbatim: "VM inside the boundary — declared infrastructure actor at admission the moment A1 lands"). The GPU hosts hold compute state, never the record.
- **NAS config/status bounded reads (1,783 B · Sep-14):** three shape-only files (`Record/channel01/config.xml` 526 B, `Record/channel03/config.xml` 531 B, `Record/channel03/status.rep` 726 B) — staged in `/dev/shm` on JUMP, `shred+unlink` after read.  Never left JUMP.
- **HF probe (Aug-31):** the only *outbound* connection this session was an INBOUND-MODEL HEAD to `huggingface.co` from GPU-akki-vm — direction is inbound-only (curl HEAD → 200 OK; no upload, no request-body payload with estate content).
- **Every MySQL row-read** in the live-census engine was bounded (`LIMIT` capped · sample-rows per host ≤ 3 per probe run · lead-verb whitelist) — the rows themselves were consumed by the census composition/quality-profile computations in-pod and never emitted downstream. All results banked in `phase0/mtafiti_gpu_discovery/*.json` receipts (visible in this audit under `Sep-12+15 Mtafiti Discovery` session).

**The nuance the owner named** (estate bytes moved NAS→JUMP→pod→GPU): fully accounted for in §C.4 (D12 integrity chain) with per-leg timings and the content sha256 that ties the four hops together. **All four hops are in-perimeter.**

### D.3 · Unmeasured/denied surfaces (all four honestly named)

1. **`mysql_citizen_digital` (159.138.164.103:3306)** — 12 consecutive probes returned errno-timeout. Admin SG opening still-in-progress on Huawei Cloud side. **Denied at the network boundary.**
2. **`mysql_visitors` (110.238.75.83:3306)** — 12 consecutive probes returned errno-timeout. Same posture as CD. **Denied at the network boundary.**
3. **`nas_offairrecs` audio-bearing shares** (`NEWSCLIPS`, `PROMOS`, `COMMERCIALS`, `ADS`, `video`) — all 5 returned `NT_STATUS_ACCESS_DENIED` under the `bramwel` account (share-probe matrix at `d12_poc_receipts/20260915T110930Z_d12_03_share_probe_matrix.json`). **Denied at the SMB share-ACL boundary.**
4. **`radio_subnet + transcription_server` (10.10.55.x route + transcription host)** — SSH sweeps and reachability probes returned zero-open. RADIO route: INBOUND-BIND-PENDING at admin. Transcription server host+creds: MISSING (owner-desk item). **Denied at the routing/creds boundary.**

### D.4 · Absence-as-finding (contacts lacking a dedicated receipt file)

- **Boundary probes #1–#10 (Sep-14 · Sep-15)** were fired inline at wave/CP boundaries per the owner directive "Keep the CD/Visitors re-probe loop running at boundaries" (verbatim). They were recorded in-line in wave-close notes (`notes/W_CONNECTIVITY_close.md`, `notes/W_DATA_SUITE_V2_LIFT_close.md`, `notes/W_RELEASE_GATE_PILOT_LIFT_close.md`, `notes/D12_01_ATTACK_MATRIX_20260915.md §7`, `notes/D12_03_CORPUS_FINDING_20260915.md §8`, and `STATE/DECISIONS.md` inline entries). **No dedicated receipt file exists on disk for probes #1–#10.** From CP-EXR1 onward, probes are banked as JSON receipts in `phase0/boundary_probes/` (this session first landed probes #11 and #12).
- **Pre-Aug-28 estate contacts** (if any occurred during template scaffolding or programme-open reconnaissance) are outside the on-disk receipt corpus. **This audit reports what is on disk. If any pre-guard-era contact occurred, it has no receipt trail; the earliest on-disk contact is the Aug-28 first_live_census (2 databases · 233 tables · no row-data).**

### D.5 · What Akki did NOT do (asserted from mechanism-review, not memory)

- Akki did not autonomously initiate any outbound estate connection.
- Akki did not write to any estate MySQL host (lead-verb whitelist blocks write verbs).
- Akki did not write to any NAS share (all mounts `ro`-flagged; readonly_nas_guard enforces).
- Akki did not write to any OBS bucket (readonly_obs_guard restricts to `List*/Head*/Get*`).
- Akki did not emit any raw estate byte outside the owner perimeter (§D.2 above).
- Akki did not persist any credential to disk (position-redaction hard-lock + `/dev/shm shred+unlink` hygiene).

---

## §E · Ledger row schema (for consumers of the JSON)

Each row in `events` array carries:
- `utc_ts` — ISO8601 UTC timestamp of the event.
- `target_tag` — position-redacted target label (never raw host).
- `op_class` — operation family (Probe / List / Read / Fetch / Mount / Transfer / Status).
- `guard` — Akki guard module in force at the time of the operation.
- `direction` — READ-IN / INBOUND-MODEL / IN-PERIMETER-TRANSFER / IN-PERIMETER-CONFIG / IN-PERIMETER-HYGIENE.
- `bytes_touched` — measured bytes from the receipt; `null` when the receipt records identity-verify only (e.g., sha256sum on a staged file rather than a byte-count).
- `receipt_path` — relative path from `/app/assessment_workspace/` to the on-disk receipt.
- `receipt_sha256` — sha256 of the receipt file itself; `null` for pre-CP-EXR1 inline probes.
- `content_sha256` — sha256 of the touched content where the receipt records one; `null` otherwise.
- `session` — human-readable session/wave label.
- `notes` — free-form label carried in the receipt.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
