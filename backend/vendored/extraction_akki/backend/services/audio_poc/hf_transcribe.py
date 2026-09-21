"""W-AUDIO-POC · CP-A5 · HF-model gap-fill transcription.

Loads the HF token via `services.secret_hygiene.hf_token
.load_hf_token_or_raise` (env-only; no file fallback) and invokes the
HF Inference API for automatic speech recognition against the audio
bytes of a gap-set recording.

Emits a `GapFillTranscript` frozen dataclass carrying only shape
metadata (text length, sha256 hex) — never the raw transcript text.
The raw transcript bytes are handed to the write-back function
which passes them through the `services.secret_hygiene.hf_token
.assert_no_transcript_leak_of_active_token` guard before any OBS
PutObject is attempted.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

from services.secret_hygiene.hf_token import load_hf_token_or_raise


DEFAULT_HF_MODEL_ID: str = "openai/whisper-small"

# HF Inference API endpoint.  As of the CP-A5 live probe (2026-09-14
# 13:44Z), the legacy `api-inference.huggingface.co` is not resolvable
# from this container; the current router is `router.huggingface.co`
# under the `hf-inference` provider path.  Individual models must be
# hosted on the `hf-inference` provider — whisper-small returned
# HTTP 400 "Model not supported by provider hf-inference" at that
# probe, so gap-fill against whisper is BLOCKED at wave-close pending
# either (a) a different provider path (e.g. fal-ai/replicate) or
# (b) a self-hosted transcription server on akki-vm/akki-vm-ii.  See
# `notes/W_AUDIO_POC_CP_A5_LIVE_PROBE_BLOCKER_20260914.md`.
_HF_INFERENCE_ENDPOINT_TMPL: str = (
    "https://router.huggingface.co/hf-inference/models/{model_id}"
)
_HF_TIMEOUT_S: float = 60.0


class HFTranscribeError(Exception):
    """Base for all HF transcription failures."""


class HFTranscribeAuthError(HFTranscribeError):
    """401 / 403 from HF Inference API."""


class HFTranscribeRateLimit(HFTranscribeError):
    """429 from HF Inference API."""


@dataclass(frozen=True)
class GapFillTranscript:
    """Shape-only record of a completed gap-fill transcription.

    No raw text field.  Length + sha256 hex only.
    """

    recording_station: str
    recording_date_utc: str
    recording_slot: str
    recording_filename_stem: str
    transcript_text_len: int
    transcript_sha256_hex: str
    model_id: str
    elapsed_s_int: int


def transcribe_gap(
    audio_bytes: bytes,
    recording_station: str,
    recording_date_utc: str,
    recording_slot: str,
    recording_filename_stem: str,
    model_id: Optional[str] = None,
) -> "tuple[GapFillTranscript, bytes]":
    """Invoke HF Inference API on `audio_bytes`.

    Returns `(GapFillTranscript, transcript_body_bytes)`.  The caller
    routes `transcript_body_bytes` to `write_gap_transcript_or_refuse`
    which enforces the release-gate + transcript-leak guard.

    Refuses via `HFTranscribeError` if `audio_bytes` is empty (pre-
    flight structural check).  Refuses via `HFTokenEnvVarMissing` if
    the env-only loader has no token.
    """
    if not audio_bytes:
        raise HFTranscribeError("audio_bytes is empty; refusing to invoke HF")
    tok = load_hf_token_or_raise()  # env-only; raises HFTokenEnvVarMissing
    model = model_id or DEFAULT_HF_MODEL_ID
    url = _HF_INFERENCE_ENDPOINT_TMPL.format(model_id=model)
    req = urllib.request.Request(
        url,
        data=audio_bytes,
        headers={
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/octet-stream",
            "User-Agent": "akki-audio-poc/1.0",
        },
        method="POST",
    )
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=_HF_TIMEOUT_S) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise HFTranscribeAuthError(f"HF auth refused (HTTP {e.code})") from None
        if e.code == 429:
            raise HFTranscribeRateLimit("HF rate limit (HTTP 429)") from None
        raise HFTranscribeError(f"HF Inference API error (HTTP {e.code})") from None
    except Exception as e:
        raise HFTranscribeError(f"HF Inference API failure: {type(e).__name__}") from None
    elapsed_s = int(time.time() - started)
    # HF whisper returns JSON like {"text": "..."}.  Extract length only.
    try:
        parsed = json.loads(body.decode("utf-8"))
        text_len = len(parsed.get("text", ""))
    except Exception:
        text_len = 0
    sha = hashlib.sha256(body).hexdigest()
    gft = GapFillTranscript(
        recording_station=recording_station,
        recording_date_utc=recording_date_utc,
        recording_slot=recording_slot,
        recording_filename_stem=recording_filename_stem,
        transcript_text_len=text_len,
        transcript_sha256_hex=sha,
        model_id=model,
        elapsed_s_int=elapsed_s,
    )
    return gft, body
