# Homeserver Maintenance Runbooks

Step-by-step Standard Operating Procedures (SOPs) for routine maintenance, diagnostics, disaster recovery, and troubleshooting on the homeserver.

---

## Runbook 1: Quick Health & Status Inspection
To run an instant, comprehensive health check:
```bash
~/.agents/skills/homeserver/scripts/check_health.sh
```
**Verification Points:**
1. **Load Average:** Below 2.0 during idle; brief spikes up to 4.0 during Docker container startup are acceptable.
2. **Temperature:** Below 60°C (Normal idle is 43-48°C).
3. **Throttled Status:** Must be `throttled=0x0`. If `0x50000` or non-zero, check power supply / microUSB cable for under-voltage.
4. **ZRAM Usage:** Check `/dev/zram0` via `zramctl`. Compression ratio should remain ~2.7x - 2.8x.
5. **Failed Units:** Must show `0 failed units` in `systemctl --failed`.
6. **Container Health:** All 13 active containers must report `Up`.

---

## Runbook 2: Docker Container Management
To list running containers and inspect real-time resource consumption:
```bash
~/.agents/skills/homeserver/scripts/docker_manager.sh list
~/.agents/skills/homeserver/scripts/docker_manager.sh stats
```

To view logs of any container (e.g., Homepage, Readeck, or Navidrome):
```bash
~/.agents/skills/homeserver/scripts/docker_manager.sh logs homepage 50
~/.agents/skills/homeserver/scripts/docker_manager.sh logs readeck 50
~/.agents/skills/homeserver/scripts/docker_manager.sh logs navidrome 50
```

To restart a single container:
```bash
~/.agents/skills/homeserver/scripts/docker_manager.sh restart <container_name>
```

To restart an entire Docker Compose stack:
```bash
~/.agents/skills/homeserver/scripts/docker_manager.sh restart-stack <stack_name>
```
*Available stacks:* `homepage`, `opengym`, `navidrome`, `homer`, `vikunja`, `dailytxt`, `readeck`, `kanboard`, `audiobookshelf`.

---

## Runbook 3: Safe Docker Disk Pruning
To reclaim disk space occupied by dangling images, dead build cache, and stopped containers:
```bash
~/.agents/skills/homeserver/scripts/docker_manager.sh prune
```
*Note:* This executes `docker system prune -f`. It preserves active images and mounted persistent volumes.

---

## Runbook 4: Syncthing Diagnostic & Repair
To check Syncthing service health, configured folders, and paired devices:
```bash
~/.agents/skills/homeserver/scripts/syncthing_status.sh
```
To restart Syncthing if synchronization is stalled:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "systemctl restart syncthing"
```

---

## Runbook 5: Package Updates & Safe Upgrades
To check upgradable Debian packages:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "apt update && apt list --upgradable"
```
To execute system updates cleanly:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "apt update && apt upgrade -y && apt autoremove -y"
```

---

## Runbook 6: Network & Fail2ban Unban
If a client IP address on LAN or VPN gets blocked accidentally:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "fail2ban-client status sshd"
~/.agents/skills/homeserver/scripts/ssh_exec.sh "fail2ban-client set sshd unbanip <IP_ADDRESS>"
```
*Note:* Subnets `192.168.29.0/24` and `100.64.0.0/10` are whitelisted in `/etc/fail2ban/jail.local`.

---

