"""W-AUDIO-POC · CP-A6 · Wave close composite.

Frozen constants that mirror the state-side output-verified seal at
`phase0/output_verified_seals/audio_poc_v1.seal.txt`.  Any drift
between this module and the on-disk seal is a wave-integrity defect;
the CP-A6 invariants ensure the constants stay pinned.
"""

from __future__ import annotations


WAVE_NAME: str = "W-AUDIO-POC"

SEAL_KIND: str = "audio_poc_wave_close"

CP_ORDER: tuple = ("CP-A1", "CP-A2", "CP-A3", "CP-A4", "CP-A5", "CP-A6")

MECHANISM_MODULES: tuple = (
    "readonly_nas_guard",
    "readonly_obs_guard",
    "release_gate",
    "recording_inventory",
    "transcript_inventory",
    "pairing_registry",
    "gap_set",
    "hf_transcribe",
    "gap_fill_writer",
    "wave_close",
)

# Blockers surfaced by the CP-A5 live HF Inference API probe on
# 2026-09-14.  Full disposition at `notes/W_AUDIO_POC_CP_A5_LIVE_
# PROBE_BLOCKER_20260914.md`.  These IDs are the escalation handles
# the owner-facing wave-close report references.
KNOWN_BLOCKERS: tuple = (
    "BLOCKER-HF-A5-01",   # HF model-hosting: whisper-small not on hf-inference provider
    "BLOCKER-HF-A5-02",   # NAS-to-bytes SMB fetch plumbing not landed this wave
    "BLOCKER-HF-A5-03",   # Release-gate verdicts R-7/R-15/R-16/R-17 PENDING on owner
)
