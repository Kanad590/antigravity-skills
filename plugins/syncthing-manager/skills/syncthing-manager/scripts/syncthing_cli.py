#!/usr/bin/env python3
"""
Syncthing Manager CLI
Monitors folder synchronization status (OBSIDIAN, Documents, Astrology, Music),
device connections (Homeserver Pi ↔ Local PC), detects sync conflict files,
and triggers on-demand folder rescans.
"""

import sys
import os
import argparse
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

CONFIG_XML = os.path.expanduser('~/.local/state/syncthing/config.xml')

def get_syncthing_credentials():
    if not os.path.exists(CONFIG_XML):
        # Fallback location
        alt_config = os.path.expanduser('~/.config/syncthing/config.xml')
        if os.path.exists(alt_config):
            cfg_path = alt_config
        else:
            return None, None
    else:
        cfg_path = CONFIG_XML

    try:
        tree = ET.parse(cfg_path)
        root = tree.getroot()
        gui = root.find('gui')
        apikey = gui.find('apikey').text if gui is not None and gui.find('apikey') is not None else None
        address = gui.find('address').text if gui is not None and gui.find('address') is not None else "127.0.0.1:8384"
        return f"http://{address}", apikey
    except Exception as e:
        return None, None

def syncthing_api(endpoint, method="GET", data=None):
    base_url, api_key = get_syncthing_credentials()
    if not base_url or not api_key:
        print("Error: Could not read Syncthing GUI API key from config.xml", file=sys.stderr)
        return None

    url = f"{base_url}{endpoint}"
    headers = {"X-API-Key": api_key}
    body = json.dumps(data).encode('utf-8') if data else None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"Syncthing API Error ({endpoint}): {e}", file=sys.stderr)
        return None

def check_conflicts(root_dirs=None):
    if not root_dirs:
        root_dirs = [os.path.expanduser('~/Documents'), os.path.expanduser('~/Music')]
    
    conflicts = []
    for rdir in root_dirs:
        if not os.path.exists(rdir):
            continue
        for root, dirs, files in os.walk(rdir):
            for f in files:
                if ".sync-conflict-" in f:
                    conflicts.append(os.path.join(root, f))
    return conflicts

def list_status():
    cfg = syncthing_api('/rest/system/config')
    conns = syncthing_api('/rest/system/connections')
    folder_stats = syncthing_api('/rest/stats/folder')

    if not cfg:
        print("Failed to reach Syncthing instance. Is it running?")
        return

    print("🔄 Syncthing Health & Synchronization Status")
    print("=" * 65)

    # Devices
    print("\n📱 Connected Devices:")
    dev_names = {d['deviceID']: d.get('name', 'Unnamed') for d in cfg.get('devices', [])}
    active_conns = conns.get('connections', {}) if conns else {}
    for dev_id, name in dev_names.items():
        is_conn = active_conns.get(dev_id, {}).get('connected', False)
        status_sym = "🟢 Online" if is_conn else "⚪ Offline"
        print(f"  • {name:<20} [{status_sym}] (ID: {dev_id[:12]}...)")

    # Folders
    print("\n📁 Synced Folders:")
    for f in cfg.get('folders', []):
        fid = f['id']
        label = f.get('label', fid)
        path = f.get('path', '')
        fstat = folder_stats.get(fid, {}) if folder_stats else {}
        last_scan = fstat.get('lastScan', 'N/A')
        print(f"  • {label:<16} Path: {path:<30} Last Scan: {last_scan[:19]}")

    # Conflict check
    conflicts = check_conflicts()
    print("\n⚠️ Sync Conflict Check:")
    if conflicts:
        print(f"  Found {len(conflicts)} conflict file(s):")
        for cf in conflicts:
            print(f"    - {cf}")
    else:
        print("  ✅ Zero sync conflicts detected! All vaults and folders in sync.")

def rescan_folder(folder_id):
    res = syncthing_api(f'/rest/db/scan?folder={folder_id}', method="POST")
    print(f"Rescan triggered for folder: {folder_id}")

def main():
    parser = argparse.ArgumentParser(description="Syncthing Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show overview of devices, folders, and conflicts")
    subparsers.add_parser("conflicts", help="Scan for sync conflict files")
    
    scan_p = subparsers.add_parser("rescan", help="Trigger rescan on a folder")
    scan_p.add_argument("folder_id", help="Folder ID to rescan")

    args = parser.parse_args()

    if args.command == "status" or not args.command:
        list_status()
    elif args.command == "conflicts":
        cfs = check_conflicts()
        if cfs:
            print(f"Found {len(cfs)} conflict file(s):")
            for c in cfs:
                print(c)
        else:
            print("Zero sync conflicts found. Clean sync state.")
    elif args.command == "rescan":
        rescan_folder(args.folder_id)

if __name__ == '__main__':
    main()