## Runbook 7: Direct SSH Shell Access
To open an interactive root shell on the homeserver:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh
# Or directly via SSH config alias:
ssh homeserver      # via LAN (192.168.1.100)
ssh homeserver-ts   # via Tailscale (100.x.y.z)
```

---

## Runbook 8: MicroSD Emergency Storage Reclaim
When disk utilization on `/` exceeds 80% or low-storage warnings appear:

### Step 1: Audit and Prune the Recursive Backup Loop
A historical backup at `/root/backups/system-backup` holds ~23 GB of recursively copied files.
1. Inspect the directory size:
   ```bash
   ~/.agents/skills/homeserver/scripts/ssh_exec.sh "du -sh /root/backups/system-backup"
   ```
2. Verify that active configurations in `/opt` and `/mnt/saman-data` are healthy before pruning.
3. Safe removal of recursive backup directory:
   ```bash
   ~/.agents/skills/homeserver/scripts/ssh_exec.sh "rm -rf /root/backups/system-backup"
   ```
   *Expected space reclaimed: ~23 GB immediately released to root filesystem.*

### Step 2: Prune Docker Builder Cache and Unused Images
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "docker builder prune -a -f && docker image prune -a -f --filter 'until=168h'"
```

### Step 3: Clear DietPi APT and Core Dump Caches
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "apt clean && rm -rf /var/cache/apt/archives/*"
```

---

## Runbook 9: Unmanaged Script Recovery (Daemonizing `audiobook_finish_watcher.py`)
Currently, `audiobook_finish_watcher.py` runs as an orphan background process (`python3 /opt/ai-maintainer/audiobook_finish_watcher.py`) without systemd supervision. If killed by EarlyOOM or a system reboot, it will not restart automatically.

### Step 1: Create the Systemd Service File
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "cat << 'EOF' > /etc/systemd/system/audiobook-finish-watcher.service
[Unit]
Description=Audiobook Finish Watcher & Library Notification Daemon
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ai-maintainer
ExecStart=/usr/bin/python3 /opt/ai-maintainer/audiobook_finish_watcher.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/audiobook_watcher.log
StandardError=append:/var/log/audiobook_watcher.log

[Install]
WantedBy=multi-user.target
EOF"
```

### Step 2: Terminate the Orphan Process and Enable the Service
```bash
# Terminate old unmanaged process
~/.agents/skills/homeserver/scripts/ssh_exec.sh "pkill -f audiobook_finish_watcher.py"

# Reload systemd and start supervised service
~/.agents/skills/homeserver/scripts/ssh_exec.sh "systemctl daemon-reload && systemctl enable --now audiobook-finish-watcher.service"

# Verify status
~/.agents/skills/homeserver/scripts/ssh_exec.sh "systemctl status audiobook-finish-watcher.service"
```

---

## Runbook 10: Syncthing Sync Failure Troubleshooting (Ghost File Pull Errors)
When Syncthing logs report errors like:
```text
WRN Failed to sync (path=".../Note.md" error="syncing: finishing: pull: no such file" folder.label=OBSIDIAN)
```
This occurs when a file was rapidly renamed, moved, or deleted on another client node (e.g. Laptop or Phone) while the server was preparing to pull the blocks, leaving an invalid file hash index in Syncthing's local database.

### Step 1: Identify the Stalled Files
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "journalctl -u syncthing --no-pager -n 30 | grep -i 'Failed to sync'"
```

### Step 2: Re-Touch or Force-Sync from Origin Node
1. On the machine where the file was modified, open the note in Obsidian and add/remove a space to update its mtime.
2. Allow Syncthing to propagate the new mtime.

### Step 3: Trigger a Folder Rescan via REST API / CLI
Force Syncthing on the homeserver to recalculate hashes for the OBSIDIAN folder (`qw9cy-zz2v4`):
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "curl -X POST -H 'X-API-Key: \$(grep -oP '(?<=<apikey>)[^<]+' /mnt/dietpi_userdata/syncthing/config.xml)' http://127.0.0.1:8384/rest/db/scan?folder=qw9cy-zz2v4"
```

### Step 4: Database Reset (Nuclear Option)
If ghost errors persist after 24 hours:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "systemctl stop syncthing && /usr/bin/syncthing --reset-database -home=/mnt/dietpi_userdata/syncthing && systemctl start syncthing"
```
*Note: This recalculates file indices from scratch without deleting actual files.*
