"""Explicit connector selection, never automatic key/password fallback."""
import os
from services.gpu_direct.workbook import DirectConnectionError


def direct_enabled():
    mode = os.environ.get('AKKI_GPU_CONNECTION_MODE')
    if mode is None:
        return False  # Existing installations are unchanged until explicitly selected.
    if mode != 'direct_workbook':
        raise DirectConnectionError('DIRECT_CONNECTION_MODE_INVALID')
    return True