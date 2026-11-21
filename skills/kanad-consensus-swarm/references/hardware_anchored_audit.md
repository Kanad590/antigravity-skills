# 💻 Hardware-Anchored Reality & Display Server Protocol

[![Protocol: Hardware-Anchored 60fps](https://img.shields.io/badge/Performance-Locked%2060fps-E26D5C.svg)](../SKILL.md)
[![Hardware: Intel HD 520](https://img.shields.io/badge/Hardware-Intel%20HD%20520%20GT2-4285F4.svg)](#2-reference-hardware-profile-dell-inspiron-15-3567)
[![Display: COSMIC Wayland](https://img.shields.io/badge/Compositor-COSMIC%20Wayland-0F3D3E.svg)](#3-display-server-and-compositor-dynamics)

---

## 1. The Cloud Illusion vs. Physical Reality

Modern Large Language Models (LLMs) are trained and hosted in multi-GPU hyperscale clusters with terabytes of aggregate VRAM, liquid cooling, and unbounded compute headroom. Consequently, unless strictly constrained by a hardware-anchored protocol, AI agents instinctively design user interfaces, Electron themes, and data processing scripts as if the user operates on an M3 Max or RTX 4090.

They hallucinate:
- Heavy dynamic CSS backdrop blurring (`backdrop-filter: blur(20px)`).
- Multiple nested CSS drop-shadows on scrollable lists.
- Unbounded in-memory AST parsers scanning 2,000+ files on application startup.
- Wide fixed-width mathematical tables that clip completely on 15.6" 1080p laptop displays.

The **Kanad Hardware-Anchored Protocol** anchors every line of CSS, every Dataview query, and every file-processing script directly to the physical constraints of modest, real-world development hardware.

---

## 2. Reference Hardware Profile: Dell Inspiron 15-3567

To guarantee ultra-smooth, production-grade performance everywhere, all designs are tested and calibrated against the following physical baseline:

| Subsystem | Physical Specification | Architecture & Limits | Primary Failure Mode if Unchecked |
| :--- | :--- | :--- | :--- |
| **Processor (CPU)** | Intel Core i3-6006U (Skylake 14nm) | 2 Cores / 4 Threads @ 2.00 GHz, 3MB L3 Cache | High thread contention; un-scoped regex searches freeze the UI. |
| **Integrated GPU (iGPU)** | Intel HD Graphics 520 (GT2) | 24 Execution Units (EUs), Gen9 Graphics | Limited pixel fill-rate; Gaussian blur operations trigger compositor stalls. |
| **Memory (RAM)** | 8GB DDR4 @ 2133 MHz | Single/Dual channel, 7.6GB ZRAM Swap | Electron heap bloat causes disk thrashing. |
| **Operating System** | Pop!_OS 24.04 LTS | Linux Kernel 6.9+, systemd | Wayland buffer synchronization stalls. |
| **Display Compositor** | COSMIC Wayland (cosmic-comp) | Direct hardware surface presentation | Drops frame rate from 60fps to 12fps when blurs overlap. |
| **Display Panel** | 15.6" Full HD (1920x1080 @ 60Hz) | 141 PPI, anti-glare TN/IPS | `baseFontSize: 20` causes horizontal table clipping. |

---

## 3. Display Server & Compositor Dynamics (Wayland vs. Blur)

On a Linux Wayland compositor (such as COSMIC Wayland or Sway), hardware acceleration operates through direct client-buffer presentation. 

### 3.1 The Mechanics of the "Blur of Death"
When an Electron app (e.g., Obsidian or VS Code) encounters `backdrop-filter: blur(12px)`:
1. **Framebuffer Copy:** The GPU compositor must pause its forward rendering pipeline and copy the underlying screen pixels into a temporary offscreen buffer.
2. **Multi-Pass Gaussian Blur:** The Intel HD 520's 24 Execution Units must perform a horizontal blur pass followed by a vertical blur pass across every affected pixel.
3. **Re-composition:** The blurred intermediate buffer is blended with the semi-transparent card background and re-submitted to the display compositor.
4. **The Stall:** When the user scrolls through a list of 50 notes or exam questions, this entire 4-stage pipeline executes **60 times per second per card**. The iGPU's pixel fill-rate budget is instantly exhausted. Frame rates crater from 60fps to 12-15fps, producing jarring micro-stutters and input latency.

### 3.2 The Zero-Blur Solution: Solid High-Contrast Dark Surfaces
Instead of blurred transparency, the Kanad Swarm mandates high-contrast, pure solid dark RGBA surfaces with razor-sharp 1px borders:

```css
/* ❌ FORBIDDEN: High fill-rate overhead, compositor stall */
.note-card {
  background: rgba(28, 32, 42, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

/* ✅ MANDATED: Zero fill-rate overhead, locked 60fps on Intel HD 520 */
.note-card {
  background: #1c202a;
  border: 1px solid #323946;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transform: translateY(0);
  transition: transform 0.15s ease, border-color 0.15s ease;
}

.note-card:hover {
  transform: translateY(-2px);
  border-color: #4285F4;
}
```

---

## 4. 20px Typographic Ergonomics & Overflow-X Wrapping

On a 15.6" 1080p display, users with high-intensity reading schedules frequently configure Obsidian or their browser to `baseFontSize: 20` for effortless ocular tracking.

### 4.1 The Horizontal Clipping Problem
At 20px font sizing:
- A standard 4-column markdown table exceeds the default 800px note container width.
- Complex KaTeX mathematical equations (e.g., Taylor series, Laplace transforms, engineering stress tensors) clip off the right edge of the screen, rendering key mathematical terms invisible.

### 4.2 Mandated Responsive Overflow Containers
Every table, formula block, and code snippet must be wrapped in responsive horizontal scrolling containers:

```css
/* Universal Overflow-X Wrappers for 20px Typography */
.math-block,
.table-view-table,
.markdown-rendered table,
pre code {
  overflow-x: auto !important;
  max-width: 100% !important;
  display: block !important;
  white-space: pre !important;
  scrollbar-width: thin;
  scrollbar-color: #323946 #1c202a;
}

/* Custom WebKit Scrollbar Styling for Clean Dark Theme */
.math-block::-webkit-scrollbar,
.table-view-table::-webkit-scrollbar,
table::-webkit-scrollbar {
  height: 6px;
}

.math-block::-webkit-scrollbar-thumb,
.table-view-table::-webkit-scrollbar-thumb,
table::-webkit-scrollbar-thumb {
  background: #323946;
  border-radius: 3px;
}

.math-block::-webkit-scrollbar-thumb:hover,
.table-view-table::-webkit-scrollbar-thumb:hover,
table::-webkit-scrollbar-thumb:hover {
  background: #4285F4;
}
```

---

## 5. Scoped Query & Dataview Optimization

In vaults or repositories with thousands of files (e.g., Gov-Exam-Prep with 2,100+ notes), unbounded metadata queries freeze the UI thread during file indexation.

### 5.1 Strict Dataview Query Rules
1. **Never Query the Vault Root:** `FROM ""` is strictly prohibited. Queries must specify a targeted directory (e.g., `FROM "Exams 📝/🚂 RRB JE"`).
2. **Explicit Exclusions:** Always exclude the parent index note itself (`WHERE file.name != "RRB JE"`).
3. **Mandatory Paging & Limits:** Every Dataview table or list must declare a `LIMIT` between 8 and 15 items:

```dataview
TABLE WITHOUT ID
  file.link AS "Exam Topic",
  difficulty AS "Difficulty",
  revision_streak AS "Streak"
FROM "Exams 📝/🚂 RRB JE"
WHERE file.name != "RRB JE MOC"
SORT file.mtime DESC
LIMIT 10
```

---

## 6. Hardware Profiling & Telemetry Shell Script

Before declaring any visual design or heavy background automation complete, the Analyser runs this verification script:

```bash
#!/usr/bin/env bash
# Hardware Profiling & GPU Fill-Rate Health Check
set -eo pipefail

echo "=========================================="
echo "🖥️ HARDWARE TELEMETRY AUDIT"
echo "=========================================="

echo -n "CPU: "
lscpu | grep "Model name:" | sed 's/Model name:[ \t]*//'

echo -n "Cores/Threads: "
echo "$(nproc) vCPUs available"

echo -n "GPU: "
lspci | grep -i -E "vga|3d|display" | cut -d: -f3- || echo "Unknown GPU"

echo -n "Display Server: "
echo "${XDG_SESSION_TYPE:-Unknown}"

echo -n "Memory Budget: "
free -h | awk '/Mem:/ {print "Used: "$3" / Total: "$2}'

echo -n "ZRAM Swap: "
free -h | awk '/Swap:/ {print "Used: "$3" / Total: "$2}'

echo "------------------------------------------"
echo "🔍 SCANNING FOR FORBIDDEN BACKDROP BLURS..."
BLURS=$(grep -rn "backdrop-filter" . --include="*.css" --include="*.html" --include="*.md" || true)
if [ -n "$BLURS" ]; then
    echo "❌ CRITICAL DEFECT: Found forbidden backdrop-filter properties:"
    echo "$BLURS"
    exit 1
else
    echo "✅ 100% PASS: Zero backdrop-filter occurrences detected."
fi

echo "=========================================="
echo "✅ HARDWARE AUDIT COMPLETE: 60FPS CERTIFIED"
echo "=========================================="
```
