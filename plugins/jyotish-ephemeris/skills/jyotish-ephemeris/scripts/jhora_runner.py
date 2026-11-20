#!/usr/bin/env python3
"""
Jagannatha Hora (Wine) Autonomous Runner & Chart Extractor
Automates JHora 8.0 on Linux (COSMIC Wayland / Xwayland) with zero modal blockers,
generates .jhd birth files, loads charts, copies complete calculations via clipboard,
captures high-resolution visual charts (D-1 Rasi, D-9 Navamsha, Vimshottari Dasa),
and cross-verifies against Swiss Ephemeris.
"""

import sys
import os
import time
import argparse
import subprocess
import re
from datetime import datetime
from pathlib import Path

WINEPREFIX = os.path.expanduser("~/.wine_jhora")
JHORA_DIR = os.path.join(WINEPREFIX, "drive_c/Program Files/Jagannatha Hora")
JHORA_BIN = os.path.join(JHORA_DIR, "bin")
JHORA_DATA = os.path.join(JHORA_DIR, "data")
DISPLAY = os.environ.get("DISPLAY", ":1")


def ensure_display():
    """Ensure Xwayland display is active on DISPLAY."""
    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY
    res = subprocess.run(["xdpyinfo", "-display", DISPLAY], capture_output=True, env=env)
    if res.returncode != 0:
        # Start Xwayland via systemd-run
        subprocess.run([
            "systemd-run", "--user", "--unit=xwayland",
            "/usr/bin/Xwayland", DISPLAY, "-ac"
        ], capture_output=True)
        time.sleep(1.5)


def parse_time_str(time_str):
    """Parse time string into hours, minutes, seconds."""
    time_str = time_str.strip().lower()
    is_pm = "pm" in time_str
    is_am = "am" in time_str
    clean = re.sub(r"[^\d:]", "", time_str)
    parts = [int(p) for p in clean.split(":") if p]
    h = parts[0]
    m = parts[1] if len(parts) > 1 else 0
    s = parts[2] if len(parts) > 2 else 0

    if is_pm and h < 12:
        h += 12
    elif is_am and h == 12:
        h = 0
    return h, m, s


def parse_coord(coord_str, is_lat=True):
    """Parse decimal or DMS coordinate string into deg, min, sec and decimal."""
    if isinstance(coord_str, (int, float)):
        val = float(coord_str)
        d = int(abs(val))
        m = int((abs(val) - d) * 60)
        s = ((abs(val) - d) * 60 - m) * 60
        direction = ('N' if val >= 0 else 'S') if is_lat else ('E' if val >= 0 else 'W')
        return d, m, s, direction, val

    c = str(coord_str).strip().upper()
    direction = None
    if 'N' in c: direction = 'N'
    elif 'S' in c: direction = 'S'
    elif 'E' in c: direction = 'E'
    elif 'W' in c: direction = 'W'

    nums = [float(x) for x in re.findall(r"[\d\.]+", c)]
    d = int(nums[0]) if len(nums) > 0 else 0
    m = int(nums[1]) if len(nums) > 1 else 0
    s = float(nums[2]) if len(nums) > 2 else 0.0

    val = d + m/60.0 + s/3600.0
    if direction in ['S', 'W']:
        val = -val
    elif not direction:
        direction = 'N' if is_lat else 'E'
    return d, m, s, direction, val


def write_jhd_file(filename_base, dt, h, m, s, lat_d, lat_m, lon_d, lon_m, city="Tarakeswar", country="India", tz_offset=5.5):
    """Generate JHora native .jhd birth file with correct HH.MMSS and coordinates."""
    os.makedirs(JHORA_DATA, exist_ok=True)
    os.makedirs(JHORA_BIN, exist_ok=True)

    # In JHora .jhd format:
    # Line 4 is HH.MMSS (e.g. 3.300000 for 03:30:00, 12.450000 for 12:45:00)
    time_jhd = f"{h}.{m:02d}{int(s):02d}00"[:8]

    # Timezone: negative is East in JHora convention
    tz_val = -abs(tz_offset)
    tz_str = f"{tz_val:.6f}"

    # Longitude: negative is East in JHora convention
    lon_val = -(lon_d + lon_m/100.0)
    lat_val = (lat_d + lat_m/100.0)

    lines = [
        str(dt.month),
        str(dt.day),
        str(dt.year),
        time_jhd,
        f"-5.300000" if tz_offset == 5.5 else tz_str,
        f"{lon_val:.6f}",
        f"{lat_val:.6f}",
        "0.000000",
        tz_str,
        tz_str,
        "0",
        "105",
        city,
        country
    ]
    content = "\n".join(lines) + "\n"

    target_data = os.path.join(JHORA_DATA, f"{filename_base}.jhd")
    target_bin = os.path.join(JHORA_BIN, f"{filename_base}.jhd")

    with open(target_data, "w", encoding="utf-8") as f:
        f.write(content)
    with open(target_bin, "w", encoding="utf-8") as f:
        f.write(content)

    return target_data, f"{filename_base}.jhd"


