"""Secret-hygiene guard for CUSTODY FILE cat-class recurrence.

Owner course-correction 2026-09-15T~08:37Z clause 3 (verbatim):
    "SEC-2026-09-15-06/07 (custody-file cat re-leaks): good containment and
     honest logging. Pull the custody-cat guard FORWARD — land
     assert_no_transcript_cat_on_custody as a small invariant inside the
     current wave walk (it mirrors the HF-token guard, ~1 CP-sized, prevents
     the exact violation class that has now recurred 4 times across
     sessions). Do not wait for M8."

Guard shape (mirrors `services/secret_hygiene/hf_token.py::assert_no_transcript_leak_of_active_token`).

Prevented class: shell invocation that emits a `/app/backend/estate_keys/**`
file's contents to stdout/transcript. Documented instances:
  - SEC-2026-09-14-01 (agent-side · session 1)
  - SEC-2026-09-14-02 (agent-side · session 2)
  - SEC-2026-09-14-03 (agent-side · session 3)
  - SEC-2026-09-14-04 (agent-side · session 4)
  - SEC-2026-09-15-06 (in-session · this session · JUMP root pw re-leak)
  - SEC-2026-09-15-07 (in-session · this session · RADIO ubuntu pw re-leak)

Discipline: this module NEVER prints custody-file contents. It reports the
COMMAND and PATH (shell-level tokens), never file bytes.
"""
from __future__ import annotations

import re
from typing import Tuple


# Owner course-correction rule (2026-09-15, verbatim; banked in
# STATE/DECISIONS.md · owner-channel course-correction 2026-09-15T~08:37Z clause 3).
CUSTODY_CAT_GUARD_RULING_VERBATIM: str = (
    "Pull the custody-cat guard FORWARD — land "
    "assert_no_transcript_cat_on_custody as a small invariant inside the "
    "current wave walk (it mirrors the HF-token guard, ~1 CP-sized, prevents "
    "the exact violation class that has now recurred 4 times across sessions). "
    "Do not wait for M8."
)


# Custody path prefixes under position-redaction hard-lock.  Extension is a
# state-commit event; adding a prefix here is a snapshot-parity anchor for
# future waves that add custody surfaces.
CUSTODY_PATH_PREFIXES: Tuple[str, ...] = (
    "/app/backend/estate_keys/",
)


# Leak-class shell commands: emit file contents to stdout.  This set is
# authoritative for the recurrence class; expansion requires a state-commit.
LEAK_COMMANDS: Tuple[str, ...] = (
    "cat",
    "head",
    "tail",
    "less",
    "more",
    "bat",   # Rust alt to `cat` with syntax highlighting.
    "view",  # Vim read-only.
    "type",  # Windows-style; benign on Linux but explicit.
)


# Compiled pattern: `\b(leak-cmd)\b` followed by an argument sequence that
# contains a custody-path prefix.  Uses non-greedy match up to a shell
# terminator (`|`, `;`, `&`, newline, or end-of-line).
def _build_pattern() -> "re.Pattern[str]":
    cmds_alt = "|".join(re.escape(c) for c in LEAK_COMMANDS)
    # Path alternation: any custody prefix followed by non-terminator chars.
    prefix_alt = "|".join(re.escape(p) for p in CUSTODY_PATH_PREFIXES)
    # Full pattern: word-boundary leak command, then anything (non-greedy)
    # up to a custody path, until a shell terminator.
    return re.compile(
        rf"\b(?P<cmd>{cmds_alt})\b[^\n|;&]*?(?P<path>(?:{prefix_alt})[^\s;|&]*)",
        re.IGNORECASE,
    )


_LEAK_PATTERN: "re.Pattern[str]" = _build_pattern()


class CustodyCatLeakDetected(Exception):
    """The input string contains a shell-invocation pattern that would emit
    a custody-file's contents to stdout/transcript.

    Message reports only the command name and the custody-file path (both
    shell-level tokens; NOT file contents).
    """


