# Homeserver Architecture & Microscopic Hardware Harmonization

Detailed technical breakdown of the hardware architecture, memory optimization layers, filesystem design, flash wear mitigation, and network topologies of the **Raspberry Pi 3 Model B+ Homeserver** running Debian 12 (DietPi 64-bit).

---

## 1. Hardware Platform & Resource Constraints

* **Board Model:** Raspberry Pi 3 Model B Plus Rev 1.3
* **SoC:** Broadcom BCM2837B0 Quad-Core ARM Cortex-A53 (aarch64 64-bit) @ 1.4 GHz
* **CPU Scaling Governor:** `schedutil` (Dynamic frequency scaling: 600 MHz idle to 1400 MHz load)
* **Physical Addressable Memory:** 1 GB LPDDR2 SDRAM (886 MiB accessible after GPU RAM carve-out)
* **Thermal Envelope:** 
  - Idle operating temp: 43°C - 48°C.
  - Active throttling register: `throttled=0x0` (Zero past or present under-voltage, frequency capping, or thermal throttling events).
* **Operating System:** Debian GNU/Linux 12 (bookworm) 64-bit (DietPi deployment)
* **Linux Kernel:** `6.12.96+rpt-rpi-v8`

---

## 2. Microscopic Memory Architecture & ZRAM Harmonization

Running 13 active Docker containers and 20 host daemons on 886 MiB of physical RAM requires precise kernel-level memory orchestration:

### A. High-Ratio ZRAM Swapping (`/dev/zram0`)
Instead of swapping directly to the slow, flash-wear-sensitive MicroSD card, the homeserver routes memory swapping through a virtual compressed RAM block device:
- **Device:** `/dev/zram0` (Priority: 100)
- **Virtual Disk Size:** 1.3 GiB (1342 MB)
- **Compression Algorithm:** `lz4` (Optimized for ultra-low ARM Cortex-A53 CPU overhead)
- **Multi-Stream Execution:** 4 independent compression streams running concurrently across all 4 CPU cores (`STREAMS: 4`).
- **Empirical Compression Performance:**
  - Baseline audit: 527 MiB uncompressed data in 189 MiB physical RAM (**2.79x ratio**).
  - Live system state: 549.4 MiB - 557 MiB data compressed to ~193.9 MiB - 195.6 MiB physical RAM (Total allocated: 201.2 MiB - 204.1 MiB).
  - **Effective Compression Ratio:** **2.79x to 2.85x**
  - **Result:** Effectively expands the usable system memory pool from 886 MiB to over 2.0 GiB without incurring I/O wait latency or flash wear.

### B. EarlyOOM Defensive Sentry (`earlyoom.service`)
To prevent the Linux kernel's default Out-Of-Memory (OOM) killer from freezing the system for minutes during low-memory thrashing, `earlyoom` continuously evaluates memory pressure:
- **Configuration (`/etc/default/earlyoom`):**
  ```bash
  EARLYOOM_ARGS="-m 10 -s 5 -r 60 --prefer node --avoid 'sshd|tailscaled|syncthing|dockerd'"
  ```
- **Sentry Thresholds:**
  - Triggers process kill when available physical RAM drops below **10%** OR available swap drops below **5%**.
  - Evaluates system state every 60 seconds (`-r 60`).
- **Defensive Hierarchy:**
  - `--avoid 'sshd|tailscaled|syncthing|dockerd'`: Kernel is strictly prohibited from terminating critical access and synchronization daemons.
  - `--prefer node`: Prioritizes killing rogue JavaScript runtimes or memory-hungry worker processes (e.g., Cline/Node workers) before any homelab infrastructure is impacted.

---

## 3. Storage Architecture, Flash Wear Mitigation & Disk Analysis

### A. Primary Storage Drive
* **Medium:** High-Endurance 256 GB MicroSD Card (`/dev/mmcblk0`)
* **Partition Layout:**
  - Partition 1: `/boot/firmware` (128 MB vfat, ~34 MB used)
  - Partition 2: `/` (234 GB ext4, ~163 GB allocated, ~59 GB available, 74% utilization)

### B. MicroSD Flash Wear Mitigation Strategies
Because flash memory cells degrade with continuous write cycles, the system employs multiple hardening layers:
1. **`noatime,lazytime` Mount Options:**
   Configured in `/etc/fstab` for both `/` and `/boot/firmware`.
   - `noatime`: Disables writing file access timestamps upon reads.
   - `lazytime`: Coalesces timestamp updates into memory, writing them only during sync flushes or file data modifications.
2. **RAM-Based tmpfs Mounts (DietPi RAMlog):**
   High-frequency I/O directories are decoupled from flash media entirely:
   - `/tmp`: 444 MiB `tmpfs` (`defaults,noatime,lazytime,nodev,nosuid,mode=1777`)
   - `/var/log`: 444 MiB `tmpfs` (`defaults,noatime,lazytime,nodev,nosuid`)
   All runtime logs and temporary files live exclusively in volatile RAM and are synced to disk periodically or on clean reboot, drastically reducing MicroSD write amplification.

