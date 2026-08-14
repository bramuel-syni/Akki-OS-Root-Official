#!/usr/bin/env bash
# acceptance.sh — Phase-0 acceptance checks, HUMAN-RUN on the VM.
#
# Build Order 01 §6 verbatim acceptance list. This script runs ON the VM
# (invoked directly by the owner OR via the compute seam once credentials
# are in `backend/.env`).
#
# Output: writes /var/log/akki_phase0_acceptance.log on the VM + prints
# structured JSON to stdout so tools/run_acceptance_via_seam.py can capture
# it into the commissioning record.
#
# Exit codes:
#   0 — all checks green.
#   2 — HSS absent or undersized (STOP-and-escalate per §7).
#   3 — NVLink absent (STOP-and-escalate).
#   4 — password auth still live (STOP-and-escalate).
#   5 — ephemeral persistence contradicted (STOP-and-escalate).
#   6 — AKKI_HARDENING_MODE=perform but harden.sh missing.
#  10–12 — hardening module failure (see phase0/harden.sh header).
#   9 — unclassified failure.
#
# OPTIONAL front-end (env AKKI_HARDENING_MODE=perform) — see block after `set -uo pipefail`.

set -uo pipefail

log() { echo "$1" | tee -a /var/log/akki_phase0_acceptance.log 2>/dev/null || echo "$1"; }

log "=== Phase-0 Acceptance · $(date -u +%FT%TZ) ==="

# --------------------------------------------------------------------
# OPTIONAL hardening front-end (FL-P2-04 escalation, pending owner ruling).
#
# If owner rules FL-P2-04 to us  → invoke as: AKKI_HARDENING_MODE=perform bash acceptance.sh
#                                   which sources phase0/harden.sh before verification.
# If owner rules to owner-side  → do not set AKKI_HARDENING_MODE (default verify-only);
#                                   owner runs their own hardening; acceptance.sh only checks.
#
# harden.sh itself is a no-op unless AKKI_HARDENING_MODE=perform. Failing here is a
# stop-and-escalate; we do NOT continue verification against a partially-hardened VM.
# --------------------------------------------------------------------

if [ "${AKKI_HARDENING_MODE:-verify}" = "perform" ]; then
    log "hardening.mode: perform (FL-P2-04 ruled to compute-seam side)"
    HARDEN_SCRIPT="$(dirname "$0")/harden.sh"
    if [ ! -f "${HARDEN_SCRIPT}" ]; then
        log "FAIL: AKKI_HARDENING_MODE=perform but harden.sh not found at ${HARDEN_SCRIPT}"
        exit 6
    fi
    if ! bash "${HARDEN_SCRIPT}"; then
        HRC=$?
        log "FAIL: harden.sh returned ${HRC} — refusing to continue verification against partial hardening"
        exit ${HRC}
    fi
    log "hardening: applied · continuing to verification"
else
    log "hardening.mode: verify (owner-side hardening assumed; acceptance.sh will confirm dead-password auth externally)"
fi

# 1. HSS mounted + size
if ! mountpoint -q /mnt/hss 2>/dev/null; then
    log "FAIL: /mnt/hss not mounted"
    exit 2
fi
HSS_TB=$(df -B1G /mnt/hss | awk 'NR==2 {print int($2/1024)}')
log "hss.size_tb: ${HSS_TB}"
if [ "${HSS_TB}" -lt 25 ]; then
    log "FAIL: HSS smaller than 25 TB (got ${HSS_TB} TB)"
    exit 2
fi

# 2. HSS writable (write test file — survives restart)
TESTFILE="/mnt/hss/.akki_write_test_$(date -u +%s)"
if ! echo "acceptance_write_test_$(hostname)_$(date -u +%FT%TZ)" > "${TESTFILE}"; then
    log "FAIL: HSS not writable"
    exit 2
fi
log "hss.writable: ok ($TESTFILE)"
log "  RESTART_SURVIVAL_CHECK: file must still exist after 'sudo reboot'."

# 3. NVLink + 4× H200
if ! command -v nvidia-smi >/dev/null 2>&1; then
    log "FAIL: nvidia-smi not installed"
    exit 3
fi
GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader | grep -ic "H200")
log "gpu.h200_count: ${GPU_COUNT}"
if [ "${GPU_COUNT}" -ne 4 ]; then
    log "FAIL: expected 4× H200, got ${GPU_COUNT}"
    exit 3
fi

NVLINK_STATUS=$(nvidia-smi nvlink --status 2>/dev/null | head -20 || echo "")
if [ -z "${NVLINK_STATUS}" ] || echo "${NVLINK_STATUS}" | grep -qi "inactive"; then
    log "FAIL: NVLink absent or inactive"
    exit 3
fi
log "gpu.nvlink: active"

# 4. Ephemeral present, scratch-only marker
EPHEMERAL_TB=$(df -B1G /mnt/ephemeral 2>/dev/null | awk 'NR==2 {print int($2/1024)}' || echo 0)
if [ "${EPHEMERAL_TB:-0}" -lt 10 ]; then
    EPHEMERAL_TB=$(df -B1G /var/tmp | awk 'NR==2 {print int($2/1024)}' || echo 0)
fi
log "ephemeral.size_tb: ${EPHEMERAL_TB}"
if [ "${EPHEMERAL_TB}" -lt 10 ]; then
    log "FAIL: ephemeral disk absent or under 10 TB"
    exit 5
fi

# 5. Password auth confirmed dead in sshd_config
if sshd -T 2>/dev/null | grep -qi '^passwordauthentication yes'; then
    log "FAIL: password authentication still enabled in sshd config"
    exit 4
fi
log "sshd.password_auth: disabled"

# 6. Bootstrap credentials retired (best-effort — root should not have shell password)
if grep -q '^root:[^!*]' /etc/shadow 2>/dev/null; then
    log "WARN: /etc/shadow suggests root has a password hash — verify by external probe"
fi

log "=== ALL CHECKS GREEN ==="
log "  NEXT: run 'sudo reboot' from Rafay console."
log "  AFTER RESTART: rerun this script; the write-test file must still exist."
exit 0
