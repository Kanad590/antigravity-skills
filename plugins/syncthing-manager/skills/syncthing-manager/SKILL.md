---
name: syncthing-manager
description: >-
  Use this skill whenever the user asks to check Syncthing sync status, check connected devices
  (Homeserver Pi, PC), verify folder synchronization (OBSIDIAN, Documents/Shared, Astrology),
  or detect and resolve sync conflict files (.sync-conflict-*).
---

# Syncthing Synchronization Manager Skill

This skill allows Antigravity to interface with the local **Syncthing** REST API (`127.0.0.1:8384`) and inspect the synchronization pipeline between the user's Linux workstation and the **Homeserver (Raspberry Pi)**.

---

## 🚀 Quick Reference Commands

Helper CLI Script: `~/.gemini/config/plugins/syncthing-manager/skills/syncthing-manager/scripts/syncthing_cli.py`

Task | Command
:--- | :---
**Full Status Overview** | `~/.gemini/config/plugins/syncthing-manager/skills/syncthing-manager/scripts/syncthing_cli.py status`
**Detect Sync Conflicts** | `~/.gemini/config/plugins/syncthing-manager/skills/syncthing-manager/scripts/syncthing_cli.py conflicts`
**Trigger Folder Rescan** | `~/.gemini/config/plugins/syncthing-manager/skills/syncthing-manager/scripts/syncthing_cli.py rescan <folder_id>`

---

## 💡 Capabilities

1. **Vault Integrity:** Guarantees that `/home/saman/Documents/OBSIDIAN` and `/home/saman/Documents/Astrology` are actively synced with the homeserver without data collision.
2. **Conflict Resolution:** Finds any hidden `*.sync-conflict-*` files created by multi-device edits so they can be merged before corruption occurs.
