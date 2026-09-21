"""Cross-key read refusal for C.13 closure.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim: "cross-key reads
refused".

Public surface:
  - `assert_scoped_key_matches_expected(*, actual_key, expected_key)`:
    returns None on match · raises `CrossKeyReadRefused` on mismatch.
  - `CrossKeyReadRefused`: exception class · structural refusal type.

Canon 8 §W11 structural role separation: this module carries ONLY the
refusal predicate + exception type. No persistence · no learned surface
· no decision surface. AST-enforced by paired invariant test 8.

Structural discipline: identity string comparison. Refusal fires on any
non-identity between actual_key and expected_key, including differing
casing (both are expected to be lowercase-hex per derive_scoped_key
contract). Absence-of-key on either side also refuses.
"""
from __future__ import annotations


class CrossKeyReadRefused(Exception):
    """Structural refusal type raised when a read presents a
    scoped_key that does not identity-match the expected scoped_key
    bound at the write boundary.

    Per owner ruling 2026-09-19T~17:54Z item (b) verbatim: 'cross-key
    reads refused'.
    """


def assert_scoped_key_matches_expected(
    *,
    actual_key: str,
    expected_key: str,
) -> None:
    """Refuse cross-key reads by identity string comparison.

    Returns None on match. Raises CrossKeyReadRefused on any
    mismatch, including empty-string / None / differing casing.
    """
    if (
        not isinstance(actual_key, str)
        or not isinstance(expected_key, str)
        or not actual_key
        or not expected_key
        or actual_key != expected_key
    ):
        raise CrossKeyReadRefused(
            "cross-key read refused · actual_key does not identity-"
            "match expected_key at scoped_key boundary · owner ruling "
            "2026-09-19T~17:54Z item (b)"
        )
    return None
