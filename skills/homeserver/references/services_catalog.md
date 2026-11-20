# Homeserver Services & Daemons Catalog

Complete catalog of all 34 active services and background daemons (14 Docker containers + 20 host daemons & systemd units) running on the Raspberry Pi 3 Model B+ Homeserver (`192.168.1.100` / `100.x.y.z`).

---

## 🐳 Part 1: Docker Containers (15 Total, 14 Active)

| Container Name | Ports | Web URL (LAN / Tailscale) | Compose / Working Path | Memory Limit | Purpose & Architectural Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **homepage** | `3000:3000` | `http://192.168.1.100:3000` | `/opt/Homepage/docker-compose.yml` | Dynamic (~16 MiB) | **Indian Govt Exam & PSU Launchpad**: Dedicated hub linking Sarkari Result, Free Job Alert, RRB Apply, SSC, IBPS, UPSC, DRDO, ISRO, HPCL, NTPC. Integrates Docker socket. |
| **homer** | `8080:8080` | `http://192.168.1.100:8080` | `/opt/homer/docker-compose.yml` | Dynamic (~0.5 MiB) | **Homelab Operational Cockpit (Tailscale Remote)**: Features Hanuman banner theme, homelab system cards, and live AI health report embed (`health_report.html`). |
| **kanboard** | `1337:80` | `http://192.168.1.100:1337` | `/root/docker-compose/kanbanboard/` | Dynamic (~15 MiB) | **Govt Exam & Task Kanban**: Project #4 (Govt Exam Tracker) and Project #5 (Syllabus Tracker). SQLite backed. |
| **readeck** | `8000:8000` | `http://192.168.1.100:8000` | `/opt/readeck/docker-compose.yml` | Dynamic (~1 MiB) | **Read-it-Later & Article Archiver**: Extracts articles, bookmarks, and web content into distraction-free reading formats. |
| **root-audiobookshelf-1** | `13378:80` | `http://192.168.1.100:13378` | `/root/docker-compose.yml` | Dynamic (~3.6 MiB) | **Audiobookshelf Streaming**: Streams audiobooks and podcasts. ⚠️ *Architectural Notice: Configured at root with host `/` bind-mounted to `/:/Files`.* |
| **navidrome** | `4533:4533` | `http://192.168.1.100:4533` | `/opt/navidrome/docker-compose.yml` | Dynamic (~8.1 MiB) | **Subsonic Music Streaming**: High-performance music streamer serving 6.2 GB audio library across 290+ albums at `/mnt/saman-data/Music`. |
| **gopeed** | `9999:9999` | `http://192.168.1.100:9999` | Standalone Docker | Dynamic (~0.8 MiB) | **Multi-Protocol Download Engine**: Supports HTTP, BitTorrent, and Magnet downloads; targets `/mnt/saman-data/Downloads` (87 GB staging). |
| **opengym-web-1** | `8090:80` | `https://homeserver.tail61b82.ts.net` | `/opt/openGym/docker-compose.yml` | Dynamic (~1 MiB) | **Fitness & Workout Web Client**: Tailscale Passkey WebAuthn secured frontend for workout, gym, and bodyweight tracking. |
| **opengym-api-1** | `3000 (int)` | Internal Docker network | `/opt/openGym/docker-compose.yml` | Dynamic (~2.6 MiB) | **Fitness REST API**: SQLite-backed backend powering workout logging and analytics. |
| **opengym-media** | Internal | Internal Docker network | `/opt/openGym/docker-compose.yml` | Transient | **Media Asset Processor**: Periodic/transient container for processing OpenGym media files and workout demos. |
| **exercisediary** | `8851:8851` | `http://192.168.1.100:8851` | `/opt/ExerciseDiary/docker-compose.yml` | Dynamic (~6.3 MiB) | **Daily Exercise Activity Journal**: Microservice for rapid daily exercise logging. |
| **clickahabit** | `8852:8852` | `http://192.168.1.100:8852` | `/data/ClickAHabit/docker-compose.yml` | Dynamic (~0.7 MiB) | **Habit Tracker**: Habit formation and streak tracking dashboard. |
| **vikunja** | `3456:3456` | `http://192.168.1.100:3456` | `/opt/vikunja/docker-compose.yml` | **300 MiB Limit** (~5.3 MiB used) | **To-Do & Productivity Suite**: Full-featured task and project organizer with hard 300 MiB memory constraint for low-RAM safety. |
| **dailytxt** | `8765:80` | `http://192.168.1.100:8765` | `/opt/DailyTxT/docker-compose.yml` | Dynamic (~1.7 MiB) | **Encrypted Personal Diary**: Web journal for quick reflections and notes. Port 8765 allowed via UFW for Tailscale (`100.64.0.0/10`). |
| **decision-wheel** | `8855:80` | `http://192.168.1.100:8855` | `/opt/decision-wheel/docker-compose.yml` | **32 MiB Limit** (~7.9 MiB used) | **Dopamine Decision Wheel**: Self-hosted HTML5 Canvas/PWA spinner to eliminate decision paralysis and navigate afternoon circadian dips. Pre-loaded with Audiobookshelf, Readeck, NSDR, Pelvic resets, and Study sprints. |

---

## ⚙️ Part 2: Host Daemons & Systemd Services (20 Core Units)

