---
name: linux-sysadmin
description: Comprehensive Linux system administration, troubleshooting, defensive Bash scripting, and systemd service/timer management for Debian/Ubuntu and production Linux environments.
category: devops
risk: low
---

# 🐧 Linux System Administration, Troubleshooting & Scripting

Unified operational handbook covering day-to-day Linux server administration, diagnostic troubleshooting workflows, robust defensive Bash scripting, and systemd service orchestration.

---

## 1. ⚙️ System Administration & Package Management

### Package Management (Debian / Ubuntu `apt`)
```bash
sudo apt update && sudo apt upgrade -y       # Update index and upgrade
apt search <package>                         # Search packages
apt show <package>                           # View package details & dependencies
sudo apt install -y <pkg1> <pkg2>            # Install packages
sudo apt remove <package>                    # Remove package (keep configs)
sudo apt purge <package>                     # Remove package and purge configs
sudo apt autoremove --purge -y               # Clean orphaned dependencies
dpkg -l | grep <keyword>                     # List installed matching packages
```

### System Inspection & Health Check
```bash
uname -a && lsb_release -a                   # Kernel & OS distribution
lscpu                                        # CPU architecture and core layout
free -h                                      # Human-readable RAM usage
df -hT                                       # Disk usage by filesystem type
uptime                                       # Load averages (1m, 5m, 15m)
ip -br a                                     # Concise IP address list
ss -tulpn                                    # Open ports and listening PIDs
```

### Storage & Filesystem Operations
```bash
lsblk -f                                     # Block devices, UUIDs, and mount points
du -ah /path 2>/dev/null | sort -rh | head -20 # Top 20 largest files/dirs
df -ih                                       # Inode usage (prevents out-of-inode false alarms)
sudo fuser -v /mountpoint                    # Find processes blocking unmount
```

---

## 2. 🔍 Diagnostic & Troubleshooting Workflow

### Rapid Triage Matrix
| Symptom | Primary Diagnostic Tool | Key Indicator |
|---|---|---|
| **High CPU / Load** | `top -b -n 1 \| head -20`, `htop` | Process consuming >90% single core, I/O wait (`%wa`) |
| **Out of Memory / OOM** | `free -h`, `journalctl -k \| grep -i oom` | Swap exhaustion, OOM-killer invocations |
| **Disk Full** | `df -h`, `du -h --max-depth=1 /var` | `/var/log` runaway, docker volumes |
| **Port Conflict / Service Down** | `ss -tulpn \| grep :<port>`, `systemctl status` | Binding collision or dead daemon |
| **Network Unreachable** | `ip r`, `ping -c 3 1.1.1.1`, `resolvectl status` | Default gateway dropped, DNS failure |

### Real-Time Process Investigation
```bash
ps aux --sort=-%cpu | head -10               # Top 10 CPU consumers
ps aux --sort=-%mem | head -10               # Top 10 Memory consumers
pgrep -fl <pattern>                          # Find PID and full command string
sudo lsof -i :<port>                         # Process using a specific port
sudo kill -15 <PID>                          # Graceful stop (SIGTERM)
sudo kill -9 <PID>                           # Force kill (SIGKILL)
```

---

## 3. 🛡️ Defensive Bash Scripting Standards

### Production Script Skeleton (`template.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# 1. Traps & Cleanup
cleanup() {
    local exit_code=$?
    # Remove temp files safely
    [[ -n "${TMP_DIR:-}" && -d "${TMP_DIR}" ]] && rm -rf "${TMP_DIR}"
    exit "${exit_code}"
}
trap cleanup EXIT INT TERM

# 2. Strict Variables & Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d "/tmp/sysadmin_XXXXXX")"

# 3. Defensive Logging
log_info()  { echo "[INFO]  $(date '+%Y-%m-%d %H:%M:%S') - $*"; }
log_warn()  { echo "[WARN]  $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2; }
log_error() { echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2; }

# 4. Input Verification
if [[ $# -lt 1 ]]; then
    log_error "Usage: $0 <target>"
    exit 1
fi
```

### Critical Defensive Rules
- **Always quote variables:** `"${var}"` (prevents word splitting and globbing).
- **Safe variable defaults:** `"${VAR:-default_value}"` avoids unset variable triggers under `set -u`.
- **Atomic file writes:** Write to a `.tmp` file and `mv` into place to avoid partial writes.
- **Check return codes explicitly:** Do not mask failures with unchecked `|| true` unless intentionally ignored.

---

## 4. ⚙️ Systemd Service & Timer Management

### Common Commands
```bash
sudo systemctl daemon-reload                 # Reload after altering .service files
sudo systemctl start|stop|restart <name>      # Service state control
sudo systemctl enable --now <name>           # Enable at boot and start immediately
sudo systemctl status <name>                 # Detailed service status and recent logs
sudo systemctl list-units --type=service --state=failed # Find all failed services
```

### Complete Service Unit Example (`/etc/systemd/system/myapp.service`)
```ini
[Unit]
Description=My Custom Application Service
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=saman
Group=saman
WorkingDirectory=/home/saman/myapp
ExecStart=/usr/bin/python3 /home/saman/myapp/main.py
Restart=on-failure
RestartSec=5s

# Security Hardening & Resource Guards
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=read-only
MemoryMax=1G
CPUQuota=150%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```

### Timer Unit (Cron Replacement)
**`/etc/systemd/system/backup.timer`**:
```ini
[Unit]
Description=Nightly Backup Timer

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=5m

[Install]
WantedBy=timers.target
```

### Journalctl Query Reference
```bash
journalctl -u <service> -f                   # Follow service logs in real time
journalctl -u <service> --since "1 hour ago" # Logs from the past hour
journalctl -u <service> -p err..emerg        # Only errors and critical alerts
journalctl -xeu <service>                    # Detailed debugging info on failed starts
sudo journalctl --vacuum-time=7d             # Prune logs older than 7 days
```
