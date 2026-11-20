#!/usr/bin/env bash
# ==============================================================================
# homeserver ssh_exec.sh - Intelligent SSH Execution Wrapper
# Automatically routes commands via LAN (192.168.1.100) or Tailscale (100.x.y.z)
# ==============================================================================
set -e

LAN_HOST="192.168.1.100"
TS_HOST="100.x.y.z"
SSH_USER="root"
SSH_KEY="$HOME/.ssh/id_ed25519"
SSH_OPTS="-i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 -o BatchMode=yes"

TARGET_HOST=""

# Check if LAN host is reachable on port 22
if nc -z -w 3 "$LAN_HOST" 22 >/dev/null 2>&1; then
    TARGET_HOST="$LAN_HOST"
elif nc -z -w 3 "$TS_HOST" 22 >/dev/null 2>&1; then
    TARGET_HOST="$TS_HOST"
else
    echo "❌ Error: Homeserver is unreachable on both LAN ($LAN_HOST:22) and Tailscale ($TS_HOST:22)." >&2
    exit 1
fi

if [ $# -eq 0 ]; then
    ssh $SSH_OPTS "$SSH_USER@$TARGET_HOST"
else
    ssh $SSH_OPTS "$SSH_USER@$TARGET_HOST" "$@"
fi