| Daemon / Service Name | Systemd Unit | Ports / Sockets | Directory / Executable Path | Purpose & Special Configuration |
| :--- | :--- | :--- | :--- | :--- |
| **DietPi Dashboard Backend** | `dietpi-dashboard-backend.service` | `5253 (IPC)` | `/opt/dietpi-dashboard` | Hardware sensor, memory, thermal, and systemd management backend. |
| **DietPi Dashboard Frontend** | `dietpi-dashboard-frontend.service` | `5252 (HTTPS)` | `/opt/dietpi-dashboard` | Web-based reactive system monitor UI. |
| **Syncthing** | `syncthing.service` | `8384 (WebUI), 22000 (Sync), 21027 (Disc)` | `/mnt/dietpi_userdata/syncthing` | P2P encrypted folder sync (Obsidian vault, Music, Books, Documents). |
| **FileBrowser** | `filebrowser.service` | `8084` | `/opt/filebrowser` | Web file manager providing direct browser access to files and media storage. |
| **Shellinabox** | `shellinabox.service` | `4200` | System daemon (`/usr/bin/shellinaboxd`) | Web-based terminal emulator allowing browser CLI access. |
| **MiniDLNA / ReadyMedia** | `minidlna.service` | `8200` | `/etc/minidlna.conf` | UPnP/DLNA media broadcast server for Smart TVs and streaming boxes. |
| **qBittorrent-nox** | `qbittorrent.service` | `1340 (WebUI), 6881 (P2P)` | `/root/.config/qBittorrent` | Headless BitTorrent client configured with persistent storage at `/mnt/saman-data/Downloads`. |
| **Nginx Web Server** | `nginx.service` | `80, 443` | `/etc/nginx`, `/var/www` | HTTP reverse proxy and static asset server. Hosts the **Local LAN Homer Dashboard** at `http://192.168.1.100/homer/` (`/var/www/homer`). |
| **MariaDB Database Server**| `mariadb.service` | `3306 (TCP)` | `/var/lib/mysql` | Core relational database engine for self-hosted apps. |
| **CUPS Print Server** | `cups.service` | `631` | `/etc/cups` | Network print server enabling wireless printing across LAN. |
| **Samba SMB Daemon** | `smbd.service` | `139, 445` | `/etc/samba/smb.conf` | Windows file sharing exposing `[Shared]` (`/srv/samba/shared`) and `[Media]` (`/mnt`). |
| **Samba NMB Daemon** | `nmbd.service` | `137, 138 (NetBIOS)` | `/etc/samba/smb.conf` | NetBIOS name resolution for local SMB client discovery. |
| **Router Proxy Relay** | `router-proxy.service` | `8885` | `/usr/bin/socat` | Socat TCP forwarder (`TCP-LISTEN:8885,fork -> 192.168.29.1:80`). Permits Jio Router administration securely via Tailscale. |
| **Who-Is-There Honey-Trap** | `who-is-there.service` | Background sniffer | `/root/who-is-there/run_tcpdump.sh` | Forensic packet sniffer on `eth0` logging non-LAN external port 22 probes into 12-hour rotated PCAP logs (`logs/router_ssh_attempts_*.pcap`). |
| **Kanboard Stage Watcher** | `kanboard-stage-watcher.service` | Event loop | `/opt/kanbanboard_automator/kanboard_stage_watcher.py` | Real-time event listener detecting tasks moved into "Done" stage and triggering automated follow-ups. |
| **AI Watchdog Daemon** | `ai-watchdog.service` | Event loop | `/opt/ai-maintainer/watchdog_daemon.py` | Autonomous AI health sentry v3.0 monitoring memory, storage, and auto-healing crashed services. |
| **AI Chat Listener** | `ai-chat.service` | `8097` | `/opt/ai-maintainer/chat_daemon.py` | Webhook / HTTP listener accepting incoming diagnostic queries and logging user notes to Homer. |
| **EarlyOOM Low-RAM Sentry**| `earlyoom.service` | Kernel hook | `/etc/default/earlyoom` | Kernel OOM interceptor: frees memory when free RAM <10% or swap <5%. Protects critical daemons and prefers killing rogue Node/heavy processes. |
| **Tailscale Node Agent** | `tailscaled.service` | WireGuard UDP / Unix Socket | `/var/lib/tailscale` | Zero-config WireGuard mesh network connecting node (`100.x.y.z`) to MagicDNS and HTTPS serve. |
| **Fail2Ban Intrusion Guard**| `fail2ban.service` | Netfilter / UFW | `/etc/fail2ban/jail.local` | Sentry monitoring SSH authentication logs; bans malicious scanners while whitelisting LAN (`192.168.29.0/24`) and Tailscale (`100.64.0.0/10`). |

---

## ⏰ Part 3: Automated Cron Jobs & Periodic Timers

1. **Kanboard Exam Automator v3 (Daily at 9:00 PM IST)**:
   - Command: `cd /opt/kanbanboard_automator && ./venv/bin/python kanboard_automator_v3.py >> automator_cron.log 2>&1`
   - Purpose: Automated task prioritization, GenAI syllabus progress insights, and schedule adjustments for Govt Exam prep.
2. **AI Server Maintainer (Daily at 3:00 AM IST & systemd timer)**:
   - Command: `/opt/ai-maintainer/run.sh`
   - Purpose: Comprehensive diagnostic scan, orphan cleanup, and generation of `health_report.html` embedded into Homer.
3. **Weekly APT Cleanup (Every Sunday at 12:00 AM IST)**:
   - Command: `/usr/bin/apt -y autoremove && /usr/bin/apt -y clean`
   - Purpose: Prunes outdated packages and clears APT cache to safeguard root partition space.
4. **SSH Sentry Watchdog (Every 15 Minutes)**:
   - Command: `systemctl is-active --quiet ssh || systemctl restart ssh`
   - Purpose: Ensures SSH daemon is automatically restarted if unexpected segfaults or memory aborts occur.
5. **Boot Permission Harmonizer (`@reboot`)**:
   - Command: `/usr/bin/chmod -R 775 /mnt && /usr/bin/chmod -R 775 /opt`
   - Purpose: Enforces consistent group read-write-execute permissions across application and data storage mounts.
