"""CENSUS-3-F · OBS audio → GPU pipeline · read-only adapter package.

Per SO §6.8 clause A verbatim (2026-09-21T~18:35Z):
  "ingestion adapters under services/data_source/{source}_read_only/"

This package is the first landing under that directive.  Sibling adapter
packages (`digicow_s3_audio_read_only/`, `nas_smb_read_only/`,
`mysql_content_axis_read_only/`, etc.) follow the same shape when they
open in CENSUS-3-C/D/E.

Additive-only per SO §3.8 · no sealed code touched.
"""

from __future__ import annotations