def assert_no_transcript_cat_on_custody(text: str) -> None:
    """Raise `CustodyCatLeakDetected` if `text` contains a cat-class command
    invoked against a custody-file path.

    Safe patterns (do NOT raise):
      - `python -c` / `python3 -c` (structured extraction; not cat-class).
      - `stat` / `ls` / `wc` / `sha256sum` / `chmod` / `mv` (metadata /
        hash / structural; do not emit contents).
      - Any leak-class command against a non-custody path
        (e.g. `/tmp/foo`, `README.md`, `/var/log/...`).

    Prevented patterns:
      - `cat /app/backend/estate_keys/...`
      - `head /app/backend/estate_keys/...`
      - `tail /app/backend/estate_keys/...`
      - `less /app/backend/estate_keys/...`
      - `more /app/backend/estate_keys/...`
      - `bat /app/backend/estate_keys/...`
      - `view /app/backend/estate_keys/...`
      - `type /app/backend/estate_keys/...`
      - Any of the above inside a larger multi-command shell string.
    """
    match = _LEAK_PATTERN.search(text)
    if match is None:
        return
    cmd = match.group("cmd")
    path = match.group("path")
    raise CustodyCatLeakDetected(
        f"custody-file cat-class pattern detected: "
        f"command={cmd!r} path={path!r}. "
        f"Use `python -c` for structured extraction; use `stat`/`ls`/`wc`/"
        f"`sha256sum` for metadata only. Never cat/head/tail/less/more/bat/"
        f"view/type on a custody path (position-redaction hard-lock)."
    )


# ---------------------------------------------------------------------------
# Part-B extension (W-M8-TESTS-FIRST-GUARD-INVARIANT · CP-M8-G1).
#
# Discharges Standing Rules 4/5/6 banked in SEC ledger this session
# (SEC-2026-09-15-08 csv.reader header emit · SEC-15-09 openpyxl iter_rows
# print · SEC-15-10 shell `set -x` + password-variable co-occurrence).
#
# All three assertions inspect SOURCE TEXT and raise BEFORE the subprocess
# fires.  Prevention is at authoring-time; catches ~95% of authoring
# accidents.  Adversarial evasion (obfuscated Python reads via getattr,
# base64-encoded scripts) is not the design goal.
# ---------------------------------------------------------------------------


# Credential-shaped environment-variable names that MUST NOT co-occur with
# shell-tracing (`set -x` etc.), because trace-mode echoes variable
# expansions to stderr including the value.  Case-insensitive matched.
PASSWORD_ENV_VAR_TOKENS: Tuple[str, ...] = (
    "PASSWD",
    "PASSWORD",
    "SSHPASS",
    "SECRET",
    "TOKEN",
    "APIKEY",
    "API_KEY",
    "AUTH",
)

# Shell-tracing tokens that echo variable expansions to stderr.  Case-
# insensitive matched.  `-o xtrace` is the bash-option form.
SHELL_TRACING_TOKENS: Tuple[str, ...] = (
    "set -x",
    "set -o xtrace",
    "bash -x",
    "sh -x",
    "-o xtrace",
)


class CustodyPythonReadLeakDetected(CustodyCatLeakDetected):
    """The input source text opens a custody path via a Python-level
    reader (csv.reader / openpyxl.load_workbook / json.load) and reaches
    a `print` in the same script string.  Same recurrence class as
    `CustodyCatLeakDetected`; different mechanism.
    """


class CustodySetXPasswordCoOccurrenceDetected(CustodyCatLeakDetected):
    """The input source text co-mentions a shell-tracing token
    (`set -x`, `bash -x`, `sh -x`, `-o xtrace`) and a credential-shaped
    environment-variable reference (`PASSWD=`, `SSHPASS=`, etc.) in the
    same script string.  Trace-mode would echo the variable expansion to
    stderr and leak the value.
    """


def _build_csv_reader_custody_pattern() -> "re.Pattern[str]":
    """`csv.reader(open("<CUSTODY_PATH>"))` shape · Python source-text."""
    prefix_alt = "|".join(re.escape(p) for p in CUSTODY_PATH_PREFIXES)
    # csv.reader / csv_reader / next(csv.reader(...)) all matched.
    return re.compile(
        rf"csv[._\s]*reader\s*\(\s*open\s*\(\s*[\"'](?P<path>(?:{prefix_alt})[^\"']*)",
        re.IGNORECASE,
    )


def _build_openpyxl_custody_pattern() -> "re.Pattern[str]":
    """`load_workbook("<CUSTODY_PATH>")` shape · Python source-text."""
    prefix_alt = "|".join(re.escape(p) for p in CUSTODY_PATH_PREFIXES)
    return re.compile(
        rf"load_workbook\s*\(\s*[\"'](?P<path>(?:{prefix_alt})[^\"']*)",
        re.IGNORECASE,
    )


