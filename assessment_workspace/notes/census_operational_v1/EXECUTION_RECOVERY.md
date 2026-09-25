# Execution recovery — COMPUTE-CENSUS-IDENTITY

## Live method verification after owner GPU workbook — 2026-09-25T18:57Z

Owner supplied **Compute Creds.xlsx** as "GPU creds" after authorizing restoration of the existing identity. Downloaded to mode0600 custody at `/app/backend/estate_keys/gpu_hosts/Compute_Creds_20260925T184738671152Z.xlsx`; sha256 `397148b327e42be61035b06a0154f3280a495295890df85c5556782d513ebaf9`. No credential value printed, placed in a receipt, or added to application env. Workbook has eleven rows/one column; initial read lacked dimensions, safely recomputed within bounded unpacked/file size. Original diagnostic error retained in intake receipt. No formulas or PEM private-key material detected. Both supplied addresses/usernames match admitted inventory. Password values match values already in historical workbook, despite different workbook bytes/layout. That is not new private signing material or proof of working passwords.

### Fresh live evidence (not historical inference)

|Host alias|Pinned server key|Methods advertised for configured account|User authenticated|Passwords/keys sent|Commands/source reads|
|---|---|---|---|---|---|
|akki-vm|MATCHED|publickey only|NO|NONE|NONE|
|akki-vm-ii|MATCHED|publickey only|NO|NONE|NONE|

One `auth_none` request per host, only AFTER matching the existing server-key pin. This is a credential-free authentication-method query, not a password failure or successful authentication. Both responded `AUTH_NONE_REJECTED` with `publickey`. **Workbook passwords cannot recover access through the tested SSH channel.** No password attempt, key installation, host-key/policy change, key generation or private-key restoration took place. This does not reveal which client public key remains authorized or establish GPU hardware/executor health.

Receipts: `phase0/drill_receipts/census_operational_v1/execution_recovery/auth_none_owner_compute_workbook/` contains exclusive per-host intent and result records. Intake/schema/private-match receipts are in parent directory. Runner intentionally consumes each digest/host attempt and replays receipts without re-probing; orphan intents also prevent retries.

### Implementation/test scope

- New additive backend modules `services/census_autonomy/auth_methods_probe.py` and `auth_methods_receipts.py`; NOT HTTP-routed, NOT a source executor or substitute identity. Uses existing admitted host inventory/pins, finite connection/auth/banner timeouts, compatible pinned key algorithms, allowlisted method output, and no channel/command or credential-auth call. Existing sealed auth/hardening and all UI remain unchanged.
- RED13/13 missing-module cases banked before implementation. Corrected test harness to return host aliases instead of host addresses and accurately model Paramiko methods; acceptance was not weakened.
- Initial13/13 GREEN; expanded23/23 diagnostic/receipt unit tests passed. Full current census slice **103 passed,2 intentionally skipped, twice**; `/app/test_reports/iteration_7.json`. Skips are prior explicitly opt-in production custody/refusal drills. Unit transports are **MOCKED**; the two live method-query receipts above are **REAL**.
- No full-platform completion or baseline-suite ratchet inferred. Current counts:2/2 server-pin checks verified;0/2 authenticated host sessions;0/1 T14 successful fresh source-output gate.

### Required next recovery input

Restoration is already authorized. Need the original private signing key from the still-authorized system/approved backup, **or an existing approved console/break-glass access route**. A further password workbook does not resolve the observed publickey-only SSH policy. Do not generate a replacement, enable password login, repin to the current mismatched private key or reset authentication on the basis of this upload. After actual restore, verify admitted identity, remote executor/connector custody, then bounded Akki census → Mtafiti → OS/DAP result.

## Latest owner choice — 2026-09-25T18:40Z

Owner verbatim: "Restore - access is granted to one system which means currently previous identity still linked". **Restoration of the existing identity is authorized; do not request the same permission again.** The owner reports an existing link, but the system name/access path holding the corresponding signing identity is not specified. This statement is not treated as independent verification of current remote authorized_keys.

