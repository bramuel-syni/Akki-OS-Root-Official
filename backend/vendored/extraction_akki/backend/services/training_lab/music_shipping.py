"""Ship the owner's labelled recordings from the media library to the GPU host for detector training. Owner custody both ends;
every file is digest-verified on arrival. Returns the manifest the worker verifies again before decoding."""
import os
import shlex
import tempfile

from services.media_library import storage, store as media
from services.training_lab import baseline


def labelled_items(tenant):
    items, _, pending = baseline.reference_set(tenant, {'unlabelled_library_audio': 'music', 'include_synthetic': False})
    rows = []
    for item in items:
        row = media.get(tenant, item['item_id'])
        if not row: continue
        rows.append({'item_id': item['item_id'], 'title': row['title'], 'label': item['label'], 'label_source': item['label_source'],
                     'file': f"{row['file_id']}{row['extension']}", 'sha256': row['sha256'], 'size_bytes': int(row['size_bytes']), 'storage_path': row['storage_path']})
    return rows, pending


def refs_dir():
    return f"{os.environ['M9_REMOTE_ROOT']}/music_refs"


def ship(host, manifest, progress=None):
    """SFTP each labelled recording that is not already present with the right digest."""
    from services.census_autonomy.remote_dispatch import _connect
    from services.training_runner.ssh_seam import execute_remote_command
    target = refs_dir()
    listing = execute_remote_command(host, f"mkdir -p {shlex.quote(target)} && cd {shlex.quote(target)} && sha256sum * 2>/dev/null || true", purpose='music_refs_inventory', timeout=120)
    present = {}
    for line in (listing.stdout_redacted or '').splitlines():
        parts = line.split()
        if len(parts) == 2: present[parts[1].lstrip('*')] = parts[0]
    todo = [m for m in manifest if present.get(m['file']) != m['sha256']]
    if not todo:
        return {'shipped': 0, 'already_present': len(manifest), 'bytes': 0}
    client, _ = _connect(host, 30)
    shipped = 0; total = 0
    try:
        sftp = client.open_sftp()
        for index, item in enumerate(todo):
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                response = storage.download(item['storage_path'])
                try:
                    for chunk in response.iter_content(1 << 16):
                        if chunk: temp.write(chunk)
                finally:
                    response.close()
                temp.flush()
                sftp.put(temp.name, f"{target}/{item['file']}")
            shipped += 1; total += item['size_bytes']
            if progress: progress(index + 1, len(todo))
        sftp.close()
    finally:
        client.close()
    check = execute_remote_command(host, f"cd {shlex.quote(target)} && sha256sum " + ' '.join(shlex.quote(m['file']) for m in todo), purpose='music_refs_verify', timeout=300)
    digests = {}
    for line in (check.stdout_redacted or '').splitlines():
        parts = line.split()
        if len(parts) == 2: digests[parts[1].lstrip('*')] = parts[0]
    bad = [m['item_id'] for m in todo if digests.get(m['file']) != m['sha256']]
    if bad:
        raise ValueError(f'SHIPPED_DIGEST_MISMATCH:{len(bad)}')
    return {'shipped': shipped, 'already_present': len(manifest) - len(todo), 'bytes': total}
