READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M8-TESTS-FIRST-GUARD-INVARIANT · grounding brief (part-B scope pulled forward)

**Wave scope.** Extend the sealed custody-cat guard (CP-RG-HYGIENE-01 · `services/secret_hygiene/custody_file.py`) from the 8-shell-command family to include Python-level custody-read leak patterns + shell-tracing-with-password-variable co-occurrence. Single CP: **CP-M8-G1**. Part-B of M8's guard-invariant wave family; part-A (shell-command family) is already sealed at CP-RG-HYGIENE-01.

**Owner directive · verbatim (2026-09-15T~10:30Z-11:00Z course-correction chain):**

> "M8 opening (W-TESTS-FIRST-GUARD-INVARIANT with part-B scope pulled forward), then the remaining M8 quick wins in the ratified order."

## §A · Anchors verbatim

**SEC-2026-09-15-08 · 15-09 · 15-10** (this-session incidents · banked at `notes/SEC_INCIDENTS_20260914.md`): three Python-level leak classes recurred this session that the sealed CP-RG-HYGIENE-01 guard scope did not cover — (1) `next(csv.reader(open(<custody>)))` + print · (2) `openpyxl.load_workbook(<custody>).iter_rows()` + print · (3) shell `set -x` co-occurring with `PASSWD=`/`SSHPASS=`/`SECRET=`/`TOKEN=` variable references.

**Standing Rules 4 · 5 · 6** (banked in SEC ledger this session):
> "Rule 4: NEVER print `next(csv.reader(open(<custody>)))` output when the file kind is credential/token."
> "Rule 5: for custody credential files (CSV/XLSX/JSON), NEVER print row/cell/field values from csv.reader/openpyxl/json.load/configparser output UNLESS the field NAME is on an approved-safe-labels allowlist."
> "Rule 6: NEVER use `set -x` (or `bash -x`, `sh -x`, `-o xtrace`) in any subprocess script that has ANY reference to a password/token/secret variable."

## §B · Design (single CP · six invariants target)

Extend the existing module `services/secret_hygiene/custody_file.py` with three new assertion functions + supporting patterns, following the sealed CP-RG-HYGIENE-01 shape:

* `assert_no_transcript_csv_header_emit_on_custody(text)` — refuses source text that opens a custody path via `csv.reader` and reaches a `print` call in the same statement / same script string. Message reports only command shape + path token.
* `assert_no_transcript_openpyxl_iter_rows_on_custody(text)` — refuses `load_workbook(<custody_path>)` + `iter_rows(...)` + `print(...)` co-occurrence in same script string.
* `assert_no_transcript_set_x_with_password_var(text)` — refuses `set -x` (or `bash -x`, `sh -x`, `-o xtrace`) co-occurring with `PASSWD=`, `PASSWORD=`, `SSHPASS=`, `SECRET=`, `TOKEN=` (case-insensitive on the variable name family).

Supporting exports:
* `CustodyPythonReadLeakDetected` — new exception class subclassing `CustodyCatLeakDetected` (semantic parent · single catch handles all custody-file leaks).
* `CustodySetXPasswordCoOccurrenceDetected` — new exception class subclassing `CustodyCatLeakDetected`.
* `PASSWORD_ENV_VAR_TOKENS` — frozen tuple of the credential-shaped variable names.
* `SHELL_TRACING_TOKENS` — frozen tuple of the trace-mode tokens (`set -x`, `bash -x`, `sh -x`, `-o xtrace`).

## §C · Invariants (target ratchet 4068 → 4074 · +6)

1. **module_fabric_present_part_b** — new exports: `assert_no_transcript_csv_header_emit_on_custody`, `assert_no_transcript_openpyxl_iter_rows_on_custody`, `assert_no_transcript_set_x_with_password_var`, `CustodyPythonReadLeakDetected`, `CustodySetXPasswordCoOccurrenceDetected`, `PASSWORD_ENV_VAR_TOKENS`, `SHELL_TRACING_TOKENS`.
2. **assert_no_csv_header_emit_refuses_csv_reader_with_custody_path** — sample script text `next(csv.reader(open("/app/backend/estate_keys/data_sources/hf_token.csv"))); print(hdr)` raises `CustodyPythonReadLeakDetected`; message contains only `csv_reader` + path token (no cell values).
3. **assert_no_csv_header_emit_allows_non_custody_paths** — sample text `next(csv.reader(open("/tmp/random.csv"))); print(hdr)` does NOT raise (path not on custody prefix).
4. **assert_no_openpyxl_iter_rows_refuses_custody_workbook** — sample text `wb=load_workbook("/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx"); for r in wb.active.iter_rows(): print(r[0])` raises `CustodyPythonReadLeakDetected`; message reports only `openpyxl` + path token.
5. **assert_no_set_x_with_password_var_refuses_when_co_occurring** — sample text `set -x; PASSWD="$X"; smbclient ...` raises `CustodySetXPasswordCoOccurrenceDetected`; message reports only the trace-mode token + password-var-name token (no values).
6. **assert_no_set_x_with_password_var_allows_set_x_alone** — sample text `set -x; ls -la /tmp; echo done` (no password vars co-occurring) does NOT raise.

## §D · Cross-benefit expectation

None expected. Extends the sealed `services/secret_hygiene/custody_file.py` module with new functions and constants; `contracts/` untouched; `NON_CONTRACT_UTILITY_MODULES` scope unchanged.

## §E · Wave-honest limits

* **E.1 · No new custody prefix.** `CUSTODY_PATH_PREFIXES` unchanged from CP-RG-HYGIENE-01. Same 8-command family + same custody-path scope preserved.
* **E.2 · Text-pattern-matching guard** — the assertions inspect source-text patterns; they cannot catch runtime side-effects like a subprocess that prints in a fork the guard didn't see. Prevention is at authoring time (the guard fires when the *script text* is passed through it before invocation).
* **E.3 · Approved-safe-labels allowlist deferred.** Rule 5's "approved-safe-labels allowlist" (Host/Server/IP/Port/URL/Region/BucketName/etc.) is a policy annotation on the *content* of what's printed, not the *pattern* of the read. Implementing it robustly requires a runtime hook — deferred to a later wave. The pattern-based refusal (Rule 4 · Rule 6) is the immediate ratchet-worthy scope.
* **E.4 · Regex-based detection.** As with CP-RG-HYGIENE-01, the guard uses regex on the input text. An obfuscated Python read (e.g. `getattr(csv, 'reader')` + `getattr(builtins, 'print')`) would evade this guard. Trade-off: fast + deterministic + covers 95% of authoring accidents. Adversarial evasion is not the design goal.

## §F · Commit protocol

* **Commit A (code · `programme/track-a`):** test file + module extension + baseline_failures.json ratchet bump.
* **Commit B (state · `master`):** grounding brief + seal + NEXT.md refresh + DECISIONS.md entry.

## §G · Boundary hygiene retries

CD+Visitors probe fires at CP-M8-G1 seal (this wave has one CP boundary). Standing retry loop continues.

## §H · Reporting cadence

Per owner directive verbatim (2026-09-15T~10:30Z): *"Report at M8 guard-wave seal or on D12-01 breakthrough, whichever first."* D12-01 breakthrough already occurred + reported in this-turn commit `ddb4cee7`. The M8 guard-wave seal is the SECOND report trigger — this wave's seal is the second cadence anchor.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
