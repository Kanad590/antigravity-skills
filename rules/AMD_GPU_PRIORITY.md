# Universal Dedicated AMD GPU Priority Rule (Global Default)

Whenever executing, rendering, or accelerating ANY graphical, video, animation, or compute task in ANY project, session, or directory:

1. **Dedicated AMD GPU Priority (`DRI_PRIME=1` First):**
   - The user's Pop!_OS system is equipped with hybrid graphics: Integrated Intel HD Graphics 520 (`00:02.0` / `/dev/dri/renderD128`) and Dedicated AMD Radeon R5 M330 / Hainan (`01:00.0` / `/dev/dri/renderD129`).
   - For all animation rendering, Remotion composition, headless Chrome/Chromium, WebGL/3D, Manim, Blender, and FFmpeg workflows, ALWAYS prioritize the dedicated AMD GPU by setting `DRI_PRIME=1` (or `DRI_PRIME=pci-0000_01_00_0`) and matching hardware flags (`--gl=angle`, `--use-angle=vulkan`, etc.).
   - Never default to software rendering or low-power integrated graphics when the dedicated AMD GPU can accelerate execution.
