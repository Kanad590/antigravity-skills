#!/usr/bin/env bash
# ==============================================================================
# homeserver syncthing_status.sh - Syncthing Sync Health & Device Diagnostic
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSH_CMD="$SCRIPT_DIR/ssh_exec.sh"

$SSH_CMD "bash -s" << 'EOF'
echo "===================================================================="
echo "          🔄 SYNCTHING STATUS & DIAGNOSTICS"
echo "===================================================================="
systemctl status syncthing --no-pager | head -n 12
echo ""

echo "▶ 📂 SYNCTHING FOLDERS CONFIGURED:"
python3 -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('/mnt/dietpi_userdata/syncthing/config.xml')
    root = tree.getroot()
    for f in root.findall('./folder'):
        print(f'• {f.attrib.get(\"label\", \"unnamed\")} [{f.attrib.get(\"id\")}] -> {f.attrib.get(\"path\")}')
except Exception as e:
    print('Error parsing config:', e)
"
echo ""

echo "▶ 📱 CONNECTED / PAIRED DEVICES:"
python3 -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('/mnt/dietpi_userdata/syncthing/config.xml')
    root = tree.getroot()
    for d in root.findall('./device'):
        d_id = d.attrib.get('id', '')
        if d_id:
            print(f'• {d.attrib.get(\"name\", \"unnamed\")} ({d_id[:7]}...)')
except Exception as e:
    print('Error parsing devices:', e)
"
echo ""

echo "▶ 📋 RECENT SYNCTHING WARNINGS / ERRORS (Last 15 lines):"
journalctl -u syncthing -p warning --no-pager -n 15 | tail -n 15
echo "===================================================================="
EOF
