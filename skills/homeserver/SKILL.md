---
name: homeserver
description: >-
  Use this skill whenever the user asks to manage, monitor, inspect, diagnose, restart,
  or perform maintenance on their Raspberry Pi homeserver (192.168.1.100 or Tailscale 100.x.y.z).
  Supports Docker containers, compose stacks, systemd services, Syncthing, storage, updates, and fail2ban.
  Also triggered by the /homeserver command.
---

# Homeserver Management & Maintenance Skill

This skill enables Antigravity to perform comprehensive diagnostics, container operations, systemd service management, storage cleanups, and administrative tasks on the user's **Raspberry Pi 3 Model B+ Homeserver** running Debian 12 (DietPi).

---

## 🚀 Quick Reference Commands

All helper scripts auto-route transparently between **LAN (`192.168.1.100`)** and **Tailscale (`100.x.y.z`)** with passwordless SSH key authentication.

Task | Command
:--- | :---
**Full Health Inspection** | `~/.agents/skills/homeserver/scripts/check_health.sh`
**Docker Containers List** | `~/.agents/skills/homeserver/scripts/docker_manager.sh list`
**Docker Real-Time Stats** | `~/.agents/skills/homeserver/scripts/docker_manager.sh stats`
**Docker Container Logs** | `~/.agents/skills/homeserver/scripts/docker_manager.sh logs <container_name> [lines]`
**Restart Docker Container**| `~/.agents/skills/homeserver/scripts/docker_manager.sh restart <container_name>`
**Restart Compose Stack** | `~/.agents/skills/homeserver/scripts/docker_manager.sh restart-stack <stack_name>`
**Prune Docker Images/Cache**| `~/.agents/skills/homeserver/scripts/docker_manager.sh prune`
**Syncthing Sync Health** | `~/.agents/skills/homeserver/scripts/syncthing_status.sh`
**Telegram Push Alert** | `tg-notify --type <type> --title "<title>" --message "<msg>"`
**Telegram Commander Daemon**| `systemctl status ai-telegram-commander.service`
**Run Arbitrary Remote Cmd** | `~/.agents/skills/homeserver/scripts/ssh_exec.sh "<command>"`
**Interactive Shell** | `ssh homeserver` (LAN) or `ssh homeserver-ts` (Tailscale)

---

## 🛠️ Workflows

### 1. Daily / Health Diagnostics
When the user asks *"How is my homeserver doing?"*, *"Check homeserver status"*, or runs `/homeserver`:
1. Execute [`check_health.sh`](./scripts/check_health.sh).
2. Review:
   - **Load Average & Uptime**
   - **SoC Temperature & Throttling Status** (must be `throttled=0x0`)
   - **Memory & ZRAM Swap** (ensure swap usage is healthy, 1.3 GiB ZRAM LZ4 @ ~2.8x compression)
   - **Disk Space** on `/` (ext4) and tmpfs mounts (`/tmp`, `/var/log`)
   - **Docker Containers** (ensure all 14 active containers are `Up`, 15 total including transient `opengym-media`)
   - **Systemd Failed Units** (ensure 0 failed units; monitor `kanboard-stage-watcher.service`, `ai-watchdog.service`, `router-proxy.service`, `who-is-there.service`)
   - **Fail2ban Status** (confirm no active ban on local or Tailscale IPs)
3. Report a clear, concise bulleted summary to the user.

### 2. Managing Docker Services & Stacks
When the user wants to restart, debug, or check logs for a specific service:
1. Locate the service from the [Services Catalog](./references/services_catalog.md).
2. For container logs:
   ```bash
   ~/.agents/skills/homeserver/scripts/docker_manager.sh logs <name> 50
   ```
3. To restart a compose stack (e.g., `homepage`, `opengym`, `navidrome`, `kanboard`, `vikunja`, `dailytxt`, `readeck`, `audiobookshelf`):
   ```bash
   ~/.agents/skills/homeserver/scripts/docker_manager.sh restart-stack <name>
   ```
4. Verify container recovery with `~/.agents/skills/homeserver/scripts/docker_manager.sh list`.

