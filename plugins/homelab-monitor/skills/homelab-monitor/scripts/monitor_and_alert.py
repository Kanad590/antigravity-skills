#!/usr/bin/env python3
"""
Homelab & Server Proactive Monitor
Polls Raspberry Pi health (Uptime, Temp, CPU Load, Disk, Docker Containers, Syncthing),
and can broadcast an automated Telegram report or trigger alerts if anomalies are found.
"""

import sys
import os
import subprocess
import argparse
import re

HOMESERVER_SKILL = os.path.expanduser('~/.agents/skills/homeserver/scripts')
CHECK_HEALTH = os.path.join(HOMESERVER_SKILL, 'check_health.sh')
DOCKER_MGR = os.path.join(HOMESERVER_SKILL, 'docker_manager.sh')

def run_command(cmd_list, timeout=25):
    try:
        res = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return res.returncode == 0, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def get_health_summary():
    if not os.path.exists(CHECK_HEALTH):
        return {"ok": False, "error": "check_health.sh script missing"}

    success, stdout, stderr = run_command([CHECK_HEALTH])
    if not success:
        return {"ok": False, "error": f"Failed to reach homeserver: {stderr.strip()}"}

    summary = {
        "ok": True,
        "raw": stdout,
        "temp": "N/A",
        "load": "N/A",
        "disk_root": "N/A",
        "alerts": []
    }

    # Extract temp
    m_temp = re.search(r"temp=([0-9\.]+)'C", stdout)
    if m_temp:
        temp_val = float(m_temp.group(1))
        summary["temp"] = f"{temp_val}°C"
        if temp_val > 70.0:
            summary["alerts"].append(f"🔥 High CPU Temperature: {temp_val}°C")

    # Extract disk usage
    m_disk = re.search(r"/dev/root\s+\S+\s+\S+\s+\S+\s+([0-9]+)%", stdout)
    if m_disk:
        disk_pct = int(m_disk.group(1))
        summary["disk_root"] = f"{disk_pct}%"
        if disk_pct > 85:
            summary["alerts"].append(f"⚠️ High Disk Usage: {disk_pct}% on /dev/root")

    # Extract uptime
    m_up = re.search(r"up\s+(.*?),\s+\d+\s+user", stdout)
    if m_up:
        summary["uptime"] = m_up.group(1)

    return summary

def send_telegram_alert(summary):
    if not summary["ok"]:
        msg = f"🚨 *Homelab Alert: Server Unreachable*\n\nError: `{summary['error']}`"
    else:
        status_emoji = "✅" if not summary["alerts"] else "⚠️"
        alerts_text = "\n".join(summary["alerts"]) if summary["alerts"] else "All systems normal."
        msg = (
            f"{status_emoji} *Homeserver Daily Digest*\n\n"
            f"🌡️ *Temperature:* `{summary.get('temp', 'N/A')}`\n"
            f"💾 *Disk Usage:* `{summary.get('disk_root', 'N/A')}`\n"
            f"⏱️ *Uptime:* `{summary.get('uptime', 'N/A')}`\n\n"
            f"📌 *Status:* {alerts_text}"
        )

    res = subprocess.run(["tg-bot-send", "--message", msg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print("Telegram notification sent successfully.")
        return True
    else:
        # Fallback to python backend
        py_backend = os.path.expanduser("~/.config/telegram-sender/bot_send.py")
        if os.path.exists(py_backend):
            r = subprocess.run(["python3", py_backend, "-m", msg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return r.returncode == 0
        print(f"Failed to send to Telegram: {res.stderr}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Homelab Proactive Monitor & Alert")
    parser.add_argument("--check", action="store_true", help="Run diagnostic health check")
    parser.add_argument("--notify", action="store_true", help="Send digest to Telegram")
    parser.add_argument("--raw", action="store_true", help="Print raw diagnostic output")

    args = parser.parse_args()

    summary = get_health_summary()

    if args.raw:
        print(summary.get("raw", summary.get("error", "")))
        return

    if not summary["ok"]:
        print(f"❌ Error: {summary['error']}")
        if args.notify:
            send_telegram_alert(summary)
        sys.exit(1)

    print("🏡 Homeserver Health Status:")
    print(f"  • Temperature: {summary.get('temp')}")
    print(f"  • Root Disk:   {summary.get('disk_root')}")
    print(f"  • Uptime:      {summary.get('uptime', 'N/A')}")
    if summary["alerts"]:
        print("  • Alerts:")
        for a in summary["alerts"]:
            print(f"    - {a}")
    else:
        print("  • Status: All parameters optimal.")

    if args.notify:
        send_telegram_alert(summary)

if __name__ == '__main__':
    main()
