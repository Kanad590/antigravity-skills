#!/usr/bin/env bash
# ==============================================================================
# homeserver check_health.sh - Comprehensive Homeserver Health Diagnostic
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSH_CMD="$SCRIPT_DIR/ssh_exec.sh"

$SSH_CMD "bash -s" << 'EOF'
echo "===================================================================="
echo "          🏡 HOMESERVER COMPREHENSIVE HEALTH REPORT"
echo "===================================================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Host: $(hostname) | Kernel: $(uname -r) | Model: $(cat /proc/device-tree/model 2>/dev/null || echo 'Unknown')"
echo ""

echo "▶ ⏱️  UPTIME & LOAD AVERAGE"
uptime
echo ""

echo "▶ 🌡️  TEMPERATURE & THROTTLING"
TEMP=$(vcgencmd measure_temp 2>/dev/null || echo "N/A")
THROTTLED=$(vcgencmd get_throttled 2>/dev/null || echo "N/A")
FREQ=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq 2>/dev/null || echo "N/A")
if [ "$FREQ" != "N/A" ]; then
    FREQ_MHZ=$((FREQ / 1000))
    echo "Temperature: $TEMP | CPU Frequency: ${FREQ_MHZ} MHz"
else
    echo "Temperature: $TEMP"
fi
echo "Throttling Status: $THROTTLED (0x0 = Clean, No Undervoltage / Throttling)"
echo ""

echo "▶ 🧠 MEMORY & SWAP (ZRAM)"
free -h
echo "Swap details:"
swapon --show
echo ""

echo "▶ 💾 STORAGE USAGE (MicroSD & Mounts)"
df -h -T / /boot/firmware /tmp /var/log
echo ""

echo "▶ 🐳 DOCKER CONTAINERS STATUS"
TOTAL_CNT=$(docker ps -a -q | wc -l)
RUNNING_CNT=$(docker ps -q | wc -l)
echo "Total Containers: $TOTAL_CNT | Running: $RUNNING_CNT"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo "▶ ⚙️ SYSTEMD SERVICES HEALTH"
FAILED=$(systemctl --failed --no-legend | wc -l)
if [ "$FAILED" -eq 0 ]; then
    echo "✅ All systemd units healthy (0 failed units)."
else
    echo "⚠️ $FAILED failed systemd unit(s) detected:"
    systemctl --failed
fi
echo ""

echo "▶ 🌐 NETWORK & VPN STATUS"
echo "LAN (eth0): $(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo 'Down')"
echo "Tailscale: $(ip -4 addr show tailscale0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo 'Down')"
echo "ZeroTier: $(ip -4 addr show ztkti4i6js | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo 'Down')"
echo ""

echo "▶ 🛡️ SECURITY & FAIL2BAN"
fail2ban-client status sshd 2>/dev/null | grep -E 'Currently banned|Total banned|Banned IP list' || echo "Fail2ban sshd check failed"
echo "===================================================================="
EOF