### 3. Monitoring Custom Daemons & Systemd Services
The homeserver hosts dedicated host daemons tailored for automation, safety, and security:
- **`ai-telegram-commander.service`**: 24/7 Telegram AI Commander daemon (`telegram_commander.py`) listening exclusively to admin Saman (`Chat ID: 571568364`). Empowers Saman to control, inspect, and command the homeserver autonomously in natural language with root superuser privileges.
- **`kanboard-stage-watcher.service`**: Watches Kanboard exam tasks moving into the "Done" stage in real time and automatically triggers study workflows, status logs, and **Telegram Bot alerts**.
- **`ai-watchdog.service`**: Auto-healer watchdog daemon (`watchdog_daemon.py`) monitoring container health, memory spikes, disk exhaustion, and auto-restarting crashed containers/services with **Telegram alerts**.
- **`fail2ban.service` & `telegram-notify` action**: Automatically bans SSH brute-force attackers and dispatches instant **Telegram Security alerts** with the banned IP and attempt count.
- **`tg-notify` (`/usr/local/bin/tg-notify`)**: Central Telegram notification engine with built-in 5-minute deduplication and anti-spam protection.
- **`router-proxy.service`**: Socat TCP relay forwarding port `8885` directly to Jio Fiber Router (`192.168.29.1:80`), allowing full web router administration over Tailscale without exposing port 80 to the WAN.
- **`who-is-there.service`**: Forensic honey-trap daemon running `tcpdump` on `eth0` for port 22 incoming attempts not originating from LAN (`! 192.168.0.0/16`), rotating PCAP capture files every 12 hours.

To inspect daemon status or logs:
```bash
~/.agents/skills/homeserver/scripts/ssh_exec.sh "systemctl status <service_name>"
~/.agents/skills/homeserver/scripts/ssh_exec.sh "journalctl -u <service_name> -n 50 --no-pager"
```