Additional bounded local lookup: recorded `backend/estate_keys/estate_ed25519` derives `SHA256:TpJcdNAQ4iSQKK5inwPueOM6Qak5NcsD5XhZpWorZ+c`, which also differs from the admitted GPU identity. Available Git history contains no entry for the GPU private/public custody paths. No configured SSH signing agent/socket is available. No keys copied, generated, overwritten or exported; no host/password attempt or estate read. Metadata receipt: `phase0/drill_receipts/census_operational_v1/execution_recovery/restore_custody_lookup_20260925T184015812388Z.json`.

Needed next input is **where the currently authorized system or original key backup is accessible**, not approval to restore. Existing public authorization cannot supply the absent private signing material. Prefer recovery through the already-authorized system; do not infer that an unrelated estate key is a replacement. T14 remains blocked.

## Authority and scope — 2026-09-25

Owner continuation verbatim: "Go ahead - dont change anything in your initial plan, mine was just to see how your plan ties up the requirements. Primary objective is to ensure requirements are met but they work. Akki OS and DAP have to be functional and deliver their promise". Latest confirmation: "You can pick it up".

This advances CP_CENSUS_OPERATIONAL_V1 MUST DO 4 / T07 and the prerequisite to T14. It does NOT close T14, redesign OS/DAP, commission Solva, or alter the nine-work-package sequence.

Protected objective: census must execute through the admitted Akki identity, not silently substitute a different credential after environment recovery.

## Independently verified local findings

- Existing configured GPU key exists at the recorded custody path, mode 0600. Its **derived private-key public fingerprint** is `SHA256:dtmtQPKdrqRioj5sas2RCucpKpP97F5c0/0tPHTux2o`.
- The admitted pin in `STATE/PINS.md:1169-1175` and `phase0/keypair_hardening_receipts/20260828T162217Z_step1_keygen.json` is `SHA256:M3Dre1A1I1ZQFo0FDsfzbWPwn5z+oxmZ02y1eZwFy1A`. Step2 records installation; step8 records key-only success and password retirement. September22 re-verification is banked at `STATE/DECISIONS.md:35674-35695`.
- These fingerprints differ. The current key's comment names September24; a comment is NOT proof of the overwrite time, actor, cause, or remote authorized_keys contents. The diagnostic recommendation claiming all those facts is NOT adopted as verified evidence.
- Generic `SSH_PRIVATE_KEY_PATH` / `SSH_PUBLIC_KEY_PATH` point to absent `/tmp/akki_mock_sshd/pod_id_ed25519` files. They are distinct from the configured per-host census identity.
- No bootstrap/per-host SSH password is configured. Recorded password retirement is intentional. Existing xlsx/CSV custody artifacts are not assumed to override that state or provide a working password.
- Bounded inspection of `backend/estate_keys/gpu_hosts` and `/root/.ssh` found no alternate private-key file. This is NOT an exhaustive backup/secret-store search.
- `hardening.run()` requires a bootstrap credential; `gpu_submit` delegates to it. Both `_write_ledger_row` defaults only return local identifiers; no production replacement was found among inspected callers. Blindly calling them would not establish the promised durable per-step ledger.
- No host changes, password attempts, estate reads, new keys, .env credential changes, or fresh live census have occurred in this recovery investigation.

## Recovery decision

Prefer restoration of the **already-admitted** private key from an authorized backup/secret mount. If unavailable, an owner-authorized console/break-glass route must explicitly admit/install a replacement with receipts, then verify key-only access and password refusal. Do not enable password login, alter host pins, regenerate a key, or repeat blind authentication attempts. Hardening installation cannot repair access without an authenticated recovery channel.

T14 remains blocked. Remote worker custody/connector configuration remains unverified, so successful SSH alone will not close it.

## Narrow additive implementation and tests-first acceptance

Add `services/census_autonomy/execution_identity.py`; compose it only in the existing additive `remote_dispatch.py`, leaving sealed `ssh_seam`, `hardening`, and `gpu_submit` unchanged. Per-host environment points to the existing receipt and its SHA-256; no private key or password value enters receipts. Verify the exact key object used by transport. Do not create new endpoints or a recovery dashboard.

