---
name: homelab-monitor
description: >-
  Use this skill whenever the user asks to monitor homeserver health, check Raspberry Pi temperature/disk,
  send an automated health report or alert to Telegram, or diagnose container status.
---

# Homelab & Server Proactive Monitor Skill

This skill provides unified monitoring and automated alerting across the user's **Raspberry Pi 3 Model B+ Homeserver** and **Telegram AI Assistant Bot** (`@SamanAssist96_bot`).

---

## 🚀 Quick Reference Commands

Helper CLI Script: `~/.gemini/config/plugins/homelab-monitor/skills/homelab-monitor/scripts/monitor_and_alert.py`

Task | Command
:--- | :---
**Check Server Status** | `~/.gemini/config/plugins/homelab-monitor/skills/homelab-monitor/scripts/monitor_and_alert.py --check`
**Send Health Report to Telegram** | `~/.gemini/config/plugins/homelab-monitor/skills/homelab-monitor/scripts/monitor_and_alert.py --check --notify`
**View Full Diagnostic Raw Log** | `~/.gemini/config/plugins/homelab-monitor/skills/homelab-monitor/scripts/monitor_and_alert.py --raw`

---

## 💡 Automated Health Checks

The script inspects:
- **CPU Temperature:** Triggers warning alert if > 70°C.
- **Root Filesystem Usage:** Warns if disk > 85%.
- **Uptime & Load:** Detects high load spikes.
- **Telegram Notification:** Formats an alert or daily digest and pushes directly to Telegram.
