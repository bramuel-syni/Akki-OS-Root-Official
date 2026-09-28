"""services.connect.human_speak · Pydantic → human-speak error translation.

Owner directive 2026-08-26 (Wave A · R2 verbatim):
    "errDetailToString replaced with a human-speak translation layer (raw
     Pydantic 422 shapes never reach the user; each failure names the field
     and the remedy in plain words). ... never 'String should have at
     least 1 character.'"

Grammar target (Canon 5 §9.2 verbatim from
`canon/text/Akki_Canon_5_Interface_Architecture.txt` lines 130-140):
    "Not to the standard you asked for. Accept as recorded statement ·
     Narrow the objective · Lower the standard. A refusal is the system
     keeping its promise. The title, the three actions, and the footer are
     binding copy, reproduced verbatim wherever this card renders. They
     are never paraphrased, shortened, or restyled for a particular
     surface."

The translator returns a structured shape the frontend renders:
    { "field": <field_name or "">, "remedy": <what to do next>,
      "plain": <one-sentence sentence in plain words> }

The frontend NEVER renders raw ValidationError shapes. The `plain` field is
the primary user-visible sentence; `field` names the offending field for
edit-in-place; `remedy` is the concrete step to unstick.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import ValidationError


# Ordered map of raw field names → plain-words nouns
_FIELD_HUMAN = {
    "host_name": "host name",
    "username": "username",
    "password": "password",
    "public_ip": "public IP",
    "private_ip": "private IP",
    "os": "operating system",
    "deploy_date": "deploy date",
    "cluster_arn": "cluster ARN",
    "secret_arn": "secret ARN",
    "region": "region",
    "database": "database name",
    "aws_access_key_id": "AWS access key id",
    "aws_secret_access_key": "AWS secret access key",
    "api_key": "API key",
    "name": "name",
    "kind": "kind",
    "draft_id": "draft id",
    "field": "field name",
    "value": "value",
}


def _humanize(field_name: str) -> str:
    return _FIELD_HUMAN.get(field_name, field_name.replace("_", " "))


def _remedy_for(kind: str, field_name: str) -> str:
    """Concrete step the operator can take, aware of the ceremony kind."""
    if field_name in {"password", "aws_secret_access_key", "api_key"}:
        return (
            "re-paste with the credential line included — the estate "
            "reads the paste one shot, and never keeps it after."
        )
    if field_name in {"host_name", "username", "public_ip", "private_ip",
                       "os", "deploy_date"}:
        return (
            "re-paste with a line labelled '" + _humanize(field_name)
            + "', or type the value into the drawer input."
        )
    if field_name in {"cluster_arn", "secret_arn", "region", "database"}:
        return (
            "re-paste including the '" + _humanize(field_name)
            + "' line, or type it into the drawer input."
        )
    return "provide a value for " + _humanize(field_name) + "."


def _plain_for_missing(field_name: str) -> str:
    """The plain sentence for an empty/missing field. Deliberately avoids
    the phrase 'String should have at least 1 character.'"""
    human = _humanize(field_name)
    return f"The {human} is empty."


def _plain_for_wrong_type(field_name: str, expected: str) -> str:
    human = _humanize(field_name)
    return f"The {human} is not the shape the estate expected."


def _first_error(errors: List[dict]) -> Optional[dict]:
    """Return the first error item — 'one question at a time' per SOLVA §5.6."""
    return errors[0] if errors else None


def translate_pydantic_error(exc: ValidationError, *, kind: str = "compute") -> Dict[str, str]:
    """Convert a Pydantic ValidationError into { field, remedy, plain }.

    The result is safe to render verbatim to the user; it will never contain
    Pydantic-internal phrases like 'String should have at least 1 character.'
    """
    errors = exc.errors() if hasattr(exc, "errors") else []
    first = _first_error(errors)
    if first is None:
        return {
            "field": "",
            "remedy": "Try re-pasting the details, or type them one by one.",
            "plain": "The estate couldn't accept that.",
        }

    # First loc segment (e.g. ("host_name",) or ("body", "host_name"))
    loc = first.get("loc", ())
    field_name = ""
    for seg in loc:
        if isinstance(seg, str) and seg not in {"body", "query", "path"}:
            field_name = seg
            break
    if not field_name and loc:
        field_name = str(loc[-1])

    err_type = first.get("type", "")
    if err_type in {"missing", "value_error.missing", "string_too_short",
                    "value_error.any_str.min_length"}:
        plain = _plain_for_missing(field_name)
    elif err_type.startswith("type_error") or err_type.startswith("value_error"):
        expected = first.get("expected", "the expected shape")
        plain = _plain_for_wrong_type(field_name, expected)
    else:
        plain = _plain_for_missing(field_name)

    return {
        "field": field_name,
        "remedy": _remedy_for(kind, field_name),
        "plain": plain,
    }


def missing_draft_error(draft_id: str) -> Dict[str, str]:
    """The human-speak 404 for a missing/expired draft.

    Never reveals internal reasons (expired vs never-existed) — both
    resolve the same way from the operator's view.
    """
    return {
        "field": "draft_id",
        "remedy": (
            "Open the Connect drawer again and re-paste — the estate "
            "keeps drafts for fifteen minutes, then lets them go."
        ),
        "plain": (
            "That draft is gone. Either it expired or it was already "
            "confirmed."
        ),
    }


def not_editable_error(field_name: str) -> Dict[str, str]:
    """Human-speak error for attempts to PATCH a secret field via the
    editable-field route (custody rule preserved)."""
    return {
        "field": field_name,
        "remedy": (
            "credentials are never edited in the URL. Re-open the drawer "
            "and paste again — the estate reads the paste one shot."
        ),
        "plain": (
            "The " + _humanize(field_name)
            + " is a credential and cannot be edited here."
        ),
    }
