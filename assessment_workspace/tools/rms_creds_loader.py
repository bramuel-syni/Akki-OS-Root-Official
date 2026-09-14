"""tools/rms_creds_loader.py — safe loader for the RMS Connection Creds sheet.

Discipline:

  * Values are held in memory only.
  * `describe()` / any print / receipt output MUST show `<cred len=N>`
    for every credential-shape field.
  * Values MAY be USED to open connections; they MUST NEVER be
    written into the transcript, into a log, or into a receipt file.

The loader parses three sheets:

  * "NAS creds"          → NAS DSM URL + NAS user + NAS password
  * "NAS Guide + Cred"   → JUMP + RADIO + admin step-by-step guidance
  * "Huawei Creds"       → 7 MySQL clusters (host + user + password)
                           with the DBs each cluster hosts.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import openpyxl


SHEET_PATH = Path(
    "/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx"
)


@dataclass
class HostCred:
    label: str
    host: str
    user: str
    password: str

    def describe(self) -> dict:
        return {
            "label": self.label,
            "host": self.host,
            "user_len": len(self.user),
            "user_prefix2": self.user[:2],
            "password_len": len(self.password),
        }


@dataclass
class MySQLCluster:
    section: str
    host: str
    user: str
    password: str
    schemas: List[str] = field(default_factory=list)

    def describe(self) -> dict:
        return {
            "section": self.section,
            "host": self.host,
            "user_len": len(self.user),
            "password_len": len(self.password),
            "schemas": list(self.schemas),
        }


@dataclass
class NASSite:
    dsm_url: str
    user: str
    password: str
    navigation_steps: List[str] = field(default_factory=list)
    channel_registry: List[dict] = field(default_factory=list)  # {channel, station, kind}

    def describe(self) -> dict:
        return {
            "dsm_url": self.dsm_url,
            "user_len": len(self.user),
            "password_len": len(self.password),
            "n_navigation_steps": len(self.navigation_steps),
            "n_channels_registered": len(self.channel_registry),
        }


@dataclass
class AdminGuidance:
    jump_lines: List[str] = field(default_factory=list)
    on_prem_step_lines: List[str] = field(default_factory=list)
    on_huawei_lines: List[str] = field(default_factory=list)


@dataclass
class RmsBindDetails:
    admin: AdminGuidance
    jump: HostCred
    radio: HostCred
    nas: NASSite
    mysql_clusters: List[MySQLCluster]


def _cells(ws) -> List[List[Optional[str]]]:
    """Return sheet as list of lists of string cells."""
    return [
        [str(c).strip() if c is not None else "" for c in row]
        for row in ws.iter_rows(values_only=True)
    ]


def load() -> RmsBindDetails:
    wb = openpyxl.load_workbook(SHEET_PATH, data_only=True)

    # ---- NAS creds sheet ----------------------------------------
    nas_sheet = _cells(wb["NAS creds"])
    nas_url = ""
    nas_user = ""
    nas_pass = ""
    nav_steps: List[str] = []
    channels: List[dict] = []
    in_channel_table = False
    for row in nas_sheet:
        first = row[0] if row else ""
        if first.startswith("http"):
            nas_url = first
        elif first.lower().startswith("username:"):
            nas_user = first.split(":", 1)[1].strip()
        elif first.lower().startswith("password:"):
            nas_pass = first.split(":", 1)[1].strip()
        elif re.match(r"^\d+\.", first):
            # numbered navigation step
            nav_steps.append(first)
        elif first == "Channel":
            in_channel_table = True
            continue
        elif in_channel_table and first and len(row) >= 3:
            channels.append({
                "channel": first,
                "station": row[1],
                "kind": row[2],
            })
    nas = NASSite(
        dsm_url=nas_url, user=nas_user, password=nas_pass,
        navigation_steps=nav_steps, channel_registry=channels,
    )

    # ---- NAS Guide + Cred sheet ---------------------------------
    guide_sheet = _cells(wb["NAS Guide + Cred"])
    # Col 0 holds JUMP + RADIO structured tuples; col 3 holds admin guidance.
    # Structure detected:
    #   rows 0..3 col0: JUMP block  = [host, user, password, label="Jump Server"]
    #   rows 7..10 col0: RADIO block = [host, user, password, label="Radio news system."]
    # Col 3 contains free-form admin guidance.
    jump_host = guide_sheet[0][0] if len(guide_sheet) > 0 else ""
    jump_user = guide_sheet[1][0] if len(guide_sheet) > 1 else ""
    jump_pass = guide_sheet[2][0] if len(guide_sheet) > 2 else ""
    jump = HostCred(label="Jump Server", host=jump_host,
                    user=jump_user, password=jump_pass)

    radio_host = guide_sheet[7][0] if len(guide_sheet) > 7 else ""
    radio_user = guide_sheet[8][0] if len(guide_sheet) > 8 else ""
    radio_pass = guide_sheet[9][0] if len(guide_sheet) > 9 else ""
    radio = HostCred(label="Radio news system.", host=radio_host,
                     user=radio_user, password=radio_pass)

    admin = AdminGuidance()
    for row in guide_sheet:
        if len(row) >= 4 and row[3]:
            text = row[3]
            if text == "Read me":
                continue
            # Free-form admin guidance — governance metadata, not secret.
            admin.on_prem_step_lines.append(text) if "prem" in text.lower() or "cifs" in text.lower() or "ssh" in text.lower() or "mysql" in text.lower() else admin.jump_lines.append(text)
            if "huawei" in text.lower() or "obs" in text.lower():
                admin.on_huawei_lines.append(text)

    # ---- Huawei Creds sheet -------------------------------------
    huawei_sheet = _cells(wb["Huawei Creds"])
    # Layout: sections separated by blank rows; first data row of a
    # section has host + user + password; subsequent rows list schemas
    # in col 0 only.
    clusters: List[MySQLCluster] = []
    current_section: Optional[str] = None
    current: Optional[MySQLCluster] = None
    # Skip header (row 0)
    for row in huawei_sheet[1:]:
        c0, c1, c2, c3 = (row + [""] * 4)[:4]
        if not any((c0, c1, c2, c3)):
            continue
        if c0 and not c1 and not c2 and not c3:
            # Could be a section title OR a schema-only row in current cluster
            if current is not None and re.search(r"[a-z]", c0):
                current.schemas.append(c0)
            else:
                current_section = c0
            continue
        if c1 and c2 and c3:
            # New cluster with host+user+password
            current = MySQLCluster(
                section=current_section or c0,
                host=c1, user=c2, password=c3,
                schemas=[c0] if c0 else [],
            )
            clusters.append(current)
            # After creating cluster, subsequent bare rows are its schemas
        elif c1 and not c2:
            # host on col1 but no user/password (WEEGO-style: creds implicit)
            current = MySQLCluster(
                section=current_section or c0,
                host=c1, user="", password="",
                schemas=[c0] if c0 else [],
            )
            clusters.append(current)

    return RmsBindDetails(
        admin=admin, jump=jump, radio=radio, nas=nas, mysql_clusters=clusters,
    )


def describe_all() -> dict:
    """Return a fully-redacted summary suitable for banking as a receipt."""
    b = load()
    return {
        "jump": b.jump.describe(),
        "radio": b.radio.describe(),
        "nas": b.nas.describe(),
        "mysql_clusters": [c.describe() for c in b.mysql_clusters],
        "admin_guidance_line_counts": {
            "jump_lines": len(b.admin.jump_lines),
            "on_prem_step_lines": len(b.admin.on_prem_step_lines),
            "on_huawei_lines": len(b.admin.on_huawei_lines),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(describe_all(), indent=2))