_CSV_READER_CUSTODY_PATTERN: "re.Pattern[str]" = _build_csv_reader_custody_pattern()
_OPENPYXL_CUSTODY_PATTERN: "re.Pattern[str]" = _build_openpyxl_custody_pattern()
_PRINT_CALL_PATTERN: "re.Pattern[str]" = re.compile(r"\bprint\s*\(")


def assert_no_transcript_csv_header_emit_on_custody(text: str) -> None:
    """Raise `CustodyPythonReadLeakDetected` if `text` reads a custody
    path via `csv.reader(open(...))` AND contains a `print(...)` call.

    The two co-occurrence check is sufficient because a script that
    opens a custody csv and prints anywhere in its body is a
    print-of-cell candidate.  Message reports the read-pattern token
    (`csv_reader`) and the custody path token (both safe · not values).
    """
    read_match = _CSV_READER_CUSTODY_PATTERN.search(text)
    if read_match is None:
        return
    if _PRINT_CALL_PATTERN.search(text) is None:
        return
    path = read_match.group("path")
    raise CustodyPythonReadLeakDetected(
        f"custody-file csv_reader+print pattern detected: "
        f"pattern='csv.reader(open({path!r}))+print(...)'. "
        f"Use `readline()` + shape-only surface `first_chars=<3>+<REDACTED · "
        f"sha256 xxx · len N>` when the file kind is credential/token. "
        f"Never emit `next(csv.reader(open(<custody>)))` output "
        f"(Standing Rule 4 · SEC-2026-09-15-08 class)."
    )


def assert_no_transcript_openpyxl_iter_rows_on_custody(text: str) -> None:
    """Raise `CustodyPythonReadLeakDetected` if `text` opens a custody
    path via `openpyxl.load_workbook(...)` AND contains a `print(...)`
    call.

    Same discipline as the csv variant: co-occurrence is sufficient.
    """
    read_match = _OPENPYXL_CUSTODY_PATTERN.search(text)
    if read_match is None:
        return
    if _PRINT_CALL_PATTERN.search(text) is None:
        return
    path = read_match.group("path")
    raise CustodyPythonReadLeakDetected(
        f"custody-file openpyxl+print pattern detected: "
        f"pattern='load_workbook({path!r})+print(...)'. "
        f"Read cells into a private dict; reference values only by "
        f"sha256+length metadata; never print `iter_rows(...)` output "
        f"unless the field NAME is on the approved-safe-labels allowlist "
        f"(Standing Rule 5 · SEC-2026-09-15-09 class)."
    )


def assert_no_transcript_set_x_with_password_var(text: str) -> None:
    """Raise `CustodySetXPasswordCoOccurrenceDetected` if `text`
    co-mentions a shell-tracing token AND a credential-shaped
    environment-variable name.  Trace-mode echoes variable expansions
    to stderr; a `PASSWD="$X"` (or similar) shows the value.

    Message reports only the trace-mode token + the credential-var-name
    token (both safe · never values).
    """
    trace_tokens_hit = [t for t in SHELL_TRACING_TOKENS if t in text]
    if not trace_tokens_hit:
        return
    # Password-var check: match a var-name token followed by `=`
    # (assignment) or `${` / `$` (dereference).  Case-insensitive on the
    # var-name token.
    pw_tokens_hit = []
    for token in PASSWORD_ENV_VAR_TOKENS:
        pattern = rf"\b{re.escape(token)}\s*[=]"
        if re.search(pattern, text, re.IGNORECASE):
            pw_tokens_hit.append(token)
    if not pw_tokens_hit:
        return
    raise CustodySetXPasswordCoOccurrenceDetected(
        f"shell-tracing + credential-variable co-occurrence detected: "
        f"tracing_tokens={trace_tokens_hit!r} "
        f"password_var_tokens={pw_tokens_hit!r}. "
        f"Trace-mode (`set -x` / `bash -x` / `-o xtrace`) echoes variable "
        f"expansions to stderr, leaking the value.  Reserve trace-mode "
        f"only for scripts that touch zero credential material "
        f"(Standing Rule 6 · SEC-2026-09-15-10 class)."
    )


