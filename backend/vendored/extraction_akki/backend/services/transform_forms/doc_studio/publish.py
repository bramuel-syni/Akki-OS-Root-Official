"""Publish the released estate pack as static downloads (owner order 2026-10-02): exact released bytes, independent of the API upstream."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from services.transform_forms.doc_studio import store

NAME = 'RMS_Estate_and_Language_Review'
PUBLIC = Path('/app/frontend/public/downloads')
MANIFEST = Path('/app/assessment_workspace/deliverables/estate_language_20261002/static_download_manifest.json')


def publish(tenant_id: str, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Copies docx/pptx/xlsx of the last released build to the static download paths; returns the manifest, or None when nothing is released."""
    build = next((b for b in reversed(record.get('builds') or []) if b['status'] == 'released'), None)
    if not build:
        return None
    bdir = store.build_dir(tenant_id, record['commission_id'], build['build_id']) / 'a' / 'out'
    PUBLIC.mkdir(parents=True, exist_ok=True)
    published = {'commission_id': record['commission_id'], 'build_id': build['build_id'], 'content_version': build['content_version'], 'published_at': record.get('updated_at'), 'files': {}}
    for out in build['outputs']:
        if out['format'] not in ('docx', 'pptx', 'xlsx'):
            continue
        dst = PUBLIC / f"{NAME}.{out['format']}"
        shutil.copyfile(bdir / out['name'], dst)
        published['files'][out['format']] = {'file': dst.name, 'bytes': dst.stat().st_size, 'sha256': hashlib.sha256(dst.read_bytes()).hexdigest(), 'source_sha256': out['sha256']}
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(published, indent=2) + '\n')
    return published
