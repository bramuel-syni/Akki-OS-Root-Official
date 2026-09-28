"""services.platform_control_plane.theme_entity — CP-P5-CP6 · M9.

Theme carrier + preventive-charter refusal wrappers per Akki OS
Pilot Platform Reference v0.2:

- §10 verbatim: theme (id, tenant_id, tokens, updated_by, updated_at).
- §8.3 M-W-3 verbatim: Theme tokens fixed set:
    logo_primary, logo_mark, colour_primary, colour_accent,
    mode ∈ {light, dark, user_choice},
    display_name (≤40 chars), login_message (≤200 chars),
    email_sender_name.
- Row 201: Refusal on unknown token / oversized-logo (>512KB) /
  >40-char display_name / >200-char login_message. WCAG-AA-refusal
  CONTRACT-MODELED.

Vocabulary:
- THEME_TOKEN_NAMES 8-tuple verbatim.
- THEME_MODE_VALUES ("light", "dark", "user_choice") verbatim.
- LOGO_MAX_BYTES = 524288 (512 * 1024).
- DISPLAY_NAME_MAX_CHARS = 40.
- LOGIN_MESSAGE_MAX_CHARS = 200.

Refusals:
- unknown token name → UnknownThemeTokenRefused
- unknown mode value → UnknownThemeModeRefused
- logo > 512KB → OversizedLogoRefused
- display_name > 40 → DisplayNameTooLongRefused
- login_message > 200 → LoginMessageTooLongRefused

WCAG-AA refusal is CONTRACT-MODELED · not shape-enforced here.

Standing-line proof:
- 4 str + 1 tuple[tuple[str,str],...] · 5 fields exact-order.
- Zero closed enum type · zero domain tokens · zero data-plane imports.
"""
from __future__ import annotations

import dataclasses
from typing import Tuple


THEME_ENTITY_ANCHOR = (
    "Akki OS Pilot Platform Reference v0.2 (17 September 2026) §10 "
    "verbatim: theme (id, tenant_id, tokens, updated_by, "
    "updated_at). §8.3 M-W-3 verbatim: Theme tokens fixed set: "
    "logo_primary, logo_mark, colour_primary, colour_accent, mode "
    "∈ {light, dark, user_choice}, display_name (≤40 chars), "
    "login_message (≤200 chars), email_sender_name. Row 201 "
    "refusals: unknown token / oversized-logo (>512KB) / >40-char "
    "display_name / >200-char login_message. WCAG-AA-refusal "
    "CONTRACT-MODELED."
)


# §8.3 M-W-3 verbatim 8-token set.
THEME_TOKEN_NAMES: Tuple[str, ...] = (
    "logo_primary",
    "logo_mark",
    "colour_primary",
    "colour_accent",
    "mode",
    "display_name",
    "login_message",
    "email_sender_name",
)


# §8.3 M-W-3 verbatim mode vocabulary.
THEME_MODE_VALUES: Tuple[str, ...] = (
    "light",
    "dark",
    "user_choice",
)


# Row 201 verbatim numeric ceilings.
LOGO_MAX_BYTES: int = 524288  # 512 KB · Row 201 verbatim
DISPLAY_NAME_MAX_CHARS: int = 40  # §8.3 verbatim
LOGIN_MESSAGE_MAX_CHARS: int = 200  # §8.3 verbatim


@dataclasses.dataclass(frozen=True)
class ThemeEntity:
    """Frozen carrier for the control-plane theme record.

    Exact-order 5 fields (4 str + 1 tuple):
    - id · theme record id.
    - tenant_id · owning tenant (ownership isolation index 1).
    - tokens · tuple of (token_name, token_value) OPEN pairs
      (composes with THEME_TOKEN_NAMES vocabulary).
    - updated_by · user_id ref.
    - updated_at · ISO-8601 UTC 'Z' str.
    """
    id: str
    tenant_id: str
    tokens: Tuple[Tuple[str, str], ...]
    updated_by: str
    updated_at: str


THEME_ENTITY_FIELDS: Tuple[str, ...] = (
    "id",
    "tenant_id",
    "tokens",
    "updated_by",
    "updated_at",
)


