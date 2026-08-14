#!/usr/bin/env bash
# harden.sh — OPTIONAL Phase-0 hardening module.
#
# Runs ONLY if AKKI_HARDENING_MODE=perform is set on the VM.
# Designed for both FL-P2-04 outcomes:
#   - Owner rules hardening to us  → invoked via `AKKI_HARDENING_MODE=perform bash acceptance.sh`.
#   - Owner rules hardening to owner-side hands → this script is never invoked;
#     acceptance.sh runs in verify-only mode; owner hardens externally.
#
# Governance:
#   - Idempotent: safe to re-run; every action checks state first.
#   - Fail-closed: exits non-zero on the first check that cannot be satisfied.
#     Downstream acceptance.sh verification catches any post-hardening drift.
#   - Never runs on-VM without an SSH key already installed in the target user's
#     authorized_keys (would lock out administrators).
#   - Never in scope: SKU selection, HSS provisioning — those are Order §6
#     bindings frozen at BUILD_STRATEGY.md and phase0/commissioning_checklist.md.
#
# Actions (in fail-closed order):
#   1. Verify SSH_AUTHORIZED_KEY was previously installed under target user
#      (otherwise refuse — hardening would strand admin access).
#   2. Disable PasswordAuthentication in sshd_config.
#   3. Disable ChallengeResponseAuthentication (PAM password path).
#   4. Restart sshd (systemctl or service, whichever exists).
#   5. Retire bootstrap credentials (lock the initial user password if present).
#   6. Emit a hardening receipt to /var/log/akki_phase0_hardening.log so the
#      acceptance.sh verification step reads a ledger-visible artifact.
#
# Exit codes (mirror acceptance.sh taxonomy):
#   0  — hardening applied cleanly (or already in place; idempotent no-op).
#   10 — refusing: SSH key not installed for target user (would lock admin).
#   11 — sshd_config not writable or restart failed.
#   12 — bootstrap credential retirement failed.

set -uo pipefail

# --------------------------------------------------------------------
# Governance guards
# --------------------------------------------------------------------

if [ "${AKKI_HARDENING_MODE:-}" != "perform" ]; then
    echo "harden.sh: AKKI_HARDENING_MODE!=perform → SKIP (verify-only)."
    exit 0
fi

HARDEN_TARGET_USER="${HARDEN_TARGET_USER:-ubuntu}"
LOG=/var/log/akki_phase0_hardening.log
touch "${LOG}" 2>/dev/null || LOG=/tmp/akki_phase0_hardening.log
log() { echo "$1" | tee -a "${LOG}"; }

log "=== Phase-0 Hardening · $(date -u +%FT%TZ) ==="
log "harden.target_user: ${HARDEN_TARGET_USER}"

# --------------------------------------------------------------------
# 1. SSH key must be installed for target user before we disable passwords
# --------------------------------------------------------------------

TARGET_HOME=$(getent passwd "${HARDEN_TARGET_USER}" | cut -d: -f6 || echo "")
if [ -z "${TARGET_HOME}" ] || [ ! -f "${TARGET_HOME}/.ssh/authorized_keys" ]; then
    log "REFUSE: no authorized_keys for ${HARDEN_TARGET_USER} — would lock admin access."
    exit 10
fi
if ! [ -s "${TARGET_HOME}/.ssh/authorized_keys" ]; then
    log "REFUSE: authorized_keys for ${HARDEN_TARGET_USER} is empty."
    exit 10
fi
KEY_COUNT=$(grep -c '^ssh-' "${TARGET_HOME}/.ssh/authorized_keys" || echo 0)
log "authorized_keys.count: ${KEY_COUNT}"

# --------------------------------------------------------------------
# 2. Disable PasswordAuthentication in sshd_config
# --------------------------------------------------------------------

SSHD_CFG=/etc/ssh/sshd_config
if [ ! -w "${SSHD_CFG}" ]; then
    log "FAIL: ${SSHD_CFG} not writable (need root)."
    exit 11
fi

# Backup once (idempotent).
[ -f "${SSHD_CFG}.pre_akki" ] || cp "${SSHD_CFG}" "${SSHD_CFG}.pre_akki"

