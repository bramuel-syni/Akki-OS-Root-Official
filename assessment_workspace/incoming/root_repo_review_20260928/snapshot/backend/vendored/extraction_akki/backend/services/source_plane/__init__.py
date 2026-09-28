"""services.source_plane — Source-Plane primitives (W1b · CP2).

Contents:
  connector.py — SourceConnector Protocol + ReadOnlyGuard + shape types

Case-agnostic. No domain tokens in the Protocol or the guard. Concrete
implementations (CP3 Synology FileStation) live in sibling modules.
"""
from __future__ import annotations
