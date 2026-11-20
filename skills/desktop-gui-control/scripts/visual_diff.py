#!/usr/bin/env python3
"""
Visual Diff Tool for GUI Verification (Pop!_OS COSMIC Wayland)
Compares two screenshots and prints the pixel coordinates of any visible changes.
"""

import sys
import os
import argparse
import subprocess
from PIL import Image
import numpy as np


def compute_diff(img1_path, img2_path, out_crop=None, threshold=15, ignore_top_bar=True):
    im1 = Image.open(img1_path).convert("RGB")
    im2 = Image.open(img2_path).convert("RGB")

    arr1 = np.array(im1)
    arr2 = np.array(im2)

    diff = np.abs(arr1.astype(int) - arr2.astype(int))
    if ignore_top_bar:
        diff[:40, :, :] = 0  # ignore panel clock

    mask = np.any(diff > threshold, axis=2)
    if not np.any(mask):
        print("No visual differences detected.")
        return False

    y_idx, x_idx = np.where(mask)
    x_min, x_max = int(x_idx.min()), int(x_idx.max())
    y_min, y_max = int(y_idx.min()), int(y_idx.max())
    print(f"Visual change detected: x=[{x_min}, {x_max}], y=[{y_min}, {y_max}], area={(x_max-x_min)*(y_max-y_min)} px")

    if out_crop:
        pad = 20
        crop = im2.crop((
            max(0, x_min - pad),
            max(0, y_min - pad),
            min(im2.width, x_max + pad),
            min(im2.height, y_max + pad)
        ))
        crop.save(out_crop)
        print(f"Cropped diff region saved to: {out_crop}")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Desktop Visual Diff Tool")
    parser.add_argument("img1", help="Path to before image")
    parser.add_argument("img2", help="Path to after image")
    parser.add_argument("--crop", "-c", help="Save cropped diff region to this path", default=None)
    parser.add_argument("--thresh", "-t", type=int, default=15, help="Difference threshold (default: 15)")
    args = parser.parse_args()

    ok = compute_diff(args.img1, args.img2, out_crop=args.crop, threshold=args.thresh)
    sys.exit(0 if ok else 1)