### C. User Data Distribution (`/mnt/saman-data` - 102.6 GB Total)
User storage is neatly structured under `/mnt/saman-data`:
- **`Downloads/`**: **87 GB** (Staging directory for qBittorrent and Gopeed downloads)
- **`Books/`**: **7.4 GB** (E-books, technical manuals, PDFs, and audio materials)
- **`Music/`**: **6.2 GB** (290+ music albums streamed via Navidrome)
- **`OBSIDIAN/`**: **1.8 GB** (Active personal and technical knowledge vault synced via Syncthing)
- **`Documents/`**: **214 MB** (Personal archives and documentation)
- **`Astrology/`**: **27 MB** (Specialized research and reference notes)

### D. Storage Anomalies & Optimization Warnings
- ⚠️ **Recursive Backup Loop (`/root/backups/system-backup`):**
  A 23 GB recursive backup directory created in June 2026. The backup process captured nested system directories recursively, locking up ~23 GB of valuable flash storage. See Runbook 8 for safe reclamation instructions.
- ⚠️ **Audiobookshelf Root Mount (`root-audiobookshelf-1`):**
  The compose file at `/root/docker-compose.yml` mounts host root `/:/Files`. While convenient for accessing arbitrary files, it grants containerized processes read/write access across system binaries and should be constrained to `/mnt/saman-data`.

---

## 4. Networking Topology & Multi-Mesh Ingress

```
                      [ INTERNET ]
                           │
                    (Jio Fiber WAN)
                           │
                  [ Jio Fiber Router ] (192.168.29.1)
                     │            │
         (LAN Ethernet)          (Port 80 Ingress)
                     │            │ (blocked from outside)
                     ▼            │
         ┌───────────────────────┐│
         │  Raspberry Pi 3B+     ││
         │  Homeserver           ││
         │  (192.168.1.100)       ││
         └───────────────────────┘│
             ▲        ▲           │
             │        │           │
   Tailscale │        │ ZeroTier  │
   Mesh VPN  │        │ Mesh VPN  │
(100.x.y.z)  (192.168.195.160)
             │        │
             ▼        ▼
       [ Remote User Nodes ]
    (Shadow-Node, Mobile, Work)
```

### A. Interfaces & Addressing
1. **Wired Physical Interface (`eth0`):**
   - Address: `192.168.1.100/24`
   - Gateway: `192.168.29.1` (Jio Fiber Home Router)
   - DNS: Direct upstream through local router and Tailscale MagicDNS.
2. **Tailscale Zero-Trust Mesh (`tailscale0`):**
   - Address: `100.x.y.z`
   - Node Identifier: `homeserver.tail61b82.ts.net`
   - MagicDNS: `100.100.100.100`
   - HTTPS Serve: `https://homeserver.tail61b82.ts.net` proxies OpenGym Web (Port 8090) with TLS termination and Passkey WebAuthn authentication.
3. **ZeroTier Mesh (`ztkti4i6js`):**
   - Address: `192.168.195.160/24`
   - Network Name: `PrivateMesh` (`f3797ba7a8bfde9a`)

### B. Network Relays & Honey-Trap Sentinels
- **Router Proxy Relay (`router-proxy.service`):**
  Uses `socat` to listen on TCP `8885` and forward traffic to `192.168.29.1:80`. This allows remote management of the Jio Fiber Router over encrypted Tailscale without opening the router's web console to the public internet.
- **Who-Is-There Honeypot (`who-is-there.service`):**
  Monitors `eth0` using `tcpdump` filtering on `port 22 and not src net 192.168.0.0/16`. Captures all non-local SSH probe attempts forwarded through router DMZ/UPnP, rotating 60 PCAP logs every 12 hours for security auditing.

### C. Firewall Rules (UFW Numbered Matrix)
Default Policy: `DEFAULT_INPUT_POLICY="DROP"`, `DEFAULT_OUTPUT_POLICY="ACCEPT"`.
- Rule 1 & 2: Port 22 SSH allowed from `100.64.0.0/10` (Tailscale) and `192.168.29.0/24` (LAN).
- Rule 10: Port 8765 (DailyTxT) allowed from `100.64.0.0/10` (Tailscale).
- Rule 11 & 30: Samba (NetBIOS & SMB) allowed on LAN.
- Rule 12: LAN subnet `192.168.29.0/24` allowed for local homelab discovery.
- Rule 15 & 33: Full ingress on ZeroTier interface `ztkti4i6js`.
- Rule 17-22 & 35-40: Full ingress on Tailscale interface `tailscale0` (ports 22, 22000 Syncthing, 21027).