# Idempotent line replacement.
if grep -qE '^\s*PasswordAuthentication\s+yes' "${SSHD_CFG}"; then
    sed -i 's/^\s*PasswordAuthentication\s\+yes/PasswordAuthentication no/i' "${SSHD_CFG}"
    log "sshd.PasswordAuthentication: flipped yes→no."
elif grep -qE '^\s*PasswordAuthentication\s+no' "${SSHD_CFG}"; then
    log "sshd.PasswordAuthentication: already no (idempotent no-op)."
else
    echo "PasswordAuthentication no" >> "${SSHD_CFG}"
    log "sshd.PasswordAuthentication: appended no."
fi

# --------------------------------------------------------------------
# 3. Disable challenge-response (PAM keyboard-interactive password path)
# --------------------------------------------------------------------

if grep -qE '^\s*ChallengeResponseAuthentication\s+yes' "${SSHD_CFG}"; then
    sed -i 's/^\s*ChallengeResponseAuthentication\s\+yes/ChallengeResponseAuthentication no/i' "${SSHD_CFG}"
    log "sshd.ChallengeResponseAuthentication: flipped yes→no."
elif ! grep -qE '^\s*ChallengeResponseAuthentication' "${SSHD_CFG}"; then
    echo "ChallengeResponseAuthentication no" >> "${SSHD_CFG}"
    log "sshd.ChallengeResponseAuthentication: appended no."
else
    log "sshd.ChallengeResponseAuthentication: already no (idempotent no-op)."
fi

# --------------------------------------------------------------------
# 4. Restart sshd — do NOT drop the current connection with a broken config
# --------------------------------------------------------------------

if ! sshd -t 2>>"${LOG}"; then
    log "FAIL: sshd -t rejected config; NOT restarting."
    exit 11
fi

if command -v systemctl >/dev/null 2>&1; then
    systemctl reload ssh 2>>"${LOG}" || systemctl reload sshd 2>>"${LOG}" || {
        log "FAIL: systemctl reload ssh/sshd failed."
        exit 11
    }
else
    service ssh reload 2>>"${LOG}" || service sshd reload 2>>"${LOG}" || {
        log "FAIL: service reload failed."
        exit 11
    }
fi
log "sshd.reload: ok."

# --------------------------------------------------------------------
# 5. Retire bootstrap credentials (lock initial user password if present)
# --------------------------------------------------------------------

if getent shadow "${HARDEN_TARGET_USER}" >/dev/null 2>&1; then
    CURRENT_HASH=$(getent shadow "${HARDEN_TARGET_USER}" | cut -d: -f2)
    if [ "${CURRENT_HASH}" = "!" ] || [ "${CURRENT_HASH}" = "*" ] || [ -z "${CURRENT_HASH}" ]; then
        log "bootstrap.credentials: ${HARDEN_TARGET_USER} already locked (idempotent no-op)."
    else
        if passwd -l "${HARDEN_TARGET_USER}" >>"${LOG}" 2>&1; then
            log "bootstrap.credentials: ${HARDEN_TARGET_USER} locked (was: hashed password)."
        else
            log "FAIL: passwd -l ${HARDEN_TARGET_USER} failed."
            exit 12
        fi
    fi
else
    log "WARN: no shadow entry for ${HARDEN_TARGET_USER} — nothing to retire."
fi

# --------------------------------------------------------------------
# 6. Emit hardening receipt for downstream ledger reading
# --------------------------------------------------------------------

RECEIPT_FILE=/var/log/akki_phase0_hardening_receipt.json
cat > "${RECEIPT_FILE}" <<JSON
{
  "hardening_ts_utc": "$(date -u +%FT%TZ)",
  "target_user": "${HARDEN_TARGET_USER}",
  "authorized_keys_count": ${KEY_COUNT},
  "sshd_password_auth": "disabled",
  "sshd_challenge_response": "disabled",
  "sshd_reload_ok": true,
  "bootstrap_credentials_retired": true,
  "sshd_config_backup": "${SSHD_CFG}.pre_akki",
  "log_path": "${LOG}"
}
JSON
log "hardening.receipt: ${RECEIPT_FILE}"

log "=== HARDENING COMPLETE ==="
log "  NEXT: acceptance.sh verification step will re-confirm password-auth-dead externally."
exit 0
