"""tools/rms_creds_loader_v2.py — adapted loader for the 2026-09-21T14 drop.

New drop shape (sha `3311dae2…`):
    * Single sheet: `Sheet1`
    * 5-column data layout: [schema, host, user, password, tag]
    * MySQL clusters only (no NAS / JUMP / RADIO / Huawei tabs)
    * 7 clusters with creds + 1 without (row 33 host + no user/password)
    * One RADIO-shaped anomaly row (row 58: 3 cells only)

Discipline:
    * Values held in memory only.
    * `describe()` emits only <cred len=N> shape.
    * NEVER prints raw values.

Delta from old loader:
    * JUMP + RADIO + NAS + Huawei not in new sheet → this v2 loader
      falls back to the OLD sheet path for those (via LEGACY_SHEET_PATH)
      to keep JUMP tunnel operable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import openpyxl


PRIMARY_SHEET_PATH = Path(
    "/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx"
)
LEGACY_SHEET_PATH = Path(
    "/app/assessment_workspace/custody/credentials/prior_baseline/"
    "d778eb1e_prior_baseline.xlsx"
)  # Populated at install-time by the install helper.


@dataclass
class HostCred:
    label: str
    host: str
    user: str
    password: str

    def describe(self) -> dict:
        return {"label": self.label, "host": self.host,
                "user_len": len(self.user),
                "user_prefix2": self.user[:2],
                "password_len": len(self.password)}


@dataclass
class MySQLCluster:
    section: str
    host: str
    user: str
    password: str
    schemas: List[str] = field(default_factory=list)
    tag: str = ""

    def describe(self) -> dict:
        return {"section": self.section, "host": self.host,
                "user_len": len(self.user),
                "user_prefix2": self.user[:2],
                "password_len": len(self.password),
                "schemas": list(self.schemas),
                "tag": self.tag}


@dataclass
class NASSite:
    dsm_url: str
    user: str
    password: str
    navigation_steps: List[str] = field(default_factory=list)
    channel_registry: List[dict] = field(default_factory=list)

    def describe(self) -> dict:
        return {"dsm_url": self.dsm_url,
                "user_len": len(self.user),
                "password_len": len(self.password),
                "n_navigation_steps": len(self.navigation_steps),
                "n_channels_registered": len(self.channel_registry)}


@dataclass
class RmsBindDetails:
    jump: HostCred
    radio: HostCred
    nas: NASSite
    mysql_clusters: List[MySQLCluster]
    provenance: Dict[str, str]


IPV4_RX = re.compile(r"^\s*(?:\d{1,3}\.){3}\d{1,3}\s*$")


def _classify_row(cells) -> str:
    """Classify a row without exposing values.

    Returns one of: EMPTY / SECTION_HEADER / COL_HEADER / CLUSTER_ROW /
    SCHEMA_ROW / HOST_ONLY_ROW / RADIO_ROW / OTHER.
    """
    non_empty = [(i, c) for i, c in enumerate(cells) if c and str(c).strip()]
    if not non_empty:
        return "EMPTY"
    positions = [i for i, _ in non_empty]

    def _first_char_bucket(v):
        s = str(v or "").strip()
        if not s: return "EMPTY"
        c = s[0]
        if c.isupper(): return "UPPER"
        if c.islower(): return "LOWER"
        if c.isdigit(): return "DIGIT"
        return "SYM"

    # Column-header row: 5+ cells AND col2 (user col) begins UPPER — real
    # usernames are lowercase in this sheet family; the header row has
    # "USERNAME"/"PASSWORD" labels (both UPPER).
    if len(non_empty) >= 5:
        col1_val = str(cells[1] or "")
        col2_bkt = _first_char_bucket(cells[2])
        col3_bkt = _first_char_bucket(cells[3])
        if col2_bkt == "UPPER" and col3_bkt == "UPPER":
            return "COL_HEADER"
        # Data row: col 1 is IPv4 OR short UPPER placeholder, AND col 2
        # is a lower-case user.
        if IPV4_RX.match(col1_val):
            return "CLUSTER_ROW"
        if col1_val and len(col1_val) <= 6 and col1_val.isupper() and col2_bkt == "LOWER":
            return "CLUSTER_ROW_HOST_PLACEHOLDER"
        return "OTHER"

    if positions == [0]:
        return "SCHEMA_ROW"

    if positions == [0, 1]:
        col1_val = str(cells[1])
        if IPV4_RX.match(col1_val):
            return "HOST_ONLY_ROW"
        return "OTHER"

    if positions == [0, 1, 2]:
        col0_val = str(cells[0])
        if IPV4_RX.match(col0_val):
            return "RADIO_ROW"
        return "OTHER"

    return "OTHER"


def load() -> RmsBindDetails:
    provenance = {
        "primary_path": str(PRIMARY_SHEET_PATH),
        "primary_sha256_first_16": "",
        "legacy_path_used_for_jump_nas_radio": str(LEGACY_SHEET_PATH),
        "legacy_present": LEGACY_SHEET_PATH.is_file(),
    }

    wb = openpyxl.load_workbook(PRIMARY_SHEET_PATH, data_only=True)

    # If the primary sheet has the new single-sheet shape, use v2 parse.
    # If it still has the old 3-tab shape, fall through to v1 parse.
    is_new_shape = ("Sheet1" in wb.sheetnames
                    and "NAS creds" not in wb.sheetnames)

    mysql_clusters: List[MySQLCluster] = []
    radio_from_new: Optional[HostCred] = None

    if is_new_shape:
        ws = wb["Sheet1"]
        rows = list(ws.iter_rows(values_only=True))
        current: Optional[MySQLCluster] = None
        current_section = ""

        for i, r in enumerate(rows):
            cells = list(r) + [None] * (7 - len(r))
            kind = _classify_row(cells)

            if kind == "EMPTY":
                continue
            if kind == "COL_HEADER":
                # Ignore column headers (never emit values into receipts).
                continue

            if kind == "SCHEMA_ROW":
                # Bare text at col 0. Could be section header (isupper()) or
                # a schema name attached to the previous cluster.
                v = str(cells[0]).strip()
                if v.isupper() and len(v) <= 22 and current is not None:
                    # New section title following the previous cluster.
                    current_section = v
                    current = None
                elif v.isupper() and len(v) <= 22 and current is None:
                    current_section = v
                else:
                    if current is not None:
                        current.schemas.append(v)
                    # If no current cluster and it's lowercase, hold as a
                    # dangling schema note attached to the LAST section.
                continue

            if kind in ("CLUSTER_ROW", "CLUSTER_ROW_HOST_PLACEHOLDER"):
                schema0 = str(cells[0] or "").strip()
                host = str(cells[1] or "").strip()
                user = str(cells[2] or "").strip()
                password = str(cells[3] or "").strip()
                tag = str(cells[4] or "").strip()
                current = MySQLCluster(
                    section=current_section or "unknown",
                    host=host, user=user, password=password,
                    schemas=[schema0] if schema0 else [],
                    tag=tag,
                )
                mysql_clusters.append(current)
                continue

            if kind == "HOST_ONLY_ROW":
                # A cluster with schema + IP but no user/password.
                schema0 = str(cells[0] or "").strip()
                host = str(cells[1] or "").strip()
                current = MySQLCluster(
                    section=current_section or "unknown",
                    host=host, user="", password="",
                    schemas=[schema0] if schema0 else [],
                    tag="",
                )
                mysql_clusters.append(current)
                continue

            if kind == "RADIO_ROW":
                # 3-cell row: [IP, user, password] — Radio News System
                host = str(cells[0] or "").strip()
                user = str(cells[1] or "").strip()
                password = str(cells[2] or "").strip()
                radio_from_new = HostCred(
                    label="Radio news system", host=host,
                    user=user, password=password,
                )
                continue

            # Otherwise: skip
    else:
        # Fall through: reuse the legacy v1 loader semantics directly.
        import sys as _sys
        _sys.path.insert(0, "/app/assessment_workspace/tools")
        import importlib
        L = importlib.import_module("rms_creds_loader")
        _prior = L.SHEET_PATH
        L.SHEET_PATH = PRIMARY_SHEET_PATH
        binds = L.load()
        L.SHEET_PATH = _prior
        provenance["fallback"] = "primary_sheet_is_old_shape_used_v1_loader"
        return RmsBindDetails(
            jump=binds.jump, radio=binds.radio, nas=binds.nas,
            mysql_clusters=binds.mysql_clusters,
            provenance=provenance,
        )

    # For JUMP + NAS + (Radio if new sheet didn't carry it): use legacy.
    jump_hc = None
    nas_site = None
    radio_hc = radio_from_new
    if LEGACY_SHEET_PATH.is_file():
        import sys as _sys
        _sys.path.insert(0, "/app/assessment_workspace/tools")
        import importlib
        L = importlib.import_module("rms_creds_loader")
        _prior = L.SHEET_PATH
        L.SHEET_PATH = LEGACY_SHEET_PATH
        try:
            legacy = L.load()
            jump_hc = legacy.jump
            nas_site = legacy.nas
            if radio_hc is None:
                radio_hc = legacy.radio
            provenance["jump_source"] = "LEGACY_SHEET"
            provenance["nas_source"] = "LEGACY_SHEET"
            if radio_from_new is None:
                provenance["radio_source"] = "LEGACY_SHEET"
            else:
                provenance["radio_source"] = "NEW_SHEET"
        finally:
            L.SHEET_PATH = _prior

    if jump_hc is None:
        jump_hc = HostCred(label="Jump Server", host="", user="", password="")
        provenance["jump_source"] = "MISSING"
    if nas_site is None:
        nas_site = NASSite(dsm_url="", user="", password="")
        provenance["nas_source"] = "MISSING"
    if radio_hc is None:
        radio_hc = HostCred(label="Radio news system", host="", user="", password="")
        provenance["radio_source"] = "MISSING"

    return RmsBindDetails(
        jump=jump_hc, radio=radio_hc, nas=nas_site,
        mysql_clusters=mysql_clusters, provenance=provenance,
    )


def describe_all() -> dict:
    b = load()
    return {
        "provenance": b.provenance,
        "jump": b.jump.describe(),
        "radio": b.radio.describe(),
        "nas": b.nas.describe(),
        "mysql_clusters": [c.describe() for c in b.mysql_clusters],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(describe_all(), indent=2))
