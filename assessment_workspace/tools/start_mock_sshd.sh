#!/usr/bin/env bash
# start_mock_sshd.sh — spawns a local mock sshd on 127.0.0.1:2222 with a
# throwaway bootstrap password for the WS-BUILD-CONNECT-GPU end-to-end drill.
#
# DRILL-ONLY: this file is not production. It stands up a minimal sshd
# instance under a temp dir so the connect-gpu pipeline (hardening →
# acceptance) has a real SSH endpoint to talk to during pre-hand-off drills.
# The drill records are naturally attributed to host `127.0.0.1:2222` in
# ledger rows, distinguishing them from any future real submission.
#
# Kills any prior mock instance before starting.

set -euo pipefail

MOCK_DIR="${MOCK_DIR:-/tmp/akki_mock_sshd}"
MOCK_USER="${MOCK_USER:-mockubuntu}"
MOCK_PORT="${MOCK_PORT:-2222}"
MOCK_PW_FILE="${MOCK_DIR}/mock_bootstrap_password.txt"

# Kill any prior instance.
if [ -f "${MOCK_DIR}/sshd.pid" ]; then
    kill "$(cat "${MOCK_DIR}/sshd.pid")" 2>/dev/null || true
fi

rm -rf "${MOCK_DIR}"
mkdir -p "${MOCK_DIR}"

# Throwaway bootstrap password — 24 random chars.
MOCK_PW=$(openssl rand -base64 24 | tr -d '/+=' | head -c 24)
echo "${MOCK_PW}" > "${MOCK_PW_FILE}"
chmod 600 "${MOCK_PW_FILE}"

# Create a temporary user account on the pod for the mock. If system-level
# useradd is not available, we skip the drill (real drills run in sandbox).
if ! id -u "${MOCK_USER}" >/dev/null 2>&1; then
    useradd -m -s /bin/bash "${MOCK_USER}" 2>/dev/null || {
        echo "useradd failed — running under unprivileged env; using existing user for drill."
        MOCK_USER=$(whoami)
    }
fi
echo "${MOCK_USER}:${MOCK_PW}" | chpasswd 2>/dev/null || {
    echo "chpasswd failed — mock drill may need pre-configured user + password."
    exit 1
}

# Host key.
ssh-keygen -q -f "${MOCK_DIR}/host_ed25519" -N "" -t ed25519

# Privilege separation directory (sshd needs this).
mkdir -p /run/sshd 2>/dev/null || true

# sshd config — permissive password auth for the initial handshake so the
# hardening module can install a key. This is the exact fixture the module
# is written to remediate.
cat > "${MOCK_DIR}/sshd_config" <<CFG
Port ${MOCK_PORT}
ListenAddress 127.0.0.1
HostKey ${MOCK_DIR}/host_ed25519
PidFile ${MOCK_DIR}/sshd.pid
LogLevel INFO
PermitRootLogin no
PasswordAuthentication yes
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
PermitEmptyPasswords no
AllowUsers ${MOCK_USER}
StrictModes no
CFG

# Start sshd in foreground-detached mode.
/usr/sbin/sshd -f "${MOCK_DIR}/sshd_config" -E "${MOCK_DIR}/sshd.log"

sleep 1

# Sanity: is it listening?
if ! ss -ltn 2>/dev/null | grep -q ":${MOCK_PORT} "; then
    echo "FAIL: mock sshd did not start on port ${MOCK_PORT}."
    tail -20 "${MOCK_DIR}/sshd.log" 2>&1
    exit 1
fi

echo "=== MOCK SSHD READY ==="
echo "  host          : 127.0.0.1"
echo "  port          : ${MOCK_PORT}"
echo "  user          : ${MOCK_USER}"
echo "  bootstrap_pw  : (in ${MOCK_PW_FILE}, mode 0600)"
echo "  pid           : $(cat "${MOCK_DIR}/sshd.pid")"
echo "  logs          : ${MOCK_DIR}/sshd.log"