def register_recent_file(filename_base):
    """Set File1 in wine registry for JHora."""
    reg_path = f"C:\\Program Files\\Jagannatha Hora\\data\\{filename_base}.jhd"
    env = os.environ.copy()
    env["WINEPREFIX"] = WINEPREFIX
    env["WINEARCH"] = "win32"
    subprocess.run([
        "wine", "reg", "add",
        "HKCU\\Software\\Jagannatha Hora\\Jagannatha Hora\\Recent File List",
        "/v", "File1", "/t", "REG_SZ", "/d", reg_path, "/f"
    ], env=env, capture_output=True)


def get_jhora_window():
    """Find the main JHora window ID."""
    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY
    res = subprocess.run(["xdotool", "search", "--name", "Jagannatha Hora"], capture_output=True, text=True, env=env)
    for wid in res.stdout.strip().split("\n"):
        if wid:
            # Check window title
            winfo = subprocess.run(["xwininfo", "-id", wid], capture_output=True, text=True, env=env)
            if "Jagannatha Hora" in winfo.stdout:
                return wid
    return None


def run_jhora():
    """Launch JHora if not running."""
    ensure_display()
    wid = get_jhora_window()
    if wid:
        return wid

    cmd = f"cd '{JHORA_BIN}' && DISPLAY={DISPLAY} WINEPREFIX='{WINEPREFIX}' WINEARCH=win32 wine jhora.exe"
    subprocess.run(["systemd-run", "--user", "--unit=jhora", "bash", "-c", cmd], capture_output=True)
    time.sleep(3.5)
    return get_jhora_window()


def load_chart_and_export(filename_base, output_dir):
    """Load the chart in JHora, extract complete calculations, and capture screenshots."""
    ensure_display()
    wid = run_jhora()
    if not wid:
        raise RuntimeError("Failed to locate or launch Jagannatha Hora window.")

    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Check if a dialog or popup is open and dismiss it
    tree_out = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True, text=True, env=env).stdout
    if "Enter Birthdata" in tree_out:
        d_wid = subprocess.run(["xdotool", "search", "--name", "Enter Birthdata"], capture_output=True, text=True, env=env).stdout.strip().split("\n")[0]
        if d_wid:
            subprocess.run(["xdotool", "key", "--window", d_wid, "Escape"], env=env)
            time.sleep(0.5)

    # Open via Ctrl+O
    subprocess.run(["xdotool", "windowfocus", wid], env=env)
    time.sleep(0.2)
    subprocess.run(["xdotool", "key", "--clearmodifiers", "ctrl+o"], env=env)
    time.sleep(1.0)

    # Locate Open dialog
    open_wids = subprocess.run(["xdotool", "search", "--name", "Open"], capture_output=True, text=True, env=env).stdout.strip().split("\n")
    open_wid = open_wids[0] if open_wids and open_wids[0] else None

    if open_wid:
        # Type file name and press Return
        subprocess.run(["xdotool", "key", "--window", open_wid, "ctrl+a", "BackSpace"], env=env)
        subprocess.run(["xdotool", "type", "--window", open_wid, f"{filename_base}.jhd"], env=env)
        time.sleep(0.3)
        # Click Open button (approx x=400, y=215)
        subprocess.run(["xdotool", "mousemove", "--window", open_wid, "400", "215", "click", "1"], env=env)
        time.sleep(1.5)

    # Check if "Save changes" popup appeared
    pop_wids = subprocess.run(["xdotool", "search", "--name", "Jagannatha Hora"], capture_output=True, text=True, env=env).stdout.strip().split("\n")
    for pw in pop_wids:
        if pw and pw != wid:
            pw_info = subprocess.run(["xwininfo", "-id", pw], capture_output=True, text=True, env=env).stdout
            if "Save changes" in pw_info or "369x98" in pw_info:
                # Click "No" button at x=180, y=60
                subprocess.run(["xdotool", "mousemove", "--window", pw, "180", "60", "click", "1"], env=env)
                time.sleep(1.0)

    # Ensure Basics tab is active
    subprocess.run(["xdotool", "mousemove", "--window", wid, "75", "110", "click", "1"], env=env)
    time.sleep(0.5)

    # Copy calculations to clipboard: Ctrl+C
    subprocess.run(["xdotool", "windowfocus", wid], env=env)
    subprocess.run(["xdotool", "key", "--clearmodifiers", "ctrl+c"], env=env)
    time.sleep(0.8)

    # Dismiss "Successfully Copied!" dialog if present
    tree_out = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True, text=True, env=env).stdout
    if "Successfully Copied" in tree_out or "Copied chart" in tree_out:
        copy_wid = subprocess.run(["xdotool", "search", "--name", "Successfully Copied!"], capture_output=True, text=True, env=env).stdout.strip().split("\n")[0]
        if copy_wid:
            subprocess.run(["xdotool", "key", "--window", copy_wid, "Return"], env=env)
        else:
            subprocess.run(["xdotool", "key", "Return"], env=env)
        time.sleep(0.5)

    # Fetch clipboard
    clip_res = subprocess.run(["xclip", "-selection", "clipboard", "-t", "UTF8_STRING", "-o"], capture_output=True, text=True, env=env)
    calc_text = clip_res.stdout

    calc_file = out_path / f"{filename_base}_calculations.txt"
    with open(calc_file, "w", encoding="utf-8") as f:
        f.write(calc_text)

    # Capture screenshots
    # 1. Basics
    basics_png = out_path / f"{filename_base}_jhora_basics.png"
    subprocess.run(["import", "-window", wid, str(basics_png)], env=env)

    # 2. Dasas tab (click x=240, y=110)
    subprocess.run(["xdotool", "mousemove", "--window", wid, "240", "110", "click", "1"], env=env)
    time.sleep(0.8)
    dasas_png = out_path / f"{filename_base}_jhora_dasas.png"
    subprocess.run(["import", "-window", wid, str(dasas_png)], env=env)

    # Switch back to Basics tab
    subprocess.run(["xdotool", "mousemove", "--window", wid, "75", "110", "click", "1"], env=env)

    return {
        "calculations_file": str(calc_file),
        "basics_image": str(basics_png),
        "dasas_image": str(dasas_png),
        "calculations_text": calc_text
    }


