"""services.output_verified_seal — W0 Integrity Fix (2026-09-13).

Owner directive verbatim ("BUILD GO", 2026-09-13):

    "W0 (Integrity Fix): Fix the "silent success" defect by parsing
    `Kind:` in seal files at 6 code sites, introduce `output_verified_seal`,
    and add "ALIVE IS NOT DONE" standing order."

Standing order (STATE/STANDING_ORDERS.md §6, verbatim):

    ALIVE IS NOT DONE. The existence of a heartbeat, a running PID, a
    directory on disk, or a filename in that directory is NOT proof of
    completion. Completion requires an OUTPUT ARTIFACT — a seal file
    whose contents, when parsed, prove the specific real work-kind that
    just finished.

Contract:

  A "real seal" is a file that
    (a) exists at the canonical `ACTIVITY_SUMMARY.md` path
        (case-insensitive), AND
    (b) carries a `Kind:` line in its body, AND
    (c) whose `Kind:` value names a real-work kind — NOT `stub`,
        `synthetic`, `unfinished`, `test_fixture`, or empty.

Primitives:
    parse_seal(run_dir)   → Optional[dict]  · returns parsed fields or None
    is_real_seal(run_dir) → bool           · the integrity gate
    output_verified_seal(run_dir, *, kind, body) → Path · the write path

Freeze invariant: `tests/invariants/test_output_verified_seal.py`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, Optional


SEALING_FILENAME = "ACTIVITY_SUMMARY.md"

# Kinds that MUST NOT be promoted to a real-work seal. Empty string is
# also banned (an unset kind = not real). This set is closed by owner
# order 2026-09-13; extending it requires a DECISIONS.md entry.
NON_REAL_KINDS = frozenset({
    "stub",
    "synthetic",
    "unfinished",
    "test_fixture",
    "",
})


def _find_seal_file(run_dir: Path) -> Optional[Path]:
    """Case-insensitive resolution of the seal file inside `run_dir`.

    Matches the W-Campaign-Infra r3 normalization (any case of
    ACTIVITY_SUMMARY.md is accepted on read). Returns the resolved
    Path if found, else None.
    """
    if not run_dir.exists() or not run_dir.is_dir():
        return None
    target = SEALING_FILENAME.lower()
    for entry in run_dir.iterdir():
        if entry.is_file() and entry.name.lower() == target:
            return entry
    return None


def parse_seal(run_dir: Path) -> Optional[Dict[str, str]]:
    """Parse the seal file inside `run_dir`.

    Returns a dict of {field_lowercase: value} if the file exists AND
    carries a `Kind:` line. Returns None if the file is missing,
    unreadable, or does not carry a `Kind:` line.

    Rationale: a seal without a `Kind:` line is exactly the silent-
    success defect this module fixes — it MUST NOT parse to a
    truthy dict.

    Field names are lowercased so callers can read `parsed["kind"]`
    regardless of the writer's casing.
    """
    seal_path = _find_seal_file(Path(run_dir))
    if seal_path is None:
        return None

    try:
        text = seal_path.read_text(encoding="utf-8")
    except OSError:
        return None

    fields: Dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        # Only accept a bare-word key (no spaces). Section headings
        # like "# Campaign run activity summary" are skipped by the
        # ':' check above.
        if not key or " " in key:
            continue
        fields[key.lower()] = value.strip()

    # A seal without `Kind:` is not a real seal — return None so the
    # gate is unambiguous.
    if "kind" not in fields:
        return None

    return fields


def is_real_seal(run_dir: Path) -> bool:
    """The integrity gate. Returns True iff:
        (a) the seal file exists at `run_dir`,
        (b) the seal carries a `Kind:` line, AND
        (c) the `Kind:` value is NOT in NON_REAL_KINDS.
    """
    parsed = parse_seal(Path(run_dir))
    if parsed is None:
        return False
    kind = parsed.get("kind", "")
    if kind in NON_REAL_KINDS:
        return False
    return True


def output_verified_seal(
    run_dir: Path,
    *,
    kind: str,
    body: Optional[Mapping[str, Any]] = None,
) -> Path:
    """Write a seal file that will be admitted by `is_real_seal`.

    Args:
        run_dir: directory where the seal file will be written. Created
            if missing.
        kind: real-work kind name. MUST NOT be in NON_REAL_KINDS (else
            ValueError). Emitted as `Kind: <kind>` at the top of the
            body (below the section heading).
        body: additional key/value pairs to include in the seal body.
            Values are stringified verbatim. Order preserved.

    Returns:
        Path to the written seal file.

    Raises:
        ValueError: if `kind` is empty, whitespace-only, or in
            NON_REAL_KINDS.
    """
    if not isinstance(kind, str) or not kind.strip():
        raise ValueError(
            "output_verified_seal refuses empty kind — 'ALIVE IS NOT "
            "DONE': every seal must name a real work-kind"
        )
    if kind in NON_REAL_KINDS:
        raise ValueError(
            f"output_verified_seal refuses banned kind {kind!r} "
            f"(NON_REAL_KINDS = {sorted(NON_REAL_KINDS)}). "
            "A seal with this kind would fail is_real_seal by design."
        )

    d = Path(run_dir)
    d.mkdir(parents=True, exist_ok=True)

    lines = ["# Campaign run activity summary", "", f"Kind: {kind}"]
    if body:
        for key, value in body.items():
            lines.append(f"{key}: {value}")

    seal_path = d / SEALING_FILENAME
    seal_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return seal_path


__all__ = [
    "SEALING_FILENAME",
    "NON_REAL_KINDS",
    "parse_seal",
    "is_real_seal",
    "output_verified_seal",
]