class ThemeEntityRefused(Exception):
    """Root refusal for theme-entity invariants."""


class UnknownThemeTokenRefused(ThemeEntityRefused):
    """Refused: token name not in THEME_TOKEN_NAMES (case-sensitive).
    §8.3 M-W-3 verbatim: Theme tokens fixed set."""


class UnknownThemeModeRefused(ThemeEntityRefused):
    """Refused: mode value not in THEME_MODE_VALUES (case-sensitive).
    §8.3 M-W-3 verbatim: mode ∈ {light, dark, user_choice}."""


class OversizedLogoRefused(ThemeEntityRefused):
    """Refused: logo bytes > LOGO_MAX_BYTES (Row 201 verbatim 512KB)."""


class DisplayNameTooLongRefused(ThemeEntityRefused):
    """Refused: display_name > DISPLAY_NAME_MAX_CHARS (§8.3 40 chars)."""


class LoginMessageTooLongRefused(ThemeEntityRefused):
    """Refused: login_message > LOGIN_MESSAGE_MAX_CHARS (§8.3 200 chars)."""


def assert_token_names_admissible(
    *, tokens: Tuple[Tuple[str, str], ...],
) -> None:
    """Preventive-charter refusal wrapper for token names.

    Refuses UnknownThemeTokenRefused when any token_name in the
    (token_name, token_value) pairs is not in THEME_TOKEN_NAMES
    (case-sensitive). Returns None on admit."""
    known = frozenset(THEME_TOKEN_NAMES)
    for name, _val in tokens:
        if name not in known:
            raise UnknownThemeTokenRefused(
                f"unknown-theme-token refused: token name not "
                f"among {len(THEME_TOKEN_NAMES)} §8.3 tokens "
                f"(case-sensitive)."
            )
    return None


def assert_theme_mode_admissible(*, mode_value: str) -> None:
    """Preventive-charter refusal wrapper for mode token value."""
    if mode_value not in frozenset(THEME_MODE_VALUES):
        raise UnknownThemeModeRefused(
            f"unknown-theme-mode refused: mode value not among "
            f"{len(THEME_MODE_VALUES)} §8.3 values (case-sensitive)."
        )
    return None


def assert_logo_size_admissible(*, logo_bytes_len: int) -> None:
    """Preventive-charter refusal wrapper for logo size."""
    if logo_bytes_len > LOGO_MAX_BYTES:
        raise OversizedLogoRefused(
            f"oversized-logo refused: bytes exceed "
            f"{LOGO_MAX_BYTES}-byte Row 201 ceiling."
        )
    return None


def assert_display_name_admissible(*, display_name: str) -> None:
    """Preventive-charter refusal wrapper for display_name length."""
    if len(display_name) > DISPLAY_NAME_MAX_CHARS:
        raise DisplayNameTooLongRefused(
            f"display-name-too-long refused: length exceeds "
            f"{DISPLAY_NAME_MAX_CHARS}-char §8.3 ceiling."
        )
    return None


def assert_login_message_admissible(*, login_message: str) -> None:
    """Preventive-charter refusal wrapper for login_message length."""
    if len(login_message) > LOGIN_MESSAGE_MAX_CHARS:
        raise LoginMessageTooLongRefused(
            f"login-message-too-long refused: length exceeds "
            f"{LOGIN_MESSAGE_MAX_CHARS}-char §8.3 ceiling."
        )
    return None


__all__ = [
    "THEME_ENTITY_ANCHOR",
    "THEME_TOKEN_NAMES",
    "THEME_MODE_VALUES",
    "LOGO_MAX_BYTES",
    "DISPLAY_NAME_MAX_CHARS",
    "LOGIN_MESSAGE_MAX_CHARS",
    "THEME_ENTITY_FIELDS",
    "ThemeEntity",
    "ThemeEntityRefused",
    "UnknownThemeTokenRefused",
    "UnknownThemeModeRefused",
    "OversizedLogoRefused",
    "DisplayNameTooLongRefused",
    "LoginMessageTooLongRefused",
    "assert_token_names_admissible",
    "assert_theme_mode_admissible",
    "assert_logo_size_admissible",
    "assert_display_name_admissible",
    "assert_login_message_admissible",
]