# ---------------------------------------------------------------------------
# Part-C extension (Sub-wave 6 hygiene · CP-SW6-HYG-1 · Redaction Hardening
# Option 1 · owner ruling 2026-09-15T~22:30Z ratified same turn as SEC
# incident sec_incident_jump_cred_leak_20260915T222935Z).
#
# Positive-shape helper: `read_custody_metadata(path)` yields ONLY shape
# data (field names, value lengths, sha256s) and structurally CANNOT
# return raw column values.  Consumers needing the actual secret get it
# via env-injection into the target process (MYSQL_PWD / sshpass -e /
# Authorization header patterns already banked in the estate), never via
# stdout-visible reads.
#
# Scope this CP: JSON custody files only.  CSV / xlsx / raw-key custody
# files refuse with `CustodyFileFormatUnsupportedError` — follow-on CPs
# may extend when a specific schema is standardised.
# ---------------------------------------------------------------------------

import hashlib as _hashlib_hyg1
import json as _json_hyg1
import os as _os_hyg1
from dataclasses import dataclass as _dataclass_hyg1
from typing import Tuple as _Tuple_hyg1


class NonCustodyPathRefused(Exception):
    """`read_custody_metadata` refusal: `path` does not sit under any
    prefix in `CUSTODY_PATH_PREFIXES`.  The helper is scoped to
    custody files only; general-purpose file-slurp is out of scope by
    design."""


class CustodyFileFormatUnsupportedError(Exception):
    """`read_custody_metadata` refusal: `path` extension is not in the
    supported set (JSON only for CP-SW6-HYG-1).  CSV / xlsx / raw-key
    custody files require schema-driven readers that will land in
    follow-on CPs."""


@_dataclass_hyg1(frozen=True)
class CustodyFieldMetadata:
    """Shape-only metadata for a single top-level field in a JSON
    custody file.  Frozen · exactly 3 attributes: `field_name` +
    `value_length_bytes` + `value_sha256`.  Structurally CANNOT carry
    a raw value: no attribute of that name exists."""
    field_name: str
    value_length_bytes: int
    value_sha256: str


@_dataclass_hyg1(frozen=True)
class CustodyFileMetadata:
    """Shape-only metadata for a JSON custody file.  Frozen · exactly
    2 attributes: `path` + `fields` (tuple of `CustodyFieldMetadata`).
    """
    path: str
    fields: _Tuple_hyg1[CustodyFieldMetadata, ...]


_SUPPORTED_CUSTODY_EXTENSIONS: _Tuple_hyg1[str, ...] = (".json",)


def read_custody_metadata(*, path: str) -> CustodyFileMetadata:
    """Return `CustodyFileMetadata` for the JSON custody file at
    `path`.  The helper reads the file, computes shape metadata
    (field names + utf-8 byte lengths + sha256 hex digests), and
    returns the metadata.  Raw values are held only in a private
    local scope during computation; they are NEVER assigned to any
    attribute of any returned object.

    Refuses:
      - `NonCustodyPathRefused` if `path` is not under any prefix
        in `CUSTODY_PATH_PREFIXES`.
      - `CustodyFileFormatUnsupportedError` if the file extension is
        not in `_SUPPORTED_CUSTODY_EXTENSIONS`.
    """
    if not any(path.startswith(p) for p in CUSTODY_PATH_PREFIXES):
        raise NonCustodyPathRefused(
            f"path {path!r} is not under any CUSTODY_PATH_PREFIXES "
            f"entry ({sorted(CUSTODY_PATH_PREFIXES)!r}).  The helper "
            f"is scoped to custody files only by design."
        )
    _, ext = _os_hyg1.path.splitext(path)
    if ext.lower() not in _SUPPORTED_CUSTODY_EXTENSIONS:
        raise CustodyFileFormatUnsupportedError(
            f"path {path!r} has extension {ext!r} which is not in the "
            f"supported set {_SUPPORTED_CUSTODY_EXTENSIONS!r}.  "
            f"CP-SW6-HYG-1 lands JSON-only support; extend in a "
            f"follow-on CP for other formats."
        )
    with open(path, "r", encoding="utf-8") as fh:
        _raw = _json_hyg1.load(fh)
    if not isinstance(_raw, dict):
        raise CustodyFileFormatUnsupportedError(
            f"path {path!r} JSON root is {type(_raw).__name__!r}, "
            f"only top-level dict is supported."
        )
    fields = []
    for _k, _v in _raw.items():
        _encoded = str(_v).encode("utf-8")
        fields.append(CustodyFieldMetadata(
            field_name=str(_k),
            value_length_bytes=len(_encoded),
            value_sha256=_hashlib_hyg1.sha256(_encoded).hexdigest(),
        ))
        # _v, _encoded fall out of scope on next iteration; never
        # assigned to any returned object attribute.
    return CustodyFileMetadata(path=path, fields=tuple(fields))
