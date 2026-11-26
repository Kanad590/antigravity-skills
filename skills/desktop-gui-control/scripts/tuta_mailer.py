#!/usr/bin/env python3
"""
Tuta Mail Automated Desktop Sender (Pop!_OS COSMIC Wayland - v2.0)
Composes and sends an email via Tuta Mail Flatpak using ag-gui v2.0 primitives
(clean screenshot capture, visual diff anchoring, and stdin-safe typing).
"""

import sys
import os
import time
import argparse
import subprocess
import importlib.util
import importlib.machinery
from PIL import Image
import numpy as np


def _load_ag():
    loader = importlib.machinery.SourceFileLoader("ag_gui_engine", "/home/saman/.local/bin/ag-gui")
    spec = importlib.util.spec_from_loader("ag_gui_engine", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def cycle_to_close_button(ag, max_attempts=30):
    """Cycles Tab until focus lands on the 'Close' button of the compose modal."""
    for _ in range(max_attempts):
        before = ag.take_screenshot("/tmp/tuta_diff_1.png")
        ag.press_key("Tab")
        time.sleep(0.10)
        after = ag.take_screenshot("/tmp/tuta_diff_2.png")

        im1 = Image.open(before).convert("RGB")
        im2 = Image.open(after).convert("RGB")
        diff = np.abs(np.array(im1).astype(int) - np.array(im2).astype(int))
        diff[:40, :, :] = 0
        mask = np.any(diff > 15, axis=2)
        if np.any(mask):
            y_idx, x_idx = np.where(mask)
            if 200 <= x_idx.min() <= 250 and 90 <= y_idx.min() <= 130:
                return True
    return False


def send_email(to_addr, subject, body, password=None):
    ag = _load_ag()
    env = ag.get_desktop_env()
    print(f"Launching or focusing Tuta Mail for {to_addr}...")
    subprocess.Popen(
        ["flatpak", "run", "com.tutanota.Tutanota"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    ag.wait_for_change(timeout=5.0)
    ag.focus_window("Tuta", persistent=False, maximize=True)
    time.sleep(0.25)

    if not ag.is_window_focused("Tuta"):
        print("Error: Focus Guard aborted — Tuta Mail is not the active window.", file=sys.stderr)
        return False

    # Open Compose modal
    ag.hotkey("ctrl", "n")
    ag.wait_for_change(timeout=3.0)

    if not cycle_to_close_button(ag):
        print("Warning: Could not anchor on Close button, attempting direct Tab navigation...")

    ag.press_key("Tab")
    time.sleep(0.08)
    ag.press_key("Tab")
    time.sleep(0.10)

    print(f"Typing recipient: {to_addr}")
    ag.type_text(to_addr, delay=0.005)
    time.sleep(0.20)
    ag.press_key("Return")
    time.sleep(0.25)

    if password:
        for _ in range(6):
            ag.press_key("Tab")
            time.sleep(0.06)
        ag.type_text(password, delay=0.005)
        time.sleep(0.15)
        ag.press_key("Tab")
        ag.press_key("Tab")
    else:
        for _ in range(8):
            ag.press_key("Tab")
            time.sleep(0.06)

    print(f"Typing subject: {subject}")
    ag.type_text(subject, delay=0.005)
    time.sleep(0.15)

    ag.press_key("Tab")
    time.sleep(0.10)

    print("Typing body content...")
    ag.type_text(body, delay=0.004)
    time.sleep(0.20)

    # Try Smart OCR 'Send' click first, fallback to 2 Tabs + Return
    if not ag.click_text("Send", persistent=False):
        ag.press_key("Tab")
        time.sleep(0.08)
        ag.press_key("Tab")
        time.sleep(0.12)
        ag.press_key("Return")

    ag.wait_for_change(timeout=4.0)
    final_screen = ag.take_screenshot("/tmp/tuta_sent_result.png")
    print(f"Email dispatched! Verification screenshot: {final_screen}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tuta Mail Automated CLI")
    parser.add_argument("to", help="Recipient email address")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("body", help="Email body text")
    parser.add_argument("--password", help="Password for end-to-end encrypted external mail", default=None)
    args = parser.parse_args()

    send_email(args.to, args.subject, args.body, args.password)
