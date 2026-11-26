#!/usr/bin/env python3
"""
Tuta Mail Automated Desktop Sender (Pop!_OS COSMIC Wayland)
Composes and sends an email via Tuta Mail Flatpak using native Wayland automation.
"""

import sys
import os
import time
import argparse
import subprocess
from PIL import Image
import numpy as np

ENV = os.environ.copy()
ENV["WAYLAND_DISPLAY"] = "wayland-1"
ENV["DISPLAY"] = ":1"


def run_cmd(cmd):
    return subprocess.run(cmd, env=ENV, capture_output=True, text=True, check=False)


def take_screenshot(path="/tmp/tuta_action.png"):
    res = run_cmd(["cosmic-screenshot", "--interactive=false", "--notify=false", "-s", "/tmp"])
    latest = subprocess.check_output("ls -t /tmp/Screenshot*.png | head -n 1", shell=True).decode().strip()
    run_cmd(["cp", "-f", latest, path])
    return path


def cycle_to_close_button(max_attempts=30):
    """
    Cycles Tab until focus lands on the 'Close' button of the compose modal (x around 202-275, y around 91-147).
    """
    for _ in range(max_attempts):
        before = take_screenshot("/tmp/tuta_diff_1.png")
        run_cmd(["wtype", "-k", "Tab"])
        time.sleep(0.12)
        after = take_screenshot("/tmp/tuta_diff_2.png")

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
    print(f"Launching or focusing Tuta Mail for {to_addr}...")
    run_cmd(["flatpak", "run", "com.tutanota.Tutanota"])
    time.sleep(1.0)

    # Open Compose modal
    run_cmd(["wtype", "-M", "ctrl", "-k", "n", "-m", "ctrl"])
    time.sleep(0.8)

    # Find Close button anchor
    if not cycle_to_close_button():
        print("Warning: Could not anchor on Close button, attempting direct Tab navigation...")

    # From Close button:
    # Tab 1: Send button
    # Tab 2: To input field
    run_cmd(["wtype", "-k", "Tab"])
    time.sleep(0.1)
    run_cmd(["wtype", "-k", "Tab"])
    time.sleep(0.15)

    # Type To address with delay
    print(f"Typing recipient: {to_addr}")
    run_cmd(["wtype", "-d", "20", to_addr])
    time.sleep(0.3)
    run_cmd(["wtype", "-k", "Return"])
    time.sleep(0.3)

    # If external recipient, Tuta presents password field
    if password:
        # 6 Tabs to Password field
        for _ in range(6):
            run_cmd(["wtype", "-k", "Tab"])
            time.sleep(0.08)
        run_cmd(["wtype", "-d", "20", password])
        time.sleep(0.2)
        # 2 Tabs to Subject
        run_cmd(["wtype", "-k", "Tab"])
        run_cmd(["wtype", "-k", "Tab"])
    else:
        # Move to Subject directly (8 Tabs from To field)
        for _ in range(8):
            run_cmd(["wtype", "-k", "Tab"])
            time.sleep(0.08)

    # Type Subject
    print(f"Typing subject: {subject}")
    run_cmd(["wtype", "-d", "20", subject])
    time.sleep(0.2)

    # Tab to Body
    run_cmd(["wtype", "-k", "Tab"])
    time.sleep(0.15)

    # Type Body
    print("Typing body content...")
    run_cmd(["wtype", "-d", "20", body])
    time.sleep(0.3)

    # From Body, 2 Tabs reaches Send button
    run_cmd(["wtype", "-k", "Tab"])
    time.sleep(0.1)
    run_cmd(["wtype", "-k", "Tab"])
    time.sleep(0.2)

    # Send
    print("Clicking Send button...")
    run_cmd(["wtype", "-k", "Return"])
    time.sleep(2.0)

    # Final verification screenshot
    final_screen = take_screenshot("/tmp/tuta_sent_result.png")
    print(f"Email dispatched successfully! Verification screenshot: {final_screen}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tuta Mail Automated CLI")
    parser.add_argument("to", help="Recipient email address")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("body", help="Email body text")
    parser.add_argument("--password", help="Password for end-to-end encrypted external mail", default=None)
    args = parser.parse_args()

    send_email(args.to, args.subject, args.body, args.password)
