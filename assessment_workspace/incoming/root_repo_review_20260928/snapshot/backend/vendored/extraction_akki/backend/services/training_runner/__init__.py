"""services.training_runner · Doc 17 lines 15, 55, 88-101 · trainer runner.

Modality-agnostic runner per Doc 17 line 88 verbatim (grounding brief
line 58): 'plus a modality-agnostic runner service (roughly 2,000-3,000
LOC)'. CP8 lands the shell + mock-SSH seam path; live-material
execution flips on Owner SSH key arrival (`GPU_CONNECT_MODE=real`).

Package layout:
  * ssh_seam.py       · mock/real SSH toggle (owner-key-blocked · CP8 lands mock).
  * moac_emitter.py   · six-check MOAC card emission (Doc 17 line 90).
  * runner.py         · orchestration: admit -> open -> mock_train ->
                        emit_moac -> whitepaper on close.
  * persistence.py    · write-once JSONL for admits + runs.

Ship-Manifest DoD path: endpoints hang off the existing
services/training/router.py (already wired at pod_shell/backend/
server.py) - no new router file introduced. That keeps
KNOWN_UNWIRED and mirror byte-match invariants untouched.
"""