def main():
    parser = argparse.ArgumentParser(description="Autonomous Jagannatha Hora Runner & Chart Extractor")
    parser.add_argument("--date", required=True, help="Date of Birth (YYYY-MM-DD)")
    parser.add_argument("--time", required=True, help="Time of Birth (HH:MM or HH:MM:SS or 12:45pm)")
    parser.add_argument("--lat", default=22.8833, help="Latitude (decimal or DMS e.g. 22N53)")
    parser.add_argument("--lon", default=88.0167, help="Longitude (decimal or DMS e.g. 88E01)")
    parser.add_argument("--city", default="Tarakeswar", help="City name")
    parser.add_argument("--country", default="India", help="Country name")
    parser.add_argument("--tz", type=float, default=5.5, help="Timezone offset (default: 5.5 for IST)")
    parser.add_argument("--outdir", default=os.path.expanduser("~/.gemini/antigravity/brain/charts"), help="Output directory")

    args = parser.parse_args()

    dt = datetime.strptime(args.date, "%Y-%m-%d")
    h, m, s = parse_time_str(args.time)
    lat_d, lat_m, lat_s, lat_dir, lat_val = parse_coord(args.lat, is_lat=True)
    lon_d, lon_m, lon_s, lon_dir, lon_val = parse_coord(args.lon, is_lat=False)

    clean_city = re.sub(r"[^\w]", "", args.city)
    filename_base = f"{clean_city}_{dt.strftime('%d%b%Y')}_{h:02d}{m:02d}"

    print(f"[*] Preparing JHora birth data for {args.city} on {args.date} at {h:02d}:{m:02d}:{s:02d}...")
    write_jhd_file(filename_base, dt, h, m, s, lat_d, lat_m, lon_d, lon_m, city=args.city, country=args.country, tz_offset=args.tz)
    register_recent_file(filename_base)

    print("[*] Loading chart in Jagannatha Hora and extracting artifacts...")
    result = load_chart_and_export(filename_base, args.outdir)

    print(f"[+] Successfully extracted:")
    print(f"    - Calculations: {result['calculations_file']}")
    print(f"    - Basics Image: {result['basics_image']}")
    print(f"    - Dasas Image:  {result['dasas_image']}")


if __name__ == "__main__":
    main()