### 4. Syncthing & File Sync Troubleshooting
When the user reports file sync delays or issues between devices (Laptop `Shadow-Node`, Desktop `HomesamanDesktop`, Phone `moto g96 5G`, and Server):
1. Execute [`syncthing_status.sh`](./scripts/syncthing_status.sh).
2. Check if the device is connected and synced.
3. If ghost file errors or stalled pulls occur (e.g. `syncing: finishing: pull: no such file`):
   Follow [Runbook 10: Syncthing Sync Failure Troubleshooting](./references/runbooks.md#runbook-10-syncthing-sync-failure-troubleshooting).
4. If necessary, restart the Syncthing daemon:
   ```bash
   ~/.agents/skills/homeserver/scripts/ssh_exec.sh "systemctl restart syncthing"
   ```

### 5. Managing Dashboards (Dual Homer Setup Pattern)
The homeserver maintains **two distinct Homer dashboards** serving different network environments:
1. **Local LAN Homer Dashboard:**
   * **Host:** Native Nginx (port `80`)
   * **URL:** `http://192.168.1.100/homer/`
   * **Config Path:** `/var/www/homer/assets/config.yml`
   * **Rule:** All service URLs in this config MUST use the local LAN IP (`192.168.1.100:<PORT>`) for fast local access.
2. **Tailscale Remote Homer Dashboard:**
   * **Host:** Docker container `homer` (port `8080`)
   * **URL:** `http://100.x.y.z:8080/`
   * **Config Path:** `/opt/homer/assets/config.yml`
   * **Rule:** All service URLs in this config MUST use the Tailscale IP (`100.x.y.z:<PORT>`) for encrypted access anywhere outside LAN.

> [!IMPORTANT]
> **Dashboard Update SOP:**
> * When asked to add or modify a service on the Homer dashboards, **ALWAYS update BOTH** config files (`/var/www/homer/assets/config.yml` and `/opt/homer/assets/config.yml`), matching their respective IP schemes.
> * Always create a timestamped backup before modifying config files (e.g. `cp config.yml config.yml.bak.$(date +%s)`).
> * Do **NOT** confuse Homer with **Homepage** (`/opt/Homepage`, port `3000`). Homepage is an independent startpage dedicated to Indian Govt Exam & PSU preparation (RRB, SSC, UPSC, DRDO, ISRO, HPCL, NTPC).

### 6. System Updates & Maintenance
When the user asks to update system packages:
1. Follow [Runbook 5: Package Updates & Safe Upgrades](./references/runbooks.md#runbook-5-package-updates--safe-upgrades).
2. Run simulation first (`apt list --upgradable`).
3. Apply updates with user consent and verify services restart properly.

### 7. Telegram Bot & Autonomous AI Commander (@SamanAssist96_bot)
The homeserver runs a dedicated 24/7 Telegram Assistant and Commander daemon connected to **`@SamanAssist96_bot`**:
- **Daemon Service:** `ai-telegram-commander.service` (`/opt/ai-maintainer/telegram_commander.py`, runs as `root`).
- **Config & Credentials:** `/opt/telegram-notifier/bot.env` (Permissions `600`).
  - Bot Token: `YOUR_TELEGRAM_BOT_TOKEN`
  - Admin ID: `571568364` (Saman / Kanad / Kd)
  - Universal Memory DB: `/opt/ai-maintainer/chat_memory.db` (`conversations` and `memories` tables)

#### Dual-Mode Architecture & Conversational Companion:
1. **Admin Mode (Saman only - Superuser with Freewill):**
   - **Autonomous Bash Execution:** For maintenance requests (e.g., restart container, prune cache, check logs), uses Gemini 2.5/3.8 Flash (with automatic rotation across 7 keys) to autonomously plan, execute root bash commands, and report results in clean Bengali + emojis + English technical terms.
   - **Multimodal Perception (Vision & Voice):** Processes photos, circuits, handwritten equations, and listens to spoken Telegram voice notes (`voice`) hands-free.
   - **Inbound PDF & Document Ingestion:** Analyzes sent exam notifications, question papers, and code scripts.
   - **Kanboard Live Exam & Syllabus Co-Pilot:** Real-time integration with Projects #4 (Govt Exams) and #5 (191 Syllabus Topics), advancing chapter mastery on command.
   - **Executive Daily Briefing (`/briefing`):** Synthesizes hardware telemetry, active exams, syllabus backlog, and pending reminders into a single morning/evening report.
   - **Web Research & URL Unfurling:** Automatically parses and summarizes external links.
   - **Humanized Conversation:** For open-ended questions (e.g., science, general knowledge, philosophy), provides warm, engaging, philosophical answers.
   - **Contact Briefing:** Empathic debriefs on guest/contact chats.
2. **Guest Mode (Group Members / External Contacts):**
   - When friends, contacts, or other accounts message or tag `@SamanAssist96_bot`:
     - **Multimodal Vision & Analysis:** If a guest sends an image, the bot inspects and answers questions with clarity and precision.
     - **Universal Peer-to-Peer Routing:** Any user can ask the bot to forward a message, photo, or note to anyone else (e.g. to Saman/Kanad/Kd, or another contact).
     - **Automated 1-2 Line File Summary:** Whenever ANY file, document, or photo is forwarded, the bot automatically generates and prepends a **crisp 1 to 2 line Bengali summary** (`📌 সারসংক্ষেপ (১-২ লাইন): ...`) explaining what it is.
     - **30% Disclosure + 70% Resistance:** Answers questions about Saman with ~30% high-level positive context (engineering focus, AI architecture, competitive technical exams like RRB/SSC Tech/PSU) while wittily guarding specific schedules and micro-details.
     - **Real-Time Reminders & Alerts:** If someone asks to remind Saman/Kanad/Kd or leave a message, the bot permanently stores it in SQLite and immediately dispatches an alert message to Saman's private Telegram (`571568364`).
     - **Authentic Vault MD-to-PDF Conversion:** Directly converts existing authentic `.md` notes from `/mnt/saman-data/OBSIDIAN` to PDF on request. Does NOT invent new textbooks from scratch.
     - **Chat-Based Internet Knowledge (No Fake PDFs):** If a requested topic is not in Obsidian, provides concise bullet points directly in the chat message rather than generating synthetic PDFs.
     - **Isolated User Journals & Zero-Confusion Identity:** Maintains separate, isolated dossiers (`user_journals` table) keyed strictly by Telegram `user_id`. Recognizes returning users, remembers personal facts (birthdays, preferences, past topics), and strictly prevents any cross-talk or mixing of users.
     - **Zero Action Isolation:** Strictly disallows any system changes, bash execution, or server access for non-admin users.
     - **Persistent Chat Memory:** All interactions and user directory records are stored in SQLite (`/opt/ai-maintainer/chat_memory.db`).

#### Proactive Alert Hooks (Anti-Spam & Deduplication):
- **Intrusion Defense:** Fail2ban triggers `/usr/local/bin/tg-notify` on SSH brute-force attack bans.
- **Service & Container Auto-Heal:** `ai-watchdog.service` auto-restarts failed host units and crashed Docker containers, dispatching recovery alerts.
- **Kanboard Stage Moves:** `kanboard-stage-watcher.service` dispatches real-time alerts when exams advance.
- **Anti-Spam Cooldown:** `/tmp/tg_notify_cache.json` suppresses identical alerts within 5 minutes.

---

## 📚 Detailed Reference Documentation
* **[Hardware & Network Architecture](./references/architecture.md):** Complete specifications of CPU, 886 MiB RAM, 1.3 GiB ZRAM LZ4, EarlyOOM sentinel, DietPi RAMlog tmpfs, Tailscale, ZeroTier, and UFW firewall.
* **[Services Catalog](./references/services_catalog.md):** Exhaustive directory of all 34 hosted services (14 Docker containers + 20 host daemons/units), compose paths, ports, and URLs.
* **[Maintenance Runbooks](./references/runbooks.md):** Step-by-step SOPs for storage cleanups, recursive backup loop mitigation, unmanaged process daemonization, fail2ban unbanning, and service recovery.