|Case|Acceptance condition|
|---|---|
|R01|Matching receipt pin and derived private-key fingerprint yield the exact verified key object for dispatch; no network in local verification.|
|R02|Different key at the same path refuses before any SSHClient construction/connection.|
|R03|Missing/malformed/changed receipt or missing receipt hash refuses; it never silently trusts a new baseline.|
|R04|Missing/unreadable/symlink/group-readable key refuses without leaking key bytes or provider diagnostics.|
|R05|Password-only configuration cannot substitute for admitted key-only census execution.|
|R06|Dispatch uses RejectPolicy, explicit known_hosts, verified pkey, no agent, no implicit key discovery, no password fallback.|
|R07|Identity refusal banks a reason-coded transport receipt and yields a blocked aggregate outcome; no estate read/false completion.|
|R08|Existing census scoped contract/live-read tests still pass; prototype bytes and sealed auth module bodies unchanged.|

Test transports are **MOCKED**; neither these checks nor a local pin match establishes real host authentication. Report these separately from T14. Retain right-reason RED and repeated GREEN logs in `phase0/drill_receipts/census_operational_v1/execution_recovery/`. Full historical invariant suite remains absent; no ratchet or multi-repository seal claim.

## Next independent work

Continue mapping original prototype actions to owning components/Canon/service/writer/acceptance cases while credential restoration is unavailable. Preserve unreviewed status; do not fabricate a whole-platform completion denominator.

## Verified implementation checkpoint — 2026-09-25

- R01–R08 satisfied at their scoped test levels: local continuity enforcement + reason-coded refusal + regression/integrity checks. **8/8 for this safeguard; NOT 8/8 recovery steps and NOT restored GPU access.**
- RED-first: 12 failed / 1 passed (`RED_execution_identity_pytest.log`); new unit/adversarial checks expanded thereafter. Full current census suite: 82 passed twice in `pytest_census_operational_run1.log` / `run2.log`, independent report `/app/test_reports/iteration_5.json`.
- Main verification caught a test-harness hazard: production refusal tests were default-enabled and could consume an older preflight receipt. Corrected to require `AKKI_RUN_IDENTITY_REFUSAL_DRILL=1` and a freshly evaluated fixture per invocation; environment parsing now matches dotenv and is restored after testing. Evidence writes use unique filenames. Reverified full suite with explicit authorization: **82 passed twice**, `GREEN_explicit_drill_1.log` / `_2.log`. Default drill execution: **2 skipped**; no production custody/commission actions when opt-in is absent. This changes safety of the test harness, not acceptance criteria.
- Actual API refusal-path run **`cr-809561ad5643`**: REFUSED / blocked; output reason `AKKI_EXECUTION_IDENTITY_NOT_VERIFIED`; both host transport records carry `IDENTITY_PIN_MISMATCH`. Exact idempotency replay returns the same run. This is a newly persisted refusal record, not source output and not T14 success. Original failed run remains unchanged.
- Local verifier read the actual private key through the SSH loader, without source/secret output, and refused both configured hosts. `local_preflight_identity_refusal.json` and later timestamped receipts bank these observations. No remote authentication was attempted by this new blocked dispatch.
- Existing historical receipt path and hash added as four non-secret per-host env settings. No password/key material changed. Backend restarted for env; existing census scheduler restarted only after confirming zero pending census jobs, so it also reloads these settings. No new schedule or worker architecture.
- Sealed auth/hardening modules and owner HTML unchanged. Source checks and prototype-hash tests passed. No UI redesign or new endpoint.
- Read-only documentary inventory generated: **888 markup event sites** (817 OS, 71 DAP), unique IDs, original-source hashes, containing conditions/list contexts. `PROTOTYPE_ACTION_INVENTORY.json`; generation receipt in this checkpoint's evidence directory. These are NOT 888 required journeys: repeated/dynamic bindings still require component/Canon/consumer/writer/test reconciliation. Their null mapping fields mean UNREVIEWED, never NOT BUILT.

### Exact remaining exit

Restore the already-admitted key from authorized custody/backup, or establish an explicitly authorized existing recovery channel. Then verify pinned-host-key authentication, remote execution/connector custody, bounded source read, canonical receipt asset registration and durable result visibility in both products. **T14 remains 0/1; Mtafiti fresh-output link remains partial.**

### Evidence interpretation correction

The independent report's `seed_data_creation: None` does not mean no operational state was written: the authorized refusal drill created the run above, while creating no users or estate source records. Unit transports/temporary test keys are **MOCKED**. Production refusal handling is real. The original report is preserved with this addendum, not rewritten to hide observations.